# Local Media Launch — Slice 0 Implementation Prototype

## Status

**Repository-grounded implementation prototype. Static inspection complete; builds, automated tests, Lanista, and runtime validation were not run.**

This artifact implements roadmap Slice 0 as a contract map and bounded prototype for Slice 1. It does not modify Colosseum and is not adopted product code.

## Basis

- Specification: `specifications/2026-08-06-colosseum-local-media-launch-specification.md`
- Roadmap: `roadmaps/2026-08-06-colosseum-local-media-launch-implementation-roadmap.md`
- Colosseum basis: `master@bb8eecb40eb8a50b7ded62f79035c555972c3fef`
- Previous roadmap basis: `879e1e93e2084659c74a228bb5792b23174236e2`

The newer Colosseum revision is authoritative for this prototype.

## Verdict

Proceed conditionally to Slice 1: shared resource, handler, routing, and error contracts.

The first code bundle should be limited to:

```text
untrusted intake
→ inspection
→ typed validation
→ media classification
→ handler selection
→ current SessionStore descriptor
→ typed result
```

It excludes taskbar UI, native picker, drag-and-drop, Open-with, persistence, recents, relocation, identification, subtitle acquisition, tray behavior, and packaging.

## Confirmed Repository Contracts

### Taskbar and shell

`qml/Taskbar.qml` is the user-facing session switcher and action surface. It reads session groups and active-session state from `SessionStore`-exposed QML APIs and already handles switching, closing, and shell actions.

The shared local-media action should not be implemented first in the taskbar. The taskbar should eventually call a stable intake contract.

### SessionStore

`native/SessionStore.h` is the shell authority for session identity and replacement.

Confirmed concepts include:

- session id;
- target key;
- content key;
- application type;
- content kind;
- title;
- target descriptor;
- saved state.

The current behavior distinguishes exact-content reuse from target replacement. A local path is therefore not sufficient as durable content identity.

Slice 1 must preserve `SessionStore` as the session-lifecycle authority. Handlers should prepare descriptors rather than creating parallel session ownership.

### Reader 2

Reader 2 state is path-keyed through a normalized path-derived key. Progress, bookmarks, and annotations depend on that key.

Implication: moved-file recovery and copy detection cannot be solved safely by Slice 1. They require the isolated continuity and identity store in Slice 2.

### Comic ingestion

At the inspected revision, `native/engine/ComicDownloader.h` exposes local archive ingestion for CBR, CBZ, CB7, and CBT.

Confirmed behavior includes:

- readable CBZ files may use archive-in-place handling;
- other accepted archive forms may extract and repack;
- successful ingestion may consume or relocate the source;
- failed ingestion preserves the source;
- asynchronous completion is guarded;
- recovery may adopt an already-produced canonical archive.

`native/comicreader/ComicReaderCore.h` consumes ordered local page URLs. It is not itself the raw archive-ingestion boundary.

Slice 1 must therefore route comic archives to an explicit importer seam and must not pass CBR or CBZ directly into the reader core.

The user-selected source copy-versus-move policy remains unresolved and must not be invented.

### Player 1 and subtitles

Player 1 exposes local file loading, playback position and duration, track selection, external subtitle attachment, and subtitle controls.

Slice 1 should prepare a validated Player 1 session descriptor only. Subtitle discovery, hashing, remote acquisition, caching, and manual add-ons remain in Slice 9.

### Persistence

The existing progress store provides a useful hermetic-test pattern, including an explicit backing path, but it is oriented around current progress/continue behavior.

It should not silently become the device-local identity database. Slice 2 owns that store.

### Platform intake

No single confirmed abstraction yet unifies:

- native file dialogs;
- drag-and-drop;
- command-line file arguments;
- `QFileOpenEvent`;
- OS Open-with;
- sandbox-granted handles;
- copy fallback for short-lived access grants.

Slice 1 must keep resource intake abstract. Platform adapters belong in Slice 6 after resource, access-lifetime, and fallback semantics are explicit.

## Slice 1 Interface Prototype

Exact names and paths remain recommendations until an execution agent confirms local conventions.

