# Preflight Architect Memory

## Current Objective
Use `kingoftheseas56/Preflight-Architect` as the durable home for planning artifacts, memory, and immutable Reference Implementation Bundles for Colosseum.

## Active Work Arcs
- Adopt or adapt the published Local Media Launch Slice 1 shared-contracts candidate in an isolated Colosseum branch or worktree, compile it, run the isolated harness and relevant shell/session regressions, and report the adopted commit plus divergences before Slice 2.
- Design and implement the narrow atomic `writePreflightReferenceBundle` bridge capability, then migrate interim split bundles into the approved `reference-code/...` layout.
- Create the smallest implementation plan for the Theatre-equivalent Biblio Library tab, with focused Qt/Qt Quick tests and one compact isolated Lanista scenario.

## Durable Decisions
- Preflight Architect may author substantial, implementable Colosseum reference code only through the approved Reference Implementation Bundle workflow.
- Reference code is subordinate to the specification, acceptance criteria, and fresh repository evidence.
- Bundles belong in the Preflight Architect repository outside Colosseum.
- Approved bundles are immutable, revision-pinned, one independently reviewable roadmap slice each, and contain one canonical code representation plus `MANIFEST.md` and `bundle.json`.
- Every generated bundle is explicitly uncompiled, untested, unexecuted, unadopted, and unverified.
- Execution agents must inspect, adapt, compile, test, run required Lanista validation, and runtime-validate before adoption. Divergence is permitted and expected.
- Preflight must not publish generated reference code directly into Colosseum.
- The principal risk is anchoring generated mechanism above fresh evidence. Safeguards include exact base commits, immutable revisions, explicit assumptions, behavioral test review, and adversarial search for a smaller design.
- Local Media Launch targets BookReader 2, ComicReader 2, and Player 1/libmpv with device-local continuity.
- Local Media Launch Slice 0 is evidence-only. Slice 1 defines shared resource, handler, routing, and error contracts.
- A repository-grounded interim Slice 1 candidate exists, but it remains uncompiled, untested, unexecuted, unadopted, and unverified.
- Because the atomic bridge is absent, Slice 1 is temporarily an ordered set of immutable `handoffs/` artifacts. Its bundle index identifies canonical parts and superseded revisions.
- `SessionStore` remains shell session-lifecycle authority. Slice 1 handlers prepare descriptors but do not mutate it.
- Format classification policy is injected. Concrete Reader 2, ComicReader 2, and Player 1 integrations must validate actual backend support.
- Handoffs are immutable. Corrections use new revision artifacts.
- Memory updates use the current GitHub file SHA.
- Durable artifacts and memory pointers should be published in the same turn.

## Repository State
- Preflight repository: `kingoftheseas56/Preflight-Architect`
- Default branch: `main`
- Colosseum repository: `kingoftheseas56/Colosseum`
- Observed Colosseum branch: `master`
- Slice 1 candidate basis: `master@bb8eecb40eb8a50b7ded62f79035c555972c3fef`

## Published Artifacts
- `handoffs/2026-08-06-colosseum-local-media-launch-slice-1-reference-implementation-bundle-index.md`
  - commit: `3bdd46800ce02d91f302f860d41910fb4b16d800`
  - file SHA: `6956c7548db67366ba732bb9a9a56360e5379091`
  - status: interim split Slice 1 Reference Implementation Bundle index; repository-grounded and statically reviewed; compilation, CTest, regressions, Lanista, adoption, and runtime validation pending.
  - canonical parts:
    - `handoffs/2026-08-06-colosseum-local-media-launch-slice-1-code-01-types-classifier.md`
    - `handoffs/2026-08-06-colosseum-local-media-launch-slice-1-code-02-inspector-handler.md`
    - `handoffs/2026-08-06-colosseum-local-media-launch-slice-1-code-03-router-r2.md`
    - `handoffs/2026-08-06-colosseum-local-media-launch-slice-1-code-04-harness.md`
    - `handoffs/2026-08-06-colosseum-local-media-launch-slice-1-code-05-build-registration.md`
  - superseded: `handoffs/2026-08-06-colosseum-local-media-launch-slice-1-code-03-router.md`
