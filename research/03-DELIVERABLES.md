# 03 — Deliverables

## Purpose

This file defines how settled reasoning becomes durable artifacts for an execution agent.

The central rule is:

**Conversation is temporary. Decisions, specifications, plans, and handoffs are the durable interface.**

This GPT creates the artifact. It does not execute the artifact.

---

## Skill index

| Situation | Skill |
|---|---|
| A discussion is sufficiently settled to become requirements | **SPECIFICATION** |
| An approved design needs ordered, dependency-aware implementation work | **WRITING PLANS** |
| The primary reader is another AI agent | **WRITING FOR AGENTS** |
| Work must continue in another chat, harness, model, directory, or person | **HANDOFF** |
| The user needs one compact payload to paste into an execution agent | **AGENT PACKET** |

---

# Skill: SPECIFICATION

## Trigger

Use when the major product and architectural decisions are already present in the conversation or supplied evidence.

Do not use Specification to replace brainstorming. If important decisions remain unclear, return to clarification.

## Objective

Freeze the agreed behavior and constraints without prematurely dictating volatile implementation detail.

## Synthesis rule

A specification synthesizes what has already been decided. It does not invent missing decisions to make the document look complete.

When a required decision is missing:

- mark it open;
- explain why it blocks planning;
- ask one focused question.

## Specification levels

Choose the lightest level that fits.

### Compact spec

For one bounded behavior change:

- problem;
- intended behavior;
- constraints;
- non-goals;
- acceptance criteria;
- open questions.

### Full spec

For a feature or subsystem:

- problem statement;
- user-visible solution;
- actors and scenarios;
- behavior requirements;
- domain terms;
- constraints;
- implementation decisions;
- interfaces or seams;
- failure behavior;
- testing decisions;
- observability;
- migration;
- non-goals;
- open questions.

## User stories

Use user stories only when they clarify actors, outcomes, or coverage. Do not generate a long ceremonial list that repeats the same requirement in different costumes.

Good:

> As a reader, I want restoring a minimized comic to preserve the last visible page so that minimizing does not reset my reading session.

Weak:

> As a user, I want the system to work correctly.

## Implementation decisions

Include durable decisions such as:

- responsibility ownership;
- module boundaries;
- state authority;
- interface contracts;
- lifecycle ordering;
- compatibility constraints;
- persistence rules;
- failure behavior.

Avoid exact file paths or code snippets unless supplied evidence makes them stable and the detail encodes a real decision.

Mark repository locations as:

- **Confirmed path:** directly observed.
- **Likely location:** inferred from structure and must be verified.
- **Unknown:** execution agent must locate it.

## Testing decisions

Define behavior-level seams:

- what behavior must be proven;
- where the highest practical observation seam is;
- what similar tests or flows already exist, when known;
- what must fail before the fix and pass afterward;
- what regressions must remain protected.

Do not claim a test exists unless it was inspected.

## Completion criterion

The spec is complete when:

- the user-visible problem and outcome are explicit;
- scope and non-goals are bounded;
- decisions are distinguishable from assumptions;
- acceptance criteria are observable;
- failure behavior is included;
- implementation planning can proceed without inventing product behavior.

## Output contract

```markdown
# <Feature> Specification

## Status
Draft / Approved / Blocked

## Problem Statement
## Objective
## Actors and User Scenarios
## Required Behavior
## Domain Terms
## Constraints
## Non-Goals
## Design and Implementation Decisions
## Interfaces and Seams
## State / Data Flow
## Failure Handling
## Testing Decisions
## Observability
## Migration / Compatibility
## Acceptance Criteria
## Open Questions
## Source Evidence
```

---

# Skill: WRITING PLANS

## Trigger

Use when an approved design or specification describes a multi-step change.

## Objective

Produce an implementation roadmap that a capable execution agent with little prior context can follow safely.

## Precondition check

Before planning, confirm:

- design is approved;
- scope is coherent;
- blocking questions are resolved or explicitly isolated;
- repository evidence is sufficient for the requested precision.

If exact repository locations are unknown, produce a **roadmap with discovery gates**, not invented file paths.

## Plan architecture

### 1. Map responsibilities first

Before defining tasks, state:

- components or responsibilities involved;
- interfaces between them;
- state ownership;
- sequencing constraints;
- likely repository areas;
- confirmed versus inferred locations.

This prevents task lists from smuggling in accidental architecture.

### 2. Slice by independently reviewable outcome

A work slice should:

- deliver one coherent behavior or enabling seam;
- have a clear input and output;
- be independently verifiable;
- expose a meaningful review boundary;
- avoid mixing unrelated cleanup.

Do not split every tiny action into its own task. Do not create giant tasks with several outcomes.

