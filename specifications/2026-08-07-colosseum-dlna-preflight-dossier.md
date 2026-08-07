# Colosseum DLNA Media Server — Preflight Dossier

> **For:** the agent that will create the implementation plan  
> **Read first:** [`2026-08-07-colosseum-dlna-planning-guide.md`](./2026-08-07-colosseum-dlna-planning-guide.md)

**Status:** Reviewed preflight. Product scope is approved; implementation and runtime compatibility are unverified.  
**Target:** `kingoftheseas56/Colosseum`  
**Repository evidence baseline:** `master` at `a7f2fa31b2b06087086395737cf64c7eeed34a6b`

## 1. Result

The planning agent should sequence known work rather than rediscover the product or protocol design.

Colosseum will expose completed Theatre videos and downloaded audiobooks as an opt-in, read-only UPnP AV MediaServer on the same LAN. It remains server-only, direct-play-only, disabled by default, and isolated from the existing torrent `StreamServer`.

## 2. Locked Scope

Included:

- completed Theatre movies and episodes;
- completed audiobooks in stored track order;
- SSDP discovery, browse, direct HTTP playback, and byte-range seeking;
- live catalog updates and stable UUID;
- settings beside the existing porn-filter control.

Excluded:

- renderer/control-point behavior, remote control, transcoding;
- internet exposure or IGD/router mappings;
- partial or failed downloads, ebooks, comics, and subtitles;
- playback-position synchronization and certification claims.

## 3. Confirmed Colosseum Seams

Recheck these at current `master` before freezing paths:

- `native/player/downloadstore.h/.cpp`: completed Theatre records; `libraryChanged()` and `removed(id)`.
- `native/engine/AudiobookDownloader.h/.cpp`: downloaded audiobook records; ordered `localFiles(pairKey)`; `finished(...)` and `removed(...)`.
- `native/engine/LocalDownloads.h/.cpp`: Downloads-page read model only; do not turn it into a network service.
- `qml/ContentPreferences.qml`: porn-filter preference only; keep DLNA separate.
- `qml/Main.qml` and `qml/SettingsPage.qml`: global object injection and settings UI.
- `native/main.cpp`: native construction, QML exposure, and shutdown wiring.
- `native/CMakeLists.txt` and `tests/CMakeLists.txt`: build and deterministic test registration.
- `native/player/streamserver.h/.cpp`: loopback torrent playback only; never expose it to the LAN.

## 4. Responsibility Map, Not Class Mandate

These rows are ownership seams, not a requirement for one class or file per row.

| Concern | Required owner |
|---|---|
| Settings, lifecycle, QML status | One native DLNA authority |
| Source normalization and immutable snapshots | Catalog responsibility |
| SSDP, SOAP, GENA, SDK callbacks | Backend responsibility |
| DIDL-Lite generation | Pure deterministic seam |
| Opaque-ID lookup and file reads | Media-serving seam |
| Controls and status | Existing Settings page |

Use the smallest implementation that preserves these boundaries.

## 5. Dependency Decision

**Recommendation:** Portable UPnP/libupnp behind a Colosseum-owned backend interface, conditional on a focused spike.

Reasons:

- BSD-3-Clause licensing fits Colosseum's MIT distribution;
- device registration, advertisements, eventing, lifecycle, web serving, and virtual-file callbacks already exist;
- it avoids implementing SSDP, SOAP, GENA, and compatibility behavior from scratch.

Kodi is behavior reference only. Do not copy Kodi source.

## 6. Mandatory Dependency Spike

Before production planning, prove:

1. a current security-fixed libupnp release and notice obligations;
2. MSVC/CMake build and link in Colosseum's supported environment;
3. Windows packaging;
4. bind to a named non-loopback IPv4 interface;
5. register, advertise, answer `M-SEARCH`, and emit `byebye`;
6. virtual `GET`, `HEAD`, read, seek, and close;
7. closed, open-ended, and suffix byte ranges;
8. offsets and sizes above 4 GiB;
9. no callbacks after unregister/finalize;
10. reinitialization after interface change;
11. discovery by current Kodi and VLC;
12. an application-controlled validation seam before GENA subscription acceptance.

Stop and report evidence if licensing, build, packaging, teardown, large-file, security, or discovery gates fail.

## 7. Service Contract

Expose one native QML authority, recommended context name `Dlna`.

Writable defaults:

- `enabled=false`
- `deviceName="Colosseum"`
- `shareVideos=true`
- `shareAudiobooks=true`

Read-only state:

- `off`, `starting`, `online`, `stopping`, or `error`;
- status text, address, port, visible item count, and last error.

Persist settings and a stable UUID in a dedicated DLNA settings group. `enabled` is desired state; startup failure must not silently overwrite it. Report `off` only after advertisements and listeners are gone.

## 8. Catalog Contract

Network callbacks consume immutable snapshots and never call QML or source `QObject`s directly.