- `research/2026-08-06-colosseum-local-media-launch-slice-0-implementation-prototype.md`
  - commit: `91d5494d0fbf8100dfa1522843d52f954b1e8a5b`
  - file SHA: `77d8ffbe82c511e1f12d7e397690ec648ca259cb`
  - status: repository-grounded Slice 0 prototype; static inspection complete; execution baselines pending.
- `roadmaps/2026-08-06-colosseum-local-media-launch-implementation-roadmap.md`
  - commit: `6c8ad2e828ce267cd323bc23d51226a10ae496f0`
  - file SHA: `2c6f0550ce003ead80a585f7a629c8930940cf06`
- `specifications/2026-08-06-colosseum-local-media-launch-specification.md`
  - commit: `597d7509c05cd73490eb68629eff1b418ec98932`
- `specifications/2026-08-06-reference-implementation-bundles.md`
  - commit: `354584f693dd7966a1cf5cd4112aec4db54ecbcd`
  - file SHA: `d1b83c3b743df37a8222ec3903481bbecdc7a999`
- `roadmaps/2026-08-06-biblio-library-theatre-equivalent-guide.md`
  - commit: `dd5f77db879f71b1cee27d5b1dcff7068250090a`
- `roadmaps/2026-08-06-colosseum-qt-test-quick-test-integration-and-brotherhood-skills-guide.md`
  - commit: `f6e69e10d9718ffc056945cbcb80353ed22e63d4`
- `specifications/brotherhood-systematic-debugging/SKILL.md`
  - commit: `2d491f118fda66540620239b55275699752ec0d1`

## Rejected Approaches and Negative Knowledge
- Do not embed large canonical implementations inside roadmap Markdown.
- Do not write unverified generated code directly into Colosseum or its `agents/` tree.
- Do not treat detailed candidate code as more authoritative than current repository evidence.
- Do not begin downstream slices from an unadopted candidate; use the execution agent's adopted commit and divergence report.
- Do not use fixed sleeps as correctness evidence or live user data as disposable fixtures.
- Do not invent repository paths, commands, APIs, tests, or Lanista capabilities.
- Do not route Local Media Launch video through Player 2; the approved target is Player 1/libmpv.

## Open Questions
- Exact action schema and server-side implementation for `writePreflightReferenceBundle`.
- File-count and size limits for atomic bundle publication.
- Migration of the interim Slice 1 split bundle into the approved atomic layout.
- Whether comic preparation must be asynchronous at the shared-contract seam.
- Concrete BookReader 2, ComicReader 2, and Player 1 supported-format policies.
- Local Media Launch platform intake, persistence, stable identity/fingerprinting, and subtitle add-on seams.

## Risks and Constraints
- Reference bundle publishing must become atomic, path-scoped to `reference-code/`, schema-validated, immutable, and optimistic-concurrency-safe.
- Current repository evidence outranks the Slice 1 candidate.
- Filesystem inspection is subject to TOCTOU; concrete handlers must reopen and validate resources.
- Extension classification is preliminary and must not replace backend probing.
- No status claim may exceed current evidence.
- User-visible completion requires current isolated Lanista evidence or an explicit blocker.

## Exact Next Action
An execution agent must re-read the current Colosseum branch, `SessionStore` declarations and definitions, `native/CMakeLists.txt`, `tests/CMakeLists.txt`, and local-media-related changes; reconstruct or adapt the Slice 1 candidate in an isolated branch or worktree; compile the production sources and `local_media_contract_harness`; run the isolated CTest and relevant taskbar/`SessionStore` regressions; and report the adopted commit, divergences, failures, and blockers. Do not begin Slice 2 or concrete reader/player integration until that report exists.

## Last Updated
2026-08-06T20:05:00+05:30
