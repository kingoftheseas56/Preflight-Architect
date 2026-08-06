# Colosseum Code Encyclopedia Pilot — Generator Contract r2

## Status

**Execution-ready preflight revision; not executed by Preflight Architect.**

This document supersedes the grammar sections of:

- `specifications/2026-08-07-colosseum-code-encyclopedia-pilot-generator-contract-r1.md`

All r1 manifest, canonical Git blob, deterministic rendering, accepted-state,
drift, explicit acceptance, generated-file integrity, error, and stop-condition
requirements remain in force unless replaced below.

## Basis

- Approved design: `Colosseum@a7f2fa31b2b06087086395737cf64c7eeed34a6b`
- Inspected source: `Colosseum@a40333dc1fc9823ceb9decd811deeadde6ac4c2d`
- r1 execution report: Agent 0 issue comment `5209289610`

## Objective

Correct r1's false `UNDOCUMENTED` classifications without weakening the core
rule that the generator harvests only a file-level explanatory comment.

## Canonical Definition

A **top-of-file explanatory comment** is the first `//` or `/* ... */` comment
after:

1. optional UTF-8 BOM;
2. leading blank lines;
3. a bounded language-specific preamble;
4. blank lines interleaved with that preamble.

The parser must inspect the first token after this bounded preamble. If that
token is not a supported comment, the file is `UNDOCUMTED`. It must never
search later in the file.

## Language-Specific Preambles

### C and C++ suffixes

For `.c`, `.cc`, `.cpp`, `.cxx`, `.h`, `.hh`, `.hpp`, and `.hxx`, skip a
contiguous run composed only of:

- exact `#pragma once`, allowing ordinary preprocessor whitespace;
- at most one matching include guard:
  - `#ifndef NAME`:&
  - followed, ignoring blanks, by `#define NAME`;
- `#include ...` directives;
- blank lines.

Rules:

- A mismatched or incomplete guard is a hard preamble stop, not a skipped token.
- Do not skip `#if`, `#ifdef`, arbitrary `#define`, arbitrary pragmas,
  declarations, namespaces, macros, or code.
- A comment ends preamble processing and is tested immediately.
- Includes after a comment are irrelevant because the comment has already been
  selected.
- Do not infer whether the selected comment is semantically good; emit it
  literally.

### QML suffix

For `.qml`, skip a contiguous run composed only of:

- lines beginning with `import `;
- lines beginning with `pragma `;
- blank lines.

Do not skip object declarations, property declarations, JavaScript blocks, or
later comments.

### JavaScript suffix

For `.js`, retain the exact r1 exception:

```text
.pragma library
```

plus following blank lines. No other JavaScript directive is skipped.

## Comment Block Rules

After the allowed preamble:

- `//` starts a line-comment block;
- consecutive `//` lines are collected;
- blank lines between those comment lines are preserved;
- trailing blank lines after the final `//` line are excluded;
- `/*` starts a block comment and is collected through the first `*/`;
- an unterminated block is fatal;
- markers, indentation, text, and internal line endings are preserved;
- no paraphrase, correction, reflow, or semantic synthesis occurs.

## Drift and Acceptance

The r1 safety model is unchanged:

- normal generation/check harvests current source but does not advance an
  existing accepted hash/comment when the blob differs;
- drifted entries display the accepted comment and a `DRIFTED` warning;
- `--check` fails while drift remains;
- explicit `--accept PATH` or reviewed bulk acceptance advances current
  hash/comment;
- new manifest entries are initially accepted;
- state integrity is machine-owned and hand edits are fatal.

Agent 0 reported these behaviors passing end to end on r1. r2 must retain the
same state-transition results while changing only preamble recognition and the
undocumented diagnostic wording.

## Diagnostic Wording

For files with no comment after the bounded preamble, render:

```text
No explanatory comment was harvested after the allowed file preamble.
```

Do not claim that no comment exists anywhere in the file.

## Required Fixture Additions

| Fixture | Shape | Expected |
|---|---|---|
| P01 | `#pragma once` + blanks + line comment | documented |
| P02 | matching include guard + comment | documented |
| P03 | mismatched guard + later comment | undocumented |
| P04 | includes + comment | documented |
| P05 | `#pragma once` + includes + comment | documented |
| P06 | QML imports + comment | documented |
| P07 | QML imports + QML pragma + comment | documented |
| P08 | QML import + object declaration + later comment | undocumented |
| P09 | arbitrary C++ pragma/define + later comment | undocumented |
| P10 | comment before includes | first comment harvested |
| P11 | allowed preamble only, no comment | undocumented |
| P12 | allowed preamble + unterminated block | fatal |

The complete r1 fixture and state-transition matrices remain required.

## Real-Tree Acceptance

Against the pinned or consciously rebased Colosseum manifest:

1. Every manifest path produces path, accepted/current blob, status, source link,
   and accepted comment or precise undocumented message.
2. `SessionStore.h` and equivalent normal preamble-comment files are documented.
3. `CbzArchive.h` remains undocumented unless its source gains a valid
   explanatory comment after the allowed preamble.
4. The exact undocumented count is reported, not predetermined.
5. A second generation produces no diff.
6. All r1 safety transitions still pass.
7. Source-comment repairs are exposed as drift and explicitly accepted.
8. The cold-agent navigation trial remains an independent final gate.

## Performance

Agent 0 measured 29.3 seconds for 473 files with one `git hash-object`
subprocess per path. This is accepted for the pilot. Batching is a follow-up
optimization and must not be mixed into the blocking grammar correction unless
it preserves canonical `--path` clean-filter behavior and all safety fixtures.

## Stop Conditions

Stop and return evidence when:

- a required preamble shape falls outside the bounded grammar;
- include-guard matching cannot be made deterministic;
- a proposed skip would pass declarations or executable code;
- r2 changes any r1 safety-state transition;
- canonical blob hashing changes;
- real-tree results contradict the expected recovered-comment mechanism.

## Reference Candidate

`handoffs/2026-08-07-colosseum-code-encyclopedia-generator-reference-r2.py`

The candidate implements this grammar but remains an unexecuted handoff artifact
until Agent 0 ports or adopts and runs it.
