# Reference Implementation Bundles

## Status
**Approved — 2026-08-06**

## Objective
Preflight Architect may author substantial, implementable Colosseum code without claiming execution or verification.

Every bundle must state:

> **Implementable reference code — uncompiled, untested, unexecuted, unadopted, and unverified.**

The approved specification, acceptance criteria, and current repository evidence outrank generated code.

## Canonical Workflow
```text
approved design
→ specification
→ execution-ready roadmap slice
→ fresh repository grounding
→ reference implementation bundle
→ static and adversarial review
→ execution-agent adoption
→ compilation and automated tests
→ Lanista and user-visible runtime validation
```

Do not generate substantial code during unresolved brainstorming. For debugging, require a falsifiable root-cause hypothesis unless the code is explicitly a diagnostic experiment.

## Non-Execution Boundary
Preflight may author complete code artifacts but must not claim to have modified Colosseum; created a branch, commit, PR, or worktree; compiled or executed the candidate; run Qt, QML, Lanista, build, benchmark, or runtime commands; fixed the behavior; or runtime-validated it.

Highest normal status:

> Repository-grounded reference implementation; static review complete; execution verification pending.

## Storage
Store immutable bundles in `kingoftheseas56/Preflight-Architect`, outside Colosseum:

```text
reference-code/
└── YYYY-MM-DD-<slice>-rN/
    ├── MANIFEST.md
    ├── bundle.json
    └── candidate.patch
```

For a standalone new file, replace `candidate.patch` with `files/<relative-target-structure>`.

Rules:
- one independently reviewable roadmap slice per bundle;
- one canonical code representation per bundle;
- patch for existing files, `files/` for complete new files;
- never overwrite; corrections use a new `-rN`;
- never publish generated reference code directly into Colosseum.

## Bundle Types
- **Candidate Patch:** default for modifying existing behavior.
- **Complete New File:** isolated harness, fixture, schema, utility, or scenario.
- **Feasibility Prototype:** experimental; never labelled implementation-ready.
- **Diagnostic Experiment:** gathers evidence; states expected observations and branches.

## Generation Gates

### 1. Approved Behavior
Require explicit user-visible behavior, approved material decisions, settled responsibility/state ownership, observable acceptance criteria, explicit non-goals, and one independently reviewable roadmap slice.

### 2. Fresh Repository Grounding
Inspect the current repository, branch, and exact commit; every existing target; direct callers/consumers; nearest working analogue; declarations/definitions; ownership/lifecycle boundaries; CMake/resources/registration; relevant Qt Test and Qt Quick Test coverage; QML harnesses/fixtures; applicable Lanista evidence; and local naming, error-handling, logging, async, and threading conventions.

The manifest lists exactly what was inspected. Uninspected paths, APIs, tests, commands, or Lanista capabilities are not confirmed. Insufficient evidence downgrades the output to an interface sketch, prototype, diagnostic experiment, or roadmap discovery gate.

### 3. Complete Slice
The candidate must:
- contain no pseudocode, ellipses, omitted branches, unresolved `TODO`, or placeholder logic;
- use inspected APIs or explicitly proposed interfaces;
- include required imports/includes, declarations/definitions, registration, resources, and build integration;
- include failure handling, cleanup, and cancellation where applicable;
- preserve unrelated behavior and avoid unrelated refactoring;
- identify ownership, lifecycle, thread-affinity, and async-ordering assumptions;
- include candidate tests where a suitable seam is known;
- remain small enough for a fresh agent to review and adapt.

“Implementable” means an agent can attempt adoption and compilation without inventing missing logic. It does not promise unchanged compilation success.

## Static Review
Check requirement-to-file/hunk traceability; declarations versus definitions; callers versus callees; type/method/signal/property consistency; state authority; ownership/lifecycle; failure, cleanup, cancellation, teardown, and re-entry; thread-affinity and async ordering; fixture isolation; build/resource registration; behavioral independence of tests; affected-surface coverage; and evidence-calibrated repository claims.

Repair static defects where possible and record remaining uncertainty.

