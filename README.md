# Preflight Architect

Preflight Architect is a repository-native, pre-execution agentic architecture system. It prepares precise, evidence-calibrated work for coding and repository-mutation agents without claiming execution it did not perform.

The repository is the canonical definition. A Custom GPT, ordinary ChatGPT session, Codex, Claude Code, or another repository-connected agent is only a front end that loads and follows the repository instructions.

## Start here

Agents should read, in order:

1. `AGENTS.md`
2. `research/PREFLIGHT-ARCHITECT-OPERATING-CONTRACT.md`
3. `MEMORY.md`
4. only the skill files routed by the current task

## Skill library

- `research/01-AGENTIC-FOUNDATIONS.md` — clarification, brainstorming, divergence, domain modeling, and scope decomposition
- `research/02-INVESTIGATION.md` — research, systematic debugging, issue intake, adversarial review, and claim audits
- `research/03-DELIVERABLES.md` — specifications, implementation roadmaps, agent-oriented writing, handoffs, and agent packets
- `research/04-QUALITY-GATES.md` — verification before handoff, challenge handling, traceability, truthful status claims, and outcome records

## Durable state

- `MEMORY.md` contains compact cross-session context.
- `handoffs/` contains immutable continuation artifacts.
- `roadmaps/` contains ordered execution plans.
- `specifications/` contains durable requirements and designs.
- `decisions/` contains consequential architectural and product decisions, including outcome notes when execution evidence overturns a published verdict.
- `research/` contains evidence briefs, published issue responses, and the skill library.
- `governance/repository-memory.md` defines memory and publishing behavior.

## Non-execution boundary

Preflight Architect may inspect supplied or retrieved evidence and produce research briefs, architecture maps, specifications, roadmaps, test strategies, acceptance criteria, risk analyses, reviews, handoffs, and agent packets.

It does not claim repository mutation, commands, tests, builds, benchmarks, deployments, runtime validation, or fixes without direct evidence from an execution-capable tool.

## Bootstrap prompt for a repository-connected agent

> Use `kingoftheseas56/Preflight-Architect` as the governing repository. Read `AGENTS.md`, then `MEMORY.md`, then only the skill documents routed by the current request. Stay within the non-execution boundary, distinguish evidence from inference, and apply verification-before-handoff before substantial final artifacts.

## Persistence

Read-only GitHub access supports inspection and reasoning but cannot update durable state. Memory and artifact publishing require a write-capable connector, coding agent, or controlled repository action.

## Licensing and attribution

The skill documents contain their own source and adaptation notes. Do not add a blanket repository license until the compatibility and intended reuse terms for all adapted material have been reviewed.
