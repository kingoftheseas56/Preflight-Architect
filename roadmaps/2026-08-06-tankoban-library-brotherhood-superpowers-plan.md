# Tankoban Library — Brotherhood Superpowers Execution Plan

> **Destination:** Brotherhood execution agent working in `kingoftheseas56/Colosseum`  
> **Source plan:** `tankoban-library-tracer-bullet-tickets-v2 (1).md`  
> **Workflow:** `brotherhood-writing-plans` → `brotherhood-executing-plans`  
> **Current repository inspected:** `master` at `236021a28e5080102538d3ec7d1b9373416d231a`  
> **Product baseline:** TB-001 is **reported completed by Hemanth** and is intentionally not re-planned here. Its exact implementation branch and commit remain to be identified before execution.  
> **Plan status:** Reviewed Brotherhood conversion. TB-002 through TB-005 are ordered and specified. Runtime execution remains unperformed.

---

## Read First

Before changing code, the executor must read:

1. This plan at the approved revision.
2. `docs/colosseum-lanista-verification.md` from the branch being executed.
3. The supplied `brotherhood-writing-plans` and `brotherhood-executing-plans` skills.
4. The actual TB-001 implementation commit, including its Library page, row module, tests, and automation names.
5. The existing Collection, Progress, LocalDownloads, Tankoban routing, manga-series, comic-series, and reader code touched by the slice being executed.

The capability ledger is authoritative. If it differs from this plan, stop with **Plan contradicted** and revise the plan before substituting another verification method.

---

## 1. Objective

Complete the retained Tankoban **Library** tab so one mixed manga/comic wall supports:

- chapter, volume, and comic reading progress;
- resume through the most recently touched reading lane;
- details fallback when no progress exists;
- canonical `seriesId`  identity for new manga saves;
- compatibility with title-keyed legacy manga saves;
- live downloaded state;
- Manga / Comics filters;
- In Progress / Not Started / Downloaded filters;
- title search;
- Last Read / Added / A–Z sorting;
- Resume / Details / Remove card actions;
- distinct empty-Collection and no-match states;
- retention of search, filters, sort, and scroll position across tab switches.

The existing **Your Collection** rows in the Manga and Comics tabs remain unchanged.

---

## 2. Scope Decision

### Excluded from this plan

**TB-001 — Retained Mixed Library Wall and Details Routing** is already reported complete.

Do not reimplement it. Before beginning the remaining work, identify and record:

- branch;
- commit SHA;
- actual new page/module/test paths;
- current tab and delegate automation names;
- evidence already produced for TB-001;
- any differences between its implementation and the source plan.

If TB-001 cannot be located, or its delivered contract materially differs from the assumptions below, report **Plan contradicted** rather than recreating it from memory.

### Remaining order

```text
Confirm TB-001 revision
        ↓
BP-001  Isolated Collection/Progress fixtures for Lanista sessions
        ↓
DB-002  Manga chapter resume + canonical save + local legacy re-file
        ↓
TB-003  Most-recent manga lane + comic resume/details compatibility
        ↓
TB-004  Live downloaded state
        ↓
TB-005  Search/filters/sorts + card menu/remove + retained browse state
        ↓
CLOSEOUT  Full suite, runtime matrix, evidence package, human visual gate
```

Execution is strictly sequential. TB-002 through TB-005 share the Library row module and page and must not be developed concurrently in the same working tree.

---

## 3. Approved Design Summary

The source plan’s product and architecture decisions remain authoritative:

- one retained mixed Library wall;
- one fetch-free pure row-derivation module;
- existing Continue routing for started entries;
- existing Collection Details routing for unstarted entries and explicit Details;
- exact winning Progress record preserved as `resumeTarget`;
- one global Progress revision;
- direct LocalDownloads aggregate-series join;
- canonical `seriesId` for new manga saves;
- opportunistic one-entry legacy manga re-file from `MangaSeries.qml`;
- canonical add and presence confirmation before legacy removal;
- preserved `addedAt`;
- no shared `LibraryButton.qml` alias mechanism;
- no bulk migration;
- no network refresh, release detection, completion model, or mark-read action;
- original Collection identity retained for Details and Remove;
- no title fallback for comics;
- deterministic, non-mutating filtering and sorting.

---

## 4. Evidence Calibration

### Confirmed on current `master`

- The current inspected `master` revision is `236021a28e5080102538d3ec7d1b9373416d231a`.
- Current `master` still has the pre-TB-001 Tandoban tab structure; the reported TB-001 implementation is therefore on another revision or has not yet reached current `master`.
- `MangaSeries.qml` currently builds manga Collection entries with the display title as `id`.
- Collection and Progress expose exact stores and revision-driven reads.
- Collection add can preserve a supplied nonzero `addedAt`.
- Collection and Progress production stores use explicit QSettings identity, while test constructors can use explicit INI paths.
- LocalDownloads is file-backed, exposes Tankoban series aggregation, and has a revision.
- The current Lanista ledger provides isolated tagged sessions, UI action commands, strict property waits, QML property reads, screenshots, and session evidence manifests.
- The current ledger also states that registry-backed QSettings are not seeded by the existing `--seed` path.

### Reported, not independently verified here

- TB-001 is implemented.
- Its mixed wall, details routes, empty state, retained page instance, and scroll retention behave correctly.
- Its tests and automation surfaces are present.

### Working inference

Because Collection and Progress use QSettings while the current session seed path covers file-backed stores, the remaining runtime scenarios cannot safely rely on deterministic Collection/Progress fixtures until an isolated test-store seam is added or an equivalent existing seam is demonstrated.

This inference creates **BP-001**. If the TB-001 branch already includes a proven isolated Collection/Progress fixture mechanism, replace BP-001 with that evidence and update this plan before execution.

---

## 5. Verification Surface Contract

The executor must first inspect TB-001 and reuse equivalent stable names where they already exist. Where no equivalent exists, add the following read-only automation surface alongside the slice that needs it. These names are testability contracts, not alternate product state owners.

### Library shell

- `tandobanTab_library` — Library tab action.
- `tandobanLibraryPage` — retained Library root.
- Root read-only properties:
  - `allRowCount`
  - `visibleRowCount`
  - `queryText`
  - `typeFilter`
  - `stateFilter`
  - `sortMode`
  - `firstVisibleEntryId`
  - `menuOpen`
  - `menuEntryId`
  - `collectionRevisionSeen`
  - `progressRevisionSeen`
  - `downloadsRevisionSeen`

### Cards

Each fixture-targeted card must have a stable object name derived from its exact fixture entry ID:

```text
tankobanLibraryCard_<fixture-safe-entry-id>
```

The card must expose read-only properties that reflect its normalized row:

- `entryId`
- `mediaType`
- `rowState`
- `resumeLane`
- `downloaded`
- `lastActivityAt`
- `addedAt`

Test fixture IDs used for direct card targeting must contain only safe ASCII identifier characters. Source-prefixed comic identity remains stored and probed in `entryId`; it must not be rewritten merely for automation.

### Manga series identity

The manga series page must expose or retain equivalent properties:

- resolved `seriesId`;
- `identityReady`;
- `legacyRefileState` with deterministic values such as `idle`, `pending`, `complete`, or `failed`;
- current Collection entry ID;
- Collection button checked/enabled state.

### Destination surfaces

