# Preflight Architect Memory

## Current Objective

Use `kingoftheseas56/Preflight-Architect` as the canonical, repository-native definition and durable memory home for Preflight Architect, while preserving approved Colosseum Local Media Launch design and handing repository execution to Agent 0.

## Active Work Arcs

- Complete the repository-native Preflight Architect definition.
- Agent 0 owns Local Media Launch execution, including the Slice 3C bare-libmpv probe, reconstruction, adoption, and runtime verification.
- Preserve Slice 1 and corrected Slice 2 r2 for Colosseum adoption.
- Keep Slice 3B comics design-first until archive ownership and identity are resolved.
- Design the narrow atomic reference-bundle publishing bridge.

## Durable Decisions

### Repository-native Preflight Architect

- This repository is the canonical definition and durable home of Preflight Architect.
- Custom GPT instructions and other front ends are adapters, not the source of truth.
- The portable definition requires an operating contract in addition to the four modular skill files.
- `research/PREFLIGHT-ARCHITECT-OPERATING-CONTRACT.md` is the current authoritative startup contract.
- Root `AGENTS.md` remains the preferred automatic-discovery entrypoint when arbitrary root writes are available.
- Read-only GitHub access supports reasoning but not durable persistence.
- Memory updates use optimistic concurrency.
- Handoffs are immutable; revisions receive new filenames.
- Do not store secrets or transcripts in memory.

### Colosseum execution boundary

- Preflight Architect may author immutable reference implementation bundles in this repository.
- Candidate code remains uncompiled, untested, unexecuted, unadopted, and runtime-unverified until an execution agent supplies evidence.
- Current repository evidence outranks candidate code.
- `SessionStore` remains the shell session-lifecycle authority.
- Local Media Launch Slice 1 owns shared inspection, classification, handler, routing, descriptor, and typed-error contracts.
- Slice 2 is a separate device-local continuity and identity store and must not reuse global `ProgressStore`.
- Slice 3C is approved under A1+B1: Player 1/mpv/OpenGL default boot, typed Player 2 failure, cancellable bare-libmpv admission before session creation, isolated external-local mode, and fingerprinting only after visual playback-start evidence.

## Repository and Branch State

- Repository: `kingoftheseas56/Preflight-Architect`
- Default branch: `main`
- Colosseum repository: `kingoftheseas56/Colosseum`
- Observed Colosseum branch: `master`
- Slice 3C pinned basis: `a40333dc1fc9823ceb9decd811deeaddE6ac4c2d` (case should be rechecked before execution)

## Published Artifacts

### Repository-native agent definition

- `research/01-AGENTIC-FOUNDATIONS.md`
  - commit: `87f151c4dc773d12c69b7e22c65abde529ea0613`
- `research/PREFLIGHT-ARCHITECT-OPERATING-CONTRACT.md`
  - commit: `5a2137cb3900d1bc86e72f1bec09767f2c631b49`
- `decisions/2026-08-06-repository-native-preflight-architect.md`
  - commit: `5614cbac23e8f073cddf69ba6b55313c2c59472a`
- `roadmaps/2026-08-06-repository-native-preflight-architect.md`
  - commit: `47950fdb8984e8868e8b034bad75a01be5bbfb01`

### Existing governing Colosseum artifacts

- `specifications/2026-08-06-reference-implementation-bundles.md`
- `specifications/2026-08-06-colosseum-local-media-launch-specification.md`
- `roadmaps/2026-08-06-colosseum-local-media-launch-implementation-roadmap.md`
- Relevant Slice 1, Slice 2 r2, and Slice 3C handoffs remain authoritative at their published repository paths.

## Rejected Approaches and Negative Knowledge

- Do not rely on Custom GPT conversation continuity as the only memory or behavior layer.
- The four skill files alone are insufficient without identity, startup, routing, non-execution, memory, and handoff rules.
- Do not duplicate the complete skill library into one monolithic prompt.
- Do not claim a read-only GitHub connector provides persistence.
- Do not use blind last-write-wins updates for `MEMORY.md`.
- Do not reuse global `ProgressStore` for local-media continuity.
- Do not treat paths or matching fingerprints as durable identity.
- Do not mutate, delete, copy, or import source media without an approved requirement.
- Do not instantiate Player 1 and Player 2 in the same process.
- Do not create a shell session before decode admission succeeds.
- Do not begin Slice 3B implementation before resolving copy/move and identity conflicts.
- Do not claim tests or runtime behavior without execution evidence.

## Open Questions

- Can the three remaining exact knowledge files be published through a connector path that accepts large Base64 payloads?
- When can root `AGENTS.md` and `README.md` be created?
- What repository-wide licensing terms correctly preserve the existing MIT and CC BY-NC adaptation notices?
- Does the Slice 3C baseline probe discriminate every required corrupt, encrypted, and unsupported-codec fixture?
- Is the null-output first-frame strengthening branch required?
- What timeout follows measured probe latency?
- How should Slice 3B reconcile archive copy/move behavior with the “never copied or imported” requirement?

## Risks and Constraints

- `research/02-INVESTIGATION.md`, `research/03-DELIVERABLES.md`, and `research/04-QUALITY-GATES.md` are not yet published; the connector rejected the first large-file write as invalid Base64.
- The current connector cannot create arbitrary root files.
- The operating contract currently points to three not-yet-present skill files; fresh agents must use the contract plus available artifacts until those files are added.
- Root and research-path operating contracts must not diverge after promotion.
- Licensing must not misrepresent third-party adapted material.
- Current repository evidence outranks candidate code and remembered state.
- No status claim may exceed supplied compile, test, and runtime evidence.

## Exact Next Action

Use a write-capable GitHub execution agent or a connector path that reliably accepts large files to:

1. add exact copies of `02-INVESTIGATION.md`, `03-DELIVERABLES.md`, and `04-QUALITY-GATES.md`;
2. add root `AGENTS.md` from `research/PREFLIGHT-ARCHITECT-OPERATING-CONTRACT.md`;
3. add a concise root `README.md`;
4. publish the repository-memory protocol;
5. verify every pointer from a fresh repository-connected session.

Agent 0 may independently continue the approved Colosseum Slice 3C probe work.

## Last Updated

2026-08-06T22:40:00+05:30
