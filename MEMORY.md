# Preflight Architect Memory

## Current Objective

Use `kingoftheseas56/Preflight-Architect` as the canonical, repository-native definition and durable memory home for Preflight Architect, while preserving approved Colosseum Local Media Launch design and handing repository execution to Agent 0.

## Active Work Arcs

- Repository-native Preflight Architect definition is COMPLETE (all manifest files published; see Published Artifacts).
- Agent 0 owns Local Media Launch execution. The Slice 3C bare-libmpv admission policy has passed its standalone compiled-and-run gate; adapter reconstruction, adoption, and live-window verification remain with Agent 0.
- Preserve Slice 1 and corrected Slice 2 r2 for Colosseum adoption.
- Keep Slice 3B comics design-first until archive ownership and identity are resolved.
- Design the narrow atomic reference-bundle publishing bridge.

## Durable Decisions

### Repository-native Preflight Architect

- This repository is the canonical definition and durable home of Preflight Architect.
- Custom GPT instructions and other front ends are adapters, not the source of truth.
- The portable definition requires an operating contract in addition to the four modular skill files.
- `research/PREFLIGHT-ARCHITECT-OPERATING-CONTRACT.md` is the current authoritative startup contract; root `AGENTS.md` is the automatic-discovery entrypoint and defers to the contract on overlap.
- Read-only GitHub access supports reasoning but not durable persistence.
- Memory updates use optimistic concurrency.
- Handoffs are immutable; revisions receive new filenames.
- Do not store secrets or transcripts in memory.

### Intake and outcome discipline (field-ratified 2026-08-06, from issue #2)