```cpp
enum class LocalMediaKind {
    Unknown,
    Book,
    ComicArchive,
    Video
};

enum class LocalMediaErrorCode {
    None,
    EmptyResource,
    UnsupportedScheme,
    NotFound,
    NotReadable,
    DirectoryNotSupported,
    UnsupportedFormat,
    AmbiguousFormat,
    HandlerUnavailable,
    LaunchRejected
};

struct LocalMediaResource {
    QUrl source;
    QString displayName;
    QString canonicalPath;
    QString extension;
    qint64 sizeBytes = -1;
    LocalMediaKind kind = LocalMediaKind::Unknown;
};

struct LocalMediaError {
    LocalMediaErrorCode code = LocalMediaErrorCode::None;
    QString userMessage;
    QString diagnostic;
};

struct LocalMediaOpenRequest {
    LocalMediaResource resource;
    QString intakeSource;
};

struct LocalMediaRoute {
    QString handlerId;
    QVariantMap sessionDescriptor;
};

class LocalMediaInspector {
public:
    virtual ~LocalMediaInspector() = default;
    virtual std::variant<LocalMediaResource, LocalMediaError>
    inspect(const QUrl &source) const = 0;
};

class LocalMediaHandler {
public:
    virtual ~LocalMediaHandler() = default;
    virtual QString id() const = 0;
    virtual bool supports(LocalMediaKind kind) const = 0;
    virtual std::variant<LocalMediaRoute, LocalMediaError>
    prepare(const LocalMediaOpenRequest &request) const = 0;
};
```

Required properties:

- intake is untrusted until inspected;
- extension is only an initial classifier;
- canonical path and stable identity remain separate;
- handlers prepare descriptors and do not mutate `SessionStore`;
- user-facing messages and diagnostics remain separate;
- all failures are typed;
- no picker, UI, recents, persistence, relocation, subtitles, or packaging behavior appears in Slice 1;
- comic archive ownership remains unresolved until approved.

Recommended handler responsibilities:

```text
Book  → validate supported Reader 2 input → prepare book descriptor
Comic → validate archive → delegate to importer seam → prepare comic descriptor
Video → validate readable local file → prepare Player 1 descriptor
```

## Likely Target Surface

These paths are recommendations, not confirmed repository decisions:

```text
native/localmedia/LocalMediaTypes.h
native/localmedia/LocalMediaInspector.h
native/localmedia/LocalMediaInspector.cpp
native/localmedia/LocalMediaRouter.h
native/localmedia/LocalMediaRouter.cpp
native/localmedia/LocalMediaHandlers.h
native/localmedia/LocalMediaHandlers.cpp
tests/local_media_contract_harness.cpp
```

The execution agent must confirm actual CMake and test placement before implementation.

## Candidate Baselines

Relevant regression surfaces were discovered for:

- taskbar and session behavior;
- Reader 2 bridge and state stores;
- comic archive probing, ingestion, reader core, and acceptance flows;
- Player 1 resume and subtitle behavior;
- progress-store isolation;
- Lanista scenarios and golden evidence.

No pass or fail result is claimed.

## Required Execution Evidence Before Slice 1 Publication

An execution agent must:

1. build the affected current targets;
2. run focused taskbar and `SessionStore` baselines;
3. run Reader 2 state baselines;
4. run comic archive ingestion and reader baselines;
5. run Player 1 local-source and subtitle baselines;
6. run the relevant persistence baseline;
7. run one isolated Lanista shell/session scenario;
8. record exact commands, targets, fixtures, results, failures, and blockers;
9. confirm the CMake and test-registration seams;
10. reconcile repository drift and failed assumptions.

A pre-existing failure becomes a named constraint or stop condition.

## Open Questions

- Which Reader 2 local book formats are currently supported?
- Does user-selected comic media get copied, moved, or imported according to another rule?
- What is the narrowest Player 1 local-source adapter?
- Which session descriptor fields are mandatory for each target?
- Should stable fingerprinting be eager or deferred?
- Which platforms are first-class for Slice 6?
- What sandbox resource representation and copy fallback are required?
- What is the smallest Lanista scenario proving that one validated resource creates exactly one correct session?

## Stop Conditions

Return to design rather than forcing Slice 1 when:

- shared contracts require an unapproved build architecture;
- comic ownership semantics conflict with the product specification;
- Reader 2 requires an unapproved migration;
- Player 1 bypasses shell session lifecycle;
- a required platform has no safe resource-lifetime strategy;
- baseline failures make intended behavior indeterminate;
- Slice 1 cannot be tested without persistence, UI, or platform intake.

## Exact Next Action

Run and record the Slice 0 baseline against `master@bb8eecb40eb8a50b7ded62f79035c555972c3fef`, reconcile drift and failed assumptions, then generate the Slice 1 Reference Implementation Bundle against the resulting exact Colosseum commit.
