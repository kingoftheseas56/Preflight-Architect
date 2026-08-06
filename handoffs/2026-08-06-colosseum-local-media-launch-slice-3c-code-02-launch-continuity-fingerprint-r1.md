# Local Media Launch Slice 3C — Code Part 02: Launch, Continuity, and Fingerprinting r1

## Status

**Reference implementation candidate; uncompiled, untested, unexecuted, unadopted, and runtime-unverified.**

## Proposed Locations

- Likely: `native/localmedia/LocalVideoLaunchAdapter.h/.cpp`
- Likely: `native/localmedia/LocalVideoContinuityBridge.h/.cpp`
- Likely: `native/localmedia/LocalVideoFingerprintCoordinator.h/.cpp`

## Launch Adapter Contract

The adapter composes existing authorities; it does not replace them.

```cpp
class LocalVideoLaunchAdapter final : public QObject {
    Q_OBJECT
public:
    LocalVideoLaunchAdapter(
        const LocalMediaRouter *router,
        const LocalMediaClassifier *classifier,
        QList<const LocalMediaHandler *> handlers,
        LocalMediaContinuityStore *continuity,
        SessionStore *sessions,
        LibmpvAdmissionProbe *probe,
        bool player2Booted,
        QObject *parent = nullptr);

    Q_INVOKABLE quint64 open(
        const QUrl &source,
        const QString &intakeSource);

    Q_INVOKABLE void cancel(quint64 generation);

signals:
    void opened(quint64 generation,
                const QString &sessionId,
                const QString &localId);
    void failed(quint64 generation,
                const colosseum::localmedia::LocalMediaError &error);
};
```

The actual adopted Slice 1 type names may differ. Preserve the sequencing contract rather than forcing these names.

## Required State

```cpp
struct PendingVideoLaunch {
    quint64 generation = 0;
    LocalMediaRouteResult route;
    qint64 inspectedSizeBytes = -1;
    qint64 inspectedModifiedAtMs = 0;
};
```

Only one pending launch is active per adapter instance. Starting a newer launch cancels the older probe and invalidates its generation.

## Open Sequence

```cpp
quint64 LocalVideoLaunchAdapter::open(
    const QUrl &source,
    const QString &intakeSource)
{
    const quint64 generation = ++m_generation;
    m_probe->cancel();

    if (m_player2Booted) {
        emit failed(
            generation,
            LocalMediaError::make(
                LocalMediaErrorCode::Player1Required,
                QStringLiteral("Open this video in the standard Colosseum player."),
                QStringLiteral(
                    "This process booted Player 2/D3D11; Player 1/OpenGL "
                    "cannot be instantiated in the same process.")));
        return generation;
    }

    LocalMediaRouteResult route =
        m_router->route(source,
                        intakeSource,
                        *m_classifier,
                        m_handlers);

    if (!route.ok) {
        emit failed(generation, route.error);
        return generation;
    }

    if (route.kind != LocalMediaKind::Video) {
        emit failed(
            generation,
            LocalMediaError::make(
                LocalMediaErrorCode::HandlerRejected,
                QStringLiteral("That file is not a video."),
                QStringLiteral("LocalVideoLaunchAdapter received kind '%1'.")
                    .arg(localMediaKindName(route.kind))));
        return generation;
    }

    m_pending = PendingVideoLaunch{
        generation,
        route,
        route.resource.sizeBytes,
        route.resource.modifiedAt.isValid()
            ? route.resource.modifiedAt.toMSecsSinceEpoch()
            : 0
    };

    m_probe->begin(
        route.resource.canonicalPath,
        generation,
        m_admissionTimeoutMs);

    return generation;
}
```

This preserves the adopted synchronous router: routing and descriptor preparation happen before admission, but `SessionStore::openOrSwitch()` remains unreachable until admission succeeds.

## Admission Completion

