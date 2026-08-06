# Biblio Library Tab - Lanista-Ready Design Guide

## Status

Planning-ready design guide. Implementation and runtime behavior remain unverified.

## Objective

Add a retained third Biblio tab:

```text
Discover | Explore | Library
```

The page should be a simple Theatre-like library wall, not a universal media-library redesign.

## Scope

The Library shows one card per saved Biblio Collection work. It joins:

```text
Collection membership
+ optional reading Progress
+ optional local ebook
+ optional local audiobook
```

Identity, download, and audiobook rules are required because they determine what a card represents and which action is honest. They remain bounded row-derivation rules.

### In scope

- retained Library page in `BiblioWorld`;
- pure Biblio row derivation;
- Collection, Progress, Books, BookTorrents, and Audiobooks read seams;
- smallest missing read-only local inventory seam;
- Resume, Read, Details, and Remove from Library;
- title/author search;
- All, In Progress, and Downloaded filters;
- Last Read, Recently Added, and A-Z sorts;
- stable semantic surfaces for Lanista;
- focused native/QML tests and isolated Lanista scenarios.

### Non-goals

- universal library abstraction;
- new identity registry;
- bulk Progress migration;
- unified download registry;
- standalone audiobook playback;
- file deletion;
- cloud sync;
- recommendations;
- removal of existing Continue Reading or Your Collection shelves;
- new Lanista commands unless the current ledger proves a gap.

## Row authority

| Concern | Authority |
|---|---|
| Membership and row identity | original Biblio Collection entry / pairKey |
| Details | original Collection entry |
| Reading progress and Resume | exact matched `kind = "book"` Progress |
| Ebook availability | Books or BookTorrents |
| Audio availability | Audiobooks |
| Remove | Collection only |
| Display row | read-only projection |

One Collection entry produces at most one row. Local forms decorate the row and never create duplicate cards.

## Legacy Progress matching

Use a small pure matcher:

1. exact Collection ID equals Progress ID;
2. pair/work key in Progress resume metadata;
3. normalized title + author;
4. title only when both records lack author.

Newest `updatedAt` wins within the same confidence level. One Progress record may populate only one row. Ambiguity yields no Resume. Do not migrate old records in this feature.

## Local availability

Use local snapshots from Books, BookTorrents, and Audiobooks. Opening Library must not trigger provider search, metadata hydration, torrent discovery, or network work.

If BookTorrents lacks a deterministic completed-download list, add only a read-only list over its existing persisted index.

```text
ebookAvailable = valid Books path || valid BookTorrents path
audioAvailable = matching Audiobooks download
downloaded = ebookAvailable || audioAvailable
```

Show separate Ebook and Audio badges.

When several ebooks exist, prefer:

1. valid path owned by matched Progress;
2. valid Books path;
3. valid BookTorrents path.

## Primary action

| Valid Resume | Ebook | Audio | Action |
|---:|---:|---:|---|
| yes | any | any | Resume |
| no | yes | any | Read |
| no | no | yes | Details |
| no | no | no | Details |

Resume uses the exact Progress object. Read uses the selected local ebook path. Details uses the original Collection entry. Audio-only opens Details in v1. Remove from Library deletes membership only, not Progress or files.

## Page structure

Extend the retained shell:

```text
BiblioWorld
  BiblioDiscoverPage
  BiblioExplorePage
  BiblioLibraryPage
```

Do not use a Loader.

Recommended responsibilities:

```text
BiblioWorld.qml
  tab and route forwarding

BiblioLibraryPage.qml
  retained query/filter/sort/scroll state
  source snapshots
  wall, cards, menus, and actions

BiblioLibraryApi.js
  pure joins, matching, rows, search, filters, and sort
```

Reuse Theatre's structural pattern, not its video concepts.

## Minimal visual contract

Each card shows cover, title, author, optional reading progress, and Ebook/Audio badges. Use fixed book-poster metrics and the existing fallback artwork stack. Keep existing Biblio shelves.

Empty states:

- `Your library is empty`
- `Nothing matches these filters`

## Lanista contract

