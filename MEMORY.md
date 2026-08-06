# Preflight Architect Memory

## Current Objective
Use `kingoftheseas56/Preflight-Architect` as the durable home for planning artifacts, memory, and immutable Reference Implementation Bundles for Colosseum.

## Active Work Arcs
- Create the smallest implementation plan for the Theatre-equivalent Biblio Library tab, with focused Qt/Qt Quick tests and one compact isolated Lanista scenario.
- Inspect Colosseum and create an implementation roadmap for the approved Local Media Launch specification.
- Design and implement the narrow atomic `writePreflightReferenceBundle` bridge capability, then select one small approved Colosseum roadmap slice as the pilot.

## Durable Decisions
- Preflight Architect may author substantial, implementable Colosseum reference code only through the approved Reference Implementation Bundle workflow.
- Reference code is subordinate to the specification, acceptance criteria, and fresh repository evidence.
- Bundles live in the Preflight Architect repository outside Colosseum.
- Bundles are immutable, revision-pinned, one independently reviewable roadmap slice each, and contain one canonical code representation plus `MANIFEST.md` and `bundle.json`.
- Every bundle is explicitly uncompiled, untested, unexecuted, unadopted, and unverified.
- Execution agents must inspect, adapt, compile, test, run required Lanista validation, and runtime-validate before adoption; divergence is permitted and expected.
- Preflight must not publish generated reference code directly into Colosseum.
- The principal risk is anchoring generated mechanism above fresh evidence; safeguards include exact base commits, immutable revisions, explicit assumptions, behavioral test review, and adversarial search for a smaller design.
- `brotherhood-systematic-debugging` remains the optional diagnostic workflow for unexpected behavior; it hands confirmed diagnoses to planning rather than patching directly.
- Biblio Library remains a retained third tab (`Discover | Explore | Library`) and a simple Theatre-like library wall, not a new library product.
- Local Media Launch remains an action/session capability targeting BookReader 2, ComicReader 2, and Player 1/libmpv with device-local continuity.
- Handoffs are immutable.
- Memory updates use the current GitHub file SHA.
- When Preflight creates a durable guide or specification, publish it and update memory in the same turn with path, commit SHA, status, and exact next action.

## Repository State
- Preflight repository: `kingoftheseas56/Preflight-Architect`
- Default branch: `main`
- Colosseum repository: `kingoftheseas56/Colosseum`
- Observed Colosseum branch: `master`

## Published Artifacts
- `specifications/2026-08-06-reference-implementation-bundles.md`
  - commit: `354584f693dd7966a1cf5cd4112aec4db54ecbcd`
  - file SHA: `d1b83c3b743df37a8222ec3903481bbecdc7a999`
  - status: Approved specification; bridge implementation and first pilot bundle pending.
- `specifications/2026-08-06-colosseum-local-media-launch-specification.md`
  - commit: `597d7509c05cd73490eb68629eff1b418ec98932`
  - status: approved product specification; repository design and runtime verification pending.
- `roadmaps/2026-08-06-biblio-library-theatre-equivalent-guide.md`
  - commit: `dd5f77db879f71b1cee27d5b1dcff7068250090a`
  - status: current planning-ready design guide; implementation and runtime verification pending.
- `roadmaps/2026-08-06-colosseum-qt-test-quick-test-integration-and-brotherhood-skills-guide.md`
  - commit: `f6e69e10d9718ffc056945cbcb80353ed22e63d4`
  - status: reviewed design guide; implementation and runtime verification pending.
- `specifications/brotherhood-systematic-debugging/SKILL.md`
  - commit: `2d491f118fda66540620239b55275699752ec0d1`
  - status: published skill.

## Rejected Approaches and Negative Knowledge
- Do not embed large canonical implementations inside roadmap Markdown.
- Do not write unverified generated code directly into Colosseum or its `agents/` tree.
- Do not treat detailed candidate code as more authoritative than current repository evidence.
- Do not generate reference code before behavior, architecture, acceptance criteria, and one roadmap slice are settled.
- Do not use fixed sleeps as correctness evidence or live user data as disposable fixtures.
- Do not invent repository paths, commands, APIs, tests, or Lanista capabilities.
- Do not expand Biblio Library into identity, download, audiobook, or migration architecture.
- Do not route Local Media Launch video through Player 2; approved target is Player 1/libmpv.

## Open Questions
- Exact action schema and server-side implementation for `writePreflightReferenceBundle`.
- File-count and size limits for atomic bundle publication.
- Pilot Colosseum roadmap slice after the bridge exists.
- Current Biblio Collection/Progress route shapes and minimum Lanista semantic properties.
- Local Media Launch integration seams: taskbar lifecycle, native picker/platform handles, reader/player contracts, persistence, identity/fingerprinting, and subtitle add-on behavior.

## Risks and Constraints
- Reference bundle publishing must be atomic, path-scoped to `reference-code/`, schema-validated, immutable, and optimistic-concurrency-safe.
- A stale memory or bundle revision must conflict rather than overwrite newer work.
- No status claim may exceed current evidence.
- User-visible completion requires current isolated Lanista evidence or an explicit blocker.

## Exact Next Action
Design an execution-ready roadmap for the narrow atomic `writePreflightReferenceBundle` bridge operation. After implementation by an execution agent, select one small approved Colosseum roadmap slice as the first Reference Implementation Bundle pilot.

## Last Updated
2026-08-06T17:56:00+05:30