Confirmed video fields at the evidence baseline:

`id`, `kind`, `title`, `subtitle`, `seriesTitle`, `season`, `episode`, `path`, `art`, `bytes`, `addedAt`, `missing`.

Confirmed audiobook fields:

`id`, `title`, `author`, `dir`, `fileCount`, `bytes`, `addedAt`, `bookId`, `bookPath`, `missing`; track order comes from `localFiles(pairKey)`.

Eligibility requires completed state, `missing == false`, an existing regular non-temporary file, positive size, supported MIME mapping, and an enabled source category.

Hierarchy:

```text
Colosseum
├── Videos
│   ├── Movies
│   └── TV Shows → Series → Season → Episode
└── Audiobooks → Author → Book → Track
```

IDs must be stable, opaque, path-free, collision-checked, and based on source identity plus track ordinal. Missing artwork never hides playable media.

## 9. Minimal UPnP AV Profile

Advertise:

- `urn:schemas-upnp-org:device:MediaServer:1`
- `urn:schemas-upnp-org:service:ContentDirectory:1`
- `urn:schemas-upnp-org:service:ConnectionManager:1`

Do not advertise `AVTransport`.

ContentDirectory implements:

- `GetSearchCapabilities` → empty;
- `GetSortCapabilities` → empty;
- `GetSystemUpdateID`;
- `Browse`.

`Browse` supports **`BrowseMetadata`** and **`BrowseDirectChildren`**, pagination, accurate `NumberReturned`, `TotalMatches`, and **`UpdateID`**. `RequestedCount=0` means all remaining children. Unknown objects return UPnP error `701`; unsupported non-empty sort returns `709`.

ConnectionManager implements `GetProtocolInfo`, `GetCurrentConnectionIDs`, and valid/invalid `GetCurrentConnectionInfo` behavior.

## 10. Eventing Contract

Event at least:

- ContentDirectory: `SystemUpdateID`, optionally `ContainerUpdateIDs`;
- ConnectionManager: `SourceProtocolInfo`, `SinkProtocolInfo`, `CurrentConnectionIDs`.

A successful subscription receives initial state. Visible catalog changes increment `SystemUpdateID`. Event delivery must be bounded and must not block catalog or media work.

## 11. GENA Callback Containment

Treat SUBSCRIBE callback URLs as untrusted network input.

Application-level policy:

- accept subscriptions only from the selected LAN interface/subnet;
- accept at most one HTTP callback URL;
- resolve once and pin one numeric IPv4 destination;
- require the destination to remain on the selected subnet;
- reject loopback, link-local, multicast, unspecified, public, other-private-subnet, user-info, fragments, non-HTTP schemes, redirects, proxies, and cross-interface routes;
- do not re-resolve DNS during notification delivery;
- bound subscription lifetime, callback timeout, retries, body size, and queued notifications;
- remove subscriptions after repeated delivery failure.

The dependency spike fails if Colosseum cannot validate the callback before notifications are sent. Add negative tests for the CallStranger/CVE-2020-12695 class.

## 12. XML Hardening

For device, SOAP, and event XML:

- reject `DOCTYPE`;
- disable external general and parameter entities;
- disable XInclude and filesystem/network entity loading;
- cap request body at 64 KiB;
- cap nesting depth at 32, nodes at 4096, attributes per element at 64, and individual text/attribute values at 16 KiB;
- reject malformed, over-limit, or trailing-content documents before executing partial actions.

Prefer a parser mode that never constructs DTD/entity machinery. Test entity expansion, external entities, deep trees, oversized values, and oversized bodies.

## 13. `protocolInfo` Is the First Compatibility Gate

After dependency viability, validate `protocolInfo` before building the full catalog.

For every actual downloaded container/extension:

1. inspect the produced file and MIME mapping;
2. emit the minimal standards-correct value in the form `http-get:*:<mime>:<additional-info>`;
3. claim `DLNA.ORG_OP=01` only after byte-range seeking is proven;
4. add DLNA profile names or conversion flags only when confirmed for the exact media;
5. test discovery, display, play, and seek in Kodi, VLC, and one real TV/console.

Do not infer codec/profile claims from extensions. A client rejection or broken seek blocks expansion to the full catalog.

## 14. HTTP Media Contract

Advertise path-free URLs:

```text
http://<lan-address>:<port>/media/<opaque-id>/<ignored-safe-slug>
```

Required:

- `GET`, `HEAD`, and full responses;
- one closed, open-ended, or suffix byte range;
- `206` with valid `Content-Range`;
- `416` with `Content-Range: bytes */<size>`;
- `Accept-Ranges: bytes`, correct MIME and length;
- 64-bit offsets, bounded-memory reads, and disconnect cancellation;
- `404` for unknown, removed, or missing IDs.

Resolve IDs against the current snapshot and canonicalize/revalidate immediately before open. Never accept a filesystem path from the request. Symlink/reparse replacement must not escape the approved file. An already-open handle may complete or fail after deletion but must never retarget.

