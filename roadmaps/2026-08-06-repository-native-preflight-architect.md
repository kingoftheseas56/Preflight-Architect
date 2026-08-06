# Repository-Native Preflight Architect Completion Roadmap

## Goal
Make `kingoftheseas56/Preflight-Architect` sufficient for repository-connected agents to recover Preflight Architect without a Custom GPT.

## Confirmed State
- `MEMORY.md` exists on `main`.
- Artifact folders are writable through the connector.
- `research/01-AGENTIC-FOUNDATIONS.md` is published.
- `research/PREFLIGHT-ARCHITECT-OPERATING-CONTRACT.md` is published.
- Arbitrary root-level writes are unavailable through this connector.

## Work Slices

### 1. Publish the complete modular skill set
Publish exact copies of:
- `02-INVESTIGATION.md`
- `03-DELIVERABLES.md`
- `04-QUALITY-GATES.md`

Verification: each file is readable from `main` and the operating-contract pointers resolve.

### 2. Publish the memory and publishing protocol
Add the repository-memory instructions under `research/`.

Verification: the protocol names optimistic concurrency, immutable handoffs, allowed artifact folders, and failure handling.

### 3. Reconcile `MEMORY.md`
Record the operating contract, skill paths, this decision, and this roadmap. Replace the old deployment-first next action.

Verification: memory is compact, current, and contains no secrets or transcripts.

### 4. Promote to root-level discovery
Using a write-capable GitHub agent:
- create root `AGENTS.md` from the operating contract;
- add a concise root `README.md`;
- decide whether the research-path operating contract remains canonical or becomes a mirror.

Verification: no conflicting instructions exist.

### 5. Resolve licensing
Preserve all attribution and explicitly decide repository-wide reuse terms before adding a blanket license.

## Risks
- pointer drift;
- duplicated instructions;
- false claims that read-only connectors provide persistence;
- incompatible licensing of adapted material;
- root and research contracts diverging.

## First Action
Use a write-capable GitHub agent to add the three remaining exact skill files and root `AGENTS.md`, then verify all pointers from a fresh repository-connected session.
