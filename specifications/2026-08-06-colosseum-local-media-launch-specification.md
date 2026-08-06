# Colosseum Local Media Launch Specification

## Status

**Approved product design.**  
**Repository implementation status:** not started or verified in this artifact.  
**Next phase:** repository inspection and implementation roadmap.

> **Destination:** This specification defines the user-visible behavior, product boundaries, persistence semantics, and integration responsibilities for opening local books, comics, and videos in Colosseum without creating a separate local-library mode.

## Problem Statement

Colosseum already has dedicated playback and reading surfaces, but users need a coherent way to open media they already possess on their device or can access through the operating system.

The feature must support local books, comics, and videos through Colosseum's existing readers and player while avoiding a parallel local-library product. Users should not need to scan folders, import collections, manage watched directories, or navigate to a persistent Local section.

The central product distinction is:

> Local media is opened as an action and lives as a session. It is not imported as a library item.

## Objective

Allow a user to hand Colosseum one or more explicit, OS-readable media files and have each opened item:

- launch immediately in the correct existing player or reader;
- behave as a normal Colosseum taskbar session;
- retain device-local progress and supported session state;
- remain recoverable if moved, renamed, replaced, or temporarily unavailable;
- use Colosseum's subtitle add-ons and optional media identification where relevant;
- never enter Colosseum's online library, synced progress, account history, or catalog continuity surfaces.

## User-Visible Outcome

A user can open a supported local file through any supported entry point:

- the taskbar-level **Open Media…* action;
- drag-and-drop into Colosseum;
- a keyboard shortcut;
- the operating system's **Open with Colosseum** action.

All entry points converge on the same launch behavior.

For a valid supported file, Colosseum opens the appropriate existing player or reader immediately. The file becomes a normal taskbar session that can be focused, minimized, restored, switched away from, and closed.

Colosseum does not create a Local page, scan the file's folder, import the source file, or add it to the online library.

## Actors and Core Scenarios

### Actor: User opening one local media file

1. The user invokes one supported entry point.
2. Colosseum receives an explicit OS-readable file reference.
3. Colosseum routes the file to the most likely existing backend.
4. The backend validates that it can open the file.
5. Colosseum creates a normal taskbar session and opens it immediately.
6. Progress and supported local state persist device-locally.

### Actor: User reopening an active file

1. The user opens a file that already has an active taskbar session.
2. Colosseum focuses and restores the existing session.
3. Colosseum does not create a duplicate active session.

### Actor: User reopening a previously closed file

1. The user opens the file directly or selects it from **Open Recent**.
2. Colosseum restores the saved device-local state.
3. Unfinished media resumes automatically.
4. Completed media follows medium-specific reopening rules.

### Actor: User opening several files

1. The user explicitly selects or drops several supported files.
2. Colosseum opens the first file immediately.
3. Remaining files appear in a temporary **Next to Open** tray.
4. The tray does not auto-advance.
5. A file enters **Open Recent** only after the user explicitly opens it.

### Actor: User recovering moved or unavailable media

1. Colosseum detects that a recent or active file is unavailable.
2. Colosseum preserves retained state.
3. The user can retry, locate the file, or close the session as appropriate.
4. A successful relocation repairs the existing local-media identity instead of creating a duplicate.

## Canonical Domain Terms

### Local Media Launch

An explicit user action that asks Colosseum to open one or more OS-readable media files.

**Excludes:** folder scanning, watched folders, background indexing, catalog import, and arbitrary web URL opening.

### Local Media Session

A taskbar-managed player or reader session created from a Local Media Launch.

A local session has the same lifecycle expectations as other Colosseum sessions, while retaining local provenance and device-local persistence.

### Local Media Identity

A device-local identity used to associate a file with progress, reader state, subtitle configuration, optional identification, and recovery behavior.

It is not a catalog item, account-level media identity, or library membership record.

### Open Recent

A small, clearable list of previously opened local files attached to the taskbar **Open Media** control.

It is a shortcut list, not a local-media library.

### Next to Open

A temporary in-memory tray containing additional files from an explicit multi-file launch.

It is not persisted across app restarts and does not auto-advance.

### Identify Media

An optional user-initiated association between a local session and an existing Colosseum title or episode.

Identification enriches presentation and add-on context but does not import the file, add it to a library, or sync local progress.

## Scope

### Included Media Families