Resume and Details scenarios need stable names and read-only identity properties on the actual destination surfaces. Reuse existing names if present; otherwise add the smallest equivalent contract:

- active manga reader: current Progress `kind`, series ID, and resume chapter/volume identifier;
- active comic reader: current Progress `kind`, series ID, and resume identifier;
- manga details: resolved series ID and visible state;
- comic details: exact source-prefixed Collection ID and visible state.

Do not create a synthetic “route passed” flag that can turn green without the real destination becoming active.

### Browse controls and menu

By TB-005, provide stable names for:

- search input;
- type filter choices;
- state filter choices;
- sort choices;
- card menu trigger;
- Resume;
- Details;
- Remove;
- removal confirmation, if the selected interaction design uses one;
- empty-Collection state;
- no-match state.

### Completion signals

Use only deterministic state:

- `ui-wait-for` on strict property equality;
- QML property values read with `qml-get`;
- actual destination visibility and identity;
- row counts and menu state;
- LocalDownloads mutation completion reflected through the real store revision and final row state.

No scenario may use an arbitrary sleep.

---

## 6. Shared Safety and Evidence Rules

Every user-visible slice must:

1. boot a disposable `lanista session run` instance;
2. use a unique pipe and tagged AppData/cache root;
3. never Drive the daily app or default pipe;
4. never mutate live Collection, Progress, Downloads, settings, or cache;
5. capture a pre-change baseline before implementation;
6. run focused tests;
7. replay the exact planned runtime scenario;
8. wait on named completion signals;
9. inspect semantic state and pixels;
10. re-exercise named regressions;
11. preserve the session manifest, logs, probe outputs, and grabs;
12. report only the status supported by current evidence.

A user-visible slice closes only as **Runtime-validated*. Green focused tests alone are **Test-reported*.

Human aesthetic judgment remains Hemanth’s gate. Runtime evidence can prove controls, identities, state transitions, and layout presence; it cannot declare that spacing, warmth, hierarchy, or overall finish “looks right.”

---

# BP-001 — Isolated Collection and Progress Fixtures

### Slice BP-001: Disposable Tankoban persistent-state fixtures

**Purpose:**  
Give every remaining Library slice deterministic Collection and Progress fixtures inside disposable Lanista sessions without reading or mutating the daily app’s QSettings.

### Dependencies
*The exact TB-001 implementation revision must be identified. Read the fresh capability ledger and confirm the current session runner behavior before changing it.*

**Implementation guidance:**  
Add the smallest tagged-session-only persistent-store seam:

1. Extend `lanista session run --seed <dir>` or its existing launch preparation so a fixture may include explicit Collection and Progress INI files.
2. Place those files beneath the tagged session’s isolated data root.
3. Pass one test-session store-root value to the launched app.
4. In `main.cpp`, use the existing explicit INI constructors for Collection and Progress only when:
   - the test-store root is present;
   - a nonempty `COLOSSEUM_APPDATA_TAG` is present;
   - the resolved fixture paths are descendants of the tagged session root.
5. Otherwise preserve the existing production constructors and QSettings identity exactly.
6. Record the resolved Collection and Progress test paths in the session manifest.
7. Refuse an out-of-root path rather than falling back to production QSettings.
8. Add fixture examples covering:
   - canonical manga;
   - legacy title-keyed manga;
   - source-prefixed comics;
   - chapter, volume, and comic Progress;
   - deterministic timestamps and `addedAt`.
9. Update `docs/colosseum-lanista-verification.md` in the same change so the ledger states exactly what tagged fixture seeding now covers and what it still does not cover.

Do not add a generic production Write command or make the daily QSettings domain configurable in ordinary launches.

**Behavior to preserve:**  
Normal app launches keep the existing Collection and Progress storage location and behavior. Existing isolated AppData/cache handling, unique-pipe behavior, LocalDownloads seeding, default gate states, and current tests remain unchanged.

**Baseline:**  
Before implementation:

- run the current session runner with a seed tree containing representative Collection and Progress fixture files;
- preserve the manifest and QML evidence showing those rows are not deterministically loaded through the current path;
- record the current production QSettings identities from source;
- do not Drive or mutate the daily app to demonstrate the gap.

The baseline demonstrates a missing isolated fixture seam, not a product failure.

**Focused tests:**  

- production launch selects existing production constructors when no test-store root is supplied;
- tagged launch selects explicit INI constructors;
- untagged launch with a test-store root is rejected or ignores it without touching the supplied files;
- path traversal or an out-of-session path is rejected;
- Collection fixture loads exact IDs and `addedAt`;
- Progress fixture loads exact kinds, IDs, resume data, and timestamps;
- mutations remain inside the fixture INIs;
- session manifest records the resolved fixture paths;
- existing CollectionStore, ProgressStore, and session-runner tests remain green.

### Lanista actions

1. Run `lanista session run` with:
   - the current built executable;
   - `--tag` for a unique disposable session;
   - `--seed` pointing at the BP-001 fixture tree;
   - a scenario that waits for `bootSplash.visible == false`.
2. Use `ping` and `get-state` to preserve capability and isolation evidence.
3. Navigate with `ui-click` to Tankoban and the retained Library tab.
4. Use `ui-wait-for` on `tankobanLibraryPage.visible == true`.
5. Use `qml-get` to read the seeded row count and representative card identity.
6. End the session through the runner so its manifest and logs are finalized.

**Completion signal:**  
`tandobanLibraryPage.allRowCount` equals the fixture’s expected Collection count, and representative card properties equal fixture values. The session manifest records Collection and Progress paths under the tagged session root.

### State / events / probes

- `get-state.appDataRoot` and `get-state.cacheRoot` contain the session tag;
- the app PID matches the session runner’s PID;
- Collection fixture IDs and `addedAt` match exactly;
- Progress fixture `kind`, ID, resume payload, and `updatedAt` match exactly;
- the production QSettings domain is not opened or modified by the tagged fixture run;
- no new typed event claim is made; the current bridge has no typed event plane.

**Visual evidence:**  
One Library grab showing representative seeded rows is sufficient as a fixture smoke exhibit. It is not the pass condition.

**Regression paths:**  

- ordinary app launch without test fixture configuration;
- current `session run` self-smoke scenario;
- LocalDownloads fixture seeding;
- session startup failure and cleanup;
- malformed seed tree;
- session root containing spaces.

### Evidence artifacts
*Preserve the BP-001 baseline and post-change session directories under the runner’s normal `artifacts/lanista-sessions/<id>/` location, including manifests, stdout, stderr, QML probe output, and the fixture smoke grab. Preserve focused-test output beside the implementation report.*

**Bridge status:** not applicable

**Completion criterion:*  
BP-001 is complete when focused tests prove production storage is unchanged and tagged fixture storage is contained, the isolated session loads deterministic Collection and Progress rows, the manifest proves the resolved paths are inside the taggd root, and the ledger is updated. This internal prerequisite does not claim a user-visible feature status.

**Stop conditions:**

- the seam can select production QSettings from a tagged fixture run;
- an out-of-root path can be accepted;
- the executor cannot prove the daily store remained untouched;
- implementation requires a generic write bridge;
- the current TB-001 branch already provides a different proven seam.

---

# TB-002 — Manga Chapter Resume and Opportunistic Legacy Re-file

### Slice TB-002: Canonical manga identity, chapter resume, and silent one-entry re-file

