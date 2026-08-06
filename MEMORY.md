# Preflight Architect Memory

## Current Objective

Use `kingoftheseas56/Preflight-Architect` as the durable home for planning artifacts, memory, and immutable Reference Implementation Bundles for Colosseum.

## Active Work Arcs

- Adopt or adapt the Local Media Launch Slice 1 shared-contracts candidate in an isolated Colosseum branch/worktree and report the adopted commit and divergences.
- Adopt or adapt the Slice 2 device-local continuity and identity-store candidate only after reconciling it with the adopted Slice 1 contracts and current Colosseum state.
- Design and implement the narrow atomic `writePreflightReferenceBundle` bridge, then migrate interim split bundles into `reference-code/...`.
- Create the smallest implementation plan for the Theatre-equivalent Biblio Library tab with focused Qt/Qt Quick tests and one isolated Lanista scenario.

## Durable Decisions

- Preflight Architect may author substantial, implementable Colosseum reference code only through the approved Reference Implementation Bundle workflow.
- Reference code is subordinate to the specification, acceptance criteria, and current repository evidence.
- Generated bundles live in the Preflight Architect repository outside Colosseum.
- Every generated candidate is explicitly uncompiled, untested, unexecuted, unadopted, and unverified.
- Execution agents must inspect, adapt, compile, test, run required Lanista validation, and runtime-validate before adoption. Divergence is permitted and expected.
- Preflight must not publish unverified generated code directly into Colosseum.
- Bundles are immutable and pinned to an exact Colosseum commit. Corrections use new revisions.
- Until the atomic bridge exists, bundles may be an ordered set of immutable `handoffs/` artifacts with a manifest or index.
- `SessionStore` remains the shell session-lifecycle authority. Shared launch handlers prepare descriptors and do not create a parallel session lifecycle.
- Local Media Launch Slice 0 is evidence-only.
- Slice 1 defines shared resource, inspection, classification, handler, routing, descriptor, and typed-error contracts.
- Slice 2 is an isolated device-local continuity and identity store. It must remain separate from online/Continue `ProgressStore` persistence.
- Slice 2 uses a stable opaque UUID. Paths are locators, fingerprints are evidence rather than automatic identity, and copy/changed-content relationships are explicit.
- Clearing recents preserves identity and continuity metadata. Full forget removes local metadata and caller-selected derived caches but never source media.
- The Slice 2 candidate has a standalone adapter boundary because Slice 1 is not adopted. It must reconcile with the actually adopted Slice 1 interface.
- Slice 2 r2 case-folds normalized locator keys on Windows and separates intrinsic record validation from referential validation.
- Slice 3C cannot honestly produce a compliant Player 1 adapter until boot behavior and pre-session libmpv admission are decided.
- Recommended Slice 3C decisions are A1: Player 1-only support with typed failure in Player 2 mode, and B1: cancellable non-visual libmpv admission before session creation.

## Repository State

- Preflight repository: `kingoftheseas56/Preflight-Architect`
- Default branch: `main`
- Colosseum repository: `kingoftheseas56/Colosseum`
- Observed Colosseum branch: `master`
- Slice 0 basis: `bb8eecb40eb8a50b7ded62f79035c555972c3fef`
- Slice 1 candidate basis: `bb8eecb40eb8a50b7ded62f79035c555972c3fef`
- Slice 2 candidate basis: `a40333dc1fc9823ceb9decd811deeadde6ac4c2d`

## Published Artifacts

### Governing Artifacts

- `specifications/2026-08-06-reference-implementation-bundles.md`
  - commit: `354584f693dd7966a1cf5cd4112aec4db54ecbcd`
  - file SHA: `d1b83c3b743df37a8222ec3903481bbecdc7a999`
- `specifications/2026-08-06-colosseum-local-media-launch-specification.md`
  - commit: `597d7509c05cd73490eb68629eff1b418ec98932`
- `roadmaps/2026-08-06-colosseum-local-media-launch-implementation-roadmap.md`
  - commit: `6c8ad2e828ce267cd323bc23d51226a10ae496f0`
  - file SHA: `2c6f0550ce003ead80a585f7a629c8930940cf06`
- `research/2026-08-06-colosseum-local-media-launch-slice-0-implementation-prototype.md`
  - commit: `91d5494d0fbf8100dfa1522843d52f954b1e8a5b`
  - file SHA: `77d8ffbe82c511e1f12d7e397690ec648ca259cb`

### Slice 1 Interim Bundle

- `handoffs/2026-08-06-colosseum-local-media-launch-slice-1-reference-implementation-bundle-index.md`
  - commit: `3bdd46800ce02d91f302f860d41910fb4b16d800`
  - file SHA: `6956c7548db67366ba732bb9a9a56360e5379091`
- Canonical parts identified by the index include:
  - `...slice-1-code-01-types-classifier.md`
  - `...slice-1-code-02-inspector-handler.md`
  - `...slice-1-code-03-router-r2.md`
  - `...slice-1-code-04-harness.md`
  - `...slice-1-code-05-build-registration.md`
