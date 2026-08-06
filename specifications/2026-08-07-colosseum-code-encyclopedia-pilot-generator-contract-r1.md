# Colosseum Code Encyclopedia Pilot — Generator Contract r1

## Status

**Execution-ready design; reference candidate unrun and unadopted.**

**Basis**

- Approved design: `kingoftheseas56/Colosseum@a7f2fa31b2b06087086395737cf64c7eeed34a6b`
- Source inspection basis: `kingoftheseas56/Colosseum@a40333dc1fc9823ceb9decd811deeadde6ac4c2d`
- Pilot only: comics ingest and reader path

## Objective

Provide one deterministic Python command that generates a pilot source index from the source tree without paraphrasing source comments, while making missing comments, source drift, and generated-file tampering visible.

## Product Contract

For every path in the pilot manifest, the generated index contains:

- repository-relative path;
- accepted canonical Git blob hash;
- current canonical Git blob hash;
- status: `CURRENT`, `DRIFTED`, `UNDOCUMENTED`, or both drifted and undocumented;
- the accepted top-of-file comment verbatim when present;
- a link to the source;
- a stable per-file anchor.

The index also reports total, documented, undocumented, and drifted counts.

The generated Markdown is not an authored knowledge layer. It contains only source-derived material plus fixed generator labels and warnings.

## Recommended Adoption Paths

These are product decisions for Agent 0 to ratify, not confirmed existing Colosseum paths:

```text
scripts/generate_code_encyclopedia.py
docs/code-map/comics-pilot-files.txt
docs/code-map/generated/comics-pilot-index.md
docs/code-map/generated/.comics-pilot-state.json
tests/code_encyclopedia/
```

## Command Contract

### Generate or refresh output without accepting drift

```text
python scripts/generate_code_encyclopedia.py \
  --paths docs/code-map/comics-pilot-files.txt \
  --output docs/code-map/generated/comics-pilot-index.md \
  --state docs/code-map/generated/.comics-pilot-state.json
```

Effects:

- harvest all manifest files;
- accept newly added manifest entries on their first appearance;
- retain previously accepted comment/hash pairs when the current blob differs;
- mark those entries `DRIFTED`;
- overwrite generated Markdown when its deterministic rendering differs;
- write acceptance state atomically;
- print counts;
- exit nonzero only on contract or I/O failure.

### Accept reviewed current source

```text
python scripts/generate_code_encyclopedia.py \
  --paths docs/code-map/comics-pilot-files.txt \
  --output docs/code-map/generated/comics-pilot-index.md \
  --state docs/code-map/generated/.comics-pilot-state.json \
  --accept native/engine/ComicDownloader.h
```

`--accept PATH` is repeatable. It advances the selected entry to the current canonical blob and current harvested comment.

For an intentional bulk review:

```text
... --accept-all-drifted
```

### Check without writing

```text
python scripts/generate_code_encyclopedia.py \
  --paths docs/code-map/comics-pilot-files.txt \
  --output docs/code-map/generated/comics-pilot-index.md \
  --state docs/code-map/generated/.comics-pilot-state.json \
  --check
```

`--check` writes nothing and fails when:

- state is absent or missing a manifest entry;
- generated Markdown differs;
- state encoding difers or -- pilot remains missing;
- any entry remains `DRIFTED`;
- parsing, hashing, or integrity validation fails.

`--check` cannot be combined with acceptance flags.

## Why Acceptance Is Separate

The approved design says a changed file remains `DRIFTED` until its comment is re-harvested. If ordinary generation always replaces the accepted hash and comment with current content, drift disappears in the same operation that detects it.

The accepted-state boundary is therefore required, not optional ceremony:

```text
current source edit
→ generate/check
→ DRIFTED, old accepted description retained as a warning
→ human/agent reads current source and repairs comment if needed
→ explicit accept
→ current hash/comment become accepted
```

Agent 0 must ratify this interpretation before adoption.

## Manifest Contract

The manifest is UTF-8 text with one repository-relative source path per line.

Allowed:

```text
# ingest
native/engine/ComicDownloader.h
native/engine/ComicDownloader.cpp

# reader
qml/comicreader/ComicReaderShell.qml
```

Rules:

- blank lines and lines beginning with `#` are ignored;
- paths are normalized to `/`;
- absolute paths and `..` are rejected;
- duplicates are rejected;
- unsupported suffixes are rejected;
- every listed path must exist as a file;
- output ordering is lexical by normalized path;
- removing a path from the manifest removes it from output and next state;
- adding a path is an explicit scope decision and accepts its initial source state.

