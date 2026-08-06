# Colosseum Local Media Launch Implementation Roadmap

## Status

**Execution-ready for repository discovery.** Product behavior is approved in
`specifications/2026-08-06-colosseum-local-media-launch-specification.md`.
Implementation and runtime behavior remain unverified.

## Goal

Open explicit OS-readable books, CBZ/CBR comics, and videos through BookReader 2,
ComicReader 2, and Player 1/libmpv as normal taskbar sessions, with isolated
device-local continuity and no local-library mode.

## Confirmed Integration Areas

- `qml/Taskbar.qml`: taskbar controls and session icons.
- `qml/Main.qml`: app/session routing.
- `native/main.cpp`: startup and platform intake.
- `native/SessionStore.h`: active sessions, focus/switch, saved session state.
- `native/ProgressStore.h`: online Continue backbone; do not reuse directly.
- `native/reader2/Reader2Bridge.h`: one-book authorization and rich reader state; current key is path-derived.
- `native/comicreader/ComicReaderCore.h`: comic entry/state contract.
- `native/player/mpvitem.h`: Player 1/libmpv loading, playback, tracks, and subtitles.
- `tests/`: existing taskbar, reader, player, progress, subtitle, and hotkey seams.

## Global Constraints

- No Local page, scan, watched folders, recursive discovery, or source-media import.
- Reject folders without enumeration.
- Use Player 1, never Player 2, for local video.
- Keep local state device-local and out of online Continue, Library, account activity, and sync.
- Validate before creating a taskbar session.
- Preserve Reader 2's one-authorized-book boundary.
- Never modify source media.
- Contact subtitle providers only after explicit **Find Subtitles Online**.
- Register as **Open with**, but never request default-app status.

## Dependency Order

1. Repository contract map and baseline.
2. Shared resource, handler, and error contracts.
3. Isolated local continuity and identity store.
4. BookReader 2, ComicReader 2, and Player 1 adapters in parallel.
5. Launch coordinator and `SessionStore` integration.
6. Taskbar control and all entry points.
7. Recents, resume, recovery, and identity conflicts.
8. Optional Identify Media.
9. Subtitle integration and manual subtitle cache.
10. Multi-file tray, privacy controls, and OS packaging.
11. End-to-end verification and rollout.

## Slice 0 — Repository Contract Map

**Steps**

1. Trace one current video, book, and comic launch into `SessionStore`.
2. Map taskbar create, focus, minimize, restore, capture-state, teardown, and close.
3. Confirm each backend's validation/open seam.
4. Confirm BookReader 2 supported formats and every path-keyed store.
5. Confirm CBZ and CBR ingestion in ComicReader 2.
6. Confirm Player 1 descriptor, state capture, completion evidence, and subtitle controls.
7. Confirm picker, drag/drop, shortcut, and OS file-open handling.
8. Confirm subtitle add-on requests and existing hash utilities.
9. Run relevant existing tests and record baseline results.

**Produces:** lifecycle, backend, persistence, platform-intake, and test maps.

**Stop if:** CBR is not supported; Reader 2 cannot safely preserve moved-file
full state; local continuity cannot be isolated from online Continue; or a
required platform cannot provide explicit readable resources without copying.

**Complete when:** Every boundary has an owner, input, output, state key, and test seam.

## Slice 1 — Shared Launch Contracts

1. Define a normalized OS-readable resource reference supporting paths and platform handles.
2. Define one/many-resource launch requests.
3. Define handler outcomes: plausible, accepted, categorized rejection, ambiguous.
4. Define session descriptor and state capture/restore contracts.
5. Route by type/extension hint, then backend validation, then limited plausible fallback.
6. Reject folders and HTTP(S) URLs before backend work.
7. Add tests proving validation has no session/persistence side effects.

**Complete when:** Every entry point can use one deterministic router and Player 2 is never a candidate.

## Slice 2 — Local Continuity and Identity Store

1. Create a separate versioned device-local schema.
2. Store opaque local identity separately from resource locator.
3. Store recents, media family, cleaned title, retained permissions, fingerprints,
   progress/state links, optional identification, and subtitle references.
4. Implement identity/recent lookup, relocation repair, changed-content and copy
   relationships, clear-recents, and full forget.
5. Keep local records out of `ProgressStore::recent()`.
6. Resolve Reader 2 relocation by migrating/aliasing all path-keyed stores or
   extending the reader boundary to accept a stable external identity.
7. Add hermetic store tests.

**Complete when:** State survives restart, clear-recents preserves continuity,
full forget removes local state/caches only, and source media remains untouched.

## Slice 3A — BookReader 2 Adapter

1. Use BookReader 2's official supported-format declaration.
2. Validate before session creation.
3. Preserve one-book authorization.
4. Build the normal reader session descriptor.
5. Preserve full reader state: position, bookmarks, highlights, annotations, and settings.
6. Repair state after relocation.
7. Resume unfinished books; reopen completed books at the final position.

**Verify:** representative supported formats open; malformed files create no
session; authorization cannot read another path; full state survives restart and relocation.

## Slice 3B — ComicReader 2 Adapter

1. Reuse the current CBZ/CBR archive/page path.
2. Exclude loose images.
3. Validate before session creation.
4. Map stable local identity to comic `entryId`.
5. Preserve page, direction, pairing, bookmarks, render profile, and other supported state.
6. Categorize corrupt, encrypted, compression, and decoder failures where available.

**Verify:** valid CBZ/CBR open; loose images and invalid archives create no
session; state survives restart/relocation; archives remain unchanged.

## Slice 3C — Player 1 Adapter