## 15. Concurrency and Backpressure

Version 1 must support at least **three simultaneous media transfers**, including multiple reads of one file, while browse, eventing, disable, and shutdown stay responsive.

The implementation may use a conservative internal cap of at least three; it is not a user setting. It must:

- use bounded per-request buffers and bounded control/event queues;
- avoid unbounded thread creation or full-file buffering;
- prevent one slow client from starving others;
- reject excess new transfers promptly with HTTP `503` and bounded `Retry-After`, not an unbounded queue;
- cancel active work cleanly during disable/shutdown.

Measure memory, threads, throughput, and control-plane latency with one, three, and over-cap clients before changing the cap.

## 16. Network and Lifecycle Boundary

Version 1 is IPv4 LAN-only.

- never bind or advertise on loopback;
- never issue IGD/router requests;
- fail closed if no safe interface exists;
- rebind and re-advertise after network changes;
- keep SDK/protocol work off the GUI thread;
- queue status back to the Qt thread;
- add explicit application shutdown ordering.

Startup:

`settings → snapshot → safe interface → SDK init → XML/callback limits → virtual resources → register → advertise → online`

Shutdown:

`stopping → reject new work → unregister/byebye → detach resources → UpnpFinish as final SDK call → release requests → off`

## 17. Settings Placement

Add a Network Sharing card to `qml/SettingsPage.qml` beside the existing global porn-filter setting:

- Enable DLNA sharing;
- Device name;
- Share videos;
- Share audiobooks;
- current status.

`ContentPreferences.qml` remains the porn-filter owner and does not absorb DLNA state.

## 18. Verification Matrix

Deterministic tests cover:

- catalog eligibility, hierarchy, sorting, track order, stable/collision-safe IDs;
- DIDL escaping, `BrowseMetadata`, `BrowseDirectChildren`, pagination, `UpdateID`;
- ConnectionManager actions;
- full/range/invalid/over-4-GiB reads;
- callback URL acceptance/rejection and DNS pinning;
- XML DTD/entity/depth/size limits;
- lifecycle, persistence, rename/toggles, teardown, queued thread delivery;
- three concurrent transfers, responsive browse, and over-cap `503`;
- isolated settings and temporary media roots.

Live matrix covers current Kodi, current VLC, and one real TV/console for discovery, browse, video play/seek, ordered audiobook play, disable/byebye, restart UUID, live add/remove, sleep/wake, firewall behavior, and absence of IGD traffic.

Record exact commands and evidence in Colosseum's test-verification document.

## 19. Execution-Only Unknowns

Do not resolve these by assumption:

1. exact security-fixed libupnp release and package shape;
2. MSVC static/dynamic runtime behavior;
3. Windows deployment and firewall behavior;
4. libupnp callback-validation seam and teardown guarantees;
5. parser configuration used by the selected stack;
6. exact `protocolInfo` values accepted by target clients;
7. actual containers/codecs produced by each Theatre source;
8. stable audiobook artwork join;
9. safe default interface on multi-homed machines;
10. measured stream cap and resource use;
11. sleep/wake and reconnect behavior;
12. client-specific DIDL quirks;
13. malformed or multiple `Range` header policy.

Each needs a named spike or test and recorded evidence.

## 20. Planning-Agent Instructions

Before writing the implementation plan:

1. diff current Colosseum seams against the evidence baseline;
2. confirm exact ownership and paths;
3. make the dependency spike the first gate;
4. make `protocolInfo` compatibility the second gate;
5. sequence the smallest vertical server before full catalog breadth;
6. map every slice to deterministic or live proof;
7. include rollback/containment for the opt-in LAN service;
8. preserve locked scope and protected existing ownership.

Do not:

- reuse the torrent `StreamServer`;
- make `ContentPreferences` own DLNA;
- interpret the responsibility map as a mandatory class count;
- write a custom UPnP stack without returning for a new decision;
- claim client compatibility before the live matrix;
- add transcoding, control, ebooks, comics, or internet access.

## 21. Sources and Status Boundary

Primary references:

- OCF UPnP resources: https://openconnectivity.org/developer/specifications/upnp-resources/upnp/
- Portable UPnP/libupnp: https://github.com/pupnp/pupnp
- NVD CVE-2020-12695: https://nvd.nist.gov/vuln/detail/CVE-2020-12695
- OWASP XML External Entity Prevention: https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html
- RFC 9110: https://www.rfc-editor.org/rfc/rfc9110.html
- Kodi UPnP server, behavior reference only: https://github.com/xbmc/xbmc/blob/master/xbmc/network/upnp/UPnPServer.cpp

This dossier records reviewed preflight decisions. It does not prove that libupnp builds or packages in Colosseum, tests pass, firewall behavior works, or clients can discover or play media. Those claims require fresh execution evidence.
