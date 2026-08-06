# Colosseum Code Encyclopedia -- Comics Pilot Bundle r1

## Status

**Execution-ready preflight; Colosseum remains unmodified.** No generator, build, test, smoke, or cold-agent trial was run here.

## Basis

- Issue: `Preflight-Architect#3`
- Design: `Colosseum@a7f2fa31b2b06087086395737cf64c7eeed34a6b`
- Inspected source: `Colosseum@a40333dc1fc9823ceb9decd811deeadde6ac4c2d`
- Scope: comics ingest and reader only

## Read First

1. `research/2026-08-07-issue-3-code-encyclopedia-pilot-response.md`
2. `specifications/2026-08-07-colosseum-code-encyclopedia-pilot-generator-contract-r1.md`
3. `handoffs/2026-08-07-colosseum-code-encyclopedia-generator-reference-r1.py`
4. Colosseum's approved code-encyclopedia design

## Decisions Agent 0 Must Ratify

1. Generate/check detects but does not accept drift.
2. Explicit accept/refresh advances a reviewed hash and comment.
3. Parsing is strict, with only `.pragma library` skipped.
4. Stale source comments are repaired before acceptance.
5. Adoption stays pinned or is explicitly rebased and reinspected.

# Six-Part Guide Contract

The adopted comics guide must contain, in order:

1. **What this subsystem is for** -- one observable outcome.
2. **The flow** -- trigger, receiver, data/identity, ownership/lifecycle change, failure branch, and generated entry at every boundary.
3. **The files that matter** -- file, role, reason to open, generated entry.
4. **Where state lives** -- authority, key, writer, reader, lifetime/persistence, failure/migration.
5. **The traps** -- failure mode, evidence, false shortcut, discriminating check.
6. **How to test it** -- harness/gate, proof, limitation, manual validation.

Every claim must be inspected at the stated basis. Generated comments must not be copied into authored prose.

# Draft Comics Guide

## 1. Purpose

Turn a selected issue into an app-owned readable archive and present its pages through the native comic-reader path while preserving catalog and reading state.

## 2. Flow

1. `qml/Main.qml` loads `qml/ComicSeries.qml` and `qml/ComicSeriesPage.qml`; those surfaces choose open-versus-download through the comics store.
2. `ComicDownloader::downloadIssue` uses temporary ownership, promotes a completed download, and passes it to archive probing. Recoverable input is not deleted before a verified app-owned result exists.
3. `CbzArchive::probe` checks structure and readable pages. Readable CBZs follow the direct path; incompatible archives follow extract/normalize/repack. Legacy loose pages use repair-before-prune migration.
4. The downloader atomically persists catalog state. Current page descriptors carry archive path plus entry name; loose-file forms remain compatibility/migration inputs.
5. `qml/MangaReader.qml` forwards entry, store, and identity inputs to `ComicReaderShell`.
6. The shell obtains pages and stored reader state, then opens `ComicReaderCore`. `parsePages` accepts archive/entry descriptors and a local-file compatibility form. A new entry advances generation and rebuilds models.
7. Single, double, or strip QML surfaces request pages through the async provider/response path. Generation checks prevent stale work publishing into a newer entry. `ComicReaderState.js` supplies pure decisions, not persistence or async ownership.

## 3. Confirmed Seed Files

- `qml/Main.qml`
- `qml/ComicSeries.qml`
- `qml/ComicSeriesPage.qml`
- `qml/MangaReader.qml`
- `native/engine/ComicDownloader.h/.cpp`
- `native/engine/CbzArchive.h/.cpp`
- `qml/comicreader/ComicReaderShell.qml`
- `native/comicreader/ComicReaderCore.h/.cpp`
- `native/comicreader/ComicReaderProvider.h`
- `native/comicreader/ComicReaderImageResponse.h`
- `qml/comicreader/ComicReaderState.js`
- single/double/strip reader surface QML files

This is not the final manifest. Add directly reached state stores, provider/cache implementations, registrations, and tests on the adoption branch.

## 4. State

