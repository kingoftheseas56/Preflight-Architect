# Preflight Architect Memory

## Current Objective

Establish `kingoftheseas56/Preflight-Architect` as the durable home for
Preflight Architect memory, handoffs, roadmaps, specifications, decisions,
and research.

The active product arc is to make Colosseum easier for agents to test through
Lanista, then make Brotherhood planning and execution require that runtime
verification.

## Active Work Arcs

### Lanista bridge capabilities

Expand Lanista behind one transport and one safety model rather than creating
several unrelated bridges.

The proposed capability areas are:

- deterministic isolated test sessions;
- semantic UI identities;
- typed application events;
- read-only domain probes;
- explainable screenshots and stronger visual-quality checks;
- correlated act-and-observe transactions;
- typed MCP tools with deadlines;
- bounded WebEngine and media observation.

The first vertical slice is Biblio per-card image diagnostics.

### Brotherhood workflow skills

Keep the workflow equivalent to the useful Superpowers core:

```text
Brotherhood Brainstorming
→ approved specification
→ Brotherhood Writing Plans
→ Brotherhood Executing Plans
```

Brotherhood Writing Plans must design both implementation and Lanista
verification for every relevant user-visible slice.

Brotherhood Executing Plans must perform the planned runtime verification,
preserve evidence, and report only the status supported by that evidence.

Lanista is a shared Colosseum verification reference, not a fourth workflow
skill.

## Durable Decisions

- `brotherhood-brainstorming` remains authoritative for design and the approved specification.
- Do not create a separate specification skill.
- Create `brotherhood-writing-plans`.
- Create `brotherhood-executing-plans`.
- Use one shared `colosseum-lanista-verification.md` reference from planning and execution.
- Missing Lanista capability is an explicit **Bridge blocked** condition.
- User-visible completion requires current running-app evidence or an explicit blocker.
- Unit tests do not substitute for runtime proof.
- Screenshot-only success is insufficient when semantic or domain evidence is available.
- The daily app and live user data are not disposable test fixtures.
- Genuine aesthetic judgment remains a human gate.
- New durable Preflight Architect artifacts belong in the Preflight-Architect repository, not Colosseum's legacy `chatgpt-handoffs` branch.
- `MEMORY.md` is compact durable context; detailed reasoning stays in linked artifacts.

## Repository and Branch State

- Colosseum repository: `kingoftheseas56/Colosseum`
- Colosseum default branch observed during this work: `master`
- Legacy handoff branch: `chatgpt-handoffs`
- Preflight repository: `kingoftheseas56/Preflight-Architect`
- Preflight default branch: `main` (confirmed 2026-08-06)
- Canonical handoffs published on `main`
- Memory revision: initial creation in this bootstrap publication

## Published Artifacts

### Canonical copies in Preflight-Architect

- `handoffs/2026-08-06-lanista-missing-bridge-capabilities-guide.md`
  - Publication commit: `ed3d536f8873d90ae3f9125e4d46498b9f8ab99e`
  - File SHA: `e4f5e7afe73976ead1fe5fa926e48cd0f43d9607`
- `handoffs/2026-08-06-brotherhood-lanista-workflow-skills-creation-guide.md`
  - Publication commit: `12e62c6ab1cc3aef7ab27e9befb2509be5950c6a`
  - File SHA: `27eeded2b29a4bc6febdef1f7924ce92dd177a3a`

### Legacy Colosseum sources

- `chatgpt/roadmaps/preflight-architect-lanista-missing-bridge-capabilities-guide.md`
  - Branch: `chatgpt-handoffs`
  - File SHA: `2c6148731b85da0ce2c71d53555c880099f6e8b4`
- `chatgpt/roadmaps/preflight-architect-brotherhood-lanista-workflow-skills-creation-guide.md`
  - Branch: `chatgpt-handoffs`
  - File SHA: `387d6be9950b8aafa8c3e0778d36729cacf31a74`

## Rejected Approaches and Negative Knowledge

- Do not rely on Custom GPT chat continuity as the only memory layer.
- Do not create a large family of overlapping Brotherhood skills.
- Do not create a separate Lanista workflow skill.
- Do not create several unrelated Lanista transports or security models.
- Do not treat bridge existence as proof agents will use it.
- Do not allow plans to say only “test manually,” “verify the UI,” or “take a screenshot.”
- Do not silently replace planned runtime verification with easier checks.
- Do not use arbitrary sleeps to conceal missing completion signals.
- Do not treat broad host-level image counters as per-card diagnosis.
- Do not store secrets, tokens, or full transcripts in `MEMORY.md`.

## Open Questions

- Confirm the actual skill root and discovery conventions in the target Brotherhood branch.
- Resolve or retire overlap between `brotherhood-brainstorming` and the older `brotherhood-superpowers` dispatcher.
- Decide whether the legacy Colosseum handoffs remain as historical pointers after canonical copies are committed.
- Freeze the exact location of `colosseum-lanista-verification.md`.
- Inspect the Biblio artwork path before freezing the first bridge design.

## Risks and Constraints

- Planned bridge capabilities must never be described as already implemented.
- Read-gated Lanista operations must remain non-mutating.
- Test sessions must be isolated from live user state.
- Memory updates must use the current GitHub file SHA to avoid overwriting newer work.
- Handoffs should remain immutable; publish revisions under new filenames.
- Runtime status must not exceed current evidence.

## Exact Next Action

Inspect the target Brotherhood branch's actual skill root and discovery
conventions, then create an approved design for:

1. `brotherhood-writing-plans`;
2. `brotherhood-executing-plans`; and
3. the shared `colosseum-lanista-verification.md` reference.

## Last Updated

2026-08-06T14:39:00+05:30
