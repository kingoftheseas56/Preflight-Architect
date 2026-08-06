# Slice 2 Reference Code — Store Implementation B r1

**Status:** implementable reference code; uncompiled, untested, unexecuted, unadopted, and unverified.

## `native/localmedia/LocalMediaContinuityStore.cpp` (part B)

```cpp
QList<LocalMediaContinuityRecord> LocalMediaContinuityStore::all() const
{
    QList<LocalMediaContinuityRecord> result;
    for (const QString &id : m_order) {
        const auto it = m_records.constFind(id);
        if (it != m_records.constEnd()) result.append(it.value());
    }
    return result;
}

QList<LocalMediaContinuityRecord> LocalMediaContinuityStore::recents(int limit) const
{
    auto result = all();
    result.erase(std::remove_if(result.begin(), result.end(),
                                [](const auto &record) {
                                    return record.lastOpenedAtMs <= 0;
                                }),
                 result.end());
    std::sort(result.begin(), result.end(),
              [](const auto &left, const auto &right) {
                  return left.lastOpenedAtMs > right.lastOpenedAtMs;
              });
    if (limit > 0 && result.size() > limit) result = result.mid(0, limit);
    return result;
}

std::optional<LocalMediaContinuityRecord>
LocalMediaContinuityStore::record(const QString &localId) const
{
    const auto it = m_records.constFind(localId.trimmed());
    return it == m_records.constEnd()
        ? std::nullopt
        : std::optional<LocalMediaContinuityRecord>(it.value());
}

QString LocalMediaContinuityStore::create(LocalMediaContinuityRecord prototype,
                                          LocalMediaStoreError *error)
{
    prototype.localId =
        QUuid::createUuid().toString(QUuid::WithoutBraces);
    const qint64 now = QDateTime::currentMSecsSinceEpoch();
    if (prototype.createdAtMs <= 0) prototype.createdAtMs = now;
    prototype.updatedAtMs = now;
    if (!upsert(prototype, error)) return {};
    return prototype.localId;
}

bool LocalMediaContinuityStore::upsert(LocalMediaContinuityRecord record,
                                       LocalMediaStoreError *error)
{
    if (error) *error = {};
    record.localId = record.localId.trimmed();
    record.currentLocator.canonicalPath =
        normalizePath(record.currentLocator.canonicalPath);

    for (auto &locator : record.locatorHistory)
        locator.canonicalPath = normalizePath(locator.canonicalPath);

    if (!validateRecord(record, error)) return false;

    const QString occupied =
        occupyingIdForPath(record.currentLocator.canonicalPath, record.localId);
    if (!occupied.isEmpty()) {
        setError(error, LocalMediaStoreErrorCode::DuplicateLocation,
                 QStringLiteral("That local file is already attached to another item."),
                 occupied);
        return false;
    }

    const auto oldRecords = m_records;
    const auto oldOrder = m_order;
    const qint64 now = QDateTime::currentMSecsSinceEpoch();

    const auto existing = m_records.constFind(record.localId);
    if (existing == m_records.constEnd()) {
        m_order.append(record.localId);
        if (record.createdAtMs <= 0) record.createdAtMs = now;
    } else if (record.createdAtMs <= 0) {
        record.createdAtMs = existing->createdAtMs;
    }

    record.updatedAtMs = now;
    m_records.insert(record.localId, std::move(record));
    return persistMutation(oldRecords, oldOrder, error);
}

bool LocalMediaContinuityStore::markOpened(const QString &localId,
                                           qint64 openedAtMs,
                                           LocalMediaStoreError *error)
{
    if (error) *error = {};
    auto it = m_records.find(localId.trimmed());
    if (it == m_records.end()) {
        setError(error, LocalMediaStoreErrorCode::NotFound,
                 QStringLiteral("The local media item was not found."));
        return false;
    }

    const auto oldRecords = m_records;
    const auto oldOrder = m_order;
    if (openedAtMs <= 0) openedAtMs = QDateTime::currentMSecsSinceEpoch();
    it->lastOpenedAtMs = openedAtMs;
    it->updatedAtMs = openedAtMs;
    return persistMutation(oldRecords, oldOrder, error);
}

bool LocalMediaContinuityStore::relocate(const QString &localId,
                                         LocalMediaLocator locator,
                                         LocalMediaStoreError *error)
{
    if (error) *error = {};
    auto it = m_records.find(localId.trimmed());
    if (it == m_records.end()) {
        setError(error, LocalMediaStoreErrorCode::NotFound,
                 QStringLiteral("The local media item was not found."));
        return false;
    }

    locator.canonicalPath = normalizePath(locator.canonicalPath);
    if (!locator.isValid()) {
        setError(error, LocalMediaStoreErrorCode::InvalidArgument,
                 QStringLiteral("The replacement location is invalid."));
        return false;
    }

    const QString occupied =
        occupyingIdForPath(locator.canonicalPath, localId);
    if (!occupied.isEmpty()) {
        setError(error, LocalMediaStoreErrorCode::DuplicateLocation,
                 QStringLiteral("The replacement file is already attached to another item."),
                 occupied);
        return false;
    }

    const auto oldRecords = m_records;
    const auto oldOrder = m_order;

    bool alreadyHistorical = false;
    for (const auto &historical : it->locatorHistory) {
        if (normalizePath(historical.canonicalPath)
            == normalizePath(it->currentLocator.canonicalPath)) {
            alreadyHistorical = true;
            break;
        }
    }

    if (!alreadyHistorical
        && normalizePath(it->currentLocator.canonicalPath)
            != locator.canonicalPath) {
        it->locatorHistory.append(it->currentLocator);
    }

    it->currentLocator = std::move(locator);
    it->updatedAtMs = QDateTime::currentMSecsSinceEpoch();
    return persistMutation(oldRecords, oldOrder, error);
}

bool LocalMediaContinuityStore::setRelationship(
    const QString &localId,
    LocalMediaRelationshipKind kind,
    const QString &otherLocalId,
    LocalMediaStoreError *error)
{
    if (error) *error = {};
    const QString id = localId.trimmed();
    const QString otherId = otherLocalId.trimmed();

    auto it = m_records.find(id);
    if (it == m_records.end() || !m_records.contains(otherId)) {
        setError(error, LocalMediaStoreErrorCode::NotFound,
                 QStringLiteral("One of the related local media items was not found."));
        return false;
    }
    if (id == otherId) {
        setError(error, LocalMediaStoreErrorCode::InvalidArgument,
                 QStringLiteral("A local media item cannot relate to itself."));
        return false;
    }

    const auto oldRecords = m_records;
    const auto oldOrder = m_order;

    for (auto relationship = it->relationships.begin();
         relationship != it->relationships.end();) {
        if (relationship->kind == kind)
            relationship = it->relationships.erase(relationship);
        else
            ++relationship;
    }

    it->relationships.append({kind, otherId});
    it->updatedAtMs = QDateTime::currentMSecsSinceEpoch();
    return persistMutation(oldRecords, oldOrder, error);
}

bool LocalMediaContinuityStore::clearRecents(LocalMediaStoreError *error)
{
    if (error) *error = {};
    const auto oldRecords = m_records;
    const auto oldOrder = m_order;

    for (auto it = m_records.begin(); it != m_records.end(); ++it)
        it->lastOpenedAtMs = 0;

    return persistMutation(oldRecords, oldOrder, error);
}

std::optional<LocalMediaContinuityRecord>
LocalMediaContinuityStore::forget(const QString &localId,
                                  LocalMediaStoreError *error)
{
    if (error) *error = {};
    const QString id = localId.trimmed();
    const auto it = m_records.constFind(id);
    if (it == m_records.constEnd()) {
        setError(error, LocalMediaStoreErrorCode::NotFound,
                 QStringLiteral("The local media item was not found."));
        return std::nullopt;
    }

    const LocalMediaContinuityRecord removed = it.value();
    const auto oldRecords = m_records;
    const auto oldOrder = m_order;

    m_records.remove(id);
    m_order.removeAll(id);

    for (auto recordIt = m_records.begin();
         recordIt != m_records.end();
         ++recordIt) {
        for (auto relationship = recordIt->relationships.begin();
             relationship != recordIt->relationships.end();) {
            if (relationship->otherLocalId == id)
                relationship = recordIt->relationships.erase(relationship);
            else
                ++relationship;
        }
    }

    if (!persistMutation(oldRecords, oldOrder, error))
        return std::nullopt;
    return removed;
}

QString LocalMediaContinuityStore::findByPath(const QString &path) const
{
    const QString normalized = normalizePath(path);
    if (normalized.isEmpty()) return {};

    for (const QString &localId : m_order) {
        const auto it = m_records.constFind(localId);
        if (it == m_records.constEnd()) continue;

        if (normalizePath(it->currentLocator.canonicalPath) == normalized)
            return localId;

        for (const auto &historical : it->locatorHistory) {
            if (normalizePath(historical.canonicalPath) == normalized)
                return localId;
        }
    }
    return {};
}

QStringList LocalMediaContinuityStore::findByFingerprint(
    const QString &algorithm,
    const QString &value) const
{
    QStringList matches;
    const QString wantedAlgorithm = algorithm.trimmed().toLower();
    const QString wantedValue = value.trimmed();

    if (wantedAlgorithm.isEmpty() || wantedValue.isEmpty()) return matches;

    for (const QString &localId : m_order) {
        const auto it = m_records.constFind(localId);
        if (it == m_records.constEnd()) continue;

        for (const auto &fingerprint : it->fingerprints) {
            if (fingerprint.algorithm.trimmed().toLower() == wantedAlgorithm
                && fingerprint.value.trimmed() == wantedValue) {
                matches.append(localId);
                break;
            }
        }
    }
    return matches;
}

QStringList LocalMediaContinuityStore::loadWarnings() const
{
    return m_loadWarnings;
}

QString LocalMediaContinuityStore::path() const
{
    return m_path;
}

QString LocalMediaContinuityStore::normalizePath(const QString &path)
{
    const QString trimmed = path.trimmed();
    if (trimmed.isEmpty()) return {};

    const QFileInfo info(trimmed);
    QString normalized = info.canonicalFilePath();
    if (normalized.isEmpty()) normalized = info.absoluteFilePath();
    return QDir::cleanPath(QDir::fromNativeSeparators(normalized));
}

bool LocalMediaContinuityStore::validateRecord(
    const LocalMediaContinuityRecord &record,
    LocalMediaStoreError *error) const
{
    if (record.localId.trimmed().isEmpty()
        || record.family == LocalMediaFamily::Unknown
        || !record.currentLocator.isValid()) {
        setError(error, LocalMediaStoreErrorCode::InvalidArgument,
                 QStringLiteral("The local media continuity record is invalid."));
        return false;
    }

    for (const auto &fingerprint : record.fingerprints) {
        if (!fingerprint.isValid()) {
            setError(error, LocalMediaStoreErrorCode::InvalidArgument,
                     QStringLiteral("A local media fingerprint is invalid."));
            return false;
        }
    }

    for (const auto &relationship : record.relationships) {
        if (relationship.otherLocalId.trimmed().isEmpty()
            || relationship.otherLocalId == record.localId) {
            setError(error, LocalMediaStoreErrorCode::InvalidArgument,
                     QStringLiteral("A local media relationship is invalid."));
            return false;
        }
    }
    return true;
}

bool LocalMediaContinuityStore::persistMutation(
    const QHash<QString, LocalMediaContinuityRecord> &oldRecords,
    const QStringList &oldOrder,
    LocalMediaStoreError *error)
{
    if (save(error)) return true;
    m_records = oldRecords;
    m_order = oldOrder;
    return false;
}

QString LocalMediaContinuityStore::occupyingIdForPath(
    const QString &path,
    const QString &exceptId) const
{
    const QString normalized = normalizePath(path);
    if (normalized.isEmpty()) return {};

    for (const QString &localId : m_order) {
        if (localId == exceptId) continue;
        const auto it = m_records.constFind(localId);
        if (it != m_records.constEnd()
            && normalizePath(it->currentLocator.canonicalPath) == normalized) {
            return localId;
        }
    }
    return {};
}

QString localMediaFamilyName(LocalMediaFamily family)
{
    return familyName(family);
}

QString relationshipKindName(LocalMediaRelationshipKind kind)
{
    return relationName(kind);
}

QString localMediaStoreErrorCodeName(LocalMediaStoreErrorCode code)
{
    switch (code) {
    case LocalMediaStoreErrorCode::None: return QStringLiteral("none");
    case LocalMediaStoreErrorCode::InvalidArgument: return QStringLiteral("invalid-argument");
    case LocalMediaStoreErrorCode::NotFound: return QStringLiteral("not-found");
    case LocalMediaStoreErrorCode::DuplicateLocation: return QStringLiteral("duplicate-location");
    case LocalMediaStoreErrorCode::IoFailure: return QStringLiteral("io-failure");
    case LocalMediaStoreErrorCode::ParseFailure: return QStringLiteral("parse-failure");
    case LocalMediaStoreErrorCode::UnsupportedVersion: return QStringLiteral("unsupported-version");
    }
    return QStringLiteral("unknown-error");
}

} // namespace colosseum::localmedia
```
