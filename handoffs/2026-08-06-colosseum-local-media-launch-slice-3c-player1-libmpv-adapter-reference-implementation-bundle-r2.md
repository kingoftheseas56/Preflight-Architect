# Local Media Launch Slice 3C — Player 1/libmpv Adapter Reference Implementation Bundle r2

## Status

**Design approved; reference implementation candidate only. Uncompiled, untested, unexecuted, unadopted, and runtime-unverified.**

This immutable r2 bundle supersedes the r1 manifest and the earlier Slice 3C conflict handoff as the active adoption input. The conflict handoff remains historical evidence. Brotherhood review approved decisions **A1 + B1**, corrected the RHI framing, and supplied the bare-libmpv admission direction.

## Basis

- Colosseum: `master@a40333dc1fc9823ceb9decd811deeadde6ac4c2d`
- Issue: `kingoftheseas56/Preflight-Architect#1`
- Slice 1 router: `handoffs/2026-08-06-colosseum-local-media-launch-slice-1-code-03-router-r2.md`
- Slice 2 correction: `handoffs/2026-08-06-colosseum-local-media-launch-slice-2-corrected-r2-reference-implementation-bundle.md`
- Prior stop-condition record: `handoffs/2026-08-06-colosseum-local-media-launch-slice-3c-player1-libmpv-conflict-and-impact-handoff.md`

## Approved Decisions

### A1 — Player 1 default, Player 2 edge guard

Player 1/mpv/OpenGL is the default runtime boot at the pinned commit. Player 2/D3D11 is an explicit opt-in boot. Local external video therefore ships through the default Player 1 path.

When the process actually booted Player 2, the launch adapter returns typed `Player1Required` and creates no session. It does not restart the process and never instantiates Player 1 inside a D3D11 boot.

### B1 — Pre-session bare-libmpv admission

The synchronous Slice 1 router remains descriptor preparation. It does not create shell sessions.

After the router succeeds, a cancellable, time-bounded, non-visual bare-libmpv probe runs before `SessionStore::openOrSwitch()`. Only an admitted resource may create or activate a session.

The baseline probe uses a private `mpv_handle`, no config/scripts, `vid=no`, `vo=null`, and waits for `MPV_EVENT_FILE_LOADED` versus an error-bearing `MPV_EVENT_END_FILE`. A live experiment must prove this rejects the required corrupt/encrypted/unsupported fixtures. If it admits a fixture that the visual player cannot decode, adoption must strengthen the probe to a null-output first-frame decode; it must not relax the no-session-on-rejection criterion.

## Corrected Finding 1

The process-wide RHI fact is confirmed but is **not a mainline shipping blocker**. The default boot already selects Player 1/OpenGL. The conflict exists only in the opt-in Player 2 boot, where Player 1 playback is unavailable globally.

## Ownership

Agent 0 owns Local Media Launch end-to-end. Agent 0 is the sole recipient for the probe evidence report, adoption decisions, divergence report, and runtime-verification results. No Player-lane handoff is required.

## Objective

Turn a validated local video resource into exactly one normal Theatre movie session backed only by Player 1/libmpv and Slice 2 device-local continuity.

The vertical must:

- admit decodable media before session creation;
- use Slice 2’s opaque `localId` as authoritative local identity;
- open playback immediately after admission;
- resume unfinished media and restart completed media at zero;
- defer cancellable fingerprinting until visual playback has started;
- preserve the shell session if the source later becomes unavailable;
- make no subtitle-provider request on open;
- make no `ProgressStore`, Continue, or account mutation;
- leave shipped downloaded-file playback behavior unchanged.

## Responsibility Map

| Responsibility | Owner |
|---|---|
| Path inspection, classification, synchronous descriptor preparation | Slice 1 router and video handler |
| Decode admission before session creation | `LibmpvAdmissionProbe` |
| Player-boot policy and launch sequencing | `LocalVideoLaunchAdapter` |
| Device-local identity, resume, completion, relocation, fingerprints | Slice 2 store through `LocalVideoContinuityBridge` |
| Shell session lifecycle | Existing `SessionStore` |
| Visual playback | Existing Player 1 `MpvItem` through a new external-local entrypoint |
| Fingerprint execution and stale-result rejection | `LocalVideoFingerprintCoordinator` |
| Downloaded-file semantics | Existing `playLocalFile()` unchanged |

## Launch Sequence

```text
user selects local video
→ Slice 1 inspect/classify/prepare descriptor
→ reject immediately if this process booted Player 2
→ bare-libmpv admission probe (cancellable + bounded)
→ re-check file metadata to detect source replacement during admission
→ find/create Slice 2 record by normalized locator
→ enrich descriptor target with opaque localId and external-local marker
→ SessionStore::openOrSwitch()
→ Player 1 external-local entrypoint calls MpvItem::loadFile()
→ apply unfinished resume after fileLoaded; completed state yields position 0
→ observe visual playbackStarted
→ begin cancellable fingerprint job
→ periodically persist Player 1 state only to Slice 2
```

No session exists before the admission step succeeds.

## Descriptor Contract