```cpp
void LocalVideoLaunchAdapter::onAdmissionFinished(
    const LocalVideoAdmissionResult &result)
{
    if (result.generation != m_generation
        || result.generation != m_pending.generation)
        return;

    if (!result.admitted) {
        emit failed(result.generation, result.error);
        return;
    }

    const QFileInfo now(m_pending.route.resource.canonicalPath);
    const qint64 modifiedAtMs =
        now.lastModified().isValid()
            ? now.lastModified().toMSecsSinceEpoch()
            : 0;

    if (!now.exists()
        || !now.isFile()
        || !now.isReadable()
        || now.size() != m_pending.inspectedSizeBytes
        || modifiedAtMs != m_pending.inspectedModifiedAtMs) {
        emit failed(
            result.generation,
            LocalMediaError::make(
                LocalMediaErrorCode::ResourceChanged,
                QStringLiteral("That video changed while Colosseum was opening it."),
                QStringLiteral(
                    "Post-admission metadata no longer matches Slice 1 inspection.")));
        return;
    }

    LocalMediaStoreError storeError;
    QString localId =
        m_continuity->findByPath(
            m_pending.route.resource.canonicalPath);

    if (localId.isEmpty()) {
        LocalMediaContinuityRecord record;
        record.family = LocalMediaFamily::Video;
        record.displayTitle =
            m_pending.route.sessionDescriptor
                .value(QStringLiteral("title"))
                .toString();
        record.currentLocator.canonicalPath =
            m_pending.route.resource.canonicalPath;
        record.currentLocator.firstSeenAtMs =
            QDateTime::currentMSecsSinceEpoch();
        record.currentLocator.lastVerifiedAtMs =
            record.currentLocator.firstSeenAtMs;

        localId = m_continuity->create(
            std::move(record),
            &storeError);
    }

    if (localId.isEmpty()) {
        emit failed(
            result.generation,
            LocalMediaError::make(
                LocalMediaErrorCode::HandlerRejected,
                QStringLiteral("Colosseum could not save local playback state."),
                storeError.diagnostic));
        return;
    }

    const auto stored = m_continuity->record(localId);
    if (!stored.has_value()) {
        emit failed(
            result.generation,
            LocalMediaError::make(
                LocalMediaErrorCode::HandlerRejected,
                QStringLiteral("Colosseum could not read local playback state."),
                QStringLiteral("Slice 2 record disappeared after create/find.")));
        return;
    }

    const QVariantMap links = stored->stateLinks;
    const bool completed =
        links.value(QStringLiteral("player1.completed")).toBool();
    const double savedPosition =
        links.value(QStringLiteral("player1.positionSeconds"))
            .toDouble();

    QVariantMap descriptor =
        m_pending.route.sessionDescriptor;
    QVariantMap target =
        descriptor.value(QStringLiteral("target")).toMap();

    target.insert(QStringLiteral("id"), localId);
    target.insert(
        QStringLiteral("path"),
        m_pending.route.resource.canonicalPath);
    target.insert(QStringLiteral("localExternal"), true);
    target.insert(QStringLiteral("localMediaId"), localId);
    target.insert(
        QStringLiteral("position"),
        completed ? 0.0 : qMax(0.0, savedPosition));

    descriptor.insert(QStringLiteral("appType"),
                      QStringLiteral("theatre"));
    descriptor.insert(QStringLiteral("contentKind"),
                      QStringLiteral("movie"));
    descriptor.insert(QStringLiteral("target"), target);

    // Persist the device-local open before the first shell-session mutation.
    // A store failure must not silently fall back to global progress.
    if (!m_continuity->markOpened(
            localId,
            QDateTime::currentMSecsSinceEpoch(),
            &storeError)) {
        emit failed(
            result.generation,
            LocalMediaError::make(
                LocalMediaErrorCode::HandlerRejected,
                QStringLiteral("Colosseum could not save local playback state."),
                storeError.diagnostic));
        return;
    }

    // The first shell-session mutation in the entire flow.
    const QString sessionId =
        m_sessions->openOrSwitch(descriptor);

    if (sessionId.isEmpty()) {
        emit failed(
            result.generation,
            LocalMediaError::make(
                LocalMediaErrorCode::InvalidSessionDescriptor,
                QStringLiteral("Colosseum could not create the player session."),
                QStringLiteral("SessionStore::openOrSwitch returned empty.")));
        return;
    }

    emit opened(result.generation, sessionId, localId);
}
```

### Required adaptation

The corrected Slice 2 candidate currently names its store `LocalMediaContinuityStore` in the issue but the r1 code candidate uses `LocalMediaContinuityStore`/`LocalMediaContinuityRecord`-style concepts with exact names that must be reconciled at adoption. The execution agent must use the actually adopted API; it must not introduce a second store.

## Continuity Bridge

Expose one narrow QML-facing bridge. It writes only Slice 2 state and never calls `ProgressStore`.

