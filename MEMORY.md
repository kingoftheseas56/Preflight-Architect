# Preflight Architect Memory

## Current Objective

Use `kingoftheseas56/Preflight-Architect` as the durable home for Colosseum pre-execution artifacts and preserve the approved Local Media Launch design while Agent 0 performs repository execution.

## Active Work Arcs

- Agent 0 owns Local Media Launch end-to-end and will execute the Slice 3C bare-libmpv probe experiment, reconstruction, adoption, and runtime verification.
- Slice 1 and corrected Slice 2 r2 still require normal Colosseum adoption, compilation, harness execution, and regression validation.
- Design the narrow atomic reference-bundle publishing bridge.
- Keep Slice 3B comics design-first until archive ownership and identity are resolved against the “never copied or imported” requirement.
- Prepare the smallest implementation plan for the Theatre-equivalent Biblio Library tab.

## Durable Decisions

- Preflight Architect may author substantial Colosseum reference code only through immutable Reference Implementation Bundles in this repository.
- Reference candidates are subordinate to specifications, acceptance criteria, and current repository evidence.
- Candidate code is explicitly uncompiled, untested, unexecuted, unadopted, and runtime-unverified until an execution agent supplies evidence.
- Generated reference code must not be written directly into Colosseum by Preflight Architect.
- `SessionStore` remains the shell session-lifecycle authority.
- Local Media Launch Slice 1 owns shared inspection, classification, handler, routing, descriptor, and typed-error contracts.
- Slice 2 is a separate device-local continuity and identity store; it must never reuse global/online `ProgressStore`.
- Slice 2 identity uses an opaque UUID. Paths are locators; fingerprints are lookup evidence and never automatic merge authority.
- Corrected Slice 2 r2 case-folds normalized locator keys on Windows and separates intrinsic record validation from referential validation.
- Slice 3C design is approved under A1+B1:
  - Player 1/mpv/OpenGL is the default boot.
  - A Player 2/D3D11 boot returns typed `Player1Required` and creates no local-video session.
  - A cancellable, time-bounded bare-libmpv admission probe runs before `SessionStore::openOrSwitch()`.
  - Existing downloaded-file `playLocalFile()` behavior remains unchanged.
  - External-local playback uses an explicit isolated mode keyed by Slice 2’s opaque `localId`.
  - No subtitle-provider, global `ProgressStore`, Continue, or account persistence is reachable on that path.
  - Fingerprinting starts only after visual playback-start evidence.
- Agent 0 owns Local Media Launch end-to-end. Probe reports, adoption decisions, divergence reports, and runtime-verification results return to Agent 0; no Player-lane handoff is required.
- Slice 3C manifest r2 supersedes manifest r1 and the earlier stop-condition handoff as active adoption input.

## Repository and Branch State

- Preflight repository: `kingoftheseas56/Preflight-Architect`
- Default branch: `main`
- Colosseum repository: `kingoftheseas56/Colosseum`
- Observed Colosseum branch: `master`
- Slice 3C pinned basis: `a40333dc1fc9823ceb9decd811deeadde6ac4c2d`

## Published Artifacts

### Governing artifacts

- `specifications/2026-08-06-reference-implementation-bundles.md`
- `specifications/2026-08-06-colosseum-local-media-launch-specification.md`
- `roadmaps/2026-08-06-colosseum-local-media-launch-implementation-roadmap.md`

### Slice 1

- `handoffs/2026-08-06-colosseum-local-media-launch-slice-1-reference-implementation-bundle-index.md`
- Canonical parts include the types/classifier, inspector/handler, router r2, harness, and build registration.

### Slice 2

- `handoffs/2026-08-06-colosseum-local-media-launch-slice-2-corrected-r2-reference-implementation-bundle.md`
  - commit: `ba6446fa35d729b01bb514581e81d469e341e16e`
  - file SHA: `fbfe556b7949e4fe36982e3f03a8638449bdc47a`
  - status: approved for adoption; compilation, harness, Windows absent-path test, and regressions remain execution work.