**Purpose:**  
A saved manga with chapter progress displays as In Progress and opens the recorded chapter; new saves use `seriesId`, while visiting a legacy title-keyed manga safely re-files that one save without changing Added order or creating a duplicate.

**Dependencies:*  
TB-001 implementation revision confirmed. BP-001 complete. Use the actual TB-001 module/page/test paths discovered on that revision.

**Implementation guidance:**  

Pure derivation:

- accept chapter-lane Progress records (`kind = "manga"`);
- match canonical Collection ID to Progress ID first;
- permit normalized-title fallback only for a legacy title-keyed manga entry;
- set `state = "inProgress"`, progress, exact `resumeTarget`, `resumeLane = "manga"`, and `lastActivityAt`;
- if canonical and legacy entries resolve to the same exact Progress identity, emit one canonical row and suppress the legacy duplicate;
- never mutate the input arrays.

Manga identity:

- change `MangaSeries.collectionEntry().id` to the resolved nonempty `seriesId`;
- prevent an empty-ID add;
- implement one re-file attempt per resolved identity in `MangaSeries.qml`;
- find only a legacy manga entry whose exact ID equals the current display title and differs from `seriesId`;
- add or update the canonical entry first with the legacy `addedAt`;
- confirm canonical presence;
- remove the exact legacy ID only after confirmation;
- if both entries already exist for the same title, preserve the older valid `addedAt` before removing the duplicate;
- gate the Collection control until identity resolution and the re-file attempt finish;
- leave `LibraryButton.qml` unchanged;
- perform no bulk migration.

Routing:

- started card activation sends the exact winning Progress record through `continueResumeRequested`;
- unstarted card activation continues to send the original Collection entry through `collectionOpenRequested`;
- do not add a Theatre resume path or a new Main router unless the existing signal is proven insufficient.

**Behavior to preserve:**  

- TB-001 mixed wall, empty state, Details routes, retained page instance, and scroll retention;
- existing Manga and Comics tabs and their Collection rows;
- existing chapter reader Continue behavior;
- exact comic Collection identities;
- shared `LibraryButton.qml` contract;
- original Added order for unrelated entries.

### Baseline
Using BP-001 fixtures on the unmodified TB-001 revision:

1. Seed:
   - one canonical manga Collection entry with chapter Progress;
   - one title-keyed legacy manga with chapter Progress matchable by normalized title;
   - one canonical/legacy duplicate pair;
   - deterministic `addedAt` values.
2. Boot an isolated session and enter Library.
3. Preserve:
   - representative card row states and resume lanes;
   - the legacy row identity;
   - destination reached by activating the chapter-progress card;
   - the legacy manga page’s current Collection identity behavior.
4. The expected pre-TB-002 baseline is that chapter matching, canonical save identity, or the local re-file contract is absent or incomplete. If TB-001 already implements any of these, record the contradiction and revise this slice rather than overwriting it.

**Focused tests:**  

Pure module:

- canonical chapter ID match;
- legacy normalized-title fallback;
- canonical match outranks fallback;
- unrelated title collision does not match a canonical entry;
- unmatched row remains Not Started;
- duplicate canonical/legacy rows collapse to one canonical row;
- exact Progress object, including nested resume data, is preserved;
- input arrays remain unchanged.

Manga series and stores:

- `collectionEntry()` uses resolved `seriesId`;
- empty `seriesId` cannot be saved;
- re-file preserves legacy `addedAt`;
- canonical add occurs before legacy removal;
- removal does not happen when canonical confirmation fails;
- re-file runs once per resolved identity;
- canonical-existing case preserves the older applicable Added date;
- page Collection state becomes checked after re-file;
- shared `LibraryButton.qml` public contract remains unchanged;
- no bulk migration path exists.

Page/routing harness:

- started activation emits the exact Progress record;
- unstarted activation emits the original Collection entry to Details.

### Lanista actions

Scenario A — Shapter resume:

1. Run a disposable seeded session with Drive enabled.
2. `ui-wait-for` `bootSplash.visible == false`.
3. `ui-click` `modePill_Tandoban`.
4. `ui-click` `tankobanTab_library`.
5. `ui-wait-for` `tandobanLibraryPage.visible == true`.
6. `qml-get` the canonical fixture card’s `rowState`, `resumeLane`, and entryId`.
7. `ui-click` that named card.
8. `ui-wait-for` the actual manga reader root `visible == true`.
9. `qml-get` its current Progress kind, series ID, and chapter resume identifier.
10. Capture the reader.

Scenario B — Legacy re-file:

1. Boot a fresh disposable session with the legacy fixture.
2. Enter Library and read the legacy card’s `entryId` and `addedAt`.
3. Activate its Details route.
4. `ui-wait-for` the manga series page `visible == true`.
5. `ui-wait-for` `identityReady == true`.
6. `ui-wait-for` `legacyRefileState == "complete"`.
7. `qml-get` resolved `seriesId`, current Collection entry ID, button checked state, and button enabled state.
8. Navigate Back using the existing named Back action.
9. `ui-wait-for` `tandobanLibraryPage.visible == true`.
10. `qml-get` `allRowCount`, the canonical card’s `entryId`, and `addedAt`.
11. Open the series page again and confirm the row count and identity remain unchanged.

Scenario C — Canonical confirmation failure:

- exercise this in the focused harness, not by corrupting the running app;
- the runtime scenario must not manufacture store failure through an unavailable Write command.

**Completion signal:**  

- chapter scenario: actual reader surface is visible and its Progress identity equals the fixture’s exact chapter Progress record;
- legacy scenario: `legacyRefileState == "complete"`, current Collection ID equals resolved `seriesId`, Library row count remains the expected single-row count, and `addedAt` equals the original legacy value;
- no step uses a sleep.

**State / events / probes:**  

Expected post-change values:

- canonical card: `rowState == "inProgress"`;
- canonical card: `resumeLane == "manga"`;
- card `entryId` remains the canonical Collection ID;
- reader Progress `kind == "manga"`;
- reader series/chapter identity equals the seeded Progress record;
- legacy page resolved `seriesId` is nonempty;
- legacy re-file state is complete;
- Collection control is checked and enabled after completion;
- returned Library row uses canonical ID;
- returned Library row retains legacy `addedAt`;
- no second row exists for the same manga.

Use QML properties and actual store-derived row state. Do not claim typed route or migration events; the current ledger does not provide them.

**Visual evidence:**  

- before grab: legacy title-keyed row visible once;
- after resume grab: real manga reader at the expected chapter;
- series-page grab after re-file: Collection control visibly In Library with no false-unsaved flicker in the captured completed state;
- returned-Library grab: one canonical row in the same Added position.

Pixels supplement the state proof. Hemanth’s eyes decide whether the transition appears visually silent and appropriately finished.

### Regression paths:**  

- unstarted manga still opens Details;
- remove then add again creates only a canonical `seriesId` entry;
- navigate Library → Manga → Library and confirm retained state;
- chapter Continue from existing non-Library surfaces;
- manga download initiation still adds the canonical Collection entry;
- unrelated legacy title collision remains a separate row;
- existing comic Details routes remain unchanged.

### Evidence artifacts
*Create proposed scenarios under the repository’s established Lanista scenario location, using names equivalent to:*

- `tb002_chapter_resume.jsonk;
- `tb002_legacy_refile.json`.

Preserve each run’s manifest, stdout, stderr, QML probe output, and grabs under its session artifact directory. Preserve focused-test output and a short slice report that cites exact artifact paths.