1. Launch through Player 1/libmpv `loadFile`.
2. Capture position, completion, tracks, subtitle setup, and supported preferences.
3. Resume unfinished videos.
4. Restart completed videos from the beginning.
5. Preserve active sessions when sources become unavailable.
6. Start playback before expensive fingerprint/hash work.

**Verify:** videos open in Player 1; Player 2 is never instantiated; minimize/restore,
resume, completion, and unavailable-source behavior match the specification.

## Slice 4 — Coordinator and Sessions

1. Resolve resource access.
2. Select and validate handler.
3. Resolve local identity and changed-content/copy decisions.
4. Find an active session by stable local identity.
5. Focus it when present.
6. Otherwise build the backend's normal session descriptor.
7. Call `SessionStore::openOrSwitch` only after validation and identity resolution.
8. Capture state through existing session lifecycle hooks.

**Guardrail:** Never use raw path as the only session identity. Resolve conflicts
before `openOrSwitch`, whose replacement behavior could otherwise clear state.

## Slice 5 — Taskbar and Entry Points

1. Add taskbar **Open Media** with open-file/file-plus semantics.
2. Attach **Open Recent** to that control.
3. Invoke the native OS multi-file picker.
4. Add the keyboard shortcut.
5. Route drag/drop and OS Open-with through the same coordinator.
6. Reject folders and offer **Select Media Files…**.
7. Preserve collapsed/expanded taskbar layouts.
8. Add no Home shelf or Local page.

**Verify:** all entry points behave identically, cancellation creates no state,
folders are not enumerated, and no path bypasses validation.

## Slice 6 — Continuity and Recovery

1. Add recents only after successful opening.
2. Keep recents compact and taskbar-attached.
3. Implement medium-specific resume/completion.
4. Add **Locate File…** for missing recents.
5. Preserve unavailable active sessions with **Retry**, **Locate File…**, and **Close Session**.
6. Ask **Continue as the Same Media** vs **Treat as New Media** for changed content.
7. Ask **Use Existing Media State** vs **Treat as a Separate Copy** for likely copies.
8. Remember the user's relationship choice.
9. Retain durable OS access where supported; otherwise use Locate File.

**Verify:** relocation repairs one identity without duplicate recents; old state
is never silently applied to changed media; sessions do not auto-reopen; local
entries stay out of online surfaces.

## Slice 7 — Identify Media

1. Add optional **Identify Media…** to active local sessions.
2. Reuse appropriate catalog search/selection.
3. Store the association device-locally.
4. Use recognized title/artwork while retaining **Local** provenance and file details.
5. Add **Remove Identification**.
6. Never create library membership or online watched/read state.

## Slice 8 — Subtitles

1. Build provider-neutral context from filename, cleaned title, size, local hash,
   parsed year/season/episode, and optional identified IDs.
2. Prepare cheap signals at open; hash cancellably after playback starts.
3. Contact providers only after **Find Subtitles Online**.
4. Preserve selected embedded/downloaded/manual subtitle, language, track, offset, and display settings.
5. Copy manual subtitles into a private device-local cache.
6. Never add subtitle files to recents or auto-search when cache entries are missing.
7. Remove supporting caches through full forget.

## Slice 9 — Multi-File, Privacy, and Packaging

1. Open the first supported file and stage the rest in temporary **Next to Open**.
2. Preserve supplied order where available.
3. Never auto-advance.
4. Add staged files to recents only after explicit opening.
5. Drop the tray at shutdown.
6. Implement **Clear Open Recent**.
7. Implement confirmed **Forget Local Media Data…** messaging.
8. Register additive OS **Open with** associations.
9. Never request or alter default-app status.

## Slice 10 — Verification and Rollout

1. Map every spec acceptance criterion to automated or runtime evidence.
2. Add focused tests for coordinator, handlers, local store, recovery, and subtitles.
3. Run existing taskbar, Reader 2, ComicReader 2, Player 1, ProgressStore,
   subtitle, and hotkey regressions.
4. Validate in the running app: picker, cancellation, drag/drop, Open-with,
   taskbar lifecycle, removable-drive recovery, durable permissions, state restoration,
   subtitle add-ons, and manual subtitle cache.
5. Inspect persistence after clear-recents and full forget.
6. Confirm no local data reaches Continue, Library, account activity, or sync.
7. Keep entry points feature-gated until every release platform passes.

**Complete when:** Runtime evidence satisfies every specification criterion on
all supported release platforms.

## Risks and Containment

- **Shadow local library:** no Local page, scan, folder grouping, persistent queue, or online continuity.
- **Reader path-key conflict:** prove migration/aliasing of all reader state before relocation ships.
- **Session replacement:** resolve identity conflicts before `openOrSwitch`.
- **Hashing cost:** start playback first; defer/cancel expensive work.
- **Online leakage:** separate store and explicit regressions.
- **Platform permissions:** one resource contract, adapters, Locate File fallback.
- **Private data:** device-local storage, explicit network actions, redacted diagnostics, complete forget.
- **UI congestion:** compact taskbar recents and temporary staging only.

## First Action

Complete Slice 0 and publish the repository contract map and baseline evidence
before changing production behavior.

## AGENT PACKET

### TASK

Implement the approved Local Media Launch specification through the ordered slices above.

### READ FIRST

- `specifications/2026-08-06-colosseum-local-media-launch-specification.md`
- this roadmap
- `qml/Taskbar.qml`
- `native/SessionStore.h`
- `native/ProgressStore.h`
- `native/reader2/Reader2Bridge.h`
- `native/comicreader/ComicReaderCore.h`
- `native/player/mpvitem.h`

### FIRST ACTION

Produce the Slice 0 contract map. Stop and return any architecture conflict
rather than changing approved product behavior.
