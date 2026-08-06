# Local Media Launch Slice 2 — Reference Code

**Status:** implementable reference code; uncompiled, untested, unexecuted, unadopted, and unverified.

**Colosseum basis:** `master@a40333dc1fc9823ceb9decd811deeadde6ac4c2d`

## `native/localmedia/LocalMediaContinuityStore.h`

```cpp
#ifnndef COLOSSEUM_LOCALMEDIA_CONTINUITY_STORE_H
#define COLOSSEUM_LOCALMEDIA_CONTINUITY_STORE_H

#include <QDateTime>
#include <QHash>
#include <QList>
#include <QString>
#include <QStringList>
#include <QVariantMap>

#include <optional>

namespace colosseum::localmedia {

enum class LocalMediaFamily {
    Unknown,
    Book,
    Comic,
    Video
};

enum class LocalMediaRelationshipKind {
    CopyOf,
    ChangedFrom
};

enum class LocalMediaStoreErrorCode {
    None,
    InvalidArgument,
    NotFound,
    DuplicateLocation,
    IoFailure,
    ParseFailure,
    UnsupportedVersion
};

struct LocalMediaStoreError {
    LocalMediaStoreErrorCode code = LocalMediaStoreErrorCode::None;
    QString userMessage;
    QString diagnostic;

    bool isError() const { return code != LocalMediaStoreErrorCode::None; }
};

struct LocalMediaFingerprint {
    QString algorithm;
    QString value;
    qint64 sizeBytes = -1;
    qint64 modifiedAtMs = 0;

    bool isValid() const {
        return !algorithm.trimmed().isEmpty()
            && !value.trimmed().isEmpty();
    }
};

struct LocalMediaLocator {
    QString canonicalPath;
    QString opaqueAccessToken;
    qint64 firstSeenAtMs = 0;
    qint64 lastVerifiedAtMs = 0;

    bool isValid() const
    {
        return !canonicalPath.trimmed().isEmpty();
    }
};

struct LocalMediaRelationship {
    LocalMediaRelationshipKind kind = LocalMediaRelationshipKind::CopyOf;
    QString otherLocalId;
};

struct LocalMediaContinuityRecord {
    QString localId;
    LocalMediaFamily family = LocalMediaFamily::Unknown;
    QString displayTitle;
    LocalMediaLocator currentLocator;
    QList<LocalMediaLocator> locatorHistory;
    QList<LocalMediaFingerprint> fingerprints;
    QVariantMap stateLinks;
    qint64 lastOpenedAtMs = 0;
    QVariantMap identification;
    QList<QVariantMap> subtitleReferences;
    QList<LocalMediaRelationship> relationships;
    qint64 createdAtMs = 0;
    qint64 updatedAtMs = 0;
};

class LocalMediaContinuityStore {
public:
    explicit LocalMediaContinuityStore(QString path);

    bool load(LocalMediaStoreError *error = nullptr);
    bool save(LocalMediaStoreError *error = nullptr) const;

    QList<LocalMediaContinuityRecord> all() const;
    QList<LocalMediaContinuityRecord> recents(int limit = -1) const;
    std::optional<LocalMediaContinuityRecord> record(const QString &localId) const;

    QString create(LocalMediaContinuityRecord prototype,
                  LocalMediaStoreError *error = nullptr);
    bool upsert(LocalMediaContinuityRecord record,
                LocalMediaStoreError *error = nullptr);
    bool markOpened(const QString &localId,
                   qint64 openedAtMs = 0,
                   LocalMediaStoreError *error = nullptr);
    bool relocate(const QString &localId,
                   LocalMediaLocator locator,
                   LocalMediaStoreError *error = nullptr);
    bool setRelationship(const QString &localId,
                        LocalMediaRelationshipKind kind,
                        const QString &otherLocalId,
                        LocalMediaStoreError *error = nullptr);
    bool clearRecents(LocalMediaStoreError *error = nullptr);
    std::optional<LocalMediaContinuityRecord> forget(
        const QString &localId,
        LocalMediaStoreError *error = nullptr);

    QString findByPath(const QString &path) const;
    QStringList findByFingerprint(const QString &algorithm,
                                const QString &value) const;
    QStringList loadWarnings() const;
    QString path() const;

    static QString normalizePath(const QString &path);

private:
    bool validateRecord(const LocalMediaContinuityRecord &record,
                        LocalMediaStoreError *error) const;
    bool persistMutation(
        const QHash<QString, LocalMediaContinuityRecord> &oldRecords,
        const QStringList &oldOrder,
        LocalMediaStoreError *error);
    QString occupyingIdForPath(const QString &path,
                               const QString &exceptId = {}) const;

    QString m_path;
    QHash<QString, LocalMediaContinuityRecord> m_records;
    QStringList m_order;
    QStringList m_loadWarnings;
};

QString localMediaFamilyName(LocalMediaFamily family);
QString relationshipKindName(LocalMediaRelationshipKind kind);
QString localMediaStoreErrorCodeName(LocalMediaStoreErrorCode code);

} // namespace colosseum::localmedia

#endif // COLOSSEUM_LOCALMEDIA_CONTINUITY_STORE_H
```