Local Media Launch ships for all three media families together:

1. **Books**
   - Open in BookReader 2.
   - Support the formats BookReader 2 officially supports, including EPUB, PDF, MOBI, and other backend-supported book formats.

2. **Comics**
   - Open in ComicReader 2.
   - Support CBZ and CBR.
   - Loose-image opening is excluded.

3. **Video**
   - Open in Player 1.
   - Player 1 uses libmpv.
   - Support video formats accepted by Colosseum's bundled and configured libmpv playback path.

Backend capability remains authoritative. An extension alone does not create an official support promise if the destination backend cannot validate and open the file.

### Supported File Locations

Accept any explicitly selected file-like resource the operating system grants Colosseum permission to read, including:

- ordinary filesystem files;
- removable drives;
- mounted network locations;
- platform document-provider or content-URI resources.

Arbitrary `http://` and `https://` URLs are not part of Local Media Launch.

When the platform supports durable access grants, Colosseum should retain that permission for future sessions. Retaining access must not copy or import the source media.

## Constraints

- Local media is an action and session type, not a separate library mode.
- No Local navigation page or permanent local catalog is introduced.
- No folder scanning, recursion, watched folders, background indexing, or media-folder monitoring.
- Folders are rejected and the user is prompted to select explicit files.
- Source media remains in its original location and is never silently copied or imported.
- Existing playback surfaces remain authoritative:
  - BookReader 2 for books;
  - ComicReader 2 for comics;
  - Player 1/libmpv for video.
- Local media data remains device-local.
- File references, progress, reader state, subtitle state, and optional identification do not sync through the user's Colosseum account.
- Local media does not appear in online Continue Watching, Continue Reading, account activity, synced watched/read status, or the online library.
- Optional identification cannot become a prerequisite for opening or using media.
- Different launch entry points must not produce different session semantics.
- Colosseum may register as an **Open with** target but must never request or take over default-app status.
- Normal valid files should open immediately without a confirmation card or staging screen.
- Invalid files must not leave broken taskbar sessions.

## Non-Goals

The first version does not include:

- a Local library tab, page, world, or navigation destination;
- folder browsing inside Colosseum;
- Kodi-style media-source management;
- recursive folder discovery;
- watched folders;
- persistent playlists or queues;
- automatic next-item playback from multi-file launches;
- loose-image comic sessions;
- automatic media identification;
- local files presented as sources on online catalog pages;
- automatic online subtitle searches when video opens;
- cross-device local-media continuity;
- online syncing of local progress or annotations;
- arbitrary remote URL playback through Local Media Launch;
- default-app takeover prompts;
- media file rename, move, delete, or organization controls.

## Required Behavior

### 1. Entry Points

Colosseum must provide one shared Local Media Launch flow reachable from:

- a taskbar-level **Open Media…* control;
- drag-and-drop;
- a keyboard shortcut;
- OS-level **Open with Colosseum**.

The primary in-app control belongs on the taskbar because local media creates sessions rather than navigation destinations.

### 2. Open Recent Placement and Behavior

**Open Recent** is attached to the taskbar **Open Media** control as a menu or anchored panel.

It must not appear as a Home shelf or permanent Local destination.

Each recent entry should display enough information to identify and resume the file without becoming a catalog card. At minimum:

- cleaned title;
- subtle **Local** provenance marker;
- useful secondary information such as source location or resume position, subject to space and privacy design;
- unavailable-state indication when access is lost.

Selecting an available recent entry opens it immediately.

Selecting an unavailable entry invokes the recovery flow.

Two distinct clearing actions are required:

- **Clear Open Recent**
  - removes visible shortcuts;
  - does not erase saved progress, annotations, identification, or subtitle state.

- **Forget Local Media Data…**
  - requires explicit confirmation;
  - removes recents, progress, reader state, local identification, subtitle configuration, and locally cached supporting subtitle assets.

### 3. File Picker

The default **Open Media…** action should invoke the platform's native file picker rather than a Kodi-style custom browser.

This is a product recommendation adopted by this specification because it:

- reinforces explicit file opening instead of local browsing;
- uses operating-system permission and document-provider mechanisms;
- avoids introducing media-source, folder-memory, sorting, filtering, and scanning expectations;
- reduces platform-specific filesystem UI Colosseum would otherwise own.

The native picker should allow multi-file selection where the platform supports it.

