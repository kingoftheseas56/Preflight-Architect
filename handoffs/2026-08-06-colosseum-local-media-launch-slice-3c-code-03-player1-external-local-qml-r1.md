# Local Media Launch Slice 3C — Code Part 03: Player 1 External-Local Isolation r1

## Status

**Reference implementation candidate; uncompiled, untested, unexecuted, unadopted, and runtime-unverified.**

## Governing Rule

Do not overload or refactor shipped `playLocalFile()` behavior. That path serves downloaded files with stream-grade identity, subtitle discovery, and global Continue semantics.

Add a distinct external-local entrypoint or a thin adapter with an explicit mode flag. Agent 0 may choose the final flag-versus-thin-adapter shape at adoption, but the behavioral boundary below is fixed.

## Proposed PlayerPage State

```qml
property bool externalLocalMode: false
property string externalLocalId: ""
property int externalLocalGeneration: 0
property bool externalLocalFingerprintStarted: false
```

## Mode Reset

Every non-external top-level playback entrypoint must clear the mode before doing any work:

```qml
function leaveExternalLocalMode() {
    root.externalLocalMode = false
    root.externalLocalId = ""
    root.externalLocalGeneration = 0
    root.externalLocalFingerprintStarted = false
}
```

At minimum, call this at the start of the current downloaded-file, arriving-file, torrent, direct-stream, live-TV, and hosted-player entrypoints that can reuse the same PlayerPage instance.

This is a discovery gate: enumerate all production routes that can call `mpv.loadFile()` or replace the active source. Do not assume the examples above are exhaustive.

## Dedicated Entry Point

```qml
function playExternalLocalFile(target) {
    var t = target || ({})

    root.externalLocalMode = true
    root.externalLocalId = String(t.localMediaId || t.id || "")
    root.externalLocalGeneration = Number(t.localGeneration || 0)
    root.externalLocalFingerprintStarted = false

    root.arrivingStreamUrl = ""
    root.clearAbLoop()
    root.cancelSleepTimer()
    root.resetSkipSegments()
    root.resetTrackAutomation()
    root.cancelUpNext()
    root.autoPausedInactive = false
    root.deadStreamKeys = ({})
    root.stubCheckedKey = ""
    root.streamCandidates = []
    root.currentStreamIndex = -1
    root.adjacentEpisodes = ({})

    root.mediaTitle = String(t.title || "")
    root.mediaTransport = "Local file"
    root.mediaYear = ""
    root.mediaArt = ""
    root.mediaLogo = ""
    root.mediaLoadingArt = ""
    root.mediaLoadingLine = ""
    root.mediaLocalPath = String(t.path || t.localPath || "")
    root.mediaId = root.externalLocalId
    root.mediaResumeHash = ""
    root.mediaResumeFileIdx = 0
    root.currentPlaybackUrl = root.mediaLocalPath

    // Isolation: embedded/local subtitles remain available through mpv,
    // but provider discovery is Slice 8 and must not run here.
    root.subStreamType = ""
    root.subStreamId = ""
    root.onlineSubs = []
    root.addedOnlineUrls = ({})
    root.subsLoading = false
    root.autoSubDone = false

    root.pendingSeekSec =
        Number(t.position || 0) > 0 ? Number(t.position) : -1
    root.resumeChoiceOpen = false
    root.resumeChoiceSec = -1
    root.resumePromptConsumed = true

    root.errored = false
    root.starting = true
    root.fileReady = false
    root.statusMsg = "Opening..."
    root.closeMenus()
    root.wakeChrome()
    root.forceActiveFocus()
    root.resetRecoveryWatch()

    mpv.loadFile(root.mediaLocalPath)

    // Deliberately omitted:
    //   root.fetchSubtitles()
    //   root.maybeHydrateContext()
    //   any Progress/Continue/account call
}
```

The existing `playLocalFile(target)` remains byte-for-byte unchanged except for an optional first-line call to `leaveExternalLocalMode()` if the PlayerPage instance can transition from external-local playback to downloaded playback.

## Dispatcher Branch

At the existing movie-session dispatch seam:

```qml
if (target.localExternal === true) {
    player.playExternalLocalFile(target)
} else {
    player.playLocalFile(target)
}
```

