# Local Media Launch Slice 3C — Code Part 04: Tests, Build, and Adoption r1

## Status

**Reference implementation candidate; uncompiled, untested, unexecuted, unadopted, and runtime-unverified.**

## Build Registration

The pinned build already exposes `Libmpv_INCLUDE_DIRS`, `Libmpv_LIBRARIES`, `MpvQt::MpvQt`, Qt Concurrent, and the `colosseum` target.

Candidate application amendments:

```cmake
target_sources(colosseum PRIVATE
    localmedia/LocalVideoAdmission.h
    localmedia/LibmpvAdmissionProbe.cpp
    localmedia/LibmpvAdmissionProbe.h
    localmedia/LocalVideoLaunchAdapter.cpp
    localmedia/LocalVideoLaunchAdapter.h
    localmedia/LocalVideoContinuityBridge.cpp
    localmedia/LocalVideoContinuityBridge.h
    localmedia/LocalVideoFingerprintCoordinator.cpp
    localmedia/LocalVideoFingerprintCoordinator.h
)

target_include_directories(colosseum PRIVATE
    ${Libmpv_INCLUDE_DIRS}
)

target_link_libraries(colosseum PRIVATE
    ${Libmpv_LIBRARIES}
)
```

Keep the existing `MpvQt::MpvQt` and Qt target links. The direct libmpv link is for the new client API caller.

Candidate probe harness:

```cmake
add_executable(local_video_admission_harness
    ../tests/local_video_admission_harness.cpp
    localmedia/LibmpvAdmissionProbe.cpp
    localmedia/LibmpvAdmissionProbe.h
    localmedia/LocalVideoAdmission.h
)

target_include_directories(local_video_admission_harness PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${Libmpv_INCLUDE_DIRS}
)

target_link_libraries(local_video_admission_harness PRIVATE
    Qt6::Core
    Qt6::Concurrent
    ${Libmpv_LIBRARIES}
)

colosseum_register_harness(
    local_video_admission_harness
    unit
    local-media
)
```

The execution agent must place this beside the repository’s current harness registrations rather than applying stale line anchors.


## Runtime Registration

At the pinned boot seam, construct the adapter with the **actual** `bootPlayer2` value, not the compile-time Player 2 capability flag. Register only the narrow QML bridge:

```cpp
LocalVideoContinuityBridge localExternalVideo(
    &localMediaContinuityStore,
    &localVideoFingerprintCoordinator);

engine.rootContext()->setContextProperty(
    QStringLiteral("LocalExternalVideo"),
    &localExternalVideo);
```

The exact engine/context variable must be reconciled with `native/main.cpp`. The launch adapter remains native orchestration; QML should not receive the raw Slice 2 store or bare libmpv probe.

## Hermetic Seam

Define an interface or injectable callable so adapter tests do not require live libmpv:

```cpp
class LocalVideoAdmission {
public:
    virtual ~LocalVideoAdmission() = default;
    virtual void begin(
        const QString &path,
        quint64 generation,
        int timeoutMs) = 0;
    virtual void cancel() = 0;
};
```

A fake probe must be able to deliver:

- success;
- categorized failure;
- timeout;
- cancellation;
- stale success after a newer generation;
- success followed by source metadata change.

Use spies/fakes for `SessionStore`, Slice 2 persistence, subtitle-provider calls, global `ProgressStore`, account calls, Player 1 load calls, Player 2 construction, and fingerprint job start.

## Acceptance-Test Matrix

| ID | Test | Type | Proves |
|---|---|---|---|
| `LML-3C-H01` | valid route + admitted probe calls session open once and Player 1 load once | hermetic | AC1 |
| `LML-3C-H02` | Player 2 boot returns `Player1Required`; session/player spies remain zero | hermetic | AC2 |
| `LML-3C-H03` | unfinished state places saved position in target | hermetic | AC3 |
| `LML-3C-H04` | completed state places zero position in target | hermetic | AC3 |
| `LML-3C-H05` | Slice 2 save/load round-trip preserves Player 1 state links | hermetic integration | AC4 |
| `LML-3C-H06` | rejected admission emits categorized failure and session count remains zero | hermetic | AC5 |
| `LML-3C-H07` | stale/cancelled probe cannot create session | hermetic | AC5 |
| `LML-3C-H08` | source changes after admission; `ResourceChanged`; no session | hermetic | AC5 |
| `LML-3C-H09` | post-open source error marks unavailable but never closes session | hermetic | AC6 |
| `LML-3C-H10` | external-local open makes zero provider, Progress, and account calls | QML hermetic | isolation |
| `LML-3C-H11` | downloaded-file path still calls existing provider/progress behavior | regression | non-goal |
| `LML-3C-H12` | fingerprint cannot start before playback-start notification | hermetic | ordering |
| `LML-3C-H13` | stale fingerprint cannot mutate store | hermetic | cancellation |
| `LML-3C-H14` | equal fingerprint emits possible matches but never merges records | hermetic | identity |
| `LML-3C-H15` | repeated open of same localId reuses one SessionStore session | hermetic | exactly one session |
| `LML-3C-H16` | relocation preserves localId and SessionStore identity | hermetic integration | source recovery |