A future custom browser requires a separate product decision because it would materially change the feature from action-based opening toward filesystem navigation.

### 4. Taskbar Control

The taskbar control must communicate “open a media file as a session” without suggesting a Local destination.

Recommended visual semantics:

- a file-plus icon where custom iconography is appropriate;
- otherwise a simple plus/open-file icon with the visible label **Open Media**;
- an attached disclosure indicator when **Open Recent** is available.

The icon implementation is a visual-design detail. The durable requirement is that the control is recognizable, taskbar-level, and provides both **Open Media…** and **Open Recent**.

### 5. Immediate Opening

A valid supported file opens immediately after selection or handoff.

Do not show:

- a launch card;
- a confirmation screen;
- a metadata preview step;
- an import prompt.

The user is interrupted only when Colosseum cannot confidently route or validate the file, detects a material identity conflict, or requires recovery.

### 6. Routing and Validation

Colosseum uses explicit routing with backend validation and limited fallback:

1. Infer the likely media family from available OS type information and filename extension.
2. Ask the likely destination backend or its adapter to validate/probe the resource.
3. If validation fails, try only other plausible handlers.
4. Ask the user to choose **Open As…* only when more than one handler is genuinely plausible or no handler can decide confidently.
5. Reject unsupported, corrupt, inaccessible, encrypted, or otherwise unreadable resources before creating a taskbar session.

The routing layer must not pretend to own the full format parser. Existing backends remain authoritative.

### 7. Session Creation and Deduplication

A successfully validated file creates one normal taskbar session.

When the same active media is opened again:

- focus and restore the existing session;
- do not create a duplicate taskbar entry;
- preserve the current playback or reading position.

A file that fails launch validation creates no taskbar session.

### 8. Presentation and Local Provenance

Before optional identification:

- use a cleaned filename as the session's primary title;
- remove the file extension;
- lightly normalize separators and obvious release-style delimiters;
- retain the exact filename and path/resource reference in session details;
- show a subtle **Local** marker.

After optional identification:

- use the recognized title and available artwork for presentation;
- continue to show the subtle **Local** marker;
- retain the original filename and location in session details;
- allow **Remove Identification** to restore cleaned-filename presentation.

### 9. Optional Identify Media

An active local session may expose **Identify Media…**.

The user can search for and select an existing Colosseum title, movie, series episode, book, or other relevant catalog entity supported by the corresponding media surface.

The association:

- remains device-local;
- is optional;
- can be corrected or removed;
- may provide recognized title, artwork, year, season/episode, and online identifiers;
- may improve subtitle and add-on context;
- does not create library membership;
- does not sync local progress;
- does not update online watched/read status;
- does not cause the file to appear as an online title source.

### 10. Persistence and App Restart

Local session state persists device-locally.

When Colosseum restarts:

- local sessions do not reopen automatically;
- Colosseum starts in its normal app context;
- reopening the same file restores its saved state;
- the user may reopen it through the filesystem or **Open Recent**.

### 11. Resume and Completion Semantics

For unfinished media:

- videos resume at the last saved playback position;
- books and comics resume at the last saved reading position.

For completed media:

- completed videos reopen from the beginning;
- completed books and comics reopen at their final saved position.

The existing player or reader may expose its normal restart/start-over controls.

### 12. Reader State

Local books and comics retain the full device-local state their existing reader supports, including where applicable:

- reading position;
- bookmarks;
- highlights;
- annotations;
- per-document layout or reading settings;
- comic reading direction;
- page-display preferences;
- other document-specific reader state already supported by the destination reader.

The Local Media Launch layer must not reduce local files to position-only reading when the existing reader supports richer state.

### 13. Video Subtitle Integration

Local video uses Colosseum's existing subtitle add-ons plus manual subtitle upload.

#### Multi-Signal Subtitle Context

Colosseum prepares a provider-neutral local-video context that may include:

- original filename;
- cleaned filename/title;
- file size;
- locally computed content hash;
- parsed year;
- parsed season and episode;
- optional online identifiers from **Identify Media…**.

Each subtitle add-on consumes the fields it supports.

Filename search remains the fallback.

#### Search Timing

When video playback begins:

- Colosseum may prepare cheap local signals;
- expensive hashing may run unobtrusively after playback starts;
- Colosseum must not contact subtitle providers automatically.

Provider requests begin only when the user chooses **Find Subtitles Online**.

