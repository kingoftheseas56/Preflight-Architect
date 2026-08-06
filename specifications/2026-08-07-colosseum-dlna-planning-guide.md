# Colosseum DLNA Media Server — Planning Guide

**Artifact class:** Repository implementation guide  
**Status:** Approved scope; repository evidence captured; implementation unverified  
**Target project:** `kingoftheseas56/Colosseum`  
**Repository evidence baseline:** Colosseum `master` at `a7f2fa31b2b06087086395737cf64c7eeed34a6b`  
**Purpose:** Give a planning agent enough durable product and repository context to create an implementation plan without reopening settled decisions or inventing repository facts.

## Outcome

Devices on the same local network can discover Colosseum as a UPnP AV/DLNA media server and directly play completed media downloaded by Colosseum.

Version 1 exposes:

- completed Theatre movies and episodes;
- completed audiobooks and their ordered tracks;
- available artwork and basic media metadata.

Colosseum is a media server only.

## Locked Product Scope

### Included

- opt-in LAN sharing;
- sharing disabled by default;
- UPnP discovery;
- browseable videos and audiobooks;
- direct play of existing files;
- HTTP byte-range seeking;
- automatic catalog updates after completed downloads or deletions;
- stable server identity across application restarts;
- settings on the existing global Settings page beside the porn-filter setting.

### Excluded

- DLNA client or renderer behavior;
- remote control of Colosseum;
- transcoding;
- internet exposure or router port forwarding;
- active, partial, failed, or paused downloads;
- ebooks;
- comics;
- subtitle resources;
- playback-position synchronization.

Do not reopen these decisions while planning unless fresh repository evidence shows a direct contradiction.

## Confirmed Repository Seams

The following locations were inspected at the evidence baseline:

- `native/player/downloadstore.h/.cpp` owns completed Theatre downloads and emits library-change/removal signals.
- `native/engine/AudiobookDownloader.h/.cpp` owns downloaded audiobook records and ordered local track paths.
- `native/engine/LocalDownloads.h/.cpp` is the Downloads page’s cross-world UI read model.
- `qml/ContentPreferences.qml` owns the explicit-content preference.
- `qml/Main.qml` creates global preferences and injects them into `qml/SettingsPage.qml`.
- `native/main.cpp` constructs native services and exposes them to QML.
- `native/CMakeLists.txt` and `tests/CMakeLists.txt` own native build and deterministic test registration.
- The existing torrent `StreamServer` is loopback playback infrastructure and is not a DLNA server.

Repository details may have changed after the evidence baseline. The planning agent must re-inspect these seams before naming exact files in its plan.

## Architectural Decisions

Create a separate native DLNA subsystem.

Conceptual responsibilities:

| Responsibility | Owner |
|---|---|
| Compose shareable Theatre and audiobook records | `DlnaCatalog` |
| Persist settings and own lifecycle/status | `DlnaService` |
| SSDP, device descriptions, SOAP, eventing | `DlnaProtocolBackend` |
| Resolve opaque IDs and serve media ranges | DLNA HTTP responder/backend |
| Render global controls and status | `SettingsPage.qml` |

Names are proposed vocabulary, not confirmed classes or paths.

The subsystem must read directly from `DownloadStore` and `AudiobookDownloader`.

It must not:

- turn `LocalDownloads` into a network service;
- add DLNA state to `ContentPreferences`;
- expose the existing torrent `StreamServer` to the LAN/
- make QML responsible for server lifecycle.

Recommended new repository area: `native/net/dlna/`. The planning agent must confirm whether current repository conventions support this location before freezing it.

## Settings Contract

A native service is the single authority exposed to QML.

### Writable state

- `enabled`, default `false`;
- `deviceName`, default `Colosseum`;
- `shareVideos`, default `true`;
- `shareAudiobooks`, default `true`.

### Read-only status

- lifecycle state: `off`, `starting`, `online`, or `error`;
- human-readable status;
- active address and port;
- visible item count;
- last error.

Persist settings and a generated server UUID under a dedicated DLNA settings group. The UUID must survive application restarts.

### UI placement