```cpp
class LocalVideoContinuityBridge final : public QObject {
    Q_OBJECT
public:
    explicit LocalVideoContinuityBridge(
        LocalMediaContinuityStore *store,
        LocalVideoFingerprintCoordinator *fingerprints,
        QObject *parent = nullptr);

    Q_INVOKABLE bool recordProgress(
        const QString &localId,
        double positionSeconds,
        double durationSeconds,
        bool completed);

    // Returns true only when the actual Player 1 error maps to a
    // missing/unreadable locator. All external-local playback failures still
    // preserve the shell session.
    Q_INVOKABLE bool handlePlaybackError(
        const QString &localId,
        const QString &code,
        const QString &message);

    Q_INVOKABLE void playbackStarted(
        const QString &localId,
        const QString &canonicalPath,
        quint64 generation);

    Q_INVOKABLE void cancelFingerprint(
        quint64 generation);
};
```

Candidate state update:

```cpp
bool LocalVideoContinuityBridge::recordProgress(
    const QString &localId,
    double positionSeconds,
    double durationSeconds,
    bool completed)
{
    const auto existing = m_store->record(localId);
    if (!existing.has_value())
        return false;

    LocalMediaContinuityRecord record = *existing;
    record.stateLinks.insert(
        QStringLiteral("player1.positionSeconds"),
        completed ? 0.0 : qMax(0.0, positionSeconds));
    record.stateLinks.insert(
        QStringLiteral("player1.durationSeconds"),
        qMax(0.0, durationSeconds));
    record.stateLinks.insert(
        QStringLiteral("player1.completed"),
        completed);
    record.stateLinks.insert(
        QStringLiteral("player1.sourceUnavailable"),
        false);

    LocalMediaStoreError error;
    return m_store->upsert(std::move(record), &error);
}
```

Candidate playback-error update:

```cpp
bool LocalVideoContinuityBridge::handlePlaybackError(
    const QString &localId,
    const QString &code,
    const QString &message)
{
    const bool unavailable =
        isMissingOrUnreadablePlayer1Error(code, message);

    if (!unavailable)
        return false;

    const auto existing = m_store->record(localId);
    if (!existing.has_value())
        return false;

    LocalMediaContinuityRecord record = *existing;
    record.stateLinks.insert(
        QStringLiteral("player1.sourceUnavailable"),
        true);

    LocalMediaStoreError error;
    m_store->upsert(std::move(record), &error);
    return true;
}
```

`isMissingOrUnreadablePlayer1Error()` must be grounded in the actually adopted `MpvItem` error mapping. Do not classify every decode/playback failure as a missing source.

This method does **not** call `SessionStore::close()`. All external-local playback failures preserve the shell session; only the Slice 2 unavailable flag is category-specific.

## Fingerprint Coordinator

Fingerprinting begins only after PlayerPage reports its existing visual `playbackStarted` truth. It must not begin after descriptor preparation, admission success, session creation, `loadFile()` dispatch, or `fileLoaded` alone.

Recommended algorithm:

```text
sha256-v1 over source bytes
```

Required mechanics:

- run outside the GUI thread;
- carry `localId`, canonical path, source generation, size, and modified time;
- cancel on superseding launch, session close, relocation, or source generation change;
- before storing, re-check generation and file metadata;
- append the fingerprint only to the same `localId`;
- call `findByFingerprint()` only to expose possible matches;
- never merge, delete, or rewrite identities automatically.

Candidate completion guard:

```cpp
if (result.cancelled
    || result.generation != m_generation
    || !sameFileMetadata(result, QFileInfo(result.path)))
    return;

const auto record = m_store->record(result.localId);
if (!record.has_value())
    return;

LocalMediaContinuityRecord updated = *record;
updated.fingerprints.append(LocalMediaFingerprint{
    QStringLiteral("sha256-v1"),
    result.hexDigest,
    result.sizeBytes,
    result.modifiedAtMs
});

LocalMediaStoreError error;
m_store->upsert(std::move(updated), &error);

// Lookup evidence only.
const QStringList possibleMatches =
    m_store->findByFingerprint(
        QStringLiteral("sha256-v1"),
        result.hexDigest);
emit fingerprintObserved(result.localId, possibleMatches);
```

## Concurrency and Ordering Invariants

1. Probe work and fingerprint work never run on the GUI thread.
2. Only one thread calls `mpv_wait_event()` for a probe handle.
3. A stale probe callback cannot create a session.
4. A stale fingerprint callback cannot mutate Slice 2.
5. Session creation occurs once, after admission.
6. Visual Player 1 playback is requested before hashing starts.
7. Store errors are surfaced; they do not silently fall back to `ProgressStore`.
8. Source disappearance after session creation never closes the session.

## Completion Criterion

This part is adoption-ready only when fake-probe tests prove the sequencing invariants and the execution agent has reconciled every type/method name against the actually adopted Slice 1 and Slice 2 APIs.
