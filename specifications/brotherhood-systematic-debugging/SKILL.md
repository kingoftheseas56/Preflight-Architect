---
name: brotherhood-systematic-debugging
description: Use when a Brotherhood Claude agent is diagnosing a bug, regression, crash, hang, stutter, race, incorrect UI state, integration failure, or performance problem before proposing or executing a fix.
---

# Brotherhood Systematic Debugging

This is the diagnostic workflow for unexpected behavior in Brotherhood and app workspaces. It replaces stock systematic debugging when the running application can be observed through Lanista.

`unexpected behavior` → **this skill** → confirmed diagnosis or named architectural question → `brotherhood-writing-plans` → `brotherhood-executing-plans`

Lanista supplies observation, action, correlation, and evidence. It does not replace causal reasoning and it does not authorize automatic patching.

## When this applies

Use this skill for crashes, hangs, races, intermittent failures, performance regressions, incorrect navigation or state restoration, QML/runtime mismatches, bridge or integration failures, and repeated unsuccessful fixes.

Do not use it for unsettled product behavior, purely aesthetic disagreement, an already-confirmed narrow fix, or work that has already reached execution.

## Iron rule

**No fix recommendation before a singular, falsifiable root-cause hypothesis has survived a discriminating experiment.**

A suspicious line, green test, correlated log, screenshot, or symptom disappearance after a broad change is not a diagnosis.

## Prerequisites
1. Confirm repository, worktree, branch, commit, build artifact, environment, and the revision that exhibits the problem.
2. Tie expected behavior to an approved spec, established behavior, known-good revision, or explicit Hemanth decision.
3. Read both ledgers fresh:
   - `Colosseum/docs/colosseum-test-verification.md` governs Qt Test, Qt Quick Test, registered CTest gates, bespoke harnesses, orphaned tests, and probes.
   - `Colosseum/docs/colosseum-lanista-verification.md` governs Lanista actions, completion signals, state reads, events, probes, waits, and captures.
4. Probe the target pipe with `ping` when the ledger and running process may differ. Live `ping` confirms bridge capability only; it does not create deterministic test coverage.
5. Use a disposable isolated Lanista session for Drive or mutation. The daily app and live user data are read-only by default.
6. Preserve the failing baseline before any code or data mutation.
7. Read existing logs, crash output, recordings, screenshots, tests, recent changes, and prior failed attempts before requesting new evidence.

A test, harness, command, wait, probe, or capture absent from the relevant ledger must not be presented as existing.

## Status vocabulary

Diagnosis status:

- **Baseline not reproduced**
- **Investigating**
- **Leading hypothesis**
- **Root cause confirmed**
- **Architecture suspect**
- **Human-only judgment**
- **Unresolved**

Planning-readiness is reported separately:

- **Test seam status:** `available` / `migration required` / `test blocked` / `not applicable`
- **Bridge status:** `available` / `bridge blocked` / `not applicable`

A diagnosis can be Root cause confirmed while its corrective plan remains test blocked, bridge blocked, or both. Do not conflate them.

## Diagnostic workflow

### 1. Establish the phenomenon

Record the exact symptom, expected and actual behavior, shortest reliable trigger, frequency, affected and unaffected paths, environment, first known bad state, last known good state, recent relevant changes, and existing evidence.

If the issue cannot be reproduced, return an observation plan rather than a fix.

### 2. Preserve a clean failing baseline

Before mutation, record the scenario, revision, executable identity, pipe, data root, fixture, completion signal, semantic state, structured events, domain probes, relevant logs, visual grabs, and evidence manifest.

A screenshot proves the visible symptom. It does not prove the upstream cause.

### 3. Map trigger to symptom

For every boundary from initiating action to visible failure, record:

- input and output;
- authoritative state owner;
- object, thread, process, service, or persistence owner;
- identifiers and correlation keys;
- lifecycle and teardown order;
- completion and failure signals;
- error and fallback behavior;
- available observability.

The goal is to identify the first boundary where good state becomes bad state.

### 4. Compare working and broken paths

Find the nearest working analogue and compare call order, state source, identity, lifecycle timing, persistence, fallback behavior, platform, fixture, cache, session, semantic names, and visual result.

List differences before deciding which one matters.

### 5. Audit deterministic verification seams

Use the test ledger to build:

```markdown
| Behavior or contract | Layer | Existing test or harness | Status | Handoff consequence |
|---|---|---|---|---|
| <C++ contract> | Qt Test | <name or none> | available / migration required / test blocked / not applicable | <reuse, register, add seam> |
| <QML behavior> | Qt Quick Test | <name or none> | available / migration required / test blocked / not applicable | <reuse, register, add seam> |
| <assembled app> | Lanista | <scenario or none> | available / bridge blocked / not applicable | <runtime replay or prerequisite> |
```

Layer authority is strict:

- Qt Test proves C++ contracts, not QML or assembled-app behavior.
- Qt Quick Test proves QML component behavior, not the Windows shell or OS lifecycle.
- A bespoke harness is not part of the standard gate unless the test ledger says so.
- Every future regression test needs a **negative control**: a deliberate break at the diagnosed boundary that proves the test can fail.
- This skill identifies the candidate regression seam and negative control; it does not implement them.

Use `migration required` when a relevant bespoke harness must be registered or converted for a named evidence benefit. Use `test blocked` when no deterministic seam or signal exists.

### 6. Audit Lanista capability

For every required runtime fact, record the fresh ledger capability and whether it is Available, Planned, Unavailable, or Human-only.

Only Available capabilities may appear as executable actions. Planned or Unavailable capabilities produce **Bridge blocked** when they prevent diagnosis or future runtime replay.

Screenshots are supporting exhibits, never the sole pass condition. Aesthetic judgment remains Human-only.