If the content hash is not yet available, search may begin with available signals and improve or refresh when stronger identity evidence becomes available.

#### Persisted Subtitle State

For each local video, retain device-locally:

- selected embedded subtitle track;
- selected downloaded add-on subtitle;
- selected manually supplied subtitle;
- subtitle language and track selection;
- timing offset;
- display preferences supported by the player;
- cached downloaded subtitle assets;
- cached manual subtitle assets.

Reopening the video reapplies the saved subtitle setup without contacting providers automatically.

#### Manual Subtitle Cache

When the user manually supplies a subtitle:

- copy it into Colosseum's private device-local subtitle cache;
- leave the original file untouched;
- do not add it to **Open Recent**;
- associate it with the local video identity;
- remove it through **Forget Local Media Data…**;
- never sync it between devices.

### 14. Multi-File Launch

When several explicit files are handed to Colosseum:

1. Preserve the user-provided ordering where the platform supplies one.
2. Open the first supported file immediately.
3. Place the remaining supported files in **Next to Open**.
4. Keep **Next to Open** temporary and app-session-only.
5. Do not add staged-but-unopened files to **Open Recent**.
6. Let the user explicitly open or remove staged items.
7. Do not auto-open the next item when the active file finishes or closes.
8. Remove failed items from the tray while preserving other staged files.

No persistent queue or playlist is created.

### 15. Folder Handling

Folders are not accepted as Local Media Launch resources.

When the user drops or selects a folder:

- do not enumerate its contents;
- do not recurse;
- do not remember it as a source;
- explain that Colosseum opens explicit files;
- offer **Select Media Files…**.

### 16. Identity, Changed Content, and Copies

A path or OS resource identifier alone is insufficient as permanent media identity.

Colosseum must retain enough device-local evidence to detect likely identity conflicts without requiring full library indexing.

#### Changed Content at a Known Location

When a remembered location now contains materially different content, ask:

- **Continue as the Same Media**
  - retain progress, identification, reader state, and subtitle configuration;

 - **Treat as New Media**
  - create a fresh local-media identity and fresh state.

Do not silently attach old state to clearly changed content.

#### Same Content at a New Location

When Colosseum detects likely duplicate content at another path, ask:

- **Use Existing Media State**
- **Treat as a Separate Copy**

Remember the user's decision for that relationship and avoid repeatedly prompting.

The exact fingerprinting and confidence mechanism is an implementation-time design subject to repository and performance evidence.

### 17. File Access and Recovery

#### Missing Recent File

When a recent file cannot be resolved:

- retain its saved state;
- display that it is unavailable;
- offer **Locate File…**;
- repair the existing identity after successful relocation;
- do not create a duplicate recent entry.

#### Open File Becomes Unavailable

When a source becomes unavailable during an active session:

- preserve the taskbar session and current state;
- pause or suspend media access as supported by the destination backend;
- offer:
  - **Retry**
  - **Locate File…**
  - **Close Session**

A backend may continue rendering already buffered content, but the user-visible recovery state must be intentional rather than an unstructured backend failure.

#### Temporary OS Permissions

When the platform grants temporary file access:

- request durable access when the platform supports it;
- do not copy the media as a fallback;
- use **Locate File…** if access later expires or is revoked.

### 18. Launch Failure

A file that cannot be opened is rejected before taskbar session creation.

The error should communicate, when available:

- cleaned filename;
- handler that rejected it;
- specific reason such as unsupported format, corruption, encryption, permissions, unsupported archive compression, or unavailable decoder;
- **Choose Another File…* ;
- **Open As…* only when another handler is plausible.

Generic “unsupported file” messaging is a fallback only when the destination backend cannot provide a more specific failure category.

## Responsibilities and Boundaries

### Shared Local Media Launch Layer

Owns:

- convergence of all entry points;
- OS-readable resource intake;
- routing orchestration;
- active-session deduplication;
- local identity coordination;
- **Open Recent**;
- **Next to Open**;
- recovery coordination;
- device-local identification association;
- privacy/forget actions;
- common provenance presentation.

Does not own:

- media decoding;
- book parsing;
- comic archive rendering;
- subtitle provider implementation;
- reader-specific annotations;
- online catalog membership;
- account progress synchronization.

### BookReader 2

Owns:

- validation and opening of officially supported book formats;
- reading position;
- bookmarks, annotations, and supported document state;
- book-specific failure details;
- book completion semantics supplied to the shared layer.

