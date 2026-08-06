---
name: brotherhood-systematic-debugging
description: Use when a Brotherhood Claude agent is diagnosing a bug, regression, crash, hang, stutter, race, incorrect UI state, integration failure, or performance problem before proposing or executing a fix.
---

# Brotherhood Systematic Debugging

This is the diagnostic workflow for unexpected behavior in Brotherhood and app workspaces. It
replaces stock systematic debugging when the running application can be observed through
Lansita.

The skill does not turn Lanista into an automatic patching surface. Lanista is the observation,
action, correlation, and evidence bridge. The debugging workflow still owns the diagnosis.

Normal delivery flow:

```text
brotherhood-brainstorming
→ brotherhood-writing-plans
→ brotherhood-executing-plans
```

Unexpected behavior flow:

```text
brotherhood-systematic-debugging
→ confirmed diagnosis or named architectural question
→ brotherhood-writing-plans
→ brotherhood-executing-plans
```

Do not run this skill as a mandatory stage for every task. Use it when the observed behavior is
not understood enough to plan a correction honestly.

## When this applies

Use this workflow for:

- crashes, hangs, deadlocks, races, and intermittent failures;
- performance regressions, stutter, excessive latency, or unexpected resource use;
- incorrect navigation, state restoration, persistence, or lifecycle behavior;
- UI behavior that differs from the approved specification;
- build, indegration, plugin, bridge, or platform failures;
- repeated unsuccessful fixes; or
- a recurrent bug where the symptom site and the causal owner are likely different.

Do not impose it on:

- a small defined fix with an already confirmed root cause;
- a product or aesthetic disagreement without a measurable defect;
- a read-only explanation of code where no failure is being investigated;
- an approved plan already containing the diagnosis; or
- a failure where the only remaining work is execution.

## Iron rule

**No fix recommendation before the root-cause investigation has produced a singular,
falsifiable hypothesis.**

The agent may propose instrumentation, experiments, and evidence-capture steps. It must not:

- presend an experiment has run when it has not;
- claim a patch fixed the bug when only the symptom disappeared;
- treat the symptom site as causal proof;
- add retries, delays, or broad refactors as diagnostic substitutes;
- treat a passing unit test as running-application proof;
- or use a Planned or Unavailable Lanista capability as if it exists.

## Prerequisites

Before any Lanista action:

1. **Confirm the repository, branch, and application baseline.**
2. **Read the current capability ledger** at
   `Colosseum/docs/colosseum-lanista-verification.md`.
3. **Probe the live pipe with `ping`** when the code, documentation, and running process may
   differ. The live probe is the authority on what the connected process can do now.
4. **Choose the safe application context.** Drive and mutation belong in a disposable, seeded,
   isolated session. The daily app and live user data are read-only by default.
5. **Preserve the failing baseline before any mutation.** Before evidence collected after a
   change is not before evidence.

If the ledger lists a required capability as Planned or Unavailable, do not invent the command,
probe, event, join, or wait. Classify the experiment as **Bridge blocked** or redesign it using
only genuinely available evidence.

## Status vocabulary

Use these statuses exactly:

- **Investigating** — baseline or mechanism is not yet narrowed enough.
- **Leading hypothesis** — one hypothesis best fits current evidence, but discriminating evidence is missing.
- **Bridge blocked** — the safest discriminating experiment depends on a Lanista capability that is not Available.
- **Root cause confirmed** — the causal mechanism is directly supported and credible alternatives have been discriminated.
- **Architecture suspect** — repeated evidence-based attempts expose competing owners, hidden shared state, or no clean observation seam.
- **Human-only judgment** — the remaining question is aesthetic, subjective, or product ownership and must be decided by Hemanth.

## The diagnostic loop

Run this loop until the issue reaches a terminal status.

### 1. Establish the phenomenon

Capture:

- exact symptom;
- expected behavior;
- actual behavior;
- reliable reproduction steps;
- frequency and timing;
- affected and unaffected paths;
- environment, versions, and branch;
- first known bad state;
- last known good state;
- recent relevant changes; and
- existing logs, traces, grabs, probes, screenshots, or recordings.

If the issue is not reproducible, the next artifact is an **observation plan**, not a fix.

**Completion criterion:** a fresh agent can state precisely what fails,, what should happen, and
how to observe it again.

### 2. Create or verify an isolated session

For any scenario that Drives, starts services, opens media, changes state, or mutates data:

- use the deterministic test profile;
- use seeded disposable data;
- preserve the session manifest;
- record the pipe, process, profile, seed,, and build identity; and
- do not reuse the daily app or Hemanth's live library as a disposable fixture.

Bounded read-only observation of the daily app is allowed only when the reported symptom is specifically
about live state that cannot be reproduced in isolation. Do not Drive or mutate it.

**Completion criterion:** the investigation has a reproducible, disposable context or an explicitly
bounded read-only exception.