**Bridge status:** available

This status is conditional on BP-001 and the named QML automation properties landing. All runtime actions use currently available session-runner, click, wait, QML-read,, and grab capabilities.

**Completion criterion:**  
TB-002 is **Runtime-validated** only when focused tests are green, both runtime scenarios pass against the committed tree, exact reader identity is proven, the legacy row is re-filed once with preserved `addedAt`, duplicate count remains zero, regressions pass, evidence is preserved, and Hemanth has the visual exhibits needed to judge the transition. Any lesser evidence must be reported with the Brotherhood status vocabulary.

**Stop conditions:**

- resolved `seriesId` differs from the reader’s Progress identity;
- a legacy title entry cannot be distinguished safely from another manga;
- canonical upsert cannot preserve `addedAt`;
- the page can remove legacy state before canonical confirmation;
- safe runtime fixture isolation is not proven;
- destination identity cannot be read from the real reader.

---

# TB-003 — Most-Recent Manga Lane and Comics End to End

### Slice TB-003: Latest manga lane and exact comic resume

**Purpose:**  
A manga resumes the newer of its chapter and volume records, comics resume their exact comic record, and unstarted rows continue to open the correct Details surface without losing provider identity.

### Dependencies
*TB-002 must be Runtime-validated. BP-001 fixtures must support chapter, volume, comic, and unstarted cases.*

**Implementation guidance:**  

 - add volume-lane Progress input (`kind = "tandoban"`);
- add comic Progress input (`kind = "comic"`);
- evaluate manga chapter and volume matches independently;
- select the larger `updatedAt`;
- define and test one deterministic equal-timestamp tie-breaker;
- preserve the exact winning Progress record as `resumeTarget`;
- expose `resumeLane` as `manga`, `tankoban`, or `comic`;
- use exact ID match only for comics;
- do not use comic title fallback;
- keep Collection entry and Progress target separate:
  - Collection entry owns Details and Remove;
  - Progress record owns Resume;
- preserve exact `gc:`, `gcd:`, and `locg:` Collection identities and payloads;
- make no network request during arbitration;
- introduce no release, caught-up, or completion state.

**Behavior to preserve:**  

 - TB-002 canonical manga identity, chapter resume, legacy fallback, and local re-file;
- TB-001 Details routes and retained state;
- exact source-specific comic Details behavior;
- existing reader resume behavior outside the Library;
- no title-based comic matching.

### Baseline
On the committed TB-002 revision, seed and preserve evidence for:

- one manga with both chapter and volume Progress where volume is newer;
- one manga where chapter is newer;
- one equal-timestamp manga;
- one exact-ID comic;
- one comic title collision with a different ID;
- one unstarted manga and comic.

Record the current row `resumeLane`, activation destination, and exact destination identity. The expected pre-TB-003 baseline is that volume/comic arbitration is absent or incomplete. If it is already present, report **Plan contradicted** and reconcile ownership before proceeding.

### Focused tests

Pure module:

- chapter only;
- volume only;
- chapter newer;
- volume newer;
- equal timestamps use the chosen deterministic tie-breaker;
- malformed or missing `updatedAt` is handled deterministically;
- exact winning object retains `kind`, ID, progress, and nested resume payload;
- comic exact-ID match;
- comic title collision does not match;
- no-progress row remains Not Started;
- Collection entry remains separate from resume target;
- no input mutation.

Page/routing harness:

- started manga emits winning Progress object;
- started comic emits exact comic Progress object;
- unstarted manga and comic emit original Collection entry to Details.

### Lanista actions

Scenario A — Lane arbitration:

1. Boot a disposable fixture session and enter Library.
2. Wait for the Library page.
3. Read the volume-newer card’s `resumeLane`; expect `tankoban`.
4. Activate it.
5. Wait for the actual manga reader.
6. Read reader Progress kind, series ID, and volume resume identifier.
7. Return to Library using the real Back path.
8. Wait for the Library page and activate the chapter-newer card.
9. Wait for the actual reader.
10. Read reader Progress kind, series ID, and chapter identifier.
11. In a separate equal-timestamp fixture run, read `resumeLane` and prove the documented tie-breaker.

Scenario B — Comics and Details:

1. Boot a fresh disposable fixture session and enter Library.
2. Read the exact comic card’s `entryId`, `rowState`, and `resumeLane`.
3. Activate it.
4. Wait for the actual comic reader.
5. Read its Progress kind and exact source-prefixed series ID.
6. Return to Library.
7. Activate the title-collision comic and prove it opens Details rather than inheriting the other comic’s Progress.
8. Activate each unstarted source fixture (`gc:`, `gcd:`, and `locg:` where representative fixtures are supported) and wait for the actual Details surface.
9. Read the Details surface’s exact Collection ID.

**Completion signal:**  

 - volume-newer card resolves to `resumeLane == "tankoban"` and the real reader reports `kind == "tandoban"`;
- chapter-newer card resolves to `resumeLane == "manga"` and the real reader reports `kind == "manga"`;
- comic card resolves to `resumeLane == "comic"` and the real comic reader reports the exact source-prefixed ID;
- unstarted and collision cards activate actual Details surfaces with their original Collection IDs.

**State / events / probes:**  

Read and preserve:

- each fixture card’s `entryId`, `rowState`, `resumeLane`, and `lastActivityAt`;
- actual reader Progress kind and ID;
- actual resume chapter/volume/comic identifier;
- Details surface Collection ID;
- retained Library `firstVisibleEntryId` before leaving and after returning;
- no network-derived state is needed to choose the target.

No typed event assertion is allowed because the current bridge does not expose typed route events.

**Visual evidence:**  

- Library grab showing distinct progress presentation for chapter, volume, and comic rows;
- manga reader grab for the newer volume case;
- manga reader grab for the newer chapter case;
- comic reader grab;
- unstarted comic Details grab retaining provider identity.

Hemanth’s eyes remain the aesthetic gate for progress legibilily and mixed-wall clarity.

**Regression paths:**  

- chapter-only manga;
- volume-only manga;
- exact timestamp tie;
- comic title collision;
- Back to retained Library position;
- Details then Back;
- legacy re-filed manga;
- existing Continue surfaces outside Library;
- all supported comic Details source paths;
- restart the same deterministic fixture session and confirm arbitration remains stable.

**Evidence artifacts:**  
Create proposed scenarios equivalent to:

- `tb003_manga_lane_arbitration.json`;
- `tb003_comic_resume_and_details.json`.

Preserve manifests, logs, QML outputs, and grabs in the session directories. Attach focused-test output and a compact identity matrix mapping fixture Collection IDs to expected Progress and destination IDs.

**Bridge status:** available

Conditional on BP-001 and readable identity properties on the real reader/details surfaces. If the actual destination cannot expose its identity without a new typed domain probe, stop and mark **Bridge blocked** rather than substituting a screenshot.

**Completion criterion:**  
TB-003 is **Runtime-validated** only when focused tests pass, the newer lane is proven in both directions, the tie is deterministic, comic resume uses exact ID, collision and unstarted entries open correct Details, Back preserves the retained Library position, all artifacts are preserved, and no provider identity or routing regression is observed.

### Stop conditions:

- comic Progress ID differs from its Collection identity with no documented translation;
- a supported provider opens Details but cannot resume through the existing reader;
- chapter and volume lanes use incompatible series identities;
- actual destination identity is unobservable;
- runtime results disagree with the plan’s routing assumptions.

---

# TB-004 — Live Downloaded State

### Slice TB-004: Download badge and revision-driven live update

**Purpose:**  
A Library card shows downloaded state when local manga or comic content exists, and the badge clears in place when the final local item is removed without reopening the tab.

### Dependencies
*TB-003 must be Runtime-validated. BP-001 must provide Collection fixtures. The existing file-backed LocalDownloads seed and mutation path must be confirmed against the current ledger and source.*

**Implementation guidance:**  

 - gather `LocalDownloads.series("tankoban")`;
- pass plain aggregate rows into the pure module;
- join:
  - canonical manga by `manga:<seriesId>`;
  - comics by `comic:<seriesId>`;
  - unvisited legacy title-keyed manga by the bounded normalized-title fallback;
- treat chapter and volume downloads as one manga series boolean;
- bind `LocalDownloads.revision` explicitly;
- add `downloaded` to normalized rows and render a separate card badge;
- implement model-level Downloaded filtering now; its visible control lands in TB-005;
- do not use `CollectionBackfill.entryForTankobanSeries()` as the sole join;
- do not expand every `LocalDownloads.items()` row unless an aggregate fixture demonstrates that `series()` is insufficient;
- add stable automation names to the existing Downloads removal controls for the fixture item if equivalent names are absent;
- use the actual LocalDownloads remove flow, including its confirmation UI, rather than a test-only mutation shortcut.

**Behavior to preserve:**  

- all TB-002/TB-003 identity, resume, Details, and retained-state behavior;
- chapter and volume remain distinct resume lanes;
- download state remains orthogonal to reading state;
- failed or in-flight work does not count unless the aggregate store reports landed content;
- existing Downloads page behavior and confirmation semantics;
- no polling or network request on Library open.

### Baseline
On the committed TB-003 revision:

1. seed Collection/Progress fixtures plus file-backed LocalDownloads data for:
   - manga chapter only;
  - manga volume only;
  - chapter and volume together;
  - exact comic;
  - legacy title-keyed manga;
  - one final removable local item.
2. Enter Library and record card `downloaded` values and visible badges.
3. Remove the final fixture item through the existing Downloads UI and return to Library.
4. Preserve evidence that the pre-TB-004 Library does not derive or react to downloaded state.

Do not mutate live downloads.

**Focused tests:**  

Pure module:

- canonical manga chapter key marks downloaded;
- canonical manga volume key marks the same row downloaded;
- chapter plus volume remains one boolean;
- exact comic key marks only its row;
- comic title collision does not match;
- bounded legacy title fallback;
- failed/in-flight aggregate state is excluded according to the actual LocalDownloads contract;
- Downloaded model filter returns only downloaded rows;
- input arrays remain unchanged.

Page/store integration:

- `LocalDownloads.revision` alone recomputes rows;
- adding landed content sets badge;
- removing final local item clears badge;
- unrelated Collection/Progress revisions are not required;
- page names the revision dependency explicitly;
- existing LocalDownloads tests remain green.

### Lanista actions

Scenario A — Seeded badges:

1. Boot a disposable session with Collection/Progress fixtures and seeded file-backed LocalDownloads.
2. Enter Library and wait for the page.
3. Read `downloadsRevisionSeen`.
4. Read each targeted card’s `downloaded` property.
5. Capture the wall showing manga and comic badges.

Scenario B — Live final-item removal:

1. In a fresh isolated fixture session, enter Library.
2. Wait for the targeted card `downloaded == true`.
3. Navigate to the existing Downloads surface using named actions.
4. Wait for the Tankoban download row to be visible.
5. Activate its named Delete local copy action.
6. If confirmation exists, activate the named confirmation action.
7. Wait for the real Downloads row/item state to indicate removal complete.
8. Return to the already-retained Library page.
9. Wait for the same card `downloaded == false`.
10. Read `downloadsRevisionSeen` and the card state.
11. Capture the wall after badge removal.

All actions must use available `ui-click`, `ui-wait-for`, `qml-get`, and grab behavior.

**Completion signal:**  

 - seeded scenario: exact fixture cards report `downloaded == true` or `false` as expected;
- removal scenario: the real Downloads surface reports the final item removed, then the retained Library card reaches `downloaded == false`;
- the Library page instance is not recreated to obtain the update.

**State / events / probes:**  

Preserve:

- LocalDownloads aggregate fixture keys;
- initial and final `downloadsRevisionSeen`;
- each card’s exact `entryId` and `downloaded`;
- retained Library page identity or retained-state properties before and after navigation;
- Downloads row/item completion state;
- no Collection or Progress mutation is required for badge clearance.

Do not claim a typed download event; use the actual revision-derived state because typed events are unavailable.

**Visual evidence:**  

- before grab with chapter/volume manga and comic badges;
- Downloads confirmation/removal grab;
- after grab with final-item badge cleared while unrelated card state remains unchanged;
- narrow and typical-width Library grabs to show badge fit.

Hemanth decides whether the badge is visually clear and appropriately integrated.

**Regression paths:**  

- chapter-only download;
- volume-only download;
- both lanes;
- exact comic;
- legacy title fallback;
- failed/in-flight job;
- final item removed;
- leave and return to Library;
- restart from the deterministic fixture;
- progress Resume and Details after badge recomputation;
- existing Downloads page removal behavior.

**Evidence artifacts:**  
Create proposed scenarios equivalent to:

- `tb004_seeded_download_badges.json`;
- `tb004_live_final_item_removal.json`.

Preserve session manifests, logs, QML-value outputs, and before/after grabs. Attach pure-join fixtures and focused-test output.

### Bridge status: available

This is conditional on the existing file-backed LocalDownloads fixture being seedable and its real removal controls being reachable in the first root window. If the current removal UI is an own-window popup or the aggregate fixture cannot be seeded, report **Bridge blocked** and add the smallest prerequisite; do not mutate files behind the running store as a substitute.

**Completion criterion:**  
TB-004 is **Runtime-validated** only when all identity joins pass focused tests, seeded badges match actual aggregate data, final-item removal clears the badge in the retained page through `LocalDownloads.revision`, regressions pass, evidence is preserved, and the visual package is ready for Hemanth’s judgment.

**Stop conditions:**

- `LocalDownloads.series()` omits a landed lane;
- a title collision marks the wrong legacy row;
- the page updates only after unrelated store changes;
- runtime verification would require direct file mutation behind the running app;
- required confirmation controls live in an unreachable secondary window;
- the plan would need polling or a sleep.

---

# TB-005 — Browse Controls, Card Menu, Safe Removal, and Surface Completion

### Slice TB-005: Complete Library browsing and card management

**Purpose:**  
The user can search, filter, sort, resume, inspect Details, and remove exact Collection entries while the Library distinguishes empty from no-match state and preserves browse state across tab switches.

### Dependencies
*TB-004 must be Runtime-validated. The normalized row contract is frozen. BP-001 fixtures support deterministic mixed rows and exact removal verification.

**Implementation guidance:**  

Search and filters:

- query is trimmed, case-insensitive title substring;
- type filter: `all`, `manga`, `comic`;
- state filter: `all`, `inProgress`, `notStarted`, `downloaded`;
- filters compose with AND semantics.

Sorts:

- Last Read default:
  1. `lastActivityAt` descending;
  2. `addedAt` descending;
  3. normalized title ascending;
  4. Collection ID ascending;
- Added:
  1. `addedAt` descending;
  2. normalized title ascending;
  3. Collection ID ascending;
- A–Z:
  1. normalized title ascending;
  2. Collection ID ascending;
- every transform returns a new array.

Presentation:

- progress presentation uses the selected resume lane;
- downloaded remains a distinct badge;
- `allRows.length == 0` shows empty Collection;
- `allRows.length > 0 && visibleRows.length == 0` shows no matches;
- counts are optional and, if used, derive from the same normalized snapshot.

Card menu:

- exactly Resume, Details, Remove;
- Resume follows card activation:
  - started → exact `resumeTarget`;
  - unstarted → Details fallback;
- Details always emits the original Collection entry;
- Remove deletes exactly that row’s current Collection ID;
- legacy unvisited row removes the title-keyed ID;
- re-filed row removes canonical `seriesId`;
- menu closes when:
  - its row disappears;
  - search/filter/sort replaces its row;
  - the page hides;
  - viewport scroll or resize invalidates its placement;
- focus must not escape behind the menu.

Retained state:

- preserve query, type filter, state filter, sort, and GridView position through Library → another Tankoban tab → Library;
- use the retained TB-001 page; do not add a separate duplicate state store;
- expose `firstVisibleEntryId` as the stable semantic scroll-retention probe; retain actual `contentY` as the implementation state.

Explicit exclusions:

- airing/publication filters;
- watched toggles;
- new-release badges;
- finale or auto-completion logic;
- mark read, caught up, or completed actions;
- Theatre-specific vocabulary.

**Behavior to preserve:**  

 - every TB-001 through TB-004 route and identity;
- exact chapter/volume/comic resume;
- live downloaded state;
- existing Manga/Comics Collection rows;
- original Collection entry payloads;
- retained page lifetime;
- no shared component refactor unless the Tandoban-specific composition is proven impossible.

### Baseline
On the committed TB-004 revision, seed a deterministic wall containing:

- multiple manga and comics;
- started and unstarted rows;
- downloaded and non-downloaded rows;
- mixed title casing;
- leading/trailing-search test data;
- deterministic timestamps and Added dates;
- equal-sort ties;
- one legacy title-keyed row;
- one canonical row;
- enough rows to scroll.

Preserve the current wall, absence or incompleteness of browse controls/menu/no-match state, initial ordering, and retained scroll behavior. If TB-001 already delivered any final controls, report the overlap and reconcile before editing.

**Focused tests:**  

Pure module:

- trimmed case-insensitive search;
- each type filter;
- each state filter;
- combined AND filters;
- Downloaded as an orthogonal state filter;
- Last Read ordering and every tie-breaker;
- Added ordering and tie-breakers;
- A–Z ordering and ID tie-breaker;
- malformed timestamps handled deterministically;
- source arrays unmodified;
- empty Collection versus no matches;
- optional counts if displayed.

Page/menu harness:

- each control updates visible model;
- started Resume emits exact Progress;
- unstarted Resume emits original Collection entry to Details;
- Details never emits Resume;
- Remove sends exact selected Collection ID;
- legacy and canonical removal stay exact;
- menu closes on removal, hide, row replacement, scroll, and resize;
- keyboard focus and pointer activation;
- retained query/filter/sort state;
- retained scroll anchor or position;
- forbidden Theatre-only terms/actions absent.

Store coverage:

- removing a legacy row affects only exact title-keyed ID;
- removing a canonical row affects only exact `seriesId`;
- `Collection.revision` updates the wall.

### Lanista actions

Scenario A — Search, filters, sorts, and empty states:

1. Boot a disposable mixed fixture session and enter Library.
2. Wait for `allRowCount` and `visibleRowCount` to equal fixture values.
3. Activate the named search input with `ui-click`.
4. Enter a mixed-case query with `ui-text-input`.
5. Wait for `queryText` and expected `visibleRowCount`.
6. Activate each type and state filter choice in separate deterministic steps.
7. After each action, wait for the filter property and expected row count.
8. Clear search and filters through named controls.
9. Activate each sort mode.
10. After each sort, read `sortMode` and `firstVisibleEntryId`.
11. Apply a query that matches no rows.
12. Wait for the no-match state visible and empty-Collection state not visible.
13. In a separate empty Collection fixture run, wait for empty-Collection state visible and no-match state not visible.
14. Capture representative states.

Scenario B — Resume and Details menu actions:

1. Open the menu on a started row.
2. Wait for `menuOpen == true` and `menuEntryId` equal to that exact row.
3. Activate Resume.
4. Wait for the actual reader surface and read its exact Progress identity.
5. Return to Library.
6. Open the menu on an unstarted row.
7. Activate Resume.
8. Wait for the actual Details surface and read its exact Collection identity.
9. Return and activate explicit Details on a started row.
10. Prove it opens Details rather than the reader.

Scenario C — Exact removal:

1. Boot a fresh fixture session containing both legacy and canonical rows.
2. Open the legacy row menu.
3. Activate Remove and its named confirmation if present.
4. Wait for `menuOpen == false`.
5. Wait for `allRowCount` to decrement by one.
6. Prove the legacy card is absent through the page’s row model/count and that the canonical card remains.
7. Repeat in a fresh session for the canonical row.
8. Prove the canonical row is absent while the unrelated legacy row remains.
9. Do not rely on an unavailable generic absence assertion; use expected counts, exact surviving IDs, and fixture-store inspection after session completion.

Scenario D — Retained browse state and menu closure:

1. Boot the scroll fixture and enter Library.
2. Set a nonempty query, non-default type/state filters, and non-default sort.
3. Clear only the query if needed to retain enough rows for scrolling while leaving filter/sort state non-default.
4. Use `ui-scroll` by a fixed amount.
5. Read `firstVisibleEntryId` and confirm the scroll position is nonzero through an available property read or scenario numeric assertion.
6. Open a card menu.
7. Scroll and wait for `menuOpen == false`.
8. Open it again, resize through the established test harness/session mechanism if available, and wait for closure; if runtime resize is not available in the ledger, keep resize closure in the page harness and do not invent a command.
9. Switch to Discover, Manga, or Comics using named tab actions.
10. Wait for that tab’s actual visible state.
11. Return to Library.
12. Wait for `queryText`, filters, and sort to equal the values set earlier.
13. Read `firstVisibleEntryId`; expect the same retained anchor.
14. Capture the restored wall.

Scenario E — Keyboard path:

- use the currently available keypress/text-input commands on the named focusable controls;
- prove search entry, filter activation, menu opening, and one action without pointer-only assumptions;
- if the current bridge cannot target the required focus transition deterministically, mark only that subcase **Bridge blocked** and name the missing semantic-focus capability rather than using timing.

### Completion signal:**  

 - every control reaches the expected root property and row count;
- each sort reaches the expected first row ID;
- no-match and empty states are mutually correct for their fixtures;
- menu actions activate the actual reader/details destination with exact identity;
- removal closes the menu and produces the exact expected row count and surviving IDs;
- tab return restores query, filters, sort, and first visible row anchor;
- no completion depends on a sleep.

### State / events / probes:**  

Preserve after each scenario:

