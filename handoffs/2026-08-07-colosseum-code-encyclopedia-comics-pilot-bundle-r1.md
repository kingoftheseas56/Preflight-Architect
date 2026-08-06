# Colosseum Code Encyclopedia -- Comics Pilot Bundle r1

## Status

**Execution-ready preflight package.** Colosseum is unmodified. No generator, build, test, smoke, or cold-agent trial was run here.

## Basis

- Issue: `kingoftheseas56/Preflight-Architect#3`
- Approved design: `kingoftheseas56/Colosseum@a7f2fa31b2b06087086395737cf64c7eeed34a6b`
- Inspected source: `kingoftheseas56/Colosseum@a40333dc1fc9823ceb9decd811deeadde6ac4c2d`
- Scope: comics ingest and reader only

## Read First

1. `research/2026-08-07-issue-3-code-encyclopedia-pilot-response.md`
2. `specifications/2026-08-07-colosseum-code-encyclopedia-pilot-generator-contract-r1.md`
3. `handoffs/2026-08-07-colosseum-code-encyclopedia-generator-reference-r1.py`
4. Colosseum's approved code-encyclopedia design

## Required Ratifications

Agent 0 must accept or replace:

1. generate/check detects but does not accept drift;
2. explicit accept/refresh advances a reviewed hash and comment;
3. top-comment parsing is strict, with only `.pragma library` skipped;
4. stale source comments are repaired before acceptance;
5. adoption stays pinned or is consciously rebased and reinspected.

# Six-Part Guide Template

```markdown
# <Subsystem> Guide
**Source basis:** `<repository>@<commit>`
**Generated index:** [source index](<relative-link>)

## 1. What this subsystem is for
One observable outcome.

## 2. The flow
For each boundary name the trigger, receiver, data/identity, ownership or
lifecycle change, failure branch, and generated entry.

## 3. The files that matter
| File | Role | Why open it | Generated entry |
|---|---|---|---|

## 4. Where state lives
Name authority, key, writer, reader, persistence/lifetime, lifecycle boundary,
and failure or migration behavior.

## 5. The traps
Name failure mode, evidence, false shortcut, and fastest discriminating check.

## 6. How to test it
Name the harness or gate, what it proves, what it does not prove, and required
manual validation.
```

Adoption gate: every file and behavior claim is inspected at the stated basis; state writers and readers are distinct; stale comments are exposed; harness claims are inspected or marked as discovery; generated comments are not duplicated into authored prose.

# Draft Comics Guide

## 1. What this subsystem is for

Turn a selected issue into an app-owned readable archive and present its pages through the native comic-reader path while preserving catalog and reading state.

## 2. The flow

1. **Choose issue.** `qml/Main.qml` loads `qml/ComicSeries.qml` and `qml/ComicSeriesPage.qml`. Those surfaces choose open-versus-download through the comics store.
2. **Download.** `ComicDownloader::downloadIssue` writes through temporary ownership, promotes a completed download, and passes it to archive probing. Recoverable input is not deleted before a verified app-owned result exists.
3. **Normalize.** `CbzArchive::probe` checks structure and readable pages. A readable CBZ follows the direct path; incompatible archives follow extraction, normalization, and repack. Legacy loose pages use repair-before-prune migration.
4. **Persist.** The downloader saves its catalog atomically. Current page descriptors carry archive path plus entry name; loose-file forms remain compatibility/migration inputs.
5. **Enter reader.** `qml/MangaReader.qml` forwards entry, store, and identity inputs to `ComicReaderShell`.
6. **Open native core.** The shell obtains pages and stored reader state, then opens `ComicReaderCore`. `parsePages` accepts archive/entry descriptors and a local-file compatibility form. A new entry advances generation and rebuilds models.
7. **Render.** Single, double, or strip QML surfaces request pages through the asynchronous provider/response path. Generation checks prevent stale work from publishing into a newer entry. `ComicReaderState.js` supplies pure decisions, not persistence or async ownership.

## 3. The files that matter

Confirmed seed, not final manifest:

| File | Role |
|---|---|
| `qml/Main.qml` | route owner |
| `qml/ComicSeries.qml` | issue open/download surface |
| `qml/ComicSeriesPage.qml` | DB/LOCG issue surface |
| `qml/MangaReader.qml` | compatibility wrapper |
| `native/engine/ComicDownloader.h/.cpp` | ingest, ownership, catalog, migration |
| `native/engine/CbzArchive.h/.cpp` | archive probe, extract, repack |
| `qml/comicreader/ComicReaderShell.qml` | reader orchestrator |
| `native/comicreader/ComicReaderCore.h/.cpp` | page parsing, models, generation |
| `native/comicreader/ComicReaderProvider.h` | image request seam |
| `native/comicreader/ComicReaderImageResponse.h` | async response/cancellation seam |
| `qml/comicreader/ComicReaderState.js` | pure reader decisions |
| reader surface QML files | single/double/strip presentation |

Agent 0 must add directly reached state stores, cache/provider implementations, registrations, and tests discovered on the adoption branch.

## 4. Where state lives

| State | Authority | Lifecycle |
|---|---|---|
| issue/catalog record | downloader/store index | persisted across restart |
| app-owned CBZ | comics storage | retained until removal |
| legacy loose pages | migration input | prune only after verified replacement |
| page descriptors | caller/store and core | replaced per opened issue |
| reader generation | `ComicReaderCore` | invalidates prior async work |
| preferences/resume | supplied store plus shell contract | persistence depends on store |
| layout/navigation decisions | `ComicReaderState.js` functions | computed, not persisted |

Exact keys and methods must be confirmed on the adoption branch.

## 5. The traps

### Stale opening comments

Confirmed at `a40333d`:

- `native/engine/ComicDownloader.h` describes loose-page extraction/archive deletion while the pinned implementation uses CBZ ownership plus fallback repack.
- `qml/ComicSeries.qml` describes extracted-page reading while the store path uses archive/entry descriptors.
- `qml/ComicSeriesPage.qml` says it is parked and unrouted, but `qml/Main.qml` loads it and it has active actions.

Repair these comments in Colosseum, expose the resulting drift, review, then explicitly accept. The generator must not reinterpret them.

### Strict parser edge

`native/engine/CbzArchive.h` starts with `#pragma once`; its later prose does not count and the file must be `UNDOCUMENTED`.

`qml/comicreader/ComicReaderState.js` starts with `.pragma library`; this is the one approved prologue implementation.