### 7. Build ranked falsifiable hypotheses

Each hypothesis must be singular and mechanistic:

```markdown
### H1: <specific causal mechanism>

Mechanism:
Supporting evidence:
Conflicting evidence:
Prediction if true:
Prediction if false:
Falsification test:
Deterministic evidence or harness:
Test seam status:
Lanista actions:
Completion signal:
State / events / probes:
Visual evidence:
Evidence artifacts:
Bridge status:
Next branch if confirmed:
Next branch if rejected:
Confidence: low / medium / high
```

Rank by explanatory power, ability to explain unaffected paths, proximity to the first divergence, ease of discrimination, experiment cost, and observer-effect risk. Do not rank by patch convenience.

### 8. Design the minimum discriminating experiment

Prefer one read-only experiment that separates several hypotheses without changing production behavior.

Define:

- session and fixture;
- controlled variable;
- deterministic test or harness;
- test seam status;
- candidate negative control;
- exact Lanista actions;
- semantic completion signal;
- state, event, probe, log, and visual windows;
- expected result matrix written before execution;
- evidence artifacts;
- bridge status;
- repeat count for intermittent defects;
- observer-effect risk;
- stop condition.

Never use a fixed sleep as a completion signal. Missing runtime completion proof is Bridge blocked.

### 9. Execute, preserve, update

For each experiment:

1. confirm revision, artifact, session, and fixture;
2. run exactly the predeclared action;
3. wait on the named signal;
4. preserve green and red evidence;
5. compare actual results to the predeclared matrix;
6. reject, retain, or rerank hypotheses;
7. choose the next minimum experiment.

Instrumentation may record at a named boundary, but must not repair behavior. Its scope, retention, privacy, correlation, and observer effect must be explicit.

If instrumentation makes the symptom disappear, the first supported finding is **observer effect**, not confirmation of the original timing theory.

## Root-cause threshold

Use **Root cause confirmed** only when:

- the symptom is reproduced under known conditions;
- the first material divergence is identified;
- a specific causal mechanism predicts the observed result;
- affected and unaffected paths are explained;
- at least one credible alternative is discriminated;
- a controlled comparison or intervention changes the predicted boundary in the predicted way;
- evidence is traceable to preserved artifacts from the investigated revision.

Correlation, temporal order, a green test, or symptom disappearance alone is insufficient.

## Architecture escalation

Use **Architecture suspect** when repeated evidence shows competing owners, hidden shared state, no clean observation or test seam, repeated local repairs that break other paths, or a broad refactor as the only way to hide the symptom.

Return the ownership map, evidence, architectural question, and smallest decision needed. Route consequential design back to `brotherhood-brainstorming`.

## Diagnostic dossier

```markdown
# Brotherhood Diagnostic Dossier: <issue>

Diagnosis status:
Test seam status:
Bridge status:
Repository / branch / commit:
Artifact / session / fixture:

## Symptom
## Expected vs Actual
## Reproduction
## Known-Good / Known-Bad
## Baseline Evidence
## Trigger-to-Symptom Map
## Working Analogue
## Evidence Available
## Evidence Missing
## Deterministic Verification Matrix
## Lanista Capability Matrix
## Ranked Hypotheses
## Experiments and Results
## Root-Cause Assessment
## Candidate Regression Seam
## Planning Verification Handoff
## Architecture Warning Signs
## Stop Conditions
## Recommended Next Workflow
## First Action
## Evidence Manifest
```

Separate Confirmed, Inferred, Hypothesis, Reported, Decided, and Unknown.

## Planning Verification Handoff

Before routing to `brotherhood-writing-plans`, provide:

```markdown
Baseline:
Behavior to preserve:

Focused tests:
- Qt Test:
- Qt Quick Test:
- Existing harnesses:
- Negative control:

Test seam status: available / migration required / test blocked / not applicable

Lanista actions:
Completion signal:
State / events / probes:
Visual evidence:
Regression paths:
Evidence artifacts:
Bridge status: available / bridge blocked / not applicable
```

Rules:

- every named deterministic test or harness must be supported by the test ledger;
- every Lanista action, signal, probe, wait, or capture must be supported by the Lanista ledger and, when needed, live `ping`;
- every inapplicable focused-test line says why;
- missing deterministic coverage is Test blocked, not Bridge blocked;
- missing runtime proof is Bridge blocked, not Test blocked;
- diagnosis status and verification blockers remain independent.

Completion criterion: Writing Plans can populate its required slice fields without inventing a test, harness, negative control, signal, probe, regression path, or evidence location.

## Handoff rules

When root cause is confirmed:

1. do not implement the fix inside this skill;
2. preserve the dossier and evidence manifest;
3. state the causal mechanism, first divergence, affected responsibility, and behavior to preserve;
4. record rejected hypotheses;
5. complete the Planning Verification Handoff;
6. route multi-step, consequential, test-migration, or bridge-changing work to `brotherhood-writing-plans`;
7. route consequential product or architecture decisions to `brotherhood-brainstorming` first.

When unresolved, hand off the evidence gap and next experiment, not a guessed fix.

## Rationalizations to reject

- "The tests pass, so the app path is fine."
- "Lanista can replay it, so the Qt regression seam exists."
- "There is no Qt Quick Test, so the bridge is blocked."
- "The harness exists, so it is part of the standard gate."
- "The regression test passes, so no negative control is needed."
- "The screenshot proves the model is wrong."
- "A two-second sleep makes it reliable."
- "The daily app is already open."
- "The probe is planned, so I can describe its result."
- "The broad refactor fixed it."
- "Instrumentation removed the race, proving timing."
- "Three patches failed, so try another."

## Required reference

Read `references/systematic-debugging-pressure-tests.md` when modifying or reviewing this skill.