Supported pilot suffixes:

```text
.c .cc .cpp .cxx .h .hh .hpp .hxx .qml .js
```

Third-party and vendored code must not be listed.

## Top-Comment Grammar

### Shared rules

1. Decode UTF-8 with optional BOM.
2. Ignore leading blank lines.
3. Apply only the one declared language prologue exception below.
4. The next logical line must begin with `//` or `/*` after indentation.
5. Otherwise mark the file `UNDOCUMENTED`.
6. Do not scan downward for a later comment.
7. Unterminated top block comments are fatal.

### JavaScript prologue exception

For `.js` only, the parser may skip exactly:

```text
.pragma library
```

plus following blank lines before looking for a comment.

This exception is grounded by `qml/comicreader/ComicReaderState.js`.

### Hard stops

The parser does not skip:

- `#pragma once`;
- includes;
- imports;
- QML pragmas;
- namespace or type declarations;
- license banners followed by a second explanatory comment;
- arbitrary directives.

Therefore `native/engine/CbzArchive.h` is `UNDOCUMENTED` under this grammar because it starts with `#pragma once`.

### Line comment block

When the first logical line starts with `//`:

- collect consecutive `//` lines;
- allow blank lines between those comment lines;
- exclude blank lines after the final `//` line;
- stop at the first other token;
- preserve comment markers, indentation, text, and internal line endings.

### Block comment

When the first logical line starts with `/*`:

- collect through the first closing `*/`;
- preserve the literal block;
- fail if no closing delimiter exists.

### “Verbatim” definition

The generator does not remove comment markers, wrap text, correct spelling, rewrite terminology, or synthesize a description. It emits the harvested block in a fenced `text` block. The source file remains the authoritative location for edits.

## Canonical Git Blob Hash

For each worktree file, hash its bytes through:

```text
git hash-object --path=<repo-relative-path> --stdin
```

Using `--path` applies the repository's normal clean filters and produces the canonical blob identifier for the file content.

The generator must fail if Git is unavailable, the invocation is outside a worktree, or hashing fails.

## Acceptance State

State is machine-owned JSON:

```json
{
  "schema": 1,
  "entries": {
    "native/engine/ComicDownloader.h": {
      "accepted_blob": "<40-or-repository-format-hash>",
      "accepted_comment": "// literal source comment..."
    }
  },
  "integrity": "sha256:<digest>"
}
```

Rules:

- `accepted_comment` is `null` for accepted undocumented files;
- the digest covers canonical JSON of `schema` and `entries`;
- state-integrity failure is fatal;
- state writes are atomic;
- no timestamps, host paths, branch names, or HEAD identifiers appear;
- unrelated repository commits cannot alter output;
- accepted entries not present in the manifest are discarded on the next write;
- a normal generation never advances an existing mismatched entry.

The digest is an accidental/manual-edit guard, not a cryptographic trust boundary.

## Generated Markdown Schema

```markdown
# Colosseum Code Encyclopedia — Generated Source Index

> **GENERATED FILE — DO NOT EDIT.** Edit source comments, then run the generator.
> Acceptance state: `docs/code-map/generated/.comics-pilot-state.json`

## Summary

- Total files: **N**
- Documented: **N**
- Undocumented: **N**
- Drifted: **N**

<a id="file-native-engine-comicdownloader-h"></a>
## `native/engine/ComicDownloader.h`

- Status: **DRIFTED**
- Accepted blob: `<hash>`
- Current blob: `<hash>`
- Source: [`native/engine/ComicDownloader.h`](../../../native/engine/ComicDownloader.h)
- Interpretation: the accepted description predates the current blob; read the source before relying on it.

```text
// literal accepted comment
```
```

For an undocumented file, the fixed body is:

```text
_No top-of-file explanatory comment was harvested._
```

No authored summary, symbol inventory, signature reference, or inferred role belongs in this layer.

## Determinism and Idempotence

The renderer must depend only on:

- sorted manifest paths;
- current file content;
- accepted state;
- fixed generator version/format.

It must not include:

- wall-clock timestamps;
- current branch name;
- repository HEAD;
- absolute paths;
- machine identifiers;
- traversal order;
- locale-dependent formatting.

Atomic writes should first compare content and skip replacement when unchanged.

Acceptance proof:

```text
generate
git diff --exit-code -- generated-index state
generate again
git diff --exit-code -- generated-index state
```

The execution agent must choose exact repository commands after adoption; Preflight does not claim these were run.

## Generated-Layer Fork Prevention

Required behavior:

- ordinary generate overwrites a hand-edited generated Markdown file;
- `--check` reports that the generated Markdown differs;
- state-integrity mismatch rejects hand-edited state;
- generated header directs edits back to source comments.

No reverse-import path from Markdown to source is permitted.

## Error Contract

Fatal errors include:

- invocation outside Git;
- missing Git executable;
- missing/empty manifest;
- invalid, duplicate, escaping, unsupported, or missing source path;
- non-UTF-8 source;
- unterminated top block comment;
- Git hash failure;
- malformed state;
- state schema mismatch;
- state integrity mismatch;
- unknown `--accept` path;
- `--check` combined with acceptance flags;
- atomic-write failure.

Errors go to stderr and produce a nonzero exit.

Drift and undocumented entries are reportable states, not generator crashes.

## Reference Candidate

The companion file:

```text
handoffs/2026-08-07-colosseum-code-encyclopedia-generator-reference-r1.py
```

implements this contract with the Python standard library.

Status:

- authored;
- internally reviewed for contract coverage;
- not copied into Colosseum;
- not executed;
- not syntax-checked by a runtime;
- not tested;
- not performance-measured.

Repository evidence outranks the candidate if adoption reveals a conflict.

## Fixture Matrix

| Fixture | Input shape | Expected |
|---|---|---|
| F01 | leading `//` block | literal documented block |
| F02 | leading `/* .. */` | literal documented block |
| F03 | blank lines then `//` | documented |
| F04 | `.pragma library`, then `//` in `.js` | documented |
| F05 | `#pragma once`, then comment | `UNDOCUMENTED` |
| F06 | import/include, then comment | `UNDOCUMENTED` |
| F07 | no comment | `UNDOCUMENTED` |
| F08 | blank lines inside `//` block | internal blanks preserved |
| F09 | trailing blanks before code | trailing blanks excluded |
| F10 | UTF-8 BOM then comment | documented |
| F11 | CRLF comment block | literal content retained deterministically |
| F12 | non-UTF-8 bytes | fatal |
| F13 | unterminated `/*` | fatal |
| F14 | duplicate manifest path | fatal |
| F15 | `../` or absolute manifest path | fatal |
| F16 | unsupported suffix | fatal |

## State-Transition Matrix

| Starting state | Action | Expected |
|---|---|---|
| no state | generate | all manifest entries initially accepted |
| current accepted entry | generate | `CURRENT`, no state change |
| source blob changed | generate | `DRIFTED`, accepted comment/hash retained |
| drifted entry | `--accept PATH``| current comment/hash accepted |
| several drifted | `--accept-all-drifted` | all current |
| source comment removed and accepted | generate | `UNDOCUMENTED` |
| source changed from documented to no comment without acceptance | generate | `DRIFTED`, old accepted comment remains visible |
| generated Markdown hand-edited | generate | edit overwritten |
| generated Markdown hand-edited | `--check` | failure |
| state hand-edited without digest repair | any | fatal integrity mismatch |
| unchanged repository at unrelated new HEAD | generate | no output diff |

## Acceptance Mapping

| Issue criterion | Contract evidence | Execution evidence required |
|---|---|---|
| 1. One command; second run no diff | deterministic command and atomic writes | run twice in adopted tree |
| 2. Every pilot file carries comment/hash/path | manifest-driven schema | compare manifest to output |
| 3. Missing comment visible and counted | `UNDOCUMENTED` rendering and summary | parser fixtures + real manifest |
| 4. Source edit marks DRIFTED until re-harvest | accepted-state boundary | edit fixture, generate, accept |
| 5. Hand edit rejected or overwritten | generate overwrite + `--check` | mutate output fixture |
| 6. Guide names only existing behavior | outside generator | source-ground guide audit |
| 7. Guide states persistence and harness | outside generator | guide audit |
| 8. Cold agent reaches right file | outside generator | independent task trial |
| 9. Wake path reaches index | outside generator | navigation trial |
| 10. No restatement/contradiction | literal fenced comment | byte/text comparison fixture |

## Stop Conditions

Stop implementation and return evidence when:

- selected pilot files exhibit a required prologue not covered by the narrow grammar;
- clean-filter behavior prevents stable canonical hashes;
- accepted-state semantics are rejected without an equivalent drift-preserving mechanism;
- the selected manifest cannot be bounded to the pilot;
- an existing repository generator or documentation convention materially conflicts with this contract.

## First Executable Action

Agent 0 creates parser fixtures F01b��F16 in a temporary or repository test harness and ports the reference candidate only after ratifying the acceptance operation.