### ComicReader 2

Owns:

- validation and opening of CBZ and CBR;
- archive/page reading behavior;
- comic-specific progress and supported reading state;
- comic-specific failure details;
- comic completion semantics supplied to the shared layer.

Loose images are not registered for Local Media Launch.

### Player 1 / libmpv

Owns:

- validation and playback of supported video resources;
- playback position and completion evidence;
- embedded subtitle tracks;
- subtitle application and playback-level subtitle preferences;
- player-specific failure details.

Player 2 and its custom FFmpeg path are outside this feature.

### Subtitle Add-on Integration

Owns:

- provider queries initiated by the user;
- translation of the provider-neutral local-video context into provider requests;
- result presentation and download;
- explicit network boundaries.

### Platform Integration

Owns:

- native file picker;
- drag-and-drop;
- keyboard shortcut routing;
- OS **Open with** registration;
- durable permission grants where supported;
- delivery of file-like resource handles.

## State and Data Flow

```text
Explicit user entry point
    ↓
OS-readable file reference(s)
    ↓
Local Media Launch intake
    ├─ normalize resource reference
    ⌜─ resolve retained OS permission where supported
    ├─ infer likely handler
    ⌔─ coordinate validation
          ↓
Destination backend validates/probes
          ⌜─ failure → actionable error, no taskbar session
          ⌔─ success
               ↓
Docal identity resolution
    ├─ active session exists → focus it
    ├─ known media → restore device-local state
    ├─ changed content → ask identity question
    └─ likely copy → ask sharing question
               ↓
Create/focus normal taskbar session
               ↓
BookReader 2 / ComicReader 2 / Player 1
               ↓
Persist device-local progress and supported state
               →
Closed session may remain accessible through Open Recent
```

For multi-file launches, only the first validated file proceeds immediately to session creation; remaining files enter the temporary **Next to Open** tray.

## Failure Handling Summary

| Condition | Required behavior |
|---|---|
| Unsupported or corrupt file at launch | Show actionable error; create no session |
| Ambiguous handler | Offer **Open As…** only after limited backend validation |
| Folder selected or dropped | Reject enumeration; offer **Select Media Files…** |
| Active file temporarily unavailable | Preserve session; offer Retry, Locate, Close |
| Recent file moved or permission revoked | Offer Locate File; preserve and repair identity |
| Known path contains changed content | Ask Same Media vs New Media |
| Same content appears at another path | Ask Existing State vs Separate Copy |
| Manual subtitle source disappears | Use cached copy; no automatic network request |
| Downloaded subtitle cache missing | Do not auto-search; allow user-initiated search |
| Subtitle provider unavailable | Preserve playback; show provider-specific failure in subtitle UI |
| One file fails in multi-file launch | Remove/mark failed item without discarding remaining staged files |

## Privacy and Data Retention

The feature stores device-local continuity data only.

Potential retained data includes:

- resource identifiers and paths;
- cleaned titles;
- recent-entry metadata;
- media fingerprints or hashes;
- progress;
- reader annotations and settings;
- subtitle configuration and cached subtitle files;
- optional catalog identification.

Colosseum must provide:

- **Clear Open Recent** for shortcut removal;
- **Forget Local Media Data…** for full local-media continuity erasure.

The full forget action must clearly state that it removes progress, annotations, identification, subtitle setup, and supporting caches. It does not delete the user's source media files.

## Observability Requirements

Implementation must make the following events diagnosable without logging private content unnecessarily:

- entry point used;
- routing candidate and final handler;
- validation result category;
- active-session deduplication result;
- identity decision required and outcome category;
- retained permission success/failure;
- file-unavailable transition and recovery result;
- subtitle context preparation state;
- subtitle provider search initiated by explicit user action;
- local state save/restore success or failure;
- forget operation completion.

Logs and diagnostics should avoid recording full private paths or filenames by default. Prefer opaque local identity and redacted resource information unless the user explicitly exports diagnostics.

## Testing Decisions

Testing should prove behavior at the highest practical seam.

### Shared Launch Tests

Prove that:

- all entry points feed the same launch contract;
- valid files create exactly one taskbar session;
- reopening an active file focuses it;
- invalid files create no taskbar session;
- folders are never enumerated;
- multi-file launches open one and stage the rest;
- staged files do not auto-advance;
- unopened staged files do not enter recents.

