# Local Media Launch Slice 2 — Reference Implementation Manifest

## Code Status

**Implementable reference code — uncompiled, untested, unexecuted, unadopted, and unverified.**

## Bundle Type

Interim split Reference Implementation Bundle. The atomic `writePreflightReferenceBundle` bridge does not yet exist, so this revision is stored as coordinated Markdown parts.

## Repository Basis

- Repository: `kingoftheseas56/Colosseum`
- Branch inspected: `master`
- Base commit: `a40333dc1fc9823ceb9decd811deeadde6ac4c2d`
- Specification: `specifications/2026-08-06-colosseum-local-media-launch-specification.md`
- Roadmap: `roadmaps/2026-08-06-colosseum-local-media-launch-implementation-roadmap.md`
- Slice 0 prototype: `research/2026-08-06-colosseum-local-media-launch-slice-0-implementation-prototype.md`

## Dependency Status

Slice 1 exists only as unadopted reference code. This Slice 2 candidate therefore does **not** include or depend on the proposed Slice 1 headers. It exposes a standalone continuity-store API and leaves one explicit adapter boundary for the eventual adopted launch-resource contract.

The execution agent must reconcile this candidate with the actually adopted Slice 1 interface before integration.

## Objective

Create an isolated, versioned, device-local continuity and identity store that:

- separates opaque local identity from resource location;
- persists current and historical locators;
- persists recency without polluting `ProgressStore::recent()`;
- persists media family, cleaned title, retained access tokens, fingerprints, progress/state links, optional identification, subtitle references, and copy/changed-content relationships;
- supports relocation repair;
- distinguishes clearing recents from fully forgetting a local item;
- never modifies or deletes source media.

## Confirmed Repository Analogues

- `native/torrent/ComicRequestLedger.{h,cpp}`: versioned JSON, `QSaveFile`, absent-file first run, version rejection, malformed-row quarantine, atomic replacement.
- `native/ProgressStore.h`: explicit persistence-path constructor and hermetic test pattern, but it remains the online/Continue authority and is not reused as the local-media identity database.
- `native/reader2/Reader2Bridge.h`: Reader 2 continuity is currently keyed by a SHA-1-derived normalized absolute path. This candidate stores that existing key as an opaque state link; it does not rewrite Reader 2 stores.
- `native/CMakeLists.txt` and `tests/CMakeLists.txt`: standalone harness target plus CTest registration.

## Proposed Target Files

```text
native/localmedia/LocalMediaContinuityStore.h
native/localmedia/LocalMediaContinuityStore.cpp
tests/local_media_continuity_store_harness.cpp
native/CMakeLists.txt
tests/CMakeLists.txt
```

These are proposed paths. The execution agent must confirm naming and placement against the current repository before adoption.

## Data Authority

The continuity store owns:

- opaque `localId`;
- media family and cleaned display title;
- current locator and locator history;
- retained opaque platform-access data;
- fingerprints supplied by other components;
- links to component-owned progress/state;
- recency;
- optional external identification;
- subtitle references;
- explicit `copy-of` and `changed-from` relationships.

It does **not** own:

- source media bytes;
- Reader 2, ComicReader 2, or Player 1 progress payloads;
- subtitle file bytes;
- platform permission acquisition;
- fingerprint computation;
- session lifecycle;
- UI state.

## Persistence Contract

- One versioned JSON document.
- Atomic replacement via `QSaveFile`.
- Missing file means an empty first-run store.
- Unknown schema version fails closed and preserves the current in-memory snapshot.
- Invalid root JSON fails closed.
- Invalid individual records are quarantined and reported through load warnings.
- Every mutating operation persists atomically or rolls its in-memory mutation back.
- No source-media path is opened for write or removal.

## Identity Contract

- `localId` is a generated UUID and remains stable across relocation.
- Canonical path is a locator, not identity.
- Fingerprints are lookup evidence, not automatically authoritative identity.
- Multiple records may share a fingerprint; copy relationships must be explicit.
- Changed-content relationships must be explicit.
- Path lookup includes current and historical locators.
- Global path comparison is case-sensitive except on Windows.
- The store does not decide whether two observations are copies or changed content.

## Recents and Forget Semantics

- `markOpened()` changes recency only.
- `clearRecents()` clears timestamps while preserving identity, locators, fingerprints, state links, identification, and subtitle references.
- `forget()` atomically removes the local record and returns the removed record to the caller.
- The caller may use returned state/cache references to remove local derived state.
- `forget()` never deletes or mutates source media.

## Reader 2 Compatibility

Until Reader 2 accepts an external stable identity, the adapter should preserve its current path-derived key in:

```text
stateLinks["reader2.pathKey"]
```

On relocation, Slice 2 preserves the previous locator and stable `localId`. Migration or aliasing of Reader 2’s component-owned files remains an integration responsibility and must not be silently performed by this store.

## Candidate Tests

The harness covers:

- first-run empty store;
- create and restart persistence;
- stable identity across relocation;
- current and historical path lookup;
- retained fingerprint, state/progress, access-token, identification, and subtitle metadata;
- recents ordering;
- clear-recents preserving continuity across restart;
- multiple records sharing one fingerprint;
- explicit copy relationship;
- full forget returning cleanup references while leaving source files untouched;
- unknown schema rejection;
- malformed-row quarantine.

## Required Execution Verification

1. Reconcile with the adopted Slice 1 types and exact current Colosseum commit.
2. Apply in an isolated branch or worktree.
3. Confirm the proposed paths and CMake insertion points.
4. Compile the harness and affected app target.
5. Run the harness directly.
6. Run `ctest` for its registered name and relevant unit label.
7. Run existing `ProgressStore`, Reader 2 store/bridge, and comic-ledger regressions.
8. Confirm no local-media row appears in `ProgressStore::recent()`.
9. Confirm clear-recents preserves Reader 2 state-link continuity.
10. Confirm full forget removes only local metadata/derived caches selected by the caller and leaves source media unchanged.
11. Add one isolated Lanista scenario only after the store is connected to a real launch/session path.

## Permitted Divergence

The execution agent may change names, paths, containers, JSON field names, error transport, or threading strategy when current repository evidence requires it. It must preserve:

- stable opaque identity;
- location/identity separation;
- isolated local persistence;
- atomic writes;
- clear-recents versus full-forget distinction;
- source-media non-destruction;
- explicit relationship semantics;
- versioned schema;
- hermetic tests.

## Stop Conditions

Stop and return evidence instead of forcing adoption when:

- the adopted Slice 1 contract makes this record shape incompatible;
- another current store already owns these exact semantics;
- Reader 2 relocation requires an unapproved migration;
- platform access tokens cannot be persisted safely as opaque data;
- the store requires live user data for tests;
- full forget cannot be scoped away from source media;
- a baseline regression makes the acceptance result ambiguous.