## Adversarial Review
Ask whether the candidate overfits the roadmap mechanism, whether a smaller/reversible change works, whether analogues differ in ownership/lifecycle/platform/threading, whether unnecessary infrastructure was added, whether stale state or teardown order invalidates it, whether tests duplicate implementation, whether an unapproved boundary was crossed, and whether detail may anchor the execution agent away from stronger evidence.

Outcome: publish; publish with risks; revise; downgrade; return to investigation; or return to design/planning.

## `MANIFEST.md` Template
```markdown
# Reference Implementation: <Slice>

## Code Status
Repository-grounded reference implementation.
Uncompiled, untested, unexecuted, unadopted, and unverified.

## Bundle Type
Candidate Patch / Complete New File / Feasibility Prototype / Diagnostic Experiment

## Authority
The approved specification and acceptance criteria are authoritative.
This code is a candidate mechanism, not a product decision.

## Repository Basis
- Repository:
- Branch inspected:
- Base commit:
- Generated:
- Preflight artifact commit:

## Implements
- Specification:
- Roadmap:
- Roadmap slice:
- Requirements:
- Acceptance criteria:

## Target Paths
### Confirmed existing paths
### Proposed new paths
### Paths requiring execution-time verification

## Repository Evidence Inspected
- Production analogues:
- Interfaces and consumers:
- Build/resource registration:
- Existing tests:
- QML harnesses and fixtures:
- Lanista evidence:
- Documentation and constraints:

## Implementation Summary
## Important Design Choices
## Behavior Preserved
## Failure Handling
## Ownership and Lifecycle
## Threading and Asynchrony
## Assumptions
## Known Compile Risks
## Known Runtime Risks
## Candidate Tests Included
## Required Verification
## Agent Adoption Instructions
## Permitted Divergence
## Stop Conditions
```

## `bundle.json` Template
```json
{
  "schema": "preflight.reference-code.v1",
  "bundleType": "candidate-patch",
  "repository": "kingoftheseas56/Colosseum",
  "baseBranch": "master",
  "baseCommit": "<exact-sha>",
  "generatedAt": "<ISO-8601>",
  "specification": {"path": "<path>", "commit": "<sha>"},
  "roadmap": {"path": "<path>", "commit": "<sha>", "slice": "<id>"},
  "codeStatus": {
    "repositoryGrounded": true,
    "staticReviewComplete": true,
    "compiled": false,
    "testsRun": false,
    "lanistaRun": false,
    "adopted": false,
    "runtimeValidated": false
  },
  "targets": [],
  "requirements": [],
  "acceptanceCriteria": [],
  "evidenceInspected": [],
  "assumptions": [],
  "verificationRequired": [],
  "stopConditions": []
}
```

`baseCommit` is mandatory. Every target is confirmed existing, proposed new, or requires verification. Requirement IDs resolve to authoritative artifacts. Preflight leaves every execution-status field false. Unknowns are explicit. Schema changes require versioning.

## Traceability
```text
requirement
→ design decision
→ roadmap slice
→ target file or patch hunk
→ candidate test
→ required execution verification
```

Every code unit must serve a requirement, approved seam, failure-handling need, verification need, or risk control.

## Execution-Agent Adoption Contract
The execution agent must:
1. read the authoritative specification and criteria;
2. verify current Colosseum branch/commit and compare with `baseCommit`;
3. inspect targets and surrounding call paths;
4. identify drift before applying code;
5. apply or reconstruct it in an isolated branch/worktree;
6. adapt whenever current evidence contradicts the bundle.
7. record every material divergence and evidence;
8. compile affected targets;
9. run designated Qt Test and Qt Quick Test coverage;
10. run the required isolated Lanista scenario;
11. perform user-visible runtime validation where required;
12. report only the highest evidence-supported status.

Classify material candidate units as adopted unchanged, adopted with adaptation, rejected due to repository evidence, superseded by a smaller/safer implementation, or blocked pending evidence.

Divergence is expected when the repository changed, assumptions are false, compilation/tests contradict the draft, a simpler compliant design exists, or lifecycle/platform/accessibility/performance/safety/threading evidence requires revision.