### Handler Contract Tests

For each media family, prove that:

- a supported representative file validates and opens in the intended backend;
- an unsupported or malformed representative file produces a categorized failure;
- routing fallback does not send every file to every backend;
- Player 2 is never selected for local video.

Exact fixture formats and test locations require repository inspection.

### Persistence Tests

Prove that:

- progress survives app restart;
- sessions do not automatically reopen;
- unfinished media resumes;
- completed video restarts;
- completed books/comics retain final position;
- full reader state restores;
- Clear Open Recent preserves continuity state;
- Forget Local Media Data erases continuity and cached subtitles.

### Identity and Recovery Tests

Prove that:

- moved media can repair an existing recent entry;
- recovery does not duplicate identity;
- changed content does not silently inherit old state;
- likely copies invoke the one-time sharing decision;
- an active unavailable file preserves the taskbar session.

### Subtitle Tests

Prove that:

- opening a video does not contact subtitle providers;
- user-initiated search receives available multi-signal context;
- manual subtitles are copied into the private cache;
- saved subtitle selection and offsets restore;
- forgetting local media removes cached supporting subtitles;
- missing cached online subtitles do not trigger automatic network search.

### Platform Integration Tests

Per supported platform, prove that:

- native file picker returns accepted resources;
- multi-select behavior matches platform capabilities;
- drag-and-drop and Open with use the same launch contract;
- durable access is retained where supported;
- association registration does not request default-app takeover.

### Runtime Validation

Execution must validate real user-visible behavior in a running application. Unit and integration tests do not replace proof of:

- taskbar focus/minimize/restore behavior;
- native picker behavior;
- drag-and-drop;
- OS Open with behavior;
- removable-drive disconnect and reconnect;
- document-provider permission persistence;
- playback/reader state restoration;
- subtitle add-on interaction.

## Migration and Compatibility

- Existing online playback and reading behavior must remain unchanged.
- Existing online progress, Continue Watching/Reading, and library data must remain separate from local continuity data.
- The feature should introduce no migration that reclassifies current downloads or cached files as Local Media Launch entries.
- Existing media files managed by other Colosseum workflows are not automatically added to **Open Recent**.
- File association registration must be additive and non-default.
- If local continuity storage changes after release, migration must preserve progress and annotations or explicitly fail safely without affecting source media.
- Rollout should allow the shared launch entry points to be disabled or hidden if a platform integration proves unstable, without affecting existing players/readers.

## Acceptance Criteria

The specification is satisfied only when all of the following are observable:

1. The taskbar exposes **Open Media…** and attached **Open Recent** access without creating a Local navigation destination.
2. Clicking **Open Media…* invokes the native OS file picker.
3. Drag-and-drop, keyboard opening, native picker selection, and **Open with Colosseum** use the same launch behavior.
4. A valid supported book opens immediately in BookReader 2.
5. A valid CBZ or CBR opens immediately in ComicReader 2.
6. A valid supported video opens immediately in Player 1/libmpv.
7. Loose image files are not accepted as comic launches.
8. No explicit file launch causes parent-folder or recursive scanning.
9. A folder is rejected and redirects the user to explicit file selection.
10. A successfully opened file becomes a normal taskbar session.
11. Reopening an already-active file focuses the existing session.
12. A malformed or unsupported file creates no taskbar session.
13. Local sessions display a cleaned title and subtle **Local** provenance.
14. Optional identification enriches title/artwork without removing Local provenance or creating library membership.
15. Local progress and state survive restart, but sessions do not automatically reopen.
16. Unfinished media resumes automatically.
17. Completed videos restart from the beginning.
18. Completed books and comics reopen at their final saved position.
19. Local books and comics restore their full supported reader state.
20. **Open Recent** can reopen available files and repair moved files through **Locate File…*.
21. **Clear Open Recent** does not erase saved continuity state.
22. **Forget Local Media Data…* erases local continuity state and cached supporting subtitles without deleting source media.
23. Multi-file opening opens one file and stages the remainder in a non-persistent, non-auto-advancing tray.
24. Changed content at a remembered location cannot silently inherit old state.
25. Likely copies at new paths require a one-time state-sharing choice.
26. An active session whose source becomes unavailable remains recoverable.
27. Opening a local video does not automatically contact subtitle providers.
28. User-initiated subtitle search uses available filename, size, hash, parsed episode/year, and optional identified metadata signals.
29. Manual subtitle upload remains available and is retained in a private device-local cache.
30. Local media never appears in online Continue Watching/Reading, account activity, synced progress, watched/read status, or library membership.
31. Colosseum registers as an available **Open with** target without requesting default-app status.
32. Source media remains untouched and is never silently copied into Colosseum storage.

