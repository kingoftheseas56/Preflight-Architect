# Slice 2 Reference Code — Store Implementation A r1

**Status:** implementable reference code; uncompiled, untested, unexecuted, unadopted, and unverified.

## `native/localmedia/LocalMediaContinuityStore.cpp` (part A)

```cpp
#include "LocalMediaContinuityStore.h"

#include <QDateTime>
#include <QDir>
#include <QFile>
#include <QFileInfo>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QSaveFile>
#include <QUuid>

#include <algorithm>

namespace colosseum::localmedia {
namespace {

void setError(LocalMediaStoreError *error,
              LocalMediaStoreErrorCode code,
              const QString &message,
              const QString &diagnostic = {})
{
    if (!error) return;
    error->code = code;
    error->userMessage = message;
    error->diagnostic = diagnostic;
}

QString familyName(LocalMediaFamily family)
{
    switch (family) {
    case LocalMediaFamily::Book: return QStringLiteral("book");
    case LocalMediaFamily::Comic: return QStringLiteral("comic");
    case LocalMediaFamily::Video: return QStringLiteral("video");
    case LocalMediaFamily::Unknown: break;
    }
    return QStringLiteral("unknown");
}

LocalMediaFamily familyFromName(const QString &value)
{
    const QString v = value.trimmed().toLower();
    if (v == QStringLiteral("book")) return LocalMediaFamily::Book;
    if (v == QStringLiteral("comic")) return LocalMediaFamily::Comic;
    if (v == QStringLiteral("video")) return LocalMediaFamily::Video;
    return LocalMediaFamily::Unknown;
}

QString relationName(LocalMediaRelationshipKind kind)
{
    return kind == LocalMediaRelationshipKind::CopyOf
        ? QStringLiteral("copy-of")
        : QStringLiteral("changed-from");
}

LocalMediaRelationshipKind relationFromName(const QString &value)
{
    return value == QStringLiteral("changed-from")
        ? LocalMediaRelationshipKind::ChangedFrom
        : LocalMediaRelationshipKind::CopyOf;
}

QJsonObject locatorToJson(const LocalMediaLocator &locator)
{
    return {
        {QStringLiteral("canonicalPath"), locator.canonicalPath},
        {QStringLiteral("opaqueAccessToken"), locator.opaqueAccessToken},
        {QStringLiteral("firstSeenAtMs"), double(locator.firstSeenAtMs)},
        {QStringLiteral("lastVerifiedAtMs"), double(locator.lastVerifiedAtMs)}
    };
}

LocalMediaLocator locatorFromJson(const QJsonObject &object)
{
    LocalMediaLocator locator;
    locator.canonicalPath = LocalMediaContinuityStore::normalizePath(
        object.value(QStringLiteral("canonicalPath")).toString());
    locator.opaqueAccessToken =
        object.value(QStringLiteral("opaqueAccessToken")).toString();
    locator.firstSeenAtMs =
        qint64(object.value(QStringLiteral("firstSeenAtMs")).toDouble());
    locator.lastVerifiedAtMs =
        qint64(object.value(QStringLiteral("lastVerifiedAtMs")).toDouble());
    return locator;
}

QJsonObject recordToJson(const LocalMediaContinuityRecord &record)
{
    QJsonArray history;
    for (const auto &locator : record.locatorHistory)
        history.append(locatorToJson(locator));

    QJsonArray fingerprints;
    for (const auto &fingerprint : record.fingerprints) {
        fingerprints.append(QJsonObject{
            {QStringLiteral("algorithm"), fingerprint.algorithm},
            {QStringLiteral("value"), fingerprint.value},
            {QStringLiteral("sizeBytes"), double(fingerprint.sizeBytes)},
            {QStringLiteral("modifiedAtMs"), double(fingerprint.modifiedAtMs)}
        });
    }

    QJsonObject stateLinks;
    for (auto it = record.stateLinks.constBegin(); it != record.stateLinks.constEnd(); ++it)
        stateLinks.insert(it.key(), it.value().toString());

    QJsonArray subtitles;
    for (const auto &subtitle : record.subtitleReferences)
        subtitles.append(QJsonObject::fromVariantMap(subtitle));

    QJsonArray relationships;
    for (const auto &relationship : record.relationships) {
        relationships.append(QJsonObject{
            {QStringLiteral("kind"), relationName(relationship.kind)},
            {QStringLiteral("otherLocalId"), relationship.otherLocalId}
        });
    }

    return {
        {QStringLiteral("localId"), record.localId},
        {QStringLiteral("family"), familyName(record.family)},
        {QStringLiteral("displayTitle"), record.displayTitle},
        {QStringLiteral("currentLocator"), locatorToJson(record.currentLocator)},
        {QStringLiteral("locatorHistory"), history},
        {QStringLiteral("fingerprints"), fingerprints},
        {QStringLiteral("stateLinks"), stateLinks},
        {QStringLiteral("lastOpenedAtMs"), double(record.lastOpenedAtMs)},
        {QStringLiteral("identification"), QJsonObject::fromVariantMap(record.identification)},
        {QStringLiteral("subtitleReferences"), subtitles},
        {QStringLiteral("relationships"), relationships},
        {QStringLiteral("createdAtMs"), double(record.createdAtMs)},
        {QStringLiteral("updatedAtMs"), double(record.updatedAtMs)}
    };
}

std::optional<LocalMediaContinuityRecord> recordFromJson(const QJsonObject &object)
{
    LocalMediaContinuityRecord record;
    record.localId = object.value(QStringLiteral("localId")).toString().trimmed();
    record.family = familyFromName(object.value(QStringLiteral("family")).toString());
    record.displayTitle = object.value(QStringLiteral("displayTitle")).toString();
    record.currentLocator =
        locatorFromJson(object.value(QStringLiteral("currentLocator")).toObject());

    for (const auto &value : object.value(QStringLiteral("locatorHistory")).toArray())
        record.locatorHistory.append(locatorFromJson(value.toObject()));

    for (const auto &value : object.value(QStringLiteral("fingerprints")).toArray()) {
        const QJsonObject fp = value.toObject();
        record.fingerprints.append({
            fp.value(QStringLiteral("algorithm")).toString(),
            fp.value(QStringLiteral("value")).toString(),
            qint64(fp.value(QStringLiteral("sizeBytes")).toDouble(-1)),
            qint64(fp.value(QStringLiteral("modifiedAtMs")).toDouble())
        });
    }

    const QJsonObject links = object.value(QStringLiteral("stateLinks")).toObject();
    for (auto it = links.constBegin(); it != links.constEnd(); ++it)
        record.stateLinks.insert(it.key(), it.value().toString());

    record.lastOpenedAtMs =
        qint64(object.value(QStringLiteral("lastOpenedAtMs")).toDouble());
    record.identification =
        object.value(QStringLiteral("identification")).toObject().toVariantMap();

    for (const auto &value : object.value(QStringLiteral("subtitleReferences")).toArray())
        record.subtitleReferences.append(value.toObject().toVariantMap());

    for (const auto &value : object.value(QStringLiteral("relationships")).toArray()) {
        const QJsonObject relationship = value.toOObject();
        record.relationships.append({relationFromName(relationship.value(QStringLiteral("kind")).toString()),
            relationship.value(QStringLiteral("otherLocalId")).toString()});
    }

    record.createdAtMs =
        qint64(object.value(QStringLiteral("createdAtMs")).toDouble());
    record.updatedAtMs =
        qint64(object.value(QStringLiteral("updatedAtMs")).toDouble());

    if (record.localId.isEmpty()
        || record.family == LocalMediaFamily::Unknown
        || !record.currentLocator.isValid()) {
        return std::nullopt;
    }
    return record;
}

} // namespace

LocalMediaContinuityStore::LocalMediaContinuityStore(QString path)
    : m_path(QDir::cleanPath(std::move(path)))
{
}

bool LocalMediaContinuityStore::load(LocalMediaStoreError *error)
{
    if (error) *error = {};
    m_records.clear();
    m_order.clear();
    m_loadWarnings.clear();

    QFile file(m_path);
    if (!file.exists()) return true;
    if (!file.open(QIODevice::ReadOnly)) {
        setError(error, LocalMediaStoreErrorCode::IoFailure,
                 QStringLiteral("The local media store could not be read."),
                 file.errorString());
        return false;
    }

    QJsonParseError parseError{};
    const QJsonDocument document =
        QJsonDocument::fromJson(file.readAll(), &parseError);
    if (parseError.error != QJsonParseError::NoError || !document.isObject()) {
        setError(error, LocalMediaStoreErrorCode::ParseFailure,
                 QStringLiteral("The local media store is corrupt."),
                 parseError.errorString());
        return false;
    }

    const QJsonObject root = document.object();
    if (root.value(QStringLiteral("schemaVersion")).toInt(-1) != 1) {
        setError(error, LocalMediaStoreErrorCode::UnsupportedVersion,
                 QStringLiteral("The local media store version is unsupported."));
        return false;
    }

    int index = 0;
    for (const auto &value : root.value(QStringLiteral("records")).toArray()) {
        const auto parsed = recordFromJson(value.toObject());
        if (!parsed || !validateRecord(*parsed, nullptr)) {
            m_loadWarnings.append(
                QStringLiteral("Quarantined malformed record %1.").arg(index++));
            continue;
        }
        if (!m_records.contains(parsed->localId))
            m_order.append(parsed->localId);
        m_records.insert(parsed->localId, *parsed);
        ++index;
    }
    return true;
}

bool LocalMediaContinuityStore::save(LocalMediaStoreError *error) const
{
    if (error) *error = {};
    const QString parent = QFileInfo(m_path).absolutePath();
    if (!parent.isEmpty() && !QDir().mkpath(parent)) {
        setError(error, LocalMediaStoreErrorCode::IoFailure,
                 QStringLiteral("The local media store directory could not be created."),
                 parent);
        return false;
    }

    QJsonArray records;
    for (const QString &localId : m_order) {
        const auto it = m_records.constFind(localId);
        if (it != m_records.constEnd())
            records.append(recordToJson(it.value()));
    }

    QJsonObject root;
    root.insert(QStringLiteral("schemaVersion"), 1);
    root.insert(QStringLiteral("records"), records);

    QSaveFile file(m_path);
    if (!file.open(QIODevice::WriteOnly)) {
        setError(error, LocalMediaStoreErrorCode::IoFailure,
                 QStringLiteral("The local media store could not be opened for writing."),
                 file.errorString());
        return false;
    }

    const QByteArray bytes =
        QJsonDocument(root).toJson(QJsonDocument::Indented);
    if (file.write(bytes) != bytes.size()) {
        file.cancelWriting();
        setError(error, LocalMediaStoreErrorCode::IoFailure,
                 QStringLiteral("The local media store could not be written."),
                 file.errorString());
        return false;
    }

    if (!file.commit()) {
        setError(error, LocalMediaStoreErrorCode::IoFailure,
                 QStringLiteral("The local media store could not be committed."),
                 file.errorString());
        return false;
    }
    return true;
}
```
