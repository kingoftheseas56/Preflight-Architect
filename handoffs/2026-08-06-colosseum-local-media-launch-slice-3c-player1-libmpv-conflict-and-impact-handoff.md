# Local Media Launch Slice 3C — Player 1/libmpv Conflict and Impact Handoff

## Status

**Blocked by confirmed architecture conflicts.** This is the required stop-condition response. No compliant adapter is claimed implemented, compiled, tested, or runtime-validated.

## Objective

Launch a validated local video as a normal `SessionStore` movie session using only Player 1/libmpv, Slice 2 continuity, deferred cancellable fingerprinting, resume/restart semantics, source-unavailable preservation, and no subtitle-provider, `ProgressStore`, or account persistence.

## Evidence Basis

- Colosseum: `master@a40333dc1fc9823ceb9decd811deeadde6ac4c2d`
- Request: `kingoftheseas56/Preflight-Architect#1`
- Slice 1 router r2
- Corrected Slice 2 r2 bundle

## Blocking Findings

1. **Player backend selection is process-wide.** Player 1/mpvqt requires OpenGL; Player 2 uses D3D11. Qt graphics API selection occurs before `QGuiApplication`, so Player 1 cannot be selected per session inside a Player 2 boot.
2. **The requested no-session-on-undecodable contract lacks a prerequisite seam.** Slice 1 preparation is synchronous, while libmpv decode failure is observed only after the player page/session is already opened.
3. **Existing local playback is not isolated.** `playLocalFile()` triggers subtitle discovery and the Player page writes global `ProgressStore`; using it unchanged violates the request.

These findings match the issue stop conditions. A reference implementation would invent behavior unless two decisions are made.

## Required Decisions

### A. Player 2 boot behavior

- **A1 — Recommended:** Support external local video only in a Player 1/OpenGL boot. In Player 2 mode, return a typed `Player1Required` failure and create no session.
- **A2:** Restart the application into Player 1 mode with explicit handoff UX.
- **A3:** Make both backends coexist in one process. Rejected for this slice because it conflicts with the current RHI architecture.

### B. Decode admission

- **B1 — Recommended:** Add a cancellable non-visual libmpv admission probe before `SessionStore::openOrSwitch()`. Only successful admission creates a session.
- **B2:** Create the session first, then close or mark it failed on libmpv rejection. This violates the requested “no session created” acceptance criterion.

## Conditional Design After A1 + B1

```text
Slice 1 validate/classify
→ require Player 1 boot
→ cancellable libmpv admission probe
→ find/create Slice 2 localId by normalized locator
→ prepare movie descriptor:
     localExternalVideo=true
     localMediaId=<Slice 2 UUID>
     localLocator=<normalized locator>
→ SessionStore::openOrSwitch()
→ Player 1 load immediately
→ apply unfinished resume after fileLoaded
→ start cancellable fingerprint job after playback-start evidence
```

### Player 1 isolation contract

Add explicit external-local mode owned by `PlayerPage.qml` or a thin Player 1 adapter:

- never instantiate Player 2;
- never call subtitle discovery/providers;
- never write global `ProgressStore` or account persistence;
- read/write only Slice 2 state links;
- seek to stored position only when incomplete;
- on EOF persist `completed=true` and `position=0`;
- on missing source after session creation preserve the session and expose relocation;
- fingerprint after playback start, off the GUI thread, generation/cancellation guarded;
- fingerprint equality is lookup evidence only and never auto-merges identities.

## Acceptance Mapping

### Hermetic tests

1. Valid descriptor selects only Player 1 branch.
2. Player 2 boot under A1 returns `Player1Required` and creates no session.
3. External-local mode suppresses subtitle discovery and all global progress/account writes.
4. Incomplete state produces one deferred seek; completed state produces zero.
5. EOF writes completed and zero position.
6. Missing source preserves the session and returns unavailable/relocate state.
7. Cancelled or stale fingerprint completion cannot mutate Slice 2 state.
8. Fingerprint match does not merge records.

### Named live-libmpv gates

- `LML-3C-MPV-01`: supported video renders first frame in Player 1.
- `LML-3C-MPV-02`: playback starts before fingerprint work.
- `LML-3C-MPV-03`: unfinished resume lands within agreed tolerance.
- `LML-3C-MPV-04`: completed video starts at zero.
- `LML-3C-MPV-05`: representative corrupt/unsupported files map to approved categories before session creation.
- `LML-3C-MPV-06`: no subtitle-provider network request.
- `LML-3C-MPV-07`: no `ProgressStore` or account mutation.
- `LML-3C-MPV-08`: source removal preserves taskbar/session state.
- `LML-3C-MPV-09`: object tracing proves no Player 2 instance exists.

## Rejected Shortcuts

Do not reuse `playLocalFile()` unchanged, switch the QML source per session, treat extension as decode proof, create then silently remove a failed session, reuse `ProgressStore`, hash before playback, or auto-merge identities on fingerprint equality.

## Exact Next Action

Approve decisions A and B. Under A1+B1, the execution agent must inspect installed MpvQt headers for a cancellable non-visual probe seam and validate it with the smallest live experiment before writing the adapter.

## Verification Notes

- **Confirmed:** descriptor transport is sufficient; backend selection is process-wide; existing local playback contacts subtitle discovery and global progress.
- **Inferred:** explicit external-local Player 1 mode is the smallest safe isolation boundary.
- **Unknown:** whether installed MpvQt exposes a suitable non-visual probe API.
- **Requires execution evidence:** decode categories, first-frame order, resume tolerance, no-network/no-global-persistence proof, source-unavailable behavior, and Player 1-only instantiation.