### 3. Preserve the failing baseline

Before any code or data mutation, preserve:

- the exact scenario definition;
- the failing visual evidence;
- relevant stuctured state and probe output;
- the relevant event window and log window;
- timing or performance measurements when relevant; and
- the evidence artifact path or identity.

A screenshot proves the visible symptom. It does not prove the upstream cause.

**Completion criterion:** the before state can be reconstructed from preserved evidence without
relying on memory.

### 4. Map the system path

Draw the path from trigger to symptom.

For each boundary record:

- input;
- output;
- state owner;
- thread or process owner when relevant;
- lifecycle and persistence boundaries;
- error handling;
- available observability; and
- the nearest working analogue.

Example:

```text
user action
ₒ route request
ₒ controller transition
→ model selection
→ delegate creation
→ image source application
→ loader/cache/network
→ visible card render
```

The experiment should observe enough boundaries to identify the first point where good state
becomes bad state.

**Completion criterion:** each credible causal owner is included in the map, and the evidence gap at
each arrow is explicit.

### 5. Compare working and broken paths

Find the nearest working analogue. Compare before judging.

Record differences in at least:

- call and event order;
- identifiers and object identity;
- lifecycle timing;
- state source and owner;
- initialization and teardown;
- persistence timing;
- platform or environment conditions;
- error handling;
- IO, cache, network, or rendering boundaries; and
- the semantic tree and visual result.

**Completion criterion:** the dossier lists observed differences without pretending they are causal.

### 6. Audit Lanista capabilities

Build a capability matrix before naming the experiment:

```markdown|
| Needed evidence | Lanista capability | Ledger status | Live ping result | Use | Alternative |
|---|---|---|---|---|---|
| Route transition ordering | Structured event stream | Available | Present | Use | None |
| Selected image source | Image probe | Planned | Absent | Bridge blocked | Read-only logs if discriminating |
| Visible rendering | Evidence capture | Available | Present | Use | Human inspection for taste |
```

Allowed ledger statuses:

- Available;
- Planned;
- Unavailable; and
- Human-only.

Never upgrade Planned to Available because the code looks close, a future handoff names it, or a test
could be imagined.

**Completion criterion:** every Lanista action or observation in the experiment traces to an Available
capability confirmed by the ledger and, when needed, the live pipe.

### 7. Build ranked falsifiable hypotheses

Each hypothesis must be singular and mechanistic.

```markdown
### H1: <specific cause>

**Mechanism:**
**Supporting evidence:**
**Conflicting evidence:**
**Prediction if true:**
**Falsification test:**
**Evidence to collect:**
**Lanista capabilities required:**
**Next branch if confirmed:**
**Next branch if rejected:**

**Confidence:** low / medium / high
```

Rank by explanatory power and ease of discrimination, not by intuition or convenience.

**Completion criterion:** every credible hypothesis has a prediction, test, and next branch.

### 8. Design the minimum discriminating experiment

Prefer a read-only experiment that distinguishes several hypotheses at once without changing production
behavior.

For the experiment define:

- starting session state;
- exact action or trigger;
- correlation identifier;
- semantic wait condition;
- state, event, probe,, log, and visual capture windows;
- expected outcome for each hypothesis;
- the status transition for each possible result;
- repeat count or variance requirement when the symptom is intermittent; and
- stop conditions.

The experiment must say before execution:

```markdown
| Result | H1 | H2 | H3 | Next action |
|---|---|---|---|---|
| Route event precedes stale model id | Support | Conflict | Reject | Probe model attachment |
| Stale model id precedes route event | Conflict | Support | Reject | Probe route ownership |
| Neither diverges | Reject | Reject | Support | Map next upstream boundary |
```

Do not use a fixed sleep as a completion signal. Use an Available semantic wait or correlated event
window. If no Available capability can prove the transition, report Bridge blocked rather than padding
the experiment with delay.

**Completion criterion:** the experiment is smaller than a patch, uses only Available capabilities,
and distinguishes the leading hypothesis from at least one credible alternative.

### 9. Collect ACT + OBSERVE evidence

When the live pipe supports it, use one correlated transaction to:

1. record the pre-action state;
2. perform the semantic action;
3. wait for a real semantic completion condition;
4. capture the relevant event window;
5. read the relevant probes;
6. capture the visual result; and
7. write the evidence manifest.

Elevated mirror or restart actions are a prerequisite at the safe base directory, not a shortcut. Use
the ledger's safepreflight, safenavigate, file probe, and browser-owned fallback rules exactly.

Collect only evidence relevant to the hypothesis matrix. More telemetry is not automatically better
evidence.

**Completion criterion:** the manifest can be used to replay the action and trace each diagnostic
claim to a specific artifact.

### 10. Update the hypotheses

After each experiment:

- record the observed result;
- update supporting and conflicting evidence;
- rank hypotheses again;
- reject hypotheses that failed their prediction;
- add a new hypothesis only when the result exposes a new causal boundary; and
- define the next minimum discriminating experiment.

Do not keep a favorite hypothesis alive by rewriting it after every failed prediction.

## Root-cause threshold

Use **Root cause confirmed** only when all of the following are true:

- the symptom is reproduced in a controlled context;
- the first bad boundary is identified;
- a specific causal mechanism explains the symptom;
- the mechanism predicts a result that was observed;
- at least one credible alternative was discriminated;
- the finding survives comparison with the nearest working path; and
- the eridence can be traced to preserved artifacts.

Correlation, temporal order, symptom disappearance, or a green test may strengthen a hypothesis. None
of them alone confirms the root cause.

## Observer effect

If the symptom disappears after instrumentation is added, the first supported conclusion is:

**The observation changed the system.**

Do not upgrade this to the original timing hypothesis. Replace the instrumentation with a lower-impact
measurement, compare instrumented and uninstrumented rates, or use a bounded counter that does not
change the timing path.

## When architecture becomes the suspect

Stop adding local patches and use **Architecture suspect** when repeated evidence-based attempts show
one or more of these patterns:

- the same concept has several active owners;
- each local repair breaks another path;
- the causal mechanism cannot be observed at a clean seam;
- instrumentation requires widespread coupling changes;
- lifecycle, persistence, and visible state disagree about authority; or
- a broad refactor is the only way to make the failure disappear.

The next artifact is not a fourth patch proposal. It is:

- the competing ownership map;
- the architectural question;
- the evidence that exposed it; and
- the smallest design decision that must be resolved before a correction can be planned.

If the question is consequential product or architectural behavior, route back to
``brotherhood-brainstorming` before writing a plan.

## Aesthetic and human-only boundary

The agent may confirm:

- spec compliance;
- measured geometry;
- state, event, and probe output;
- visual overlap, missing content, or other mechanical defects; and
- differences between an approved spec and the running surface.

It must not claim authority over:

- whether a screen feels polished;
- whether spacing feels right;
- whether an animation feels coherent;
- whether a surface is beautiful; or
- any other taste judgment that belongs to Hemanth.

When mechanical requirements pass but the surface still feels wrong, report **Human-only judgment**,
attach the evidence, and ask for the product decision.

## Diagnostic dossier

Deliver the result in this form:

```markdown
# Brotherhood Diagnostic Dossier: <Issue>

## Status
Investigating / Leading hypothesis / Bridge blocked /
Root cause confirmed / Architecture suspect / Human-only judgment

## Symptom
## Expected vs Actual
## Reproduction
## Repository / Branch / Build
## Isolated Session
## Known-Good / Known-Bad
## System Path
## Working Analogue
## Baseline Evidence
## Evidence Available
## Evidence Missing
## Lanista Capability Matrix
## Ranked Hypotheses
## Minimum Discriminating Experiment
## Experiment Result Matrix
## Evidence Manifest
## Findings
## Root-Cause Threshold
## Architecture Warning Signs
## Stop Conditions
## Recommended Next Skill
## First Action for Next Agent
```

The dossier must separate:

- **Confirmed** — directly supported by inspected or collected evidence;
- **Inferred** — the best conclusion from confirmed evidence;
- **Hypothesis** — a plausible mechanism awaiting a discriminating test;
- **Decided** — a product or architectural choice; and
- **Unknown** — the evidence is insufficient.

## Stop conditions

Stop and return a precise status when:

- the failure cannot be reproduced — return an observation plan;
- the required bridge capability is not Available — return Bridge blocked;
- the instrumentation changes the behavior — return the observer-effect finding;
- credible hypotheses remain indistinguishable — return the missing evidence or capability;
- repeated local attempts expose competing owners — return Architecture suspect;
- the remaining disagreement is subjective — return Human-only judgment; or 
- the root-cause threshold is met — return Root cause confirmed.

## Handoff rules

When the diagnosis is confirmed:

1. do not implement the fix inside this skill;
2. preserve the diagnostic dossier and evidence manifest;
3. route to `brotherhood-writing-plans` for the smallest corrective plan; and
4. route to `brotherhood-brainstorming` first if the diagnosis exposes a consequential product or
   architectural decision.

When Bridge blocked:

- name the exact evidence gap;
- name the smallest safe Lanista prerequisite;
- state why existing evidence cannot discriminate the hypotheses; and
- do not silently turn the debugging task into a broad bridge infrastructure campaign.

## Pressure-test reference

Read `references/systematic-debugging-pressure-tests.md` when reviewing or modifying this skill.
The cases test patch-first pressure, test-green false confidence, screenshot-only diagnosis, missing
bridge capabilities, sleep temptation, daily-app risk, broad-change false proof, observer effects,
architectural patch loops, aesthetic boundaries, and the root-cause threshold.
