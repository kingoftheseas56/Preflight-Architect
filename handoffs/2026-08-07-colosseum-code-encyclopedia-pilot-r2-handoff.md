# Handoff — Colosseum Code Encyclopedia Pilot r2

## Objective

Adopt the r2 bounded-preamble grammar while preserving the r1 safety behavior
that Agent 0 executed successfully.

## Current Status

- r1 branch head `2080bf3`: inspected and executed by Agent 0.
- r1 merge: rejected because it falsely marked 100 explained files as silent.
- r1 drift/acceptance/integrity behavior: reported passing.
- r2 branch: `preflight/issue-3-code-encyclopedia-pilot-r2`.
- r2 grammar and reference candidate: authored, not run by Preflight Architect.

## Read First

1. `research/2026-08-07-issue-3-agent-0-review-response-r2.md`
2. `specifications/2026-08-07-colosseum-code-encyclopedia-pilot-generator-contract-r2.md`
3. `handoffs/2026-08-07-colosseum-code-encyclopedia-generator-reference-r2.py`
4. The r1 comics pilot bundle for unchanged guide, manifest, and cold-agent work.

## Decision

The first explanatory comment after a **bounded language preamble** is the
harvest target.

- C/C++: blanks, `#pragma once`, one matching include-guard pair, and includes.
- QML: blanks, imports, and QML pragmas.
- JavaScript: blanks and exact `.pragma library`.
- Any other token stops the search.
- Never scan for an arbitrary later comment.

## Non-Goals

- No general comment discovery.
- No semantic rewriting of source comments.
- No batching optimization in the blocking fix.
- No full-repository expansion beyond the approved pilot.
- No self-certification of the cold-agent trial.

## Implementation Slices

### 1. Port the grammar

Replace only r1's preamble/comment-selection logic with r2's bounded grammar.

**Completion:** P01–P12 and the unchanged r1 parser fixtures pass.

### 2. Protect safety behavior

Rerun the complete r1 state-transition suite.

**Completion:** idempotence, clean check, persistent drift, accepted-text
rendering, explicit acceptance, state-integrity rejection, and generated-index
overwrite/check behave exactly as Agent 0 reported.

### 3. Run the real manifest

Use the same 473-file pinned manifest unless adoption deliberately changes it.

**Completion:** normal preamble-comment files recover; exact counts are recorded;
`CbzArchive.h` remains undocumented unless source changes.

### 4. Repair stale source prose

Verify and repair `ComicDownloader.h`, `ComicSeries.qml`, and
`ComicSeriesPage.qml` where supported by current source behavior.

**Completion:** generation exposes drift before explicit acceptance.

### 5. Finish guide and navigation gates

Complete the manifest call/state/test edges, land the six-part guide and wake
pointer, then run a genuinely fresh comics task.

**Completion:** cold agent reaches the correct source, state authority, and test
seam without prior conversation context.

## Risks

- Overbroad include skipping could select a declaration-level comment. Contain
  it by accepting includes only in the initial contiguous preamble.
- Guard parsing could silently skip mismatched macros. Require exact names.
- r2 could accidentally alter accepted-state behavior. Treat any transition
  difference as a stop condition.
- Reported 319/473 documentation is an estimate, not an acceptance constant.

## First Action

Review the r2 contract, then run the new P01–P12 grammar fixtures before
executing the 473-file manifest.

# AGENT PACKET

## TASK

Adopt r2's bounded-preamble grammar into the Colosseum code-encyclopedia pilot.

## OBJECTIVE

Recover real file-level explanations hidden behind normal C++ and QML preambles
without weakening strict first-comment selection or r1's verified safety model.

## CONSTRAINTS

Do not merge r1. Do not scan for arbitrary comments. Preserve literal source
text, canonical blob hashes, persistent drift, explicit acceptance, and
machine-owned generated artifacts.

## ACCEPTANCE TESTS

P01–P12; all r1 parser and state transitions; real 473-file manifest; exact
undocumented count; stale-comment drift/acceptance; cold-agent task.

## FIRST ACTION

Run the grammar fixtures against the r2 candidate or equivalent port before the
real-tree generation.