- `allRowCount`;
- `visibleRowCount`;
- `queryText`;
- `typeFilter`;
- `stateFilter`;
- `sortMode`;
- `firstVisibleEntryId`;
- `menuOpen`;
- `menuEntryId`;
- exact destination Progress or Collection identity;
- Collection revision before and after removal;
- exact surviving fixture IDs;
- retained page identity and scroll anchor.

Do not assert unavailable typed events or generic item absence. Use real model state and post-session fixture INI inspection for exact deletion.

**Visual evidence:**  
Create an eyes-on gallery containing:

- default Last Read wall;
- active search;
- each filter family;
- no matches;
- empty Collection;
- progress plus downloaded badges;
- menu near left, right, top, and bottom viewport edges where fixtures permit;
- menu after long title selection;
- narrow, typical, and wide windows;
- retained state after tab return;
- keyboard focus indication;
- before and after exact removal.

Automation proves state. Hemanth closes the aesthetic gate for spacing, hierarchy, menu placement, long-title handling, and overall finish.

### Regression paths:**  

- card tap versus menu Resume;
- unstarted Resume fallback;
- explicit Details on a started row;
- legacy exact-ID removal;
- canonical exact-ID removal;
- Collection revision update;
- menu closure on search/filter/sort;
- menu closure on page hide and scroll;
- resize closure in harness if runtime resize is unavailable;
- retained query/filter/sort/scroll;
- pointer and keyboard;
- narrow and wide layout;
- existing Manga and Comics Collection rows;
- chapter, volume, comic resume;
- live downloaded badge update;
- restart with deterministic fixture;
- forbidden Theatre-only actions remain absent.

**Evidence artifacts:**  
Create proposed scenarios equivalent to:

- `tb005_search_filters_sorts.json`;
- `tb005_menu_routes.json`;
- `tb005_exact_removal.json`;
- `tb005_retained_state.json`;
- `tb005_keyboard_path.json` where deterministically supported.

Preserve all session directories, manifests, logs, probe outputs, and grabs. Generate one eyes-on gallery or brief referencing the exact committed build and run IDs. Attach focused-test output and post-session fixture INI inspection for removal cases.

**Bridge status:** available

Runtime resize and complex focus traversal must be checked against the fresh ledger. If unavailable, their runtime subcases are **Bridge blocked** while the remaining slice may only close after the approved plan is revised or the smallest prerequisite lands. Do not silently replace them with a screenshot or harness-only claim.

**Completion criterion:**  
TB-005 is **Runtime-validated** only when focused tests pass, every supported control and menu route is proven in the running committed app, exact removal is proven for legacy and canonical IDs, empty/no-match states are distinct, retained state is proven semantically, regressions pass, evidence is preserved, and Hemanth approves the eyes-on surface. If any required runtime subcase is bridge blocked, the slice remains **Bridge blocked** rather than partially closed.

### Stop conditions:

- shared controls require Theatre-specific values;
- the selected card cannot present progress/download state without unrelated shared refactoring;
- removal requires broad title-based deletion;
- menu focus escapes behind the overlay;
- exact post-removal identity cannot be proved safely;
- state retention depends on a recreated page;
- verification requires an invented bridge command, arbitrary sleep, or live data.

---

# CLOSEOUT GATE — Not an Implementation Slice

Run only after BP-001 is complete and TB-002 through TB-005 have each been reported with Brotherhood status.

## Automated gates

Inspect and run the current equivalents of:

- TB-001’s actual Tandoban Library API harness;
- TB-001’s actual Tankoban Library page harness;
- aggregate Tandoban Library runner;
- Tandoban tab contract tests;
- Collection store tests;
- Progress store tests;
- relevant LocalDownloads tests;
- existing Theatre Library regressions;
- normal Colosseum build target;
- all new BP-001 and TB-002 through TB-005 focused tests.

Do not assume the source plan’s proposed filenames match the delivered TB-001 branch. Record actual paths.

## Runtime suite

Replay the preserved deterministic scenarios from each slice against the final committed tree, not merely the intermediate slice commits.

Required matrix:

| Dimension | Cases |
|---|---|
| Entry identity | canonical manga, title-keyed legacy manga, re-filed manga, GetComics, GCD, LOGG |
| Reading state | unstarted, chapter, volume, both lanes, comic |
| Download state | none, chapter, volume, both manga lanes, comic, final item removed |
| Browse state | each filter, combined filters, each sort, active search |
| Navigation | card Resume, Details fallback, menu Resume, menu Details, menu Remove |
| Retention | Library → Discover → Library; Library → Manga/Comics → Library |
| Window | narrow supported, typical, wide; resize behavior where bridge-supported |
| Input | pointer and keyboard where deterministically bridge-supported |
| Empty | empty Collection; nonempty Collection with no matches |

## Closeout completion signals

- every final-tree scenario reaches its named property/destination signals;
- all exact IDs and resume kinds match fixtures;
- every session manifest proves tagged data/cache and fixture paths;
- no scenario uses the default pipe or live data;
- final evidence paths resolve;
- focused tests and build output belong to the final committed tree;
- Hemanth receives and reviews the visual gallery.

## Performance and architecture checks

- row derivation remains synchronous over local snapshots only;
- Library open performs no network refresh;
- recomputation follows only Collection, Progress, LocalDownloads revisions and user controls;
- filtering/sorting do not mutate source arrays;
- no repeated `LocalDownloads.items()` expansion without evidence;
- large synthetic fixtures remain responsive in the focused harness;
- delegates do not retain stale row/menu state;
- retained page construction does not create unacceptable Tankoban startup cost;
- no Theatre-specific behavior or manual completion action has entered the surface.

Performance claims requiring measurement remain **Test-reported** or **Runtime-validated** only at the strength of the actual measurement produced.

## Documentation gate

Resolve the source-plan mismatch around the missing context/ADR reference:

- locate the intended document on the actual implementation branch; or
- add a reviewed decision record in the repository’s accepted documentation location.

Do not claim an ADR was consulted unless it was retrieved.

## Final status report

Report each item with the exact Brotherhood vocabulary:

| Item | Required closing status |
|---|---|
| BP-001 | Complete internal prerequisite |
| TB-002 | Runtime-validated |
| TB-003 | Runtime-validated |
| TB-004 | Runtime-validated |
| TB-005 | Runtime-validated |
| Final build/tests | Test-reported, with exact logs |
| Final combined runtime suite | Runtime-validated |
| Aesthetic surface | Hemanth approved, or still open |

Permitted non-closing statuses remain:

- Test-reported;
- Implemented, verification pending;
- Bridge blocked;
- Verification failed;
- Plan contradicted.

Do not translate these into “done.”

---

## 7. Traceability

| Requirement | Delivery slice | Runtime proof |
|---|---|---|
| Fourth retained Library tab | TB-001, reported complete | Confirm its prior evidence; replay in closeout |
| Mixed manga/comic wall | TB-001 | Seeded Library fixture |
| Chapter Resume | TB-002 | Real manga reader exact chapter identity |
| Canonical manga saves | TB-002 | Series page and fixture-store identity |
| Legacy compatibility | TB-002 | Re-file scenario with preserved `addedAt` |
| No duplicate after re-file | TB-002 | Row count plus fixture-store inspection |
| Newer manga lane | TB-003 | Chapter-newer and volume-newer reader scenarios |
| Comic Resume | TB-003 | Real comic reader exact source-prefixed ID |
| Comic Details compatibility | TB-003 | Provider fixtures open actual Details |
| Downloaded badge | TB-004 | Seeded aggregate data plus card property |
| Live badge removal | TB-004 | Real Downloads removal and revision-derived card state |
| Search and filters | TB-005 | Named controls, root properties, row counts |
| Sorts | TB-005 | Sort property plus first row ID |
| Card menu routes | TB-005 | Actual reader/details destinations |
| Exact Remove | TB-005 | Revision, counts, surviving IDs, fixture INI |
| Empty vs no matches | TB-005 | Separate deterministic fixtures |
| Retained browse state | TB-005 | Properties and first visible row after tab return |
| Existing Collection rows unchanged | closeout | Named regression paths |
| No release/completion features | all + closeout | Static and surface audit |

