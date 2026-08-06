# Biblio Library Tab - Theatre-Equivalent Implementation Guide

> Purpose: Give a fresh agent enough approved design context to run `brotherhood-writing-plans` for a small Biblio Library tab that mirrors Theatre's existing Library pattern.
>
> Status: Planning-ready design guide. No implementation or runtime verification is claimed.
>
> Supersedes: `roadmaps/2026-08-06-biblio-library-tab-lanista-ready-design-guide.md`.

## 1. Objective

Replicate Theatre's retained Library-tab pattern for Biblio.

The result should be:

```text
Discover | Explore | Library
```

The Library tab should show saved Biblio books in a retained wall, using Biblio's existing Collection, Progress, routes, and shared card/artwork primitives.

This is not a new library product. It is Biblio's equivalent of Theatre's existing Library surface.

## 2. Scope

### In scope

- Add `Library` to Biblio's existing tab bar.
- Mount one retained `BiblioLibraryPage` beside Discover and Explore.
- Build rows from existing Biblio Collection entries.
- Attach existing book Progress when it matches reliably.
- Reuse existing Details, Resume, and Collection removal routes.
- Reuse Theatre's structural pattern:
  - local store snapshots;
  - pure row derivation;
  - retained wall;
  - simple search/filter/sort;
  - card actions.
- Adapt the card only for book metadata:
  - title;
  - author;
  - cover;
  - optional progress;
  - optional local-format indicator when already available.
- Add the minimum semantic names needed for Lanista.
- Add focused tests and one compact isolated Lanista scenario.

### Out of scope

- A universal media-library framework.
- A new book identity system.
- Bulk migration of old Progress records.
- A unified download registry.
- A new audiobook playback route.
- Separate ebook and audiobook cards.
- File deletion.
- Cloud sync.
- Recommendations, genres, completion state, or new-release logic.
- Replacing Continue Reading or Your Collection.
- Broad artwork-pipeline changes.
- New Lanista commands unless the current ledger proves one is missing.
- Refactoring Theatre's Library.

## 3. Theatre is the reference shape

Theatre already follows this shape:

```text
TheatreWorld
  retained LibraryPage
    Collection entries
    + Progress
    + existing downloaded state
    -> pure rows
    -> wall
    -> Resume / Details / Remove
```

Biblio should follow the same responsibility split.

Reuse Theatre's pattern, not its video-specific concepts.

Do not import:

- watched state;
- episodes;
- airing;
- finales;
- new-episode metadata;
- video-specific resume routing.

## 4. Biblio page structure

Extend `qml/BiblioWorld.qml` from:

```text
Discover | Explore
```

to:

```text
Discover | Explore | Library
```

Keep all three pages as direct retained children.

Conceptual structure:

```text
BiblioWorld
  BiblioDiscoverPage
  BiblioExplorePage
  BiblioLibraryPage
```

Do not use a Loader for the Library page.

Retention should preserve:

- search text;
- selected filter;
- selected sort;
- scroll position.

The current Discover and Explore behavior must remain unchanged.

## 5. Data model

The row model should remain as small as Theatre's.

One Biblio Collection entry becomes one card.

Conceptual row:

```text
entry
title
author
cover
progressRecord
progress
downloaded
canResume
```

The row is a read-only projection. Do not persist it.

### Authorities

| Concern | Authority |
|---|---|
| Library membership | `Collection.items("biblio")` |
| Card identity | original Collection entry ID |
| Details action | original Collection entry |
| Resume action | matched existing book Progress record |
| Remove action | Collection removal |
| Display row | pure derived object |

Do not create a separate identity registry.

## 6. Progress matching

Keep matching conservative.

Use the simplest repository-supported match that Theatre-equivalent behavior needs:

1. exact Collection entry ID to Progress ID;
2. an already-existing stable book/work ID in Progress metadata, if present;
3. title plus author only if the repository already carries both consistently.

If no reliable match exists:

- show the saved card;
- do not show Resume;
- open Details.

Do not add a general legacy reconciliation engine.
Do not bulk-migrate Progress.
Do not block the Library tab on solving every historic identity case.

The rule is:

> uncertain identity falls back to Details, not new infrastructure.

