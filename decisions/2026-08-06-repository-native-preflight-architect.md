# Decision: Make Preflight Architect Repository-Native

## Status
Approved and partially implemented.

## Context
Preflight Architect previously depended on Custom GPT instructions plus four uploaded knowledge files. That split the agent definition between platform configuration and GitHub.

## Decision
The repository is the canonical definition and durable home of Preflight Architect.

The portable definition consists of:
- `research/PREFLIGHT-ARCHITECT-OPERATING-CONTRACT.md`
- four modular skill files
- repository memory and publishing instructions
- `MEMORY.md`
- durable artifact folders

Custom GPT instructions, ordinary ChatGPT prompts, Codex, and other agents are adapters that load and follow the repository definition.

## Why Four Skill Files Alone Are Insufficient
The skill files contain detailed workflows, but not the full identity, startup protocol, non-execution boundary, routing rules, memory behavior, or agent-packet requirement.

## Consequences
- Preflight Architect can operate without the Custom GPT.
- Behavior becomes versioned and inspectable.
- Read-only connectors can reason but cannot persist changes.
- Write-capable connectors or coding agents are required for memory and artifact updates.
- Root `AGENTS.md` remains desirable for automatic discovery.

## Current Connector Constraint
This connector can update `MEMORY.md` and approved artifact folders, but cannot create arbitrary root files. Therefore the operating contract currently lives under `research/`.

## Rejected Approaches
- Custom GPT as the only canonical definition.
- Uploading only the four knowledge files.
- Duplicating all skills in one monolithic prompt.
- Blind last-write-wins memory updates.

## Revisit When
- arbitrary root writes become available;
- repository instruction conventions change;
- agents fail to follow modular pointers reliably;
- licensing strategy changes.