---

## 8. Risks and Safeguards

| Risk | Prevention | Detection | Containment |
|---|---|---|---|
| Tagged tests touch live Collection/Progress | BP-001 explicit INI paths restricted to tagged root | manifest plus fixture-store tests | stop all user-visible runtime work |
| Legacy save loss | canonical add → confirmation → exact legacy remove | failure-path tests and fixture inspection | keep identity change isolated |
| Duplicate canonical/legacy rows | one-shot re-file plus canonical-row preference | row count and duplicate fixtures | rollback TB-002 only |
| Wrong title fallback | fallback only for legacy manga; canonical wins | collision fixtures | return identity map |
| Wrong resume lane | preserve exact Progress object and compare timestamps once | exact reader identity scenarios | pure-module rollback |
| Comic prefix loss | preserve original Collection entry | provider fixture matrix | source-specific rollback |
| Stale download badge | explicit revision dependency | live final-item removal | no polling |
| Menu removes wrong item | exact current Collection ID | surviving-ID and fixture INI checks | stop before broad deletion |
| Retained state lies | retained page plus semantic first-row probe | tab-away/back scenario | no duplicate state owner |
| Screenshot-only confidence | require signals and probes | evidence audit | report non-closing status |
| Unsupported bridge assumption | fresh ledger check before each slice | `ping` and plan comparison | Bridge blocked / plan revision |
| Aesthetic overclaim | local reviews gallery | not involved | keep visual gate open |

---

## 9. Rejected Approaches

- Reimplement TB-001: rejected because Hemanth reports it complete; first locate its revision.
- Seed Collection/Progress by driving the daily app: rejected because live user data is not a fixture.
- Treat current `--seed` as QSettings isolation without proof: rejected by the current ledger and store architecture.
- Add a generic Lanista Write command: rejected; the prerequisite is bounded launch-time fixture injection.
- Add aliases to `LibraryButton.qml`: rejected; legacy correction remains local to manga identity resolution.
- Delete legacy before canonical confirmation: rejected because it creates a data-loss window.
- Bulk-migrate every legacy manga: rejected by scope.
- Use title fallback for comics: rejected because provider identity is exact and source-prefixed.
- Route started rows through Details: rejected because Continue already owns resume.
- Copy Theatre Library behavior: rejected because release/watched/finale semantics are out of scope.
- Poll for downloads or wait with sleeps: rejected; revision and strict property signals are required.
- Verify everything only at closeout: rejected; each user-visible slice carries its own runtime proo.
- Execute TB-004 and TB-005 concurrently: rejected because they share the same row/page contracts.

---

## 10. Verification Before Handoff

### Request fidelity

- TB-001 is left out of implementation scope.
- TB-002 through TB-005 preserve the source plan’s product behavior.
- The plan is converted into the exact Brotherhood slice field contract.
- Runtime verification is specified per user-visible slice rather than deferred.

### Evidence integrity

- Current-master facts are separated from the user-reported TB-001 state.
- The isolated fixture prerequisite is labeled as an inference-driven safeguard.
- No runtime action, build, or test is claimed to have run.
- Planned and unavailable bridge features are not used as if available.

### Internal consistency

- BP-001 precedes every fixture-dependent user-visible slice.
- Every slice has baseline, tests, actions, completion signals, probes, visuals, regressions, artifacts, bridge status, and completion criteria.
- Resume, Details, Remove, identity, and revision ownership remain consistent across slices.
- Closeout replays final-tree scenarios rather than trusting intermediate evidence.

### Remaining execution-time discoveries

- exact TB-001 branch/commit and delivered file paths;
- actual automation names already present in TB-001;
- actual reader/details identity properties;
- whether runtime resize and all keyboard focus transitions are deterministically supported;
- whether the existing Downloads confirmation remains in the first root window;
- exact current test runner commands.

A discovery that changes a product or architecture decision is **Plan contradicted**, not executor discretion.

---

# AGENT PACKET

## TASK

Execute the remaining Tankoban Library work in Brotherhood format. Do not reimplement TB-001.

## OBJECTIVE

Finish canonical manga identity, chapter/volume/comic resume, live downloaded state, browse controls, exact removal, and retained browse state with per-slice running-app proof.

## CONTEXT

- Repository: `kingoftheseas56/Colosseum`
- Current inspected `master`: `236021a28e5080102538d3ec7d1b9373416d231a`
- TB-001: reported complete, exact revision unknown
- Authoritative verification inventory: `docs/colosseum-lanista-verification.md`
- Execution workflow: `brotherhood-executing-plans`

## DECISIONS

- Locate TB-001; do not rebuild it.
- Land BP-001 before runtime-verifying the remaining slices unless equivalent isolation already exists.
- Use exact Progress record for Resume.
- Use original Collection entry for Details and Remove.
- Canonical manga save ID is resolved `seriesId`.
- Re-file one legacy manga locally with preserved `addedAt`.
- No shared LibraryButton alias, bulk migration, comic title fallback, release model, polling, or sleeps.
- Execute sequentially.

## NON-GOALS

- TB-001 reimplementation;
- changes to existing Manga/Comics Collection rows;
- new release or completion features;
- generic production write bridge;
- broad shared-component refactor;
- new Main router without evidence.

## IMPLMENNTATION SLICES

1. Confirm TB-001 revision and reconcile its delivered contract.
2. BP-001 — isolated Collection/Progress fixtures.
3. TB-002 — canonical manga identity, chapter Resume, local legacy re-file.
4. TB-003 — latest manga lane and exact comic Resume/Details.
5. TB-004 — revision-driven downloaded badge and live removal update.
6. TB-005 — browse controls, menu actions, exact removal, retained state.
7. Closeout — final-tree tests, runtime suite, evidence audit, Hemanth visual gate.

## ACCEPTANCE TESTS

Use each slice’s Focused tests, Completion signal, State / events / probes, Regression paths, and Completion criterion exactly. A user-visible slice closes only as Runtime-validated.

## RISKS

Live-data contamination, identity loss, duplicate saves, wrong lane selection, comic-prefix loss, stale download state, wrong-row removal, unproven state retention, and bridge capability drift.

## FIRST ACTION

Identify the exact branch and commit containing TB-001. Read its Library page/module/tests and the fresh Lanista ledger. Record any contract differences. Then execute BP-001 only; do not begin TB-002 until deterministic tagged Collection/Progress fixtures are proven or equivalent existing evidence removes the prerequisite.

## SUGGESTED SKILLS

- `brotherhood-executing-plans`
- systematic debugging if runtime evidence contradicts the plan
- QML lifecycle and retained-state testing
- identity migration safety
- Lanista isolated-session scenario design