Use the current isolated Lanista session and existing commands. No new command is expected.

Required stable surfaces:

```text
biblioLibraryTab
biblioLibraryPage
biblioLibrarySearch
biblioLibraryFilterAll
biblioLibraryFilterInProgress
biblioLibraryFilterDownloaded
biblioLibrarySortLastRead
biblioLibrarySortAdded
biblioLibrarySortAz
biblioLibraryGrid
biblioLibraryEmptyState
biblioLibraryNoResults
biblioLibraryMenu
biblioLibraryCard_<stable work identity>
```

Page properties:

```text
query
stateFilter
sortMode
rowCount
visibleCount
emptyReason
contentY
```

Card properties:

```text
entryId
title
author
progress
canResume
canRead
ebookAvailable
audioAvailable
primaryAction
```

These are stable product semantics, not arbitrary QObject reflection.

### Isolated fixture

Seed local data for:

1. saved work with no Progress or download;
2. valid resumable Progress;
3. legacy title/author Progress match;
4. local ebook with no Progress;
5. audiobook-only work;
6. optional missing cover.

Never use the daily app or live user data.

### Required scenarios

1. Open Biblio Library, assert row count, and capture the wall.
2. Exercise search, In Progress, Downloaded, A-Z, scrolling, tab switch, and retained state.
3. Verify Resume, Read, audio-only Details, and plain Details routing.
4. Remove one work and assert row removal while lower-layer tests prove Progress/files remain.
5. Verify empty and no-results states.
6. Capture visual enidence for wall, filters, empty states, and a card with progress and both badges.

Use property/event waits, not sleeps. If a route cannot be distinguished with current probes, the plan must add the smallest semantic read seam before relying on it.

## Test responsibilities

Pure/native tests cover row identity, exact-versus-fuzzy Progress matching, ambiguity, duplicate prevention, badges, path preference, primary action, search/filter/sort, and membership-only removal.

Qt Quick Test covers retained page state, controls, empty states, card presentation, and emitted action payloads.

Only Lanista proves assembled-app navigation, real routes, tab retention, and user-visible behavior.

## Acceptance criteria

- `Discover | Explore | Library` exists.
- Library is retained.
- Every saved work appears once.
- Collection pairKey is row identity.
- exact Progress owns Resume.
- ambiguous matches never Resume.
- ebook/audio badges come from local state without network work.
- Resume precedes Read.
- ebook-only reads.
- audio-only opens Details.
- Remove affects membership only.
- search, three filters, and three sorts work.
- empty and no-results states differ.
- query/filter/sort/scroll survive tab switches.
- existing shelves remain.
- semantic surfaces exist.
- focused tests pass.
- isolated Lanista scenarios pass with current artifacts.

## `brotherhood-writing-plans` handoff

The next agent should use this guide as approved design input and inspect the current Collection, Progress, Books, BookTorrents, Audiobooks, routes, tests, and `docs/colosseum-lanista-verification.md`.

The plan must preserve this scope, use repository-confirmed paths, separate row logic/page wiring/local availability/tests/Lanista replay, and include for each slice:

```markdown
Purpose:
Dependencies:
Likely files:
Implementation guidance:
Behavior to preserve:
Focused tests:
Lanista actions:
Completion signal:
State / properties:
Visual evidence:
Regression paths:
Evidence artifacts:
Bridge status:
Completion criterion:
```

Recommended planning order:

1. repository and route inventory;
2. pure row model and fixtures;
3. smallest missing local read seam;
4. retained page/tab;
5. card actions and removal;
6. semantic names/properties;
7. native and QML tests;
8. isolated Lanista scenarios;
9. ledger reconciliation.

## Stop conditions

Return for review if pairKey is not sufficiently unique, one Progress can Resume multiple works, inventory requires network work, audio requires new playback architecture, a unified registry becomes mandatory, the page requires unrelated navigation restructuring, the plan expands into migration/redesign, or Lanista needs unavailable commands.

## First action

Inspect current data and route shapes, then invoke `brotherhood-writing-plans` to produce the bounded implementation plan.
