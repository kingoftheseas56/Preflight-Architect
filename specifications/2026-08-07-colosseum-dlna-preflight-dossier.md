# Colosseum DLNA Media Server — Preflight Dossier

> **For:** the agent that will create the implementation plan  
> **Read first:** [`2026-08-07-colosseum-dlna-planning-guide.md`](./2026-08-07-colosseum-dlna-planning-guide.md)

**Status:** Reviewed preflight. Product scope is approved; implementation and runtime compatibility remain unverified.  
**Target:** `kingoftheseas56/Colosseum`  
**Repository baseline:** `master` at `a7f2fa31b2b06087086395737cf64c7eeed34a6b`

## 1. Result

The remaining read-only preflight work is complete enough for a planning agent to sequence implementation rather than repeat architecture and protocol research.

**Recommended dependency:** Portable UPnP/libupnp, behind a Colosseum-owned backend interface, conditional on a focused MSVC/build/package/runtime spike.

**Recommended flow:**

```text
DownloadStore ──────────┐
                         ├─> immutable DLNA catalog snapshot
AudiobookDownloader ─────┘       ├─> ContentDirectory
                                 └─> opaque-ID media lookup

SettingsPage <─> native DlnaService <─> libupnp backend
```

The feature remains server-only, LAN-only, opt-in, direct-play-only, and limited to completed Theatre videos and audiobooks.

## 2. Locked Boundary

Included:

- UPnP AV MediaServer discovery on the same LAN;
- disabled by default;
- completed Theatre movies and episodes;
- completed audiobooks and ordered tracks;
- basic metadata and available artwork;
- HTTP direct play and single-range seeking;
- live catalog additions/removals;
- stable UUID across restarts;
- settings beside the porn filter on the existing global Settings page.

Excluded:

- client/control-point or renderer behavior;
- remote control;
- transcoding;
- internet exposure or router mappings;
- active, partial, paused, failed, ebook, comic, or subtitle resources;
- resume-position synchronization;
- formal DLNA certification claims.

Do not reopen this scope without contradictory current repository evidence.

## 3. Confirmed Colosseum Seams

All paths were inspected at the baseline commit and must be rechecked at current `master`.

### Completed videos

Owner:

- [`native/player/downloadstore.h`](https://github.com/kingoftheseas56/Colosseum/blob/a7f2fa31b2b06087086395737cf64c7eeed34a6b/native/player/downloadstore.h)
- [`native/player/downloadstore.cpp`](https://github.com/kingoftheseas56/Colosseum/blob/a7f2fa31b2b06087086395737cf64c7eeed34a6b/native/player/downloadstore.cpp)

`DownloadStore::downloadedVideos()` returns:

`id`, `kind`, `title`, `subtitle`, `seriesTitle`, `season`, `episode`, `path`, `art`, `bytes`, `addedAt`, `missing`.

Mutation signals:

- `libraryChanged()`
- `removed(id)`

Use `id` as the stable source identity. `path` is private and must never appear in URLs, XML, UI status, or normal logs.

### Completed audiobooks

Owner:

- [`native/engine/AudiobookDownloader.h`](https://github.com/kingoftheseas56/Colosseum/blob/a7f2fa31b2b06087086395737cf64c7eeed34a6b/native/engine/AudiobookDownloader.h)
- [`native/engine/AudiobookDownloader.cpp`](https://github.com/kingoftheseas56/Colosseum/blob/a7f2fa31b2b06087086395737cf64c7eeed34a6b/native/engine/AudiobookDownloader.cpp)

`downloadedAudiobooks()` returns:

`id`, `title`, `author`, `dir`, `fileCount`, `bytes`, `addedAt`, `bookId`, `bookPath`, `missing`.

`localFiles(pairKey)` returns existing audio files in stored order. That order is authoritative.

Mutation signals:

- `finished(pairKey, dirPath)`
- `removed(pairKey)`

### UI and construction

- [`native/engine/LocalDownloads.h`](https://github.com/kingoftheseas56/Colosseum/blob/a7f2fa31b2b06087086395737cf64c7eeed34a6b/native/engine/LocalDownloads.h) is the Downloads-page read model. Do not turn it into a network service.
- [`qml/ContentPreferences.qml`](https://github.com/kingoftheseas56/Colosseum/blob/a7f2fa31b2b06087086395737cf64c7eeed34a6b/qml/ContentPreferences.qml) owns only the explicit-content preference. Keep it unchanged.
- [`qml/SettingsPage.qml`](https://github.com/kingoftheseas56/Colosseum/blob/a7f2fa31b2b06087086395737cf64c7eeed34a6b/qml/SettingsPage.qml) renders the global setting card.
- [`qml/Main.qml`](https://github.com/kingoftheseas56/Colosseum/blob/a7f2fa31b2b06087086395737cf64c7eeed34a6b/qml/Main.qml) injects objects into Settings.
- [`native/main.cpp`](https://github.com/kingoftheseas56/Colosseum/blob/a7f2fa31b2b06087086395737cf64c7eeed34a6b/native/main.cpp) constructs native services and QML context properties.

At the baseline, `AudiobookDownloader` exists before `DownloadStore`; `LocalDownloads` is created after `DownloadStore`. Construct DLNA after `DownloadStore` exists and before QML loads, then expose a separate `Dlna` context property.

Add an explicit `aboutToQuit` stop path even though native objects are application-owned.

### Build and tests

- [`native/CMakeLists.txt`](https://github.com/kingoftheseas56/Colosseum/blob/a7f2fa31b2b06087086395737cf64c7eeed34a6b/native/CMakeLists.txt): C++17, Qt 6, CMake, MSVC-aware; Qt Network is already linked.
- [`tests/CMakeLists.txt`](https://github.com/kingoftheseas56/Colosseum/blob/a7f2fa31b2b06087086395737cf64c7eeed34a6b/tests/CMakeLists.txt): deterministic harnesses belong in CTest.
- [`docs/colosseum-test-verification.md`](https://github.com/kingoftheseas56/Colosseum/blob/a7f2fa31b2b06087086395737cf64c7eeed34a6b/docs/colosseum-test-verification.md): future verification commands and evidence must be recorded here.

### Protected existing server

[`native/player/streamserver.h`](https://github.com/kingoftheseas56/Colosseum/blob/a7f2fa31b2b06087086395737cf64c7eeed34a6b/native/player/streamserver.h) is a loopback Stremio/torrent playback service, not DLNA. Keep it loopback-only and lifecycle-independent.

## 4. Responsibility and Thread Model

Conceptual owners:

| Responsibility | Owner |
|---|---|
| persisted settings, QML state, lifecycle, errors | `DlnaService` |
| source normalization and immutable snapshots | `DlnaCatalog` |
| SDK lifecycle and callback translation | `IDlnaBackend` plus libupnp adapter |
| device/service XML and SOAP dispatch | protocol backend |
| deterministic DIDL-Lite | pure serializer |
| opaque-ID file lookup and per-request handles | media adapter |
| controls/status | `SettingsPage.qml` |

Likely new area: `native/net/dlna/`; the planning agent must confirm current conventions before freezing paths.

Thread rules:

- source objects and `DlnaService` remain on the Qt/application thread;
- libupnp callbacks may run on SDK worker threads;
- callbacks never call QML or downloader QObjects directly;
- capture source rows on their owning thread, normalize, then atomically publish an immutable snapshot;
- a browse/open operation holds its snapshot or request-local file handle until completion;
- backend status crosses to Qt through queued delivery;
- coalesce bursty source signals before rebuilding.

## 5. Dependency Decision

### Verdict

Use [Portable UPnP/libupnp](https://github.com/pupnp/pupnp), conditionally.

Primary-source evidence shows APIs for interface-scoped initialization, root-device registration, advertisements, GENA subscriptions/notifications, orderly unregister/finish, a built-in web server, and virtual `get_info/open/read/seek/close` callbacks. The repository uses BSD-3-Clause licensing.

Prefer its built-in web server for Version 1. Avoid a second Qt HTTP server unless the spike proves a named requirement cannot be met.

Rejected defaults:

- **Platinum:** GPLv2-or-later unless commercially licensed; poor default fit for preserving an MIT distribution.
- **Qt-native UPnP:** Qt supplies transport primitives, but Colosseum would own SSDP, SOAP, GENA, descriptions, compatibility quirks, and maintenance.
- **Sidecar server:** duplicates indexing/configuration and adds packaging/process lifecycle.

### Mandatory first spike

Before production work, prove:

1. selected current security-fixed libupnp tag and licence/notice obligations;
2. MSVC/CMake build and link in Colosseum’s supported environment;
3. runtime packaging;
4. initialization on a named non-loopback IPv4 interface;
5. registration, advertisement, `M-SEARCH`, and `byebye`;
6. virtual resource `GET`, `HEAD`, read, seek, close;
7. closed, open-ended, and suffix ranges;
8. offsets and sizes above 4 GiB;
9. no callbacks after unregister/finish;
10. re-initialization after interface change;
11. discovery by current Kodi and VLC.

Stop and return evidence if build, packaging, teardown, large-file seeking, licensing, or current security review fails. Do not silently replace libupnp with a custom protocol stack.

## 6. Service Contract

QML-facing native authority, recommended context name `Dlna`.

Writable defaults:

- `enabled=false`
- `deviceName="Colosseum"`
- `shareVideos=true`
- `shareAudiobooks=true`

Read-only status:

- state: `off`, `starting`, `online`, `stopping`, `error`;
- human-readable status;
- active address and port;
- visible item count;
- last error.

Persist these plus a stable UUID in a dedicated DLNA settings group. `enabled` is desired state; runtime failure must not silently rewrite it.

Startup occurs after the event loop begins:

```text
settings
→ initial snapshot
→ safe LAN interface
→ libupnp init
→ bounded SOAP size
→ virtual callbacks
→ device/services registration
→ advertise
→ Online
```

Shutdown:

```text
Stopping
→ reject new work
→ unregister/byebye
→ detach virtual resources
→ UpnpFinish as final SDK call
→ release requests
→ Off
```

`off` is reported only after advertisements/listeners are gone.

Runtime changes:

- device rename: controlled re-registration, same UUID;
- source toggle: new visible snapshot and event update, no app restart;
- completion/removal: coalesced snapshot update;
- interface loss: clean leave and safe rebind, otherwise `error`;
- port collision: another safe port, same UUID.

## 7. Catalog Contract

Eligibility requires:

- completed source row;
- `missing == false`;
- existing regular file;
- size greater than zero;
- not temporary/partial;
- supported MIME mapping;
- enabled source category.

Hierarchy:

```text
0 Colosseum
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

Ordering is case-insensitive and deterministic:

- movies by title then ID;
- episodes by season, episode, title, ID;
- books by author/title/ID;
- tracks exactly by `localFiles()` order.

### Opaque identity

Root is `id="0"`, `parentID="-1"`. Fixed top-level IDs may be readable literals.

Source-derived IDs are path-free:

```text
<type-prefix> + base64url(
  SHA-256("colosseum-dlna-v1" + NUL + canonical-source-key)
)
```

Keys:

- video item: `video:` + DownloadStore `id`;
- series: normalized `seriesTitle`;
- season: normalized `seriesTitle` + numeric season;
- book: `audiobook:` + audiobook `id`;
- author: normalized author;
- track: audiobook `id` + stored ordinal.

Normalize Unicode, trim/collapse whitespace, and case-fold synthetic metadata keys. Detect collisions; never use a path as disambiguation.

### Metadata mapping

Movies:

- `dc:title = title`
- class `object.item.videoItem.movie`
- `bytes` verified against file before `res@size`
- `art` optional

Episodes:

- hierarchy from `seriesTitle`, `season`, `episode`
- class `object.item.videoItem`
- no invented non-standard episode subclass

Audiobooks:

- author and book are containers;
- each ordered file is `object.item.audioItem.audioBook`;
- `dc:creator = author`;
- order comes from Browse result order;
- do not pretend music-track metadata is semantically correct without client evidence.

The confirmed audiobook row has no dedicated cover field. Omit art or use a packaged generic image; do not parse ebook files just to obtain a cover.

## 8. Minimal UPnP AV Profile

Official source collection: [OCF UPnP resources](https://openconnectivity.org/developer/specifications/upnp-resources/upnp/).

Device:

```text
urn:schemas-upnp-org:device:MediaServer:1
```

Required services:

```text
urn:schemas-upnp-org:service:ContentDirectory:1
urn:schemas-upnp-org:service:ConnectionManager:1
```

Do not advertise AVTransport.

### ContentDirectory

Implement:

- `GetSearchCapabilities` → empty;
- `GetSortCapabilities` → empty;
- `GetSystemUpdateID`;
- `Browse`.

Do not expose Search. Accept empty `SortCriteria`; unsupported non-empty sort returns `709`.

Browse supports:

- `BrowseMetadat`
- `BrowseDirectChildren`
- `ObjectID`, `Filter`, `StartingIndex`, `RequestedCount`, `SortCriteria`
- `Result`, `NumberReturned`, `TotalMatches`, `UpdateIDa

Rules:

- `RequestedCount=0` means all remaining children;
- total count is before pagination;
- metadata browse returns one object;
- unknown object returns `701`;
- XML is UTF-8 and escaped.

Event:

- `SystemUpdateID`
pdate ID 0 info and invalid-ID error;
- event state.

**Lifecycle with fake backend**

- default off and isolated persistence;
- startup success/failure;
- no premature online;
- disable completes backend stop before off;
- rename re-registration;
- source-toggle update;
- app shutdown;
- worker callback queued to Qt.

**Media adapter**

- GET/HEAD;
- closed/open/suffix and unsatisfiable ranges;
- malformed/multiple-range safe behavior;
- unknown/removed ID;
- deletion after open;
- ignored slug;
- traversal/reparse rejection;
- 64-bit sparse-file tests.

Tests use temporary settings and media roots, never real user data.

### Opt-in integration harness

Provide one synthetic MediaServer fixture that:

- runs without full QML;
- prints UUID/address/port/state;
- records SOAP actions and ranges;
- supports packet capture and Kodi/VLC inspection;
- stops cleanly with byebye.

It is a harness, not a second production implementation.

### Live matrix

Require discovery, browse, video play/seek, ordered audiobook play, and disable/byebye in:

- current Kodi;
- current VLC;
- one real TV or console.

Also verify:

- restart UUID stability;
- completion/removal while online;
- rename/toggles;
- sleep/wake and network reconnect;
- active transfer during disable;
- Windows firewall behavior;
- file larger than 4 GiB;
- no DLNA traffic when disabled;
- no IGD requests.

Record exact commands and evidence in `docs/colosseum-test-verification.md`.

## 13. Execution-Only Unknowns

Do not resolve these by assumption:

1. exact libupnp tag and package shape;
2. MSVC static/dynamic runtime behavior;7. actual formats/codecs produced by every Theatre source;
8. client-specific protocolInfo/DIDL quirks;
9. stable audiobook artwork join;
10. supported concurrent streams;
11. sleep/wake and network-change behavior.

Each has a spike or test above.

## 14. Planning-Agent Handoff
Before writing the implementation plan:
1. diff current Colosseum seams against `a7f2fa31b2b06087086395737cf64c7eeed34a6b`;
2. confirm exact paths and ownership;
3. make the libupnp spike the first gate;
4. mark paths confirmed/likely/unknown;
5. preserve protected ownership and locked scope;
6. map every work slice to deterministic or live proof;
7. include rollback/containment for an opt-in LAN service;
8. leave compatibility unverified until the live matrix runs.

Do not:
- reuse torrent `StreamServer`;
- make `ContentPreferences` own DLNA;
- write a custom UPnP stack without returning for a new decision;
- add transcoding, remote control, ebooks, comics, or internet access;
- claim client compatibility before evidence.

**First planning action:** produce a current seam-diff and a libupnp spike task with explicit pass/fail evidence, then sequence production work.

## 15. Sources and Status Boundary

Primary sources:
- [Colosseum baseline commit](https://github.com/kingoftheseas56/Colosseum/commit/a7f2fa31b2b06087086395737cf64c7eeed34a6b)
- [Portable UPnP/libupnp](https://github.com/pupnp/pupnp)
- [libupnp public API](https://github.com/pupnp/pupnp/blob/main/upnp/inc/upnp.h)
- [libupnp web server](https://github.com/pupnp/pupnp/blob/main/upnp/src/genlib/net/http/webserver.c)
- [OCF UPnP resources](https://openconnectivity.org/developer/specifications/upnp-resources/upnp/)
- [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html)
- [Platinum SDK](https://github.com/axiomatic-systems/Platinum)
- [Kodi UPnP server reference](https://github.com/xbmc/xbmc/blob/master/xbmc/network/upnp/UPnPServer.cpp)
- [Kodi licence](https://github.com/xbmc/xbmc/blob/master/LICENSE.md)
Kodi is behavior reference only; do not copy its source.

This dossier captures repository seams, source fields, protocol behavior, dependency recommendation, lifecycle/thread/security contracts, and verification gates. It does not prove libupnp builds, the feature exists, tests pass, firewall behavior works, or clients can discover/play Colosseum. Those claims require fresh execution evidence.