## Verification Requirements
Name required evidence without inventing unsupported commands:
- candidate applies or is reconstructed cleanly;
- affected targets compile;
- candidate tests fail before where practical and pass after;
- relevant existing Qt and Qt Quick suites remain passing;
- QML has no new relevant warnings;
- lifecycle/cleanup is observed where risky;
- an isolated current Lanista scenario verifies semantic behavior;
- original user-visible and named regression flows are exercised;
- disposable fixtures avoid live user data;
- fixed sleeps are not correctness evidence.

Preflight records this plan, not its results.

## Stop Conditions
Stop and return evidence when repository state materially differs; a target/interface is missing; adoption needs an unapproved architectural decision; build/test surfaces differ; state/lifecycle/persistence/thread assumptions are contradicted; tests cannot distinguish behavior; Lanista lacks a required capability; verification would use live data unsafely; scope expands; or evidence invalidates the approved design.

## Atomic Publishing Capability
Add a narrow operation named conceptually `writePreflightReferenceBundle`.

Inputs: immutable directory name; complete `MANIFEST.md`; complete `bundle.json`; Base64 patch/code files; target branch; current branch-head SHA or concurrency token; Colosseum repository/branch/base commit; commit message; optional author metadata.

Behavior:
- write only beneath `reference-code/`;
- reject absolute paths, traversal, wrong repository, and overwrite;
- validate filenames, counts, per-file/total size, required files, JSON syntax, and schema;
- create all files atomically in one Git commit;
- use optimistic concurrency;
- return commit SHA and paths;
- leave no partial bundle after failure.

Existing name uses a new revision. Stale revision requires reread/reconcile. Invalid path/schema rejects before writing. Oversize bundles split by roadmap slice, never truncate.

## Doctrine Amendment
> Preflight Architect does not mutate the target repository or claim implementation success. When explicitly requested, and when an approved repository-grounded roadmap slice exists, it may author a complete Reference Implementation Bundle outside the target repository. The bundle must be implementable in form, pinned to inspected repository evidence, and explicitly marked uncompiled, untested, unexecuted, unadopted, and unverified.

> Reference code is subordinate to the specification, acceptance criteria, and current repository evidence. An execution agent must inspect, adapt, compile, test, and runtime-validate it before adoption.

> Substantial reference code is produced only through the Reference Implementation workflow. Small snippets remain acceptable elsewhere solely to remove ambiguity.

## Principal Risk
The principal risk is anchoring: a detailed candidate may outrank fresh evidence in an agent’s reasoning.

Safeguards: one slice per bundle; exact base commit; immutable revisions; explicit assumptions; authoritative specifications; fresh inspection; permitted divergence; no direct Colosseum writes; no unsupported status upgrades; behavioral test review; adversarial search for a smaller design.

## Acceptance Criteria
1. Ordinary snippets and formal bundles are distinct.
2. Bundles require approved behavior, a roadmap slice, and fresh grounding.
3. Every bundle pins an exact Colosseum base commit.
4. Every bundle has one code representation, manifest, and JSON metadata.
5. Candidate logic is complete for its bounded slice.
6. Static/adversarial review makes no execution claim.
7. Execution agents may adapt or reject candidates.
8. Required Qt, QML, Lanista, compile, and runtime evidence is named.
9. Bundles live outside Colosseum.
10. Publication is immutable, atomic, path-scoped, schema-valid, and concurrency-safe.
11. Memory records the artifact pointer, status, risk, and exact next action.
12. No status claim exceeds evidence.

## Non-Goals
This specification does not implement the bridge, create `reference-code/` through an unapproved path, generate the first bundle, select the pilot slice, alter Colosseum testing/Lanista, permit direct unverified Colosseum writes, make Preflight autonomous, or require unchanged adoption.

## Exact Next Action
Design and implement the narrow atomic `writePreflightReferenceBundle` bridge operation. Then select one small approved Colosseum roadmap slice as a pilot exercising revision pinning, atomic publication, traceability, candidate tests, divergence reporting, and Qt/Lanista verification handoff.