## 7. Download and audiobook handling

Downloads and audiobooks are optional card decorations, not prerequisites for the page.

Use only availability information already exposed through existing Biblio-facing APIs.

Allowed behavior:

- show a small Downloaded or Ebook indicator when an existing readable ebook record is available;
- show an Audio indicator when an existing audiobook record is already associated with the saved work;
- use an existing local ebook path for Read only if the current route already supports it.

Required fallback:

- no reliable local ebook route -> Details;
- audiobook-only -> Details;
- missing download inventory -> omit the indicator.

Do not add:

- a unified local-media registry;
- a BookTorrents inventory project;
- a new standalone audiobook player;
- download ranking rules beyond what the current APIs already provide.

Local availability must not become a prerequisite for showing Collection entries.

## 8. User-visible behavior

The page should provide the Theatre-equivalent basics.

### Header controls

- Search by title or author.
- Small state filter:
  - All;
  - In Progress;
  - Downloaded, only if existing availability data makes this honest.
- Small sort control:
  - Recently Added;
  - Last Read;
  - A-Z.

If Downloaded cannot be implemented from existing read APIs without new infrastructure, omit it from v1 instead of expanding scope.

### Card behavior

Primary click:

- Resume when a reliable matching Progress record exists and the existing route supports it;
- otherwise open Details.

Context menu:

- Resume, when available;
- Details;
- Remove from Library.

A direct Read action for an unstarted local ebook is optional and should be included only if it reuses an existing route without additional architecture.

### Remove

Use explicit wording:

```text
Remove from Library
```

Remove the Collection entry only.

Do not delete:

- Progress;
- ebook files;
- audiobook files.

### Empty states

- No saved Collection entries:
  - `Your library is empty`
- Search/filter hides all rows:
  - `Nothing matches`

## 9. Visual contract

Use Theatre's wall mechanics and the existing shared poster/artwork components where they already fit.

Biblio-specific card differences should be limited to:

- author shown as secondary text;
- book cover aspect ratio;
- optional reading progress;
- optional Ebook or Audio indicator.

Do not create a new card framework.

If the Theatre card cannot support author text cleanly:

- compose a small Biblio card using existing lower-level shared artwork and metric primitives;
- do not add book-specific branches to Theatre's video card.

The page must not introduce a raw, page-local image pipeline that bypasses the shared fallback stack.

## 10. Minimal implementation boundaries

Likely responsibilities:

```text
qml/BiblioWorld.qml
  add Library tab
  retain Library page
  forward existing actions

qml/BiblioLibraryPage.qml
  store snapshots
  query/filter/sort state
  wall and card presentation
  action signals

qml/BiblioLibraryApi.js
  small pure row derivation
  search/filter/sort
```

These names are recommendations. `brotherhood-writing-plans` must inspect the current tree before freezing exact paths.

Avoid unrelated refactoring.

## 11. Focused tests

Tests should match the limited scope.

### Pure row tests

Cover:

- one Collection entry creates one row;
- exact Progress match enables Resume;
- unmatched Progress leaves Details as the action;
- search matches title and author;
- filter and sort are deterministic;
- Remove uses the original Collection entry;
- optional downloaded state reflects existing supplied input only.

Do not test a speculative identity or download platform.

### Qt Quick Test

Cover:

- page visibility and retained state;
- search/filter/sort update the wall;
- empty and no-results states;
- card displays title, authoq, cover, and optional progress;
- action signals carry the original Collection or Progress object;
- tab hiding does not destroy page state.

Qt Quick Test does not prove the assembled navigation flow.

## 12. Minimal Lanista verification

Use the current isolated Lanista session and existing commands.

No broad new observability contract is required.

### Required stable names

Add only the names needed for the scenario:

```text
biblioLibraryTab
biblioLibraryPage
biblioLibrarySearch
biblioLibraryGrid
biblioLibraryEmptyState
biblioLibraryCard_<stable entry id>
```

Use stable Collection identity, not delegate index, for card names.

Expose only the minimum stable page state needed by current `qml-get` or `ui-query`, such as:

```text
query
rowCount
visibleCount
contentY
```

### Isolated fixture

Seed a small disposable fixture:

1. one saved book with matching Progress;
2. one saved book without Progress;
3. optionally one saved book with existing downloaded metadata.

Do not use the daily app or live user data.

### Scenario

```text
launch isolated session
-> enter Biblio
-> click Library
-> assert Library page visible
-> assert expected cards visible
-> search for one known title or author
-> assert wall narrows to the expected card
-> clear search
-> open one card action:
     Resume when the fixture has reliable Progress,
     otherwise Details
-> return to Library
-> verify search/scroll state is retained across a tab switch
-> remove one fixture card
-> assert it disappears
-> capture the Library wall
```

Use semantic waits and property assertions, not sleeps.

### Evidence

Preserve:

- scenario result;
- semantic snapshot or UI dump;
- final wall capture;
- failure artifacts when applicable.

### Status

- Lower-layer tests pass, Lanista not run:
  - `Test-reported`
- Current isolated scenario passes:
  - `Runtime-validated`
- Required current Lanista capability is absent:
  - `Bridge blocked`
- Scenario fails:
  - `Verification failed`

A screenshot alone is not sufficient when card identity or action can be asserted semantically.

## 13. Acceptance criteria

1. Biblio shows `Discover | Explore | Library`.
2. Library is retained like Theatre's Library.
3. Existing Discover and Explore behavior remains unchanged.
4. Existing Continue Reading and Your Collection remain.
5. Every Biblio Collection entry appears at most once.
6. Each card shows title, author, and cover.
7. Reliable matching Progress enables Resume.
8. Unmatched or uncertain Progress does not enable a wrong Resume.
9. Card fallback action is Details.
10. Remove affects Collection membership only.
11. Search works for title and author;.
12. The selected minimal filter and sort work.
13. Empty and no-result states are distinct.
14. Search/filter/sort/scroll survive tab switches.
15. Existing local availability may decorate cards but does not block the page.
16. No new identity registry, download registry, or audiobook architecture is introduced.
17. Focused tests pass.
18. The compact isolated Lanista scenario passes with current evidence before claiming runtime validation.

## 14. Instructions for `brotherhood-writing-plans`

Use this guide as the approved design input.

Inspect at minimum:

```text
qml/TheatreWorld.qml
qml/LibraryPage.qml
qml/LibraryApi.js
qml/BiblioWorld.qml
existing Biblio Collection and Progress helpers
existing Biblio Details and Resume routes
existing shared poster/card components
docs/colosseum-lanista-verification.md
relevant current tests
```

The plan should be short and proportional.

Recommended slices:

1. inspect and map Theatre/Biblio routes and existing test seams;
2. add the small Biblio row projection;
3. add the retained Library tab/page;
4. wire existing actions and removal;
5. add minimal semantic names;
6. add focused tests;
7. run the compact isolated Lanista scenario.

Each slice should include:

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

Do not add prerequisite architecture unless repository inspection proves the feature cannot work without it.

## 15. Stop conditions

Return for review if the plan starts to require:

- a universal library abstraction;
- a new persisted identity model;
- bulk Progress migration;
- a unified download registry;
- a new audiobook route;
- changes to Theatre's video domain;
- restructuring unrelated Biblio navigation;
- live user data;
- new Lanista commands not justified by the current ledger;
- more than the minimal Theatre-equivalent controls and actions.

## Agent Packet

### TASK

Use `brotherhood-writing-plans` to create the bounded implementation plan for Biblio's Theatre-equivalent Library tab.

### OBJECTIVE

Add one retained Biblio Library wall using existing Collection, Progress, routes, and shared presentation primitives, then prove the basic workflow through isolated Lanista.

### DECISIONS

- Theatre is the structural reference.
- One Collection entry becomes one card.
- Reliable existing Progress enables Resume.
- Uncertain matching falls back to Details.
- Downloads and audiobooks are optional decorations.
- Remove affects Collection only.
- Existing shelves remain.
- No new platform or migration work.

### NON-GOALS

Identity platform, download registry, audiobook playback architecture, universal library framework, file deletion, cloud sync, or broad refactoring.

### FIRST ACTION

Inspect Theatre's current Library implementation beside `BiblioWorld.qml`, map the existing Biblio action routes, and write the smallest execution plan that satisfies this guide.