Do not infer external-local mode from a `"local:" + path` ID. The authoritative marker is `target.localExternal === true`, and the authoritative identity is the opaque Slice 2 `localMediaId`.

## Progress Isolation

Add the branch before the existing global `Progress` checks:

```qml
function recordProgress(silent) {
    if (root.externalLocalMode) {
        if (root.externalLocalId.length
                && mpv.duration > 0
                && mpv.position >= 0) {
            LocalExternalVideo.recordProgress(
                root.externalLocalId,
                mpv.position,
                mpv.duration,
                false)
        }
        return
    }

    // Existing implementation remains unchanged below.
    // ...
}
```

This permits the existing 5-second timer and lifecycle call sites to remain intact while guaranteeing that external-local state never reaches `Progress.recordSilent()` or `Progress.record()`.

If the Player lane owner prefers a thin adapter instead of this branch, it must prove the same negative call invariant with spies.

## Resume

Keep the existing deferred seek mechanism:

```qml
root.pendingSeekSec =
    Number(t.position || 0) > 0 ? Number(t.position) : -1
```

Apply it only after the actual Player 1 file-loaded signal through the existing seek path. The launch adapter already forces completed media to position zero.

## Playback-Started Fingerprint Gate

Use the PlayerPage’s existing `playbackStarted` truth, which requires a non-error active player and position advancement.

```qml
onPlaybackStartedChanged: {
    if (!root.externalLocalMode
            || !root.playbackStarted
            || root.externalLocalFingerprintStarted
            || !root.externalLocalId.length)
        return

    root.externalLocalFingerprintStarted = true
    LocalExternalVideo.playbackStarted(
        root.externalLocalId,
        root.mediaLocalPath,
        root.externalLocalGeneration)
}
```

The live gate must timestamp:

```text
visual playbackStarted
fingerprint job started
```

and prove the first precedes the second.

## Completion

Attach an external-local-only EOF branch to the existing `MpvItem::endFile(reason)` signal:

```qml
Connections {
    target: mpv

    function onEndFile(reason) {
        if (!root.externalLocalMode)
            return

        if (String(reason).toLowerCase() === "eof") {
            LocalExternalVideo.recordProgress(
                root.externalLocalId,
                0,
                mpv.duration,
                true)
        }
    }
}
```

Do not infer completion from duration fraction alone in this slice. Live libmpv EOF evidence is the completion authority.

## Source Unavailable

For an external-local source error after session creation:

```qml
Connections {
    target: mpv

    function onPlaybackError(code, message) {
        if (!root.externalLocalMode)
            return

        var unavailable =
            LocalExternalVideo.handlePlaybackError(
                root.externalLocalId,
                String(code || ""),
                String(message || ""))

        root.errored = true
        root.starting = false
        root.statusMsg = unavailable
            ? "Source unavailable"
            : (String(message || "").length
               ? String(message)
               : "Playback failed")

        // Deliberately do not call Sessions.close() for either category.
        // Retry / Locate / Close actions belong to Slice 6.
    }
}
```

The execution agent must inspect existing generic playback-error handlers. If one closes the active session, add an external-local guard at that exact lifecycle boundary; do not globally weaken normal stream recovery.

## Subtitle and Network Boundary

On external-local open:

- `fetchSubtitles()` is never called;
- `Subtitles.fetch()` is unreachable;
- `subStreamType` and `subStreamId` are empty;
- embedded subtitles remain visible through `MpvItem.subtitleTracks`;
- user-selected local subtitle attachment remains allowed;
- online provider search remains deferred to Slice 8.

## Account and Continue Boundary

On external-local playback:

- `Progress.get()` is not used for resume;
- `Progress.recordSilent()` is never called;
- `Progress.record()` is never called;
- no account API receives local identity, path, state, or fingerprint;
- Slice 2 is the only continuity authority.

## Required Regression Protection

Prove unchanged behavior for shipped downloaded files:

1. `playLocalFile()` still uses stream-grade `id`;
2. it still calls `fetchSubtitles()`;
3. it still records global Continue progress;
4. arriving/download handoff remains unchanged;
5. normal torrent/direct/live playback remains unchanged.

## Completion Criterion

This part is adoption-ready when a QML harness with provider and persistence spies proves both positive external-local behavior and negative network/global-progress behavior, while downloaded-file regression cases remain green.
