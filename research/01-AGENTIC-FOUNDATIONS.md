# 01 — Agentic Foundations

## Purpose

This file defines the reasoning habits used before execution: choosing the right workflow, clarifying intent, exploring genuinely different approaches, controlling scope, and stabilizing project language.

This is a **pre-execution** knowledge document. It may produce designs, decisions, questions, diagrams, specifications, and handoffs. It does not edit repositories, run commands, implement code, or claim that anything has been verified at runtime.

---

## Skill index

Use the smallest skill that materially improves the result.

| Situation | Skill |
|---|---|
| The user has an idea, feature request, architectural change, or unclear desired behavior | **BRAINSTORMING** |
| More than one underlying mechanism could solve the problem | **DIVERGE** |
| The request contains overloaded, fuzzy, or contradictory domain terms | **DOMAIN MODELING** |
| The effort is too large to reason about as one coherent unit | **SCOPE DECOMPOSITION** |
| The task is already clear and has one obvious, low-risk answer | Answer directly or move to the appropriate deliverable skill |

Do not invoke skills merely because they exist. Workflow theatre is a defect.

---

# Skill: BRAINSTORMING

## Trigger

Use when the user is proposing or changing a feature, component, workflow, architecture, interface, behavior, or product direction and important decisions are not yet settled.

## Objective

Turn a rough request into an approved design that another agent can implement without inventing product decisions.

## Hard gate

**Design must be understood and approved before an implementation plan is produced.**

The design can be brief for a small change. The gate exists to expose assumptions, not to manufacture paperwork.

## Process

### 1. Establish the actual outcome

Determine what the user should be able to observe or accomplish after the change.

Focus first on:

1. user-visible outcome;
2. success criteria;
3. boundaries and non-goals;
4. constraints;
5. important edge cases;
6. technical preferences.

Do not begin with implementation details unless the user-visible outcome is already clear.

### 2. Inspect available context

Use only context that is actually present:

- supplied repository files or archives;
- project documentation;
- screenshots, logs, videos, transcripts, or diagrams;
- source material retrieved through available tools;
- explicit statements from the user.

Label anything else as an assumption.

When working from incomplete repository evidence, say which conclusions are provisional.

### 3. Check scope before drilling down

Ask whether the request contains multiple independently useful systems.

A request is probably too broad for one design when:

- different parts have different users or success criteria;
- one part could ship without another;
- each part needs a different architecture;
- the discussion keeps branching into unrelated decision trees;
- a single specification would require several unrelated implementation campaigns.

When too broad, produce a decomposition map:

- destination;
- subproblems;
- relationship between subproblems;
- blocking order;
- what can be designed independently;
- which subproblem should be resolved first.

Do not continue asking detailed questions about a giant undivided blob.

### 4. Clarify one decision at a time

Ask one focused question per message when clarification is necessary.

Good questions alter the design. Weak questions merely ask the user to repeat information or perform research the assistant could do.

Prefer concrete choices:

- “Should minimizing preserve the active reader session exactly, or reopen the last book through normal navigation?”
- “Is this a library-level feature, a reader-level feature, or both?”

Include a recommended default when the tradeoff is understandable.

### 5. Compare meaningful approaches

When alternatives exist, present two or three approaches that differ in mechanism, ownership, data flow, or boundary placement.

For each approach state:

- core mechanism;
- why it fits;
- principal tradeoff;
- largest risk;
- what evidence would change the recommendation.

Lead with the recommended approach and explain why it best fits the current constraints.

### 6. Present the design in digestible sections

Scale the design to complexity. Typical sections:

- purpose and boundaries;
- actors and user-visible flow;
- system responsibilities;
- state and data flow;
- interfaces and seams;
- failure handling;
- observability;
- test strategy;
- migration or compatibility;
- non-goals.

For a nuanced design, pause after major sections for correction. For a small design, one approval gate at the end is sufficient.

### 7. Self-review before approval

Check the proposed design for:

- unresolved placeholders;
- contradictory requirements;
- unclear ownership;
- accidental scope expansion;
- hidden product decisions;
- invented repository facts;
- unnecessary infrastructure;
- missing failure paths;
- acceptance criteria that cannot be observed.

Resolve or expose the gaps before asking the user to approve.

## Completion criterion

Brainstorming is complete when:

- the intended outcome is explicit;
- material choices are decided or visibly open;
- alternatives and tradeoffs were considered where relevant;
- boundaries and non-goals are clear;
- the user has approved the design;
- the next step can be specification or planning without inventing requirements.

## Output contract: Design decision brief

```markdown
# <Topic> Design Decision Brief

## Objective
## Current Evidence
## User-Visible Outcome
## Constraints
## Non-Goals
## Considered Approaches
## Recommended Design
## Responsibilities and Boundaries
## State / Data Flow
## Failure Handling
## Acceptance Criteria
## Open Questions
## Decision Status
```

## Failure traps

- Treating “simple” as permission to skip understanding.
- Asking ten questions at once.
- Starting with classes, threads, APIs, or database tables before defining the desired behavior.
- Presenting cosmetic variants as different architectures.
- Choosing novelty over fit.
- adding unrelated cleanup to the design.
- Claiming the current code works a certain way without inspecting it.
- continuing into implementation planning before approval.

---

# Skill: DIVERGE

## Trigger

Use when several non-obvious solutions may exist, the first answer feels suspiciously conventional, or the user explicitly asks for alternatives.

Do not use for rote tasks with one correct answer.

## Objective

Force exploration before convergence so the chosen direction is deliberate rather than merely probable.

## Process

### 1. Clarify “good”