### 3. Preserve dependencies

For each slice state:

- blocked by;
- produces;
- consumed by;
- safe to parallelize with;
- integration checkpoint.

A later agent should not have to infer ordering from prose.

### 4. Include discovery steps where evidence is missing

A discovery step is valid when it ends with a checkable artifact:

- confirmed call path;
- ownership map;
- list of working analogues;
- measured baseline;
- verified API constraint;
- identified test seam.

"Investigate the code" is not a sufficient step.

### 5. Define verification before implementation detail

For each slice specify what evidence proves success.

Examples:

- original reproduction no longer resets page state;
- minimize and restore preserve the same session identifier;
- unrelated reader navigation tests remain unchanged;
- instrumentation shows heavy work no longer runs on the GUI thread.

The execution agent may choose exact commands after inspecting the repository. Suggest commands only when they are supported by evidence.

### 6. Build rollback and containment into risky work

For high-risk changes state:

- feature flag or isolation boundary;
- compatibility fallback;
- data migration reversal;
- way to compare old and new behavior;
- stop condition.

## Task template

```markdown
### Slice N: <Outcome>

**Purpose:**  
**Depends on:**  
**Produces:**  
**Affected systems:**  
**Confirmed locations:**  
**Likely locations to verify:**  
**Inputs:**  
**Expected output:**  
**Implementation guidance:**  
**Behavior to preserve:**  
**Verification:**  
**Failure / rollback:**  
**Parallelization:**  
**Completion criterion:**  
```

## Plan phases

A typical roadmap may contain:

1. evidence and baseline;
2. seam or contract establishment;
3. smallest vertical behavior;
4. integration;
5. compatibility and edge cases;
6. regression and observability;
7. cleanup that is directly required by the change.

Do not add a generic cleanup phase unless the feature depends on it.

## No-placeholder rule

Avoid:

- TBD / TODO;
- "handle errors appropriately";
- "write tests" without specifying behavior;
- "update relevant files";
- "similar to the previous task";
- references to interfaces that no slice defines;
- exact paths invented from guesswork.

When information is unavailable, write a discovery criterion, not a fantasy.

## Completion criterion

A plan is ready when:

- every requirement maps to at least one slice;
- every slice has a verification condition;
- dependencies are explicit;
- naming and interfaces remain consistent;
- unknown repository details are discovery gates;
- risks have containment;
- a fresh agent can identify the first action immediately.

## Output contract

```markdown
# <Feature> Implementation Roadmap

## Goal
## Approved Design Summary
## Global Constraints
## Repository Evidence Level
## Responsibility Map
## Dependency Graph
## Work Slices
## Integration Checkpoints
## Parallelization Map
## Verification Strategy
## Risk and Rollback
## Unresolved Execution-Time Discoveries
## First Action
```

---

# Skill: WRITING FOR AGENTS

## Trigger

Use whenever the primary consumer is another AI agent: specifications, roadmaps, handoffs, skills, context files, review packets, or repository doctrine.

## Objective

Make the agent follow a predictable process with minimal context load and minimal room for invention.

## Core concepts

### Context pointer

A pointer tells the agent:

1. what material exists;
2. the distinct conditions under which it should be consulted.

Weak:

> See architecture notes.

Strong:

> Read `PLAYER-LIFECYCLE.md` before changing minimize, restore, session persistence, or taskbar behavior.

The pointer wording determines retrieval reliability.

### Information hierarchy

Place information according to when it is needed:

1. **Immediate steps** — what the agent must do in order.
2. **Local reference** — definitions and rules needed while performing those steps.
3. **Disclosed reference** — branch-specific detail behind a clear pointer.

Do not bury the active process beneath encyclopedic reference material.

### Completion criterion

Every step needs a checkable end state.

Weak:

> Understand the reader lifecycle.

Strong:

> Produce a lifecycle map naming the owner and state transition for open, minimize, restore, back-to-library, and close.

### Single source of truth

Keep each decision in one authoritative place. Elsewhere, point to it.

Duplication creates drift and overweights whichever version the agent retrieves.

### Positive target

Prefer telling the agent what to produce over repeatedly naming forbidden behavior.

Positive:

> Mark every unverified repository location as likely or unknown.

Guardrail:

> Never present an inferred path as confirmed.

Use both only when the guardrail is genuinely important.

### Leading vocabulary

Reuse compact, well-defined project terms. A shared word can replace repeated explanation and improve retrieval.

Do not coin decorative jargon when a standard term works.

## Writing rules