## Named Live-libmpv Gates

### `LML-3C-MPV-01` — Supported first frame

A representative supported local video is admitted, opens exactly one Theatre movie session, instantiates Player 1, calls `loadFile`, and renders/advances.

### `LML-3C-MPV-02` — Playback before fingerprint

Trace monotonic timestamps for:

```text
session-open
loadFile
fileLoaded
playbackStarted
fingerprint-start
```

Pass only when `playbackStarted < fingerprint-start`.

### `LML-3C-MPV-03` — Unfinished resume

Persist a mid-file position, restart the application, reopen the same `localId`, and prove actual Player 1 position lands within the agreed tolerance.

### `LML-3C-MPV-04` — Completed restart

Reach real `endFile("eof")`, restart, reopen, and prove playback begins at zero rather than the prior near-end position.

### `LML-3C-MPV-05` — Decode admission discrimination

Before any session exists, test:

- corrupt/truncated;
- encrypted/protected;
- unsupported codec;
- missing/unreadable.

Each must return the approved typed category. If the baseline `vid=no` probe falsely admits any fixture, stop and implement the null-output first-frame strengthening branch before proceeding.

### `LML-3C-MPV-06` — No subtitle-provider contact

Instrument the network/provider seam. Opening and playing external-local media produces zero subtitle-provider requests.

### `LML-3C-MPV-07` — No global/account persistence

Instrument `ProgressStore`, Continue refresh, and account persistence. External-local playback produces zero calls and no Continue row. Slice 2 state must still update.

### `LML-3C-MPV-08` — Source unavailable preserves session

After session creation, remove or revoke the source. Player 1 surfaces unavailable state while the same taskbar/session ID remains present.

### `LML-3C-MPV-09` — Player 1 only

Object construction and QML tracing show one Player 1 surface and zero Player 2 backend/video-item instances for the local-video flow.

### `LML-3C-MPV-10` — Player 2 edge guard

Boot with the existing Player 2 opt-in. Local-video launch returns `Player1Required`, creates no session, and does not attempt a Player 1 object.

## Adoption Slices

### Slice A — Probe experiment

**Produces:** measured evidence for supported and rejected fixtures.  
**Stop condition:** baseline probe is insufficient and no bounded strengthening experiment exists.  
**Verification:** `LML-3C-MPV-05`.

### Slice B — Typed admission component

**Depends on:** Slice A.  
**Produces:** cancellable probe with fake seam and harness.  
**Verification:** `H06/H07/H08` plus timeout/cancel measurements.

### Slice C — Launch adapter and Slice 2 link

**Depends on:** adopted/reconciled Slice 1 and corrected Slice 2 r2.  
**Produces:** admission-before-session vertical and opaque-localId descriptor.  
**Verification:** `H01-H06`, `H15-H16`.

### Slice D — Player 1 external-local mode

**Depends on:** Slice C.  
**Produces:** dedicated external-local entrypoint with no provider/global progress.  
**Verification:** `H09-H11`, `MPV-01`, `MPV-06`, `MPV-07`, `MPV-09`.

### Slice E — Resume, completion, and unavailable source

**Depends on:** Slice D.  
**Produces:** real state round-trip and session-preservation behavior.  
**Verification:** `MPV-03`, `MPV-04`, `MPV-08`.

### Slice F — Deferred fingerprint

**Depends on:** reliable visual playback-start signal.  
**Produces:** cancellable post-playback hash with no automatic merge.  
**Verification:** `H12-H14`, `MPV-02`.

### Slice G — Regression and integration checkpoint

**Depends on:** all prior slices.  
**Produces:** clean baseline plus adopted commit report.  
**Verification:** existing Player 1, downloaded-file, SessionStore, ProgressStore, Slice 1, Slice 2, Reader 2, and comic-ledger regressions.

## Required Evidence Report

Agent 0 must return:

- adopted commit and exact paths;
- compile/build output;
- hermetic test output;
- live-gate results with fixture descriptions;
- probe latency distribution and selected timeout;
- every divergence from the reference code;
- proof downloaded-file behavior is unchanged;
- proof no provider/global/account side effect occurred;
- proof source-unavailable state retained the same session ID;
- remaining unverified platforms or codecs.

## Rollback and Containment

- Keep the external-local dispatcher branch isolated behind its explicit target marker.
- Do not modify the semantics of `playLocalFile()`.
- If live admission is unreliable, disable only external-local video launch and retain Slice 1/2 adoption.
- Never fall back to Player 2, global progress, extension-only admission, or pre-play hashing.
- A failed integration must not delete Slice 2 records or source media.

## First Executable Action

Create the smallest `local_video_admission_harness` at the pinned commit and run `LML-3C-MPV-05` fixtures before reconstructing the rest of the bundle.
