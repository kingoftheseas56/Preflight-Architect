# Local Media Launch — Slice 1 Reference Implementation Bundle Index

## Code Status

**Implementable reference code — uncompiled, untested, unexecuted, unadopted, and unverified.**

- Target repository: `kingoftheseas56/Colosseum`
- Base branch: `master`
- Base commit: `bb8eecb40eb8a50b7ded62f79035c555972c3fef`
- Roadmap slice: `1 — shared resource, handler, routing, and error contracts`
- Packaging: interim split Markdown bundle
- Static review: completed
- Build, CTest, Qt Test, Qt Quick Test, Lanista, and runtime validation: not run

The approved specification, acceptance criteria, and current repository evidence outrank this candidate.

## Packaging Deviation

The approved atomic `reference-code/...` bridge does not yet exist. This bundle is therefore published as an ordered set of immutable Markdown artifacts under `handoffs/`.

This is not the final approved storage form. An execution agent must reconstruct the files in an isolated Colosseum branch or worktree. When the atomic bridge exists, migrate the adopted or revised candidate into one immutable `reference-code/...` bundle.

## Authority

1. `specifications/2026-08-06-colosseum-local-media-launch-specification.md`
   - commit: `597d7509c05cd73490eb68629eff1b418ec98932`
2. `roadmaps/2026-08-06-colosseum-local-media-launch-implementation-roadmap.md`
   - commit: `6c8ad2e828ce267cd323bc23d51226a10ae496f0`
3. `research/2026-08-06-colosseum-local-media-launch-slice-0-implementation-prototype.md`
   - commit: `91d5494d0fbf8100dfa1522843d52f954b1e8a5b`

## Canonical Ordered Source Set

1. `handoffs/2026-08-06-colosseum-local-media-launch-slice-1-code-01-types-classifier.md`
   - commit: `8877d5de6288549f1ec876ba09aeab276d866193`
  - file SHA: `02b1c29924a43d179d19e7ce00c18688d8872c6b`
  - provides: value types, typed results, error codes, extension classifier

2. `handoffs/2026-08-06-colosseum-local-media-launch-slice-1-code-02-inspector-handler.md`
   - commit: `726ed430bd1882b15cd7f5587bdeebedd6a09b3d`
  - file SHA: `53f9acf65aad16aa02d172b37350ee7d8ecabea0`
  - provides: local-file inspection and handler interface

3. `handoffs/2026-08-06-colosseum-local-media-launch-slice-1-code-03-router-r2.md`
   - commit: `1a73224a234362647982a53cf466b80955045820`
  - file SHA: `28ce1ea3eef8f2216c4eb40686b05ce87c112622`
  - provides: fail-closed routing and current `SessionStore` descriptor validation
   - supersedes: `handoffs/2026-08-06-colosseum-local-media-launch-slice-1-code-03-router.md`

4. `handoffs/2026-08-06-colosseum-local-media-launch-slice-1-code-04-harness.md`
   - commit: `1105c8a0359b15ca637370275f98ff914e066e94`
  - file SHA: `5307c273b846b79c4ddc0c35dbd79de432694f99`
  - provides: deterministic local-only contract harness

5. `handoffs/2026-08-06-colosseum-local-media-launch-slice-1-code-05-build-registration.md`
   - commit: `6dfd1ebb088b83212d1fd27af1ac18f39f84f809`
  - file SHA: `cf9d5d6ce944595c99b0b6f36be350eb6effd9e1`
  - provides: candidate native and CTest registration changes

## Machine-Readable Metadata

```json
{
  "schema": "preflight.reference-code.v1",
  "bundleType": "interim-split-candidate",
  "repository": "kingoftheseas56/Colosseum",
  "baseBranch": "master",
  "baseCommit": "bb8eecb40eb8a50b7ded62f79035c555972c3fef",
  "roadmapSlice": "1-shared-resource-handler-routing-error-contracts",
  "codeStatus": {
    "repositoryGrounded": true,
    "staticReviewComplete": true,
    "compiled": false,
    "testsRun": false,
    "lanistaRun": false,
    "adopted": false,
    "runtimeValidated": false
  },
  "canonicalParts": [
    "handoffs/2026-08-06-colosseum-local-media-launch-slice-1-code-01-types-classifier.md",
    "handoffs/2026-08-06-colosseum-local-media-launch-slice-1-code-02-inspector-handler.md",
    "handoffs/2026-08-06-colosseum-local-media-launch-slice-1-code-03-router-r2.md",
    "handoffs/2026-08-06-colosseum-local-media-launch-slice-1-code-04-harness.md",
    "handoffs/2026-08-06-colosseum-local-media-launch-slice-1-code-05-build-registration.md"
  ],
  "supersededParts": [
    "handoffs/2026-08-06-colosseum-local-media-launch-slice-1-code-03-router.md"
  ]
}
```

## Objective

Provide a pure Qt Core seam that:

1. accepts untrusted local-file intake;
2. validates and canonicalizes the resource;
3. classifies it using an injected extension policy;
4. selects exactly one injected handler;
5. asks the handler to prepare a current `SessionStore`-compatible descriptor;
6. validates the descriptor before shell mutation;
7. returns typed user-facing and diagnostic failures.

## Included

- `LocalMediaResource`
- `LocalMediaKind`
- typed error and result structures
- local-file inspector
- injected extension classifier
- handler interface
- fail-closed router
- provisional `SessionStore` descriptor validation
- isolated deterministic contract harness
- candidate CMake and CTest registration

## Non-Goals

No taskbar UI, picker, drag-and-drop, command-line intake, Open-with, persistence, identity database, recents, resume, relocation, content-change handling, media identification, subtitle acquisition, multi-file tray, privacy controls, packaging, or concrete BookReader 2, ComicReader 2, or Player 1 handler.

## Important Decisions

- `SessionStore` remains the only shell session-lifecycle authority.
- Handlers prepare descriptors but do not mutate `SessionStore`.
- Supported-format policy is injected; the candidate does not invent complete Reader 2 or Player 1 format support.
- Zero or multiple matching handlers fail deterministically.
- Canonical path is provisional location identity, not durable content identity.
- Stable fingerprints and continuity persistence remain later slices.
- Comic archive routing ends at an importer handler seam; copy-versus-move behavior remains unresolved.
- User-facing messages and diagnostics remain separate.

## Static Review Findings

- The original router artifact omitted a direct `<utility>` include for `std::as_const`; immutable revision `code-03-router-r2.md` corrects it.
- File inspection uses filesystem metadata and remains subject to time-of-check/time-of-use races. Concrete handlers must reopen and validate the resource.
- Extension classification is preliminary and must not substitute for backend probing.
- Synchronous handler preparation may be unsuitable for comic import. An execution agent may adapt the handler contract to an asynchronous result while preserving typed errors and fail-closed routing.
- The proposed `native/localmedia/` location and CMake insertion points are recommendations, not repository facts.

## Acceptance Checks

The execution agent must demonstrate:

- empty or invalid intake is rejected;
- non-local URLs are rejected;
- missing files, directories, and unreadable files are rejected;
- extension matching is normalized and case-insensitive;
- extensionless and unregistered formats are rejected;
- zero and multiple matching handlers fail closed;
- invalid descriptors are rejected before `SessionStore` mutation;
- a valid fake handler returns a descriptor with one provisional target identity;
- the harness is local-only, deterministic, and requires no GUI or network;
- relevant existing shell and `SessionStore` baselines remain passing.

## Required Verification

1. Re-read current Colosseum branch and target files.
2. Record drift from `bb8eecb40eb8a50b7ded62f79035c555972c3fef`.
3. Reconstruct the candidate in an isolated branch or worktree.
4. Confirm actual source-list and test-registration insertion points.
5. Compile the new production sources and harness.
6. Run the isolated contract harness through CTest.
7. Run relevant current taskbar and `SessionStore` regressions.
8. Record every adopted, adapted, rejected, superseded, or blocked unit.
9. Do not advance to Slice 2 or concrete Slice 3 integrations until the adopted contracts and commit are reported.

## Stop Conditions

Stop and return evidence when:

- the current repository already has a stronger shared result or routing abstraction;
- `SessionStore` descriptor requirements materially differ;
- classification requires backend probing before a safe media kind can be assigned;
- comic ingestion cannot fit a synchronous preparation seam;
- the candidate needs persistence, UI, platform intake, or direct reader/player mutation to be testable;
- repository drift invalidates the proposed build registration.

# AGENT PACKET

## TASK

Adopt or adapt Local Media Launch Slice 1 shared contracts.

## OBJECTIVE

Establish a testable pure-Qt intake, classification, handler-selection, descriptor-preparation, and typed-error seam without changing user-visible behavior.

## CONTEXT

Use the ordered source set above. The code is pinned to Colosseum `master@bb8eecb40eb8a50b7ded62f79035c555972c3fef` and has not been compiled or run.

## DECISIONS

`SessionStore` remains lifecycle authority. Classification policy and handlers are injected. Routing fails closed. Stable identity, persistence, UI, and concrete integrations are deferred.

## CONSTRAINTS

Current repository evidence outranks the candidate. Divergence is expected when justified and must be recorded.

## ACCEPTANCE TESTS

Build and run the isolated contract harness, then preserve the relevant current shell/session regression baseline.

## RISKS

Repository drift, synchronous comic preparation, extension overtrust, TOCTOU filesystem checks, and accidental duplication of an existing abstraction.

## FIRST ACTION
Re-read the current `SessionStore` declarations and definitions, `native/CMakeLists.txt`, `tests/CMakeLists.txt`, and all local-media-related changes at the actual adoption commit before applying any candidate file.