- Inbound issues are a supported intake channel governed by the ISSUE INTAKE skill (`research/02-INVESTIGATION.md`): inbound claims are classified before any verdict (a requester's "confirmed" is Reported here; mutable-state claims carry Outdated risk), and a single-hypothesis-plus-fix-menu framing triggers an alternative-explanation pass against the raw symptom.
- Falsified or superseded published verdicts flow back into this file via the OUTCOME RECORD gate (`research/04-QUALITY-GATES.md`); originals stay immutable, corrections are recorded here and (for consequential artifacts) in `decisions/`.
- Issue responses publish under `research/` as `YYYY-MM-DD-issue-<N>-<topic>-response.md` with `artifact_class: issue-response`.

### Status vocabulary mapping (Brotherhood interop)

The Brotherhood execution side uses its own status vocabulary. Correspondence, so cross-system handoffs do not mistranslate:

- Preflight **Execution-ready** ≈ Brotherhood "plan approved, ready to execute".
- Preflight **Test-reported** = Brotherhood **Test-reported** (same meaning: green tests, no runtime replay).
- Preflight **Verified** is WEAKER than Brotherhood **Runtime-validated**: Verified proves the precise claim inspected; Runtime-validated additionally requires the original user-visible symptom replayed in the running app (or human-witnessed confirmation).
- Brotherhood **Bridge blocked** has no Preflight equivalent; treat it as "requires execution evidence" with the missing capability named.

### Colosseum execution boundary

- Preflight Architect may author immutable reference implementation bundles in this repository.
- Candidate code remains uncompiled, untested, unexecuted, unadopted, and runtime-unverified until an execution agent supplies evidence.
- Current repository evidence outranks candidate code.
- `SessionStore` remains the shell session-lifecycle authority.
- Local Media Launch Slice 1 owns shared inspection, classification, handler, routing, descriptor, and typed-error contracts.
- Slice 2 is a separate device-local continuity and identity store and must not reuse global `ProgressStore`.
- Slice 3C is approved under A1+B1: Player 1/mpv/OpenGL default boot, typed Player 2 failure, cancellable bare-libmpv admission before session creation, isolated external-local mode, and fingerprinting only after visual playback-start evidence.
- Slice 3C admission requires video enabled through `vo=null` and positive decoded-frame evidence (`dwidth > 0`). `FILE_LOADED` is diagnostic only. The default timeout is 3000 ms and must not be reduced from local-disk measurements without slow-source evidence.
- Admission proves openable plus one decoded frame, not whole-file integrity; corruption after the first valid frame is a later playback failure and must preserve the session.

## Repository and Branch State

- Repository: `kingoftheseas56/Preflight-Architect`
- Default branch: `main`
- Colosseum repository: `kingoftheseas56/Colosseum`
- Observed Colosseum branch: `master`
- Slice 3C pinned basis: `a40333dc1fc9823ceb9decd811deeadde6ac4c2d` (case verified via `git rev-parse` by the execution agent, 2026-08-06; the earlier uppercase-E transcription was a typo). Note: Colosseum master has since advanced (comic-reader resume fix `df003eb`).

## Published Artifacts

### Repository-native agent definition (complete)

- `research/01-AGENTIC-FOUNDATIONS.md` — commit `87f151c4dc773d12c69b7e22c65abde529ea0613`
- `research/PREFLIGHT-ARCHITECT-OPERATING-CONTRACT.md` — commit `5a2137cb3900d1bc86e72f1bec09767f2c631b49`
- `decisions/2026-08-06-repository-native-preflight-architect.md` — commit `5614cbac23e8f073cddf69ba6b55313c2c59472a`
- `roadmaps/2026-08-06-repository-native-preflight-architect.md` — commit `47950fdb8984e8868e8b034bad75a01be5bbfb01`
- `AGENTS.md`, `README.md`, `governance/repository-memory.md`, `research/02-INVESTIGATION.md`, `research/03-DELIVERABLES.md`, `research/04-QUALITY-GATES.md` — commit `463c8af7d142968b4f5fb11e1b98bf2e8a300d24` (published by a write-capable execution agent 2026-08-06, amended per the issue-#2 field review: ISSUE INTAKE skill, OUTCOME RECORD gate, issue-response destination, contract-authority note)

### Existing governing Colosseum artifacts

- `specifications/2026-08-06-reference-implementation-bundles.md`
- `specifications/2026-08-06-colosseum-local-media-launch-specification.md`
- `roadmaps/2026-08-06-colosseum-local-media-launch-implementation-roadmap.md`
- Relevant Slice 1, Slice 2 r2, and Slice 3C handoffs remain authoritative at their published repository paths.
- `handoffs/2026-08-06-colosseum-local-media-launch-slice-3c-code-01-libmpv-admission-probe-r3.md` — commit `24e00b6625a3cd4760db23143b69c40511a28fd6`; file SHA `af6c61e952f6807f01d3a0a52f5fdd195fc8846d` (test-reported fixture outcomes, error taxonomy, timeout caveat, and permanent regression guards).

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

### Outcome record: issue #2 (comic reader resume, 2026-08-06)

- **Falsified:** the advisory verdict in `research/2026-08-06-issue-2-comic-reader-resume-response.md` endorsed the briefing's inactive-long-strip `pageInView` mechanism as the leading explanation for the page-1 reset.
- **Confirmed actual cause (runtime trace + eyes-on):** a state-identity ordering defect — both comic open paths set `openChapterId` (mounting the reader) BEFORE the baked identity (`gcdId`/`bakedReleases`), so resume read the transient `gc:` progress key while saves went to `gcd:<id>`, and the first presentation overwrote the real record with page 1. Fixed in Colosseum `df003eb`; the briefing's "record at page 2" claim was itself stale (the record had already degraded).
- **Settling evidence class:** full-lifecycle QML runtime trace, then user verification.
- **Lessons institutionalized:** the ISSUE INTAKE skill (inbound-claim classification, alternative-explanation tripwire) and the OUTCOME RECORD gate — both published in commit `463c8af`. The response's honest status labels ("Hypothesis", "Not verified") worked as designed and prevented a wrong fix from being trusted; the intake gap is what cost a cycle. The recommended inactive-strip `active` gate remains a valid, separate latent-hardening follow-up (not the resume bug).

### Outcome record: issue #1 Slice 3C admission probe (2026-08-06)

- **Falsified:** Code Part 01 r1's baseline disabled both video and audio and treated `FILE_LOADED` as sufficient or potentially sufficient admission evidence. In the live harness this universally rejected valid video under P0, while `FILE_LOADED` alone admitted truncated and encrypted sources.
- **Confirmed actual policy (compiled-and-run fixture matrix):** keep video enabled through `vo=null`, disable audio/config/scripts, and admit only after observed `dwidth > 0`. Code Part 01 r2 reproduced the expected fixture discrimination, event ordering, cancellation, timeout, and stale-generation behavior against the installed libmpv.
- **Settling evidence class:** standalone MSVC/libmpv harness with deterministic fixtures, event traces, latency measurements, and regression guards, reported by Agent 0 on issue #1.
- **Operational correction:** error values `-16`, `-17`, and `-13` are recorded as observed diagnostics rather than universal product semantics; use a 3000 ms default because removable, network, sleeping-disk, and large-4K sources were not measured. Admission guarantees one decoded frame, not whole-file integrity.
- **Durable pointer:** `handoffs/2026-08-06-colosseum-local-media-launch-slice-3c-code-01-libmpv-admission-probe-r3.md`.

## Open Questions

- What repository-wide licensing terms correctly preserve the existing MIT and CC BY-NC adaptation notices?
- Does the final adopted harness include a distinct unsupported-codec fixture beyond unrecognized-container garbage?
- How should Slice 3B reconcile archive copy/move behavior with the "never copied or imported" requirement?
- Do removable, network-mounted, sleeping-disk, or large-4K sources require source-class timeout or retry behavior in the later recovery slice?

## Risks and Constraints

- Root and research-path operating statements must not diverge; `AGENTS.md` explicitly defers to the operating contract on overlap.
- Licensing must not misrepresent third-party adapted material.
- Current repository evidence outranks candidate code and remembered state.
- No status claim may exceed supplied compile, test, and runtime evidence.
- Custom GPT front-end instructions may predate the published `AGENTS.md`; on conflict, the repository definition wins and the front end should be updated.

## Exact Next Action

Agent 0 reconstructs and adopts the Slice 3C adapter in Colosseum, then reports the live-window gates for Player 1 session creation, external-local progress isolation, subtitle-provider silence, and source-unavailable session preservation. Preflight Architect should evaluate any returned divergence through RECEIVING CHALLENGE and record further outcomes without rewriting immutable handoffs.

## Last Updated

2026-08-06T23:11:00+05:30