### Slice 3C — canonical approved bundle

- `handoffs/2026-08-06-colosseum-local-media-launch-slice-3c-player1-libmpv-adapter-reference-implementation-bundle-r2.md`
  - commit: `82e06cb28f4ff879bd9352d87eafe492e39690d2`
  - file SHA: `4cab6dc7fcb545d5dcb776a32f8bcb85506e5727`
- `handoffs/2026-08-06-colosseum-local-media-launch-slice-3c-code-01-libmpv-admission-probe-r1.md`
  - commit: `d682b63c99329d0acc2645f3626703b1c6c61e34`
  - file SHA: `504a88d784da123f2de0a3486dd530aec0fea88c`
- `handoffs/2026-08-06-colosseum-local-media-launch-slice-3c-code-02-launch-continuity-fingerprint-r1.md`
  - commit: `a662e8b274388d9949befa25a9dce6242bf870f6`
  - file SHA: `f0ed83072cee9c58ce021d263495f26e17199662`
- `handoffs/2026-08-06-colosseum-local-media-launch-slice-3c-code-03-player1-external-local-qml-r1.md`
  - commit: `1217aae107110e6f0065ec75ef6f8446ed95ebb1`
  - file SHA: `35c40ecc70978a95bec350f90023ff54b7e3d5ec`
- `handoffs/2026-08-06-colosseum-local-media-launch-slice-3c-code-04-tests-build-adoption-r1.md`
  - commit: `83386d8d9d9238051318a74d032590c21a8c2663`
  - file SHA: `1acd05873b312f8caf22a5e97a2bac6657df4bad`

## Rejected Approaches and Negative Knowledge

- Do not reuse global `ProgressStore` for local-media continuity.
- Do not treat a path or matching fingerprint as durable identity.
- Do not mutate, delete, copy, or import source media without an approved requirement.
- Do not reuse shipped downloaded-file `playLocalFile()` semantics for external-local playback.
- Do not instantiate Player 1 and Player 2 in the same process.
- Do not restart the application into Player 1 for the opt-in Player 2 edge case.
- Do not create a shell session before decode admission succeeds.
- Do not claim `MPV_EVENT_FILE_LOADED` alone is decode proof unless the fixture experiment establishes sufficient discrimination.
- Do not begin Slice 3B comic reference code before the copy/move and identity conflict is resolved.
- Do not claim tests or runtime behavior without execution evidence.

## Open Questions

- Does the baseline `vid=no`, `vo=null` probe discriminate every required corrupt, encrypted, and unsupported-codec fixture?
- Is the null-output first-frame strengthening branch required?
- What timeout follows measured probe latency?
- What exact paths and APIs result after Agent 0 reconciles Slice 1, Slice 2 r2, and current Colosseum?
- How should Slice 3B reconcile `ingestLocalArchive` copy/move behavior with the “never copied or imported” requirement?
- What exact schema should the future atomic `writePreflightReferenceBundle` action expose?

## Risks and Constraints

- Current repository evidence outranks candidate code.
- Colosseum may advance between candidate generation and adoption.
- Filesystem inspection is subject to TOCTOU; concrete handlers must reopen and validate resources.
- A stale probe or fingerprint result must never mutate session or continuity state.
- The baseline admission policy must be strengthened if live fixtures expose false admission.
- No status claim may exceed supplied compile, test, and runtime evidence.

## Exact Next Action

Agent 0 will build the smallest bare-libmpv admission harness at Colosseum `a40333dc1fc9823ceb9decd811deeadde6ac4c2d` and run supported, corrupt, encrypted, unsupported-codec, missing, and removed-mid-probe fixtures. Agent 0 will report latency, discrimination, and whether the strengthening branch is required. Preflight Architect performs no further Slice 3C execution unless new evidence or a new design request is returned.

## Last Updated

2026-08-06T22:19:00+05:30