- issue/catalog record: downloader/store index; persisted;
- app-owned CBZ: comics storage; retained until removal;
- legacy loose pages: migration input; prune after verified replacement;
- page descriptors: caller/store plus core; replaced per issue;
- reader generation: `ComicReaderCore`; invalidates prior async work;
- preferences/resume: supplied store plus shell contract;
- layout/navigation decisions: pure `ComicReaderState.js` functions.

Exact keys and methods require adoption-branch confirmation.

## 5. Traps

Confirmed stale openings at `a40333d`:

- `ComicDownloader.h` describes loose-page extraction/archive deletion while implementation uses CBZ ownership plus fallback repack.
- `ComicSeries.qml` describes extracted-page reading while the store path uses archive/entry descriptors.
- `ComicSeriesPage.qml` says it is parked/unrouted, but `Main.qml` loads it and it has active actions.

Repair those comments, generate to expose drift, review, then explicitly accept. Do not teach the generator to reinterpret them.

Strict parser edges:

- `CbzArchive.h` starts with `#pragma once`; later prose does not count, so it is `UNDOCUMENTED`.
- `ComicReaderState.js` starts with `.pragma library`; this is the one approved prologue exception.

Other traps: silent hash acceptance, hand-edited generated files, identity collapse, stale async publication, and unbounded pilot scope.

## 6. Test Gates

Parser fixtures must cover line/block comments, leading blanks, `.pragma library`, hard stops such as `#pragma once` and imports, missing comments, BOM/CRLF, invalid UTF-8, unterminated blocks, and invalid manifest paths.

Integration must prove first generation, second-run no-diff, persistent `DRIFTED`, explicit acceptance, manifest add/remove, generated-output overwrite/check, state-integrity failure, unrelated-commit stability, exact `UNDOCUMENTED` count, and complete entry fields.

Execution must locate existing downloader/archive and reader core/provider/QML harnesses and their registrations. The complete `tests/` listing exceeded connector response limits.

A fresh agent must perform a real comics navigation task. Record wake file, code-map page, guide/index entries used, first correct source file, wrong turns, state owner, and test seam. This package's author cannot self-certify that gate.

# Manifest and Discoverability

Add a file only for a direct call/include, QML load, state authority, async/cache dependency, selected-type registration, or existing test proving selected behavior. Record inbound evidence. Exclude third-party/vendor code and stop at generic infrastructure once the comics contract is named.

Recommended paths:

```text
docs/code-map/README.md
docs/code-map/guides/comics-ingest-reader.md
docs/code-map/generated/comics-pilot-index.md
docs/code-map/comics-pilot-files.txt
```

Add one pointer to the confirmed agent wake path:

> Read `docs/code-map/README.md` before changing comics download, archive ingest, comic catalog state, reader state, page delivery, or comic-reader tests.

# Roadmap

1. Ratify semantics, pin, and paths.
2. Implement parser and state-transition fixtures.
3. Adopt or replace the reference generator; create manifest/output/state; prove no-diff.
4. Repair stale comments; detect drift before explicit acceptance.
5. Complete manifest from calls, state, async work, registrations, and tests.
6. Ground the guide and add the landing/wake pointer.
7. Run generator, product, smoke, and independent cold-agent gates.

Stop if the narrow grammar fails selected files, clean filters prevent stable hashes, drift-preserving acceptance is rejected without an equivalent, or the pilot cannot be bounded.

# AGENT PACKET

## TASK
Adopt and validate the comics-only code-encyclopedia pilot in Colosseum.

## OBJECTIVE
Deliver a deterministic source-comment index, one six-part comics guide, and one thin wake-path pointer that lead a fresh agent to correct comics source and tests.

## CONSTRAINTS
Preserve comments verbatim; include `UNDOCUMENTED`; use canonical Git blob hashes; never hand-edit generated files; keep scope comics-only; do not self-certify cold-agent success.

## SLICES
Ratify -> fixtures -> generator -> source-comment repairs -> manifest discovery -> guide/pointer -> verification.

## FIRST ACTION
Read the approved design and record decisions for the five ratifications before copying the reference candidate.

## VERIFICATION STATUS
Repository evidence supports the design and flow. Generator behavior, complete coverage, idempotence, builds/tests, smoke behavior, and cold-agent navigation remain unverified.