- Status: repository-grounded interim split bundle; compilation, CTest, regressions, Lanista, adoption, and runtime validation pending.

### Slice 2 Interim Bundle

- `handoffs/2026-08-06-colosseum-local-media-launch-slice-2-manifest-r1.md`
  - commit: `b12c757b061982ee97f7dd5304ac9de55b2dd977`
  - file SHA: `274d4be97a51b91b6a06d966aa362f2d8104670e`
- `handoffs/2026-08-06-colosseum-local-media-launch-slice-2-code-01-types-store-header-r1.md`
  - commit: `aff73bc89233b10fece3579dfc588a7ffd0d47c8`
  - file SHA: `742e394a47c6f60b48130292712b25d35a394027`
- `handoffs/2026-08-06-colosseum-local-media-launch-slice-2-code-02-store-implementation-a-r1.md`
  - commit: `43d2d564619c2d3120a3a495496da04747d9d91c`
  - file SHA: `085af4576384fd68357514e1edbd3fb4e1b279ce`
- `handoffs/2026-08-06-colosseum-local-media-launch-slice-2-code-03-store-implementation-b-r1.md`
  - commit: `bb151fd340c35bf8337d85a07be1a8b617090bd7`
  - file SHA: `c2f5e988c04891969108bd6309dc634eb26df249`
- `handoffs/2026-08-06-colosseum-local-media-launch-slice-2-code-04-tests-build-r1.md`
  - commit: `104c55ccf4c78dfedd5ca5c8881091e5c8576957`
  - file SHA: `64ae966396b4c710fe88c84a0e5f85991d14aef9`
- Status: standalone, repository-grounded continuity-store candidate with versioned JSON, atomic `QSaveFile` persistence, hermetic harness, and build registration. Uncompiled, untested, unexecuted, unadopted, and unverified.


### Slice 2 Corrected r2 and Slice 3C Stop-Condition Handoff

- `handoffs/2026-08-06-colosseum-local-media-launch-slice-2-corrected-r2-reference-implementation-bundle.md`
  - commit: `ba6446fa35d729b01bb514581e81d469e341e16e`
  - file SHA: `fbfe556b7949e4fe36982e3f03a8638449bdc47a`
  - status: reviewed correction bundle; uncompiled, untested, unadopted, and runtime-unverified.
- `handoffs/2026-08-06-colosseum-local-media-launch-slice-3c-player1-libmpv-conflict-and-impact-handoff.md`
  - commit: `ed00c9fc654d05fc1ce0aa1ecf40044570fa78f7`
  - file SHA: `78fff9893b9da79a2cbcc5d5f83331d209cd78dd`
  - status: blocked stop-condition handoff; requires Player 2 boot-policy and decode-admission decisions.

## Rejected Approaches and Negative Knowledge

- Do not embed large canonical implementations inside roadmaps.
- Do not write unverified generated code directly into Colosseum or its `agents/` tree.
- Do not begin downstream integration from an unadopted upstream candidate without recording the dependency gap and providing an adapter boundary.
- Do not reuse `ProgressStore` as the local-media identity database.
- Do not treat a path as durable media identity.
- Do not automatically merge records because fingerprints match.
- Do not delete or mutate source media during create, relocate, clear-recents, or forget.
- Do not claim tests or runtime behavior without execution evidence.
- Do not route Local Media Launch video through Player 2; the approved target is Player 1/libmpv.

## Open Questions

- Exact adopted Slice 1 interfaces, paths, and divergences.
- Exact action schema and server-side implementation for `writePreflightReferenceBundle`.
- Whether retained platform access tokens may be stored as opaque strings on each supported platform.
- The actual Reader 2 state migration or aliasing strategy after relocation.
- Whether local-media persistence needs a worker-thread wrapper before integration.
- The deterministic write-failure test seam.
- Concrete BookReader 2 and ComicReader 2 integration boundaries for Slice 3.
- Slice 3C decision A: reject in Player 2 boot, restart into Player 1, or redesign for backend coexistence.
- Slice 3C decision B: add pre-session non-visual libmpv admission or relax the no-session-on-decode-failure criterion.
- Whether installed MpvQt exposes a cancellable non-visual admission/probe API.

## Risks and Constraints

- Current repository evidence outranks all candidate code.
- The split-bundle format is temporary and lacks atomic publication.
- Colosseum may advance between candidate generation and adoption.
- Filesystem inspection is subject to TOCTOU; concrete handlers must reopen and validate resources.
- Fingerprints are lookup evidence, not identity decisions.
- No status claim may exceed available evidence.
- User-visible completion requires current isolated Lanista evidence or an explicit blocker.

## Exact Next Action

Obtain product/architecture decisions for Slice 3C A and B. Recommended default: A1+B1. In parallel, the execution agent must adopt/reconcile Slice 1 and corrected Slice 2 r2 in an isolated branch, compile and run their harnesses/regressions, and report adopted commits and divergences. Do not implement Slice 3C until the decisions and MpvQt probe evidence exist.

## Last Updated

2026-08-06T21:28:00+05:30