The Network Sharing controls belong in `qml/SettingsPage.qml` beside the existing global explicit-content setting.

The card contains:

- Enable DLNA sharing;
- Device name;
- Share videos;
- Share audiobooks;
- current server status.

`qml/ContentPreferences.qml` remains the owner of the porn-filter preference and should not absorb DLNA state.

Disabling sharing must stop advertisements and listeners before the UI reports `off`.

## Catalog Contract

### Sources

The catalog composes:

- completed Theatre records from `DownloadStore`;
- downloaded audiobook records and ordered tracks from `AudiobookDownloader`.

Network code consumes immutable snapshots. Protocol callbacks must not call QML or downloader objects directly.

### Eligibility

A media item is visible only when:

- its source reports it as completed;
- its local path exists;
- it is a regular file;
- its size is greater than zero;
- it is not a partial or temporary file;
- its category is enabled in settings.

### Browse hierarchy

```text
Colosseum
├── Videos
│   ├── Movies
│   └── TV Shows
│       └── Series
│           └── Season
│               └── Episode
└── Audiobooks
    └── Author
        └── Book
            └── Track
```

Sorting is deterministic and case-insensitive.

- Episodes sort by season and episode.
- Audiobook tracks preserve `AudiobookDownloader::localFiles()` order.

### Identity

Each container and media item receives a stable opaque ID derived from source identity and track position, never from its filesystem path.

A catalog record contains enough information for browse output and streaming:

- object ID and parent ID;
- media class;
- title;
- author or series;
- season, episode, or track number where applicable;
- canonical local path held only inside native code;
- MIME type;
- byte length;
- artwork reference.

Missing artwork must not hide an otherwise playable item.

## UPnP Contract

Version 1 must provide:

- a UPnP MediaServer device;
- SSDP advertisements and `M-SEARCH` responses;
- device and service descriptions;
- `ContentDirectory`;
- `ConnectionManager`;
- `BrowseMetadata`;
- `BrowseDirectChildren`;
- pagination through `StartingIndex` and `RequestedCount`;
- accurate `NumberReturned` and `TotalMatches`;
- `GetSystemUpdateID`.

Full UPnP Search is not required. Search capabilities may be advertised as empty.

The system update ID increments only when the effective visible catalog changes, including video/audiobook toggle changes.

## Network Boundary

- LAN IPv4 only in Version 1.
- Never bind or advertise on loopback.
- Never configure UPnP IGD or router port forwarding.
- Fail closed when no safe LAN interface is available.
- When disabled, no SSDP advertisement or media HTTP listener remains active.
- Network-interface changes trigger safe rebind and re-advertisement.
- Protocol work runs away from the GUI thread.
- Native status updates cross back through a queued thread boundary.

## HTTP Media Contract

Advertised URLs use an opaque media ID:

```text
http://<lan-address>:<port>/media/<opaque-id>/<safe-display-name>
```

The URL must neither contain nor accept a filesystem path.

Required behavior:

- `GET`;
- `HEAD`;
- full-file responses;
- one byte range per request;
- closed, open-ended, and suffix ranges;
- `206 Partial Content` with valid `Content-Range`;
- `416 Range Not Satisfiable` with `Content-Range: bytes */<size>`;
- `Accept-Ranges: bytes`;
- correct `Content-Length` and MIME type;
- bounded-memory streaming;
- cancellation on client disconnect;
- `404` for unknown, removed, or missing media IDs.

Before opening a file, resolve the ID against the current catalog snapshot and revalidate the canonical path. Path input or symlink replacement must not permit access to another file.

## Failure Behavior

- Startup failure moves the service to `error` with a user-readable message.
- A port collision may select another safe port while preserving the UUID.
- Changing the device name while online triggers re-advertisement.
- Removing a file removes it from future browse results without restarting.
- A failed catalog rebuild retains the previous valid snapshot and records the error.
- Shutdown stops advertisements, rejects new requests, and closes active work without indefinitely blocking the GUI.
- Restarting Colosseum with sharing enabled starts from persisted settings.

## Observability

The plan must include structured logging for:

- lifecycle transitions;
- selected interface, address, and port;
- catalog revision and counts by media type;
- browse container, offset, request count, and result count;
- HTTP status, range, and bytes served;
- rejected or unknown IDs;
- bind, multicast, dependency, and protocol failures.

Normal logs must not expose raw local paths or source download URLs.

## Dependency Decision Gate

Use an existing UPnP implementation behind a Colosseum-owned backend interface.

Before the planning agent locks a library into the implementation plan, it must obtain evidence for:

- licence compatibility with Colosseum’s MIT distribution;
- successful build with Colosseum’s supported MSVC toolchain;
- SSDP discovery by Kodi and VLC;
- MediaServer, ContentDirectory, ConnectionManager, and eventing support;
- acceptable Windows packaging and deployment;
- clean shutdown and interface rebinding.

Portable UPnP/libupnp is a candidate, not an approved dependency.

Kodi is behavior reference only. Do not copy Kodi source into Colosseum.

If no candidate passes the gate, the agent must stop and return the evidence gap rather than planning a custom protocol stack by assumption.

## Verification Requirements for the Future Plan

The implementation plan must map work to the following evidence.

### Deterministic coverage

- catalog filtering excludes partial, failed, zero-byte, and missing files;
- hierarchy, sorting, audiobook order, and opaque IDs are deterministic;
- source toggles change the visible catalog and system update ID;
- range handling covers full, closed, open-ended, suffix, invalid, and unsatisfiable requests;
- unknown IDs and removed files return `404`;
- service lifecycle covers default-off, persistence, startup failure, clean stop, and rename re-advertisement;
- DIDL-Lite output escapes metadata and reports correct pagination counts;
- tests use isolated settings and never modify the user’s real configuration.

Deterministic harnesses belong in normal CTest. Live multicast and real-device checks remain explicit integration/manual verification.

### Compatibility matrix

Verify discovery, browse, play, and seek with:

- Kodi;
- VLC;
- at least one real smart TV or console.

The implementation change must update `docs/colosseum-test-verification.md` with exact commands and expected evidence.

## Acceptance Criteria

1. Disabled sharing emits no SSDP advertisements and accepts no DLNA HTTP connections.
2. Enabling sharing exposes one stable `Colosseum` MediaServer on the same LAN.
3. Clients browse movies, shows, seasons, episodes, audiobooks, and ordered tracks.
4. A completed video plays and seeks in Kodi, VLC, and one real living-room device.
5. Audiobook tracks play in Colosseum’s stored order.
6. Newly completed media appears without an application restart.
7. Deleted or missing media disappears without an application restart.
8. Partial and failed downloads never appear.
9. Video and audiobook toggles take effect without restarting the application.
10. The server UUID survives application restart.
11. Raw filesystem paths are neither exposed nor accepted.
12. Disabling sharing stops discovery and serving.
13. Existing local playback and download behavior remains unchanged.

## Planning Instructions

The next agent must create a dependency-aware implementation plan from this guide.

Before planning:

1. Re-inspect the confirmed Colosseum seams at current `master`.
2. Identify changes since the evidence baseline.
3. Run the UPnP dependency decision gate.
4. Confirm exact ownership, thread boundaries, build integration, and test seams.
5. Mark all repository paths as confirmed, likely, or unknown.
6. Stop and return when a dependency or repository fact cannot be established.

The resulting plan must:

- slice work into independently reviewable outcomes;
- preserve the locked scope;
- include verification for every slice;
- include containment and rollback for the LAN-facing service;
- avoid unrelated refactoring;
- leave runtime compatibility unverified until the named client matrix is exercised.

## Open Execution-Time Discoveries

These do not reopen product scope:

- exact UPnP dependency and packaging method;
- exact policy for machines with several LAN interfaces;
- whether existing audiobook data provides a stable artwork join;
- final MIME and UPnP protocol-info mappings for formats actually produced by Colosseum.

## Status Boundary

This guide records approved product and architecture decisions. It does not claim that DLNA code exists, that a dependency builds, or that discovery, playback, seeking, shutdown, or compatibility has been tested.