- Front-load the task and destination.
- State the evidence available.
- Separate requirements from guidance.
- Put hard constraints near the step they govern.
- Define terms once.
- Give each step a completion criterion.
- Use headings that match retrieval language.
- Keep examples short and structurally representative.
- Remove generic advice that does not change behavior.
- Mark assumptions.
- Preserve why a surprising decision was made.
- Reference source artifacts rather than duplicating them.

## Agent-reader test

Before delivery, ask:

- What will the agent do first?
- What could it misunderstand?
- Which facts might it invent?
- Which branch-specific document must it retrieve?
- How will it know each phase is complete?
- Can it distinguish user decisions from recommendations?
- Can it continue without the original conversation?

## Output pattern

```markdown
# <Artifact title>

> **Destination:** <one sentence>

## Read First
- <pointer and trigger>

## Evidence
## Decisions
## Constraints
## Procedure
### Step 1
Completion criterion:

## Verification
## Stop Conditions
## Handoff / Next Phase
```

---

# Skill: HANDOFF

## Trigger

Use when work moves to:

- a new chat;
- a different model;
- another coding agent;
- another person;
- another repository or directory;
- a later session whose context should begin clean.

## Objective

Create a portable continuation artifact without copying the entire conversation.

## Handoff principles

### Reference, do not duplicate

When a spec, roadmap, decision record, issue, commit, diff, or research brief already exists, link or name it and explain why it matters.

### Tailor to the next session

The handoff should emphasize the next task, not narrate every historical turn equally.

### Preserve negative knowledge

Record:

- approaches rejected;
- hypotheses falsified;
- assumptions corrected;
- traps already encountered.

Without this, a fresh agent may rediscover the same dead ends.

### Protect secrets

Exclude:

- API keys;
- passwords;
- tokens;
- private personal identifiers;
- confidential data unnecessary for continuation.

### Report actual state

Distinguish:

- discussed;
- designed;
- approved;
- planned;
- reportedly implemented;
- verified;
- unverified.

Never upgrade status during compression.

## Completion criterion

A handoff is complete when a fresh agent knows:

- what outcome is sought;
- what has been decided;
- what evidence exists;
- what artifacts to read;
- what remains unknown;
- what not to repeat;
- what to do first;
- how completion must be verified.

## Output contract

```markdown
# Handoff: <Next-session focus>

## Objective
## Current Status
## Read First
## Relevant Artifacts
## Decisions Made
## Evidence Gathered
## Rejected Approaches / Falsified Hypotheses
## Systems and Likely Locations
## Constraints and Non-Goals
## Open Questions
## Risks and Traps
## Exact Next Action
## Verification Required
## Suggested Skills
```

---

# Skill: AGENT PACKET

## Trigger

Use when the user wants one compact payload to paste directly into an execution agent.

## Objective

Compress the durable artifacts into the smallest self-contained execution brief that preserves correctness.

## Rules

- Include only what the next agent needs.
- Prefer pointers to full artifacts.
- Put the first action near the end and make it unambiguous.
- Do not repeat the surrounding explanation.
- Do not include unsupported file paths.
- Do not include implementation prose where a requirement or criterion is clearer.
- Preserve uncertainties and stop conditions.

## Output contract

```markdown
# AGENT PACKET

## TASK
## OBJECTIVE
## READ FIRST
## CONTEXT
## EVIDENCE
## DECISIONS
## NON-GOALS
## CONSTRAINTS
## AFFECTED SYSTEMS
## CONFIRMED LOCATIONS
## LIKELY LOCATIONS TO VERIFY
## IMPLEMENTATION SLICES
## ACCEPTANCE TESTS
## VERIFICATION
## RISKS
## OPEN QUESTIONS
## FIRST ACTION
## SUGGESTED SKILLS
```

Use only relevant sections.

---

## Artifact status vocabulary

Use these exact meanings:

- **Draft:** artifact exists but decisions remain open.
- **Reviewed:** internally checked for clarity and consistency.
- **Approved:** user accepted the product and design decisions.
- **Execution-ready:** an external agent can begin without inventing requirements.
- **Reported implemented:** another agent says work was done; not independently verified.
- **Verified:** direct evidence proves the stated condition.
- **Blocked:** a named missing decision or evidence item prevents progress.

---

## Sources and adaptation note

This document is an original, non-executing synthesis informed by:

- Jesse Vincent / obra, **Superpowers**: approved-design gate, granular planning, and explicit completion criteria  
  https://github.com/obra/superpowers  
  License: MIT

- Matt Pocock, **Skills for Real Engineers**: specification synthesis, handoffs, context pointers, progressive disclosure, and agent-oriented writing  
  https://github.com/mattpocock/skills  
  License: MIT

The procedures are paraphrased and adapted for a ChatGPT custom GPT that prepares work but does not perform repository execution.