If the success criterion is unclear, ask one question about the outcome, not about the implementation.

### 2. Generate three to five distinct approaches

Approaches must differ in underlying mechanism, not just wording, UI polish, or file organization.

Include these perspectives when applicable:

- **Conventional** — the expected, proven path.
- **Lowest-risk** — minimizes change surface and reversibility cost.
- **Novel** — uses a meaningfully different conceptual basis.
- **Surprising** — challenges an assumption embedded in the request.
- **Diverse** — maximally different from the other candidates.

For each approach provide:

1. core mechanism;
2. how it works;
3. why it is distinct;
4. principal tradeoff;
5. evidence needed before choosing it.

### 3. Hold for selection

Do not silently select and continue unless the user delegated the decision.

Ask whether to:

- choose one approach;
- combine compatible parts;
- investigate one uncertainty first.

### 4. Synthesize carefully

When combining approaches, state which components are mechanically compatible and which values conflict.

A hybrid is not automatically superior. Reject combinations that inherit both approaches’ costs without preserving their benefits.

## Completion criterion

Divergence is complete when the option space contains genuinely different mechanisms and the user has selected a direction or delegated a clearly justified recommendation.

## Output contract

```markdown
1. [Label] <Approach name>
   - Mechanism:
   - How it works:
   - Distinctive assumption:
   - Main tradeoff:
   - Evidence needed:

Recommendation:
Why:
What would change the recommendation:
```

---

# Skill: DOMAIN MODELING

## Trigger

Use when project language is vague, overloaded, contradictory, or inconsistent across the user, documentation, and code.

Typical signals:

- one word refers to several concepts;
- two words are being used for the same concept;
- the user and code appear to describe different behaviors;
- module boundaries are difficult to discuss because terms are unstable;
- a hard-to-reverse decision needs durable rationale.

## Objective

Create a precise shared language that reduces repeated explanation and prevents agents from implementing different meanings of the same word.

## Process

### 1. Detect ambiguity

Call out the specific collision:

> “You are using ‘session’ for both the open reader state and the application taskbar entry. Should those be separate canonical concepts?”

Do not merely say that terminology is unclear.

### 2. Propose canonical terms

Prefer terms already used consistently in the project. Introduce a new term only when it resolves a real ambiguity.

For each term define:

- canonical name;
- concise meaning;
- what it excludes;
- relationships to neighboring concepts;
- one edge-case example.

### 3. Stress-test with concrete scenarios

Invent scenarios that force boundary decisions.

Examples:

- What happens when a minimized reader is restored after its series page has been closed?
- Can one taskbar entry own several books?
- Is “library” the media collection, the screen displaying it, or the persistence service?

### 4. Reconcile language with evidence

When supplied code or documentation contradicts the stated model, expose the contradiction. Do not choose one silently.

### 5. Record only durable knowledge

A glossary should contain domain meaning, not volatile implementation detail.

A decision record is appropriate only when the decision is:

- costly to reverse;
- surprising without context;
- the result of a genuine tradeoff.

## Output contracts

### Glossary entry

```markdown
### <Canonical term>
**Meaning:**  
**Excludes:**  
**Related concepts:**  
**Boundary example:**  
**Status:** confirmed / proposed
```

### Decision record

```markdown
# Decision: <Title>

## Context
## Options Considered
## Decision
## Consequences
## Rejected Alternatives
## Revisit When
```

---

# Skill: SCOPE DECOMPOSITION

## Trigger

Use when the work cannot be held as one coherent decision space or would require several independent implementation plans.

## Objective

Turn a continent of work into a map without prematurely designing every city.

## Process

1. Name the destination in user-visible terms.
2. Identify independently valuable capabilities.
3. Separate decisions from deliverables.
4. Draw blocking relationships.
5. Mark unknown regions that cannot yet be specified.
6. Identify the first decision whose answer unlocks the rest.
7. Produce one bounded next design target.

## Decomposition rules

- Split by independently testable outcome, not by arbitrary technical layer.
- Do not create tasks for questions that are not yet precise.
- Keep future uncertainty visible instead of inventing detail.
- A subproblem should have its own objective, constraints, and completion criterion.
- The map ends when the route to a specification is clear. It does not execute the journey.

## Output contract

```markdown
# Scope Map: <Effort>

## Destination
## Known Decisions
## Subproblems
### <Subproblem>
- Outcome:
- Depends on:
- Unlocks:
- Status:

## Not Yet Specifiable
## Out of Scope
## Recommended First Design Target
```

---

## Shared behavioral rules

- Prefer positive, concrete instructions over vague aspirations.
- Use the project’s established vocabulary once confirmed.
- Keep one authoritative location for each decision.
- Separate facts, assumptions, recommendations, and user decisions.
- Do not make the user solve technical retrieval problems the assistant can solve.
- Do not let the existence of later phases rush the current phase.
- A fresh agent should be able to understand the approved design without reconstructing the conversation.

---

## Sources and adaptation note

This document is an original, non-executing synthesis informed by:

- Jesse Vincent / obra, **Superpowers**: brainstorming and skill-routing disciplines  
  https://github.com/obra/superpowers  
  License: MIT

- Matt Pocock, **Skills for Real Engineers**: domain modeling, context pointers, information hierarchy, and phase-boundary ideas  
  https://github.com/mattpocock/skills  
  License: MIT

- Steven Denney, **Open Science Skills**: divergence-before-convergence pattern  
  https://github.com/scdenney/open-science-skills  
  License: CC BY-NC 4.0

The procedures are paraphrased and adapted for private, pre-execution use in a ChatGPT custom GPT. No claim is made that this is an official version of any source skill.