```text
appType      = "theatre"
contentKind  = "movie"
title        = display title
target.id    = Slice 2 opaque localId
target.path  = normalized current locator
target.localExternal = true
target.localMediaId  = opaque localId
target.position      = completed ? 0 : saved position
```

`target.id` intentionally outranks `target.path` in `SessionStore` deduplication. Relocation changes the locator without changing the taskbar/session identity.

## Slice 2 State Contract

```text
stateLinks["player1.positionSeconds"]  number
stateLinks["player1.durationSeconds"]  number
stateLinks["player1.completed"]        bool
stateLinks["player1.sourceUnavailable"] bool
```

Completion is authoritative. When `completed=true`, the next open starts at zero even if an older position remains present.

A fingerprint match is lookup evidence only. It never merges local records automatically.

## Durable Bundle Parts

All four code parts are canonical immutable handoffs in this repository. Sandbox copies are non-authoritative.


1. `...slice-3c-code-01-libmpv-admission-probe-r1.md`
   - typed admission results;
   - cancellable worker;
   - baseline bare-libmpv event loop;
   - required live-experiment branch.

2. `...slice-3c-code-02-launch-continuity-fingerprint-r1.md`
   - launch adapter;
   - Slice 2 record reconciliation;
   - descriptor enrichment;
   - continuity bridge;
   - post-playback fingerprint coordination.

3. `...slice-3c-code-03-player1-external-local-qml-r1.md`
   - dedicated external-local Player 1 entrypoint;
   - subtitle-provider suppression;
   - `ProgressStore` isolation;
   - resume/completion/source-unavailable behavior;
   - explicit preservation of shipped `playLocalFile()`.

4. `...slice-3c-code-04-tests-build-adoption-r1.md`
   - build registration;
   - fake-probe hermetic seams;
   - acceptance traceability;
   - named live-libmpv gates;
   - adoption order and stop conditions.

## Non-Goals

- No Player 2 playback or process restart UX.
- No change to downloaded-file `playLocalFile()` semantics.
- No subtitle provider search; Slice 8 owns it.
- No Continue row or global/account progress.
- No automatic identity merge from fingerprint equality.
- No Retry/Locate/Close UI; Slice 6 owns it.
- No comic/archive behavior.
- No unrelated PlayerPage refactor.

## Acceptance Traceability

| Issue criterion | Bundle evidence required |
|---|---|
| Valid video creates exactly one Player 1 session | fake-admission adapter test + live gate `LML-3C-MPV-01` |
| Player 2 never selected/instantiated | boot-policy unit test + object trace gate `LML-3C-MPV-09` |
| Unfinished resumes; completed starts at zero | continuity unit tests + gates `LML-3C-MPV-03/04` |
| Resume round-trips across restart | Slice 2 persistence harness integration test |
| Malformed/undecodable creates no session | fake-rejection test + live gate `LML-3C-MPV-05` |
| Source unavailable preserves session | session-spy test + live gate `LML-3C-MPV-08` |
| Hermetic where possible; live gates named | Code Part 04 |

## Stop Conditions

Return evidence instead of forcing adoption if:

- the adopted Slice 1 descriptor differs materially from the candidate contract;
- the bare-libmpv baseline probe admits a required rejection fixture and no bounded null-output decode can discriminate it;
- the Player lane cannot isolate external-local playback without changing downloaded-file behavior;
- Slice 2 adoption changes its local identity or state-link contract;
- baseline Player, SessionStore, ProgressStore, or continuity regressions make results ambiguous.

## Verification Notes

- **Confirmed from pinned source:** default boot selects Player 1/OpenGL; Player 2 is opt-in; SessionStore accepts `target.id` before `target.path`; existing `playLocalFile()` invokes subtitle discovery and global progress.
- **Approved product/architecture decisions:** A1 + B1 and a separate external-local mode/adapter.
- **Inferred:** the smallest safe integration is router preparation → admission → Slice 2 reconciliation → session open.
- **Requires execution evidence:** compilation, harnesses, timeout budget, libmpv error categorization, corrupt/encrypted fixture behavior, first-frame/fingerprint ordering, network/persistence isolation, source-unavailable behavior, and Player 1-only object tracing.

# AGENT PACKET

## TASK

Adopt Slice 3C under approved A1+B1 using this manifest and its four code parts.

## OBJECTIVE

Ship the first end-to-end local-media vertical: validated local video → pre-session libmpv admission → exactly one Player 1 session → Slice 2-only continuity.

## CONSTRAINTS

Preserve downloaded-file behavior. Never create a session before admission. Never instantiate Player 2 for local video. Never contact subtitle providers or global/account progress. Never hash before visual playback-start evidence.

## FIRST ACTION

In an isolated worktree at the pinned commit, build the smallest bare-libmpv probe harness and run the supported, corrupt, encrypted, and unsupported fixtures. Record whether `FILE_LOADED` versus `END_FILE(error)` discriminates every required case before reconstructing the adapter.

## VERIFICATION

Compile and run every hermetic harness, then run all named live gates. Report adopted paths/commits and every divergence from this candidate. Do not mark the slice verified until the original user-visible flow and regressions are runtime-validated.
