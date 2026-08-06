# Preflight Architect Memory

## Current Objective
Use `kingoftheseas56/Preflight-Architect` as the durable home for memory and planning artifacts.

Active arc: plan a bounded Biblio Library tab using Brotherhood Writing Plans, with deterministic lower-layer tests and isolated Lanista runtime verification.

## Durable Decisions
- Biblio Library is a retained third tab: `Discover | Explore | Library`.
- Scope is a simple Theatre-like library wall, not a universal media-library redesign.
- One card represents one saved Biblio Collection work, keyed by the existing Collection entry ID / pairKey.
- The row is a read-only projection; no new persistence entity or identity registry.
- Exact matched book Progress owns Resume.
- Legacy Progress matching may use bounded ordered fallback; ambiguous matches must not Resume.
- Local ebook availability comes from Books or BookTorrents.
- Local audiobook availability decorates the same work card.
- Audio-only opens Details in v1; no standalone audiobook playback architecture.
- Any local form satisfies Downloaded, with distinct Ebook and Audio badges.
- Remove from Library removes Collection membership only, not Progress or files.
- Existing Continue Reading and Your Collection shelves remain.
- Register existing tests before selective migration.
- Qt Test and Qt Quick Test do not replace running-app proof.
- Fixed sleeps are not correctness signals.
- Live user data is not a disposable fixture.
- User-visible completion requires current isolated Lanista evidence or an explicit blocker.
- Handoffs are immutable.
- Memory updates use the current GitHub file SHA.
- Whenever Preflight Architect creates a guide, publish the canonical repository edition and update `MEMORY.md` in the same turn with path, commit SHA, status, and exact next action.

## Repository State
- Preflight: `kingoftheseas56/Preflight-Architect`, branch `main`.
- Colosseum: `kingoftheseas56/Colosseum`, observed branch `master`.

## Published Artifacts
- `handoffs/2026-08-06-lanista-missing-bridge-capabilities-guide.md`
  - commit `ed3d536f8873d90ae3f9125e4d46498b9f8ab99e`
- `handoffs/2026-08-06-brotherhood-lanista-workflow-skills-creation-guide.md`
  - commit `12e62c6ab1cc3aef7ab27e9befb2509be5950c6a`
- `roadmaps/2026-08-06-colosseum-qt-test-quick-test-integration-and-brotherhood-skills-guide.md`
  - commit `f6e69e10d9718ffc056945cbcb80353ed22e63d4`
  - file SHA `48836852cdb3a3041df7bb7d1fc04186490cea0e`
  - status: reviewed design guide; implementation and runtime verification pending
- `roadmaps/2026-08-06-biblio-library-tab-lanista-ready-design-guide.md`
  - commit `32834b424475f2ab6bca5b728a9150a0fffec55f`
  - file SHA `ed80358af4614def5620d851c5ffddf288ad2de7`
  - status: planning-ready design guide; implementation and runtime verification pending

## Open Questions
- Confirm exact installed Brotherhood skill root and discovery conventions.
- Confirm current Collection, Progress, Books, BookTorrents, Audiobooks, and routing APIs.
- Confirm whether BookTorrents needs the proposed small read-only completed-download list.
- Confirm deterministic isolated fixture seeding for Collection, Progress, and local availability.
- Confirm the exact semantic properties needed to distinguish Resume, Read, and Details routes in Lanista.

## Risks and Constraints
- Do not expand the Biblio Library into a universal abstraction, download registry, Progress migration, or standalone audio project.
- Do not claim planned capabilities are implemented.
- Do not use screenshots alone where semantic evidence is available.
- Do not attach tests to the daily app or live user state.
- Status must not exceed current evidence.

## Exact Next Action
Invoke `brotherhood-writing-plans` using `roadmaps/2026-08-06-biblio-library-tab-lanista-ready-design-guide.md` as the approved design input. First inspect current Collection, Progress, Books, BookTorrents, Audiobooks, routing, tests, fixtures, and the fresh Lanista ledger. Produce a bounded implementation plan with pure row derivation, the smallest missing local read seam, retained page wiring, semantic names/properties, focused tests, isolated Lanista scenarios, and evidence artifacts.

## Last Updated
2026-08-06T15:54:00+05:30