## Repository Evidence and Discovery Gates

### Confirmed Product Decisions

The behaviors in this specification were explicitly selected by the product owner during the Brotherhood brainstorming session, including the correction that local video uses Player 1/libmpv rather than Player 2.

### Repository Evidence Level

This specification does not claim that all required seams already exist.

Before implementation planning, inspect and confirm:

- current taskbar session creation, focus, minimize, restore, and close ownership;
- current Player 1 launch request and progress persistence boundaries;
- BookReader 2 supported-format validation and state persistence boundaries;
- ComicReader 2 CBZ/CBR opening and state persistence boundaries;
- subtitle add-on query contracts and whether they can accept provider-neutral multi-signal context;
- current local hash/fingerprint utilities, if any;
- platform file picker, drag/drop, file association, and durable permission support;
- current progress and annotation stores and whether local identities can remain isolated from online identities;
- suitable tests and fixture conventions.

Any exact repository paths, classes, schemas, or commands not directly inspected must remain **likely** or **unknown** during planning.

## Risks

### Shadow-Library Drift

Open Recent, identification, artwork, and rich persistence could gradually become a local library.

**Guardrail:** no Local page, scanning, folder organization, persistent queue, or online continuity integration.

### Identity False Positives

Content fingerprinting may merge changed editions or intentional copies.

##Guardrail:** ask before applying shared state when identity confidence is consequential.

### Hashing Cost

Large video hashing could delay playback or consume excessive I/O.

**Guardrail:** playback starts immediately; expensive identity work runs opportunistically and must be cancellable or deferred.

### Platform Permission Differences

OS-readable file handles and durable access vary across platforms.

**Guardrail:** use platform-native permission models, preserve user intent, and fall back to **Locate File…** rather than copying media.

### Privacy Leakage

Paths, filenames, and hashes may expose personal media activity.

##Guardrail:** device-local storage, no account sync, explicit provider search, redacted diagnostics, and complete local-data erasure.

### Backend Capability Drift

Reader/player supported formats may change over time.

**Guardrail:** backend validation remains authoritative; the shared router does not hard-code unsupported promises independently.

### UI Congestion

The taskbar control, recent panel, and multi-file tray could overwhelm session management.

**Guardrail:** keep Open Recent compact, keep Next to Open temporary, and avoid a permanent Local destination.

## Open Questions for Repository Design

These are implementation discoveries, not unresolved product decisions:

1. What exact shared request contract can represent filesystem paths, document-provider handles, and other OS-readable resources without forcing every backend to understand every platform type?
2. Which existing component should own the Local Media Identity store?
3. What evidence can distinguish changed media and likely copies at acceptable I/O cost?
4. How do existing subtitle add-ons accept or need to be extended for hash, size, season, episode, and optional catalog identifiers?
5. How should taskbar presentation expose an anchored Open Recent menu within current layout constraints?
6. Which platforms can retain durable resource permission, and what fallback behavior is required per platform?
7. What exact completion thresholds do current player and readers expose or require?
8. Which existing persistence stores can be reused without causing local state to appear in online continuity surfaces?

None of these questions authorizes changing the product behavior specified above. If repository evidence makes a product requirement infeasible, stop and return the conflict for product review.

## Verification Notes

- **Confirmed:** user-selected product behavior and non-goals recorded in the brainstorming conversation.
- **Corrected:** local video uses Player 1/libmpv; Player 2 is explicitly outside scope.
- **Recommended and adopted in this spec:** native OS file picker and a taskbar file-plus/open-media affordance.
- **Requires repository evidence:** exact integration seams, data models, platform APIs, supported-format declarations, and test locations.
- **Requires runtime validation:** file picker, drag/drop, Open with, taskbar lifecycle, device permissions, disconnect/reconnect, playback/reader restoration, and subtitle provider behavior.

## Next Phase

Create an implementation roadmap with an initial repository-inspection slice. The roadmap must not invent exact files or APIs before confirming the current Colosseum architecture.
