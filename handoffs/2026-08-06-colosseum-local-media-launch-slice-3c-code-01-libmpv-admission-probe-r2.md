# Local Media Launch Slice 3C — Code Part 01: Bare-libmpv Admission Probe r2

## Status

**Design correction accepted from Agent 0's compiled-and-run evidence. Reference implementation amendment only; not compiled, run, adopted, or independently runtime-verified by Preflight Architect.**

This immutable r2 supersedes `2026-08-06-colosseum-local-media-launch-slice-3c-code-01-libmpv-admission-probe-r1.md` for the libmpv option policy, success condition, event handling, and live-gate expectations. All unaffected r1 contracts remain in force.

## Evidence Received

Agent 0 executed `LML-3C-MPV-05` at Colosseum `master@a40333dc1fc9823ceb9decd811deeadde6ac4c2d` and reported:

- the r1 P0 policy (`vid=no`, `audio=no`) rejects every file, including a valid H.264 MP4;
- the valid file ended with libmpv error `-16` because no audio or video track was enabled;
- P4, with video enabled and null output, discriminates by positive decoded-frame evidence;
- therefore the r1 “strengthening branch” is mandatory, not contingent.

This is **test-reported evidence from Agent 0**, not a test rerun by Preflight Architect.

## Assessment

**Accept.**

The failure is fatal to r1 as adoption input. `MPV_EVENT_FILE_LOADED` is not sufficient admission evidence, and disabling both audio and video makes positive decode impossible. The public cancellation, timeout, generation, typed-error, and no-session-before-admission contracts remain sound.

## Canonical P4 Option Policy

Replace the r1 option block with:

```cpp
// P4: decode video through a null output.
// Do not disable video; admission requires positive decoded-frame evidence.
const bool optionsOk =
    setOption(ctx, "config", "no")
    && setOption(ctx, "load-scripts", "no")
    && setOption(ctx, "audio", "no")
    && setOption(ctx, "vo", "null")
    && setOption(ctx, "idle", "yes");
```

The following r1 option is prohibited:

```cpp
setOption(ctx, "vid", "no")
```

Do not add a visible output, user configuration, scripts, or audio output.

## Positive Decode Observation

After `mpv_initialize(ctx)` succeeds and before dispatching `loadfile`, observe decoded video width:

```cpp
constexpr uint64_t kDecodedWidthObservation = 2;

const int observeResult = mpv_observe_property(
    ctx,
    kDecodedWidthObservation,
    "dwidth",
    MPV_FORMAT_INT64);

if (observeResult < 0) {
    const QString diagnostic =
        QStringLiteral("mpv_observe_property(dwidth) failed: %1")
            .arg(QString::fromUtf8(mpv_error_string(observeResult)));
    destroy();
    return LocalVideoAdmissionResult::failure(
        generation,
        admissionError(
            LocalMediaErrorCode::HandlerRejected,
            QStringLiteral("Colosseum could not inspect that video."),
            diagnostic),
        QStringLiteral("observe-dwidth"),
        observeResult,
        elapsed.elapsed());
}
```

`dwidth` must be treated as decoded-frame evidence only when the observed property value is present and greater than zero.

## Corrected Success Result

Replace r1's success marker:

```cpp
result.mpvEvent = QStringLiteral("file-loaded");
```

with:

```cpp
result.mpvEvent = QStringLiteral("decoded-frame");
```

A positive `MPV_EVENT_FILE_LOADED` may be retained in diagnostics, but it must never return admission success.

## Corrected Event Loop

Replace the r1 `MPV_EVENT_FILE_LOADED` success branch with the following policy:

```cpp
bool fileLoadedSeen = false;

while (elapsed.elapsed() < timeoutMs) {
    if (cancelled->load(std::memory_order_acquire)) {
        destroy();
        return LocalVideoAdmissionResult::failure(
            generation,
            admissionError(
                LocalMediaErrorCode::AdmissionCancelled,
                QString(),
                QStringLiteral("Admission was superseded or cancelled.")),
            QStringLiteral("cancelled"),
            0,
            elapsed.elapsed());
    }

    mpv_event *event = mpv_wait_event(ctx, 0.05);

    switch (event->event_id) {
    case MPV_EVENT_FILE_LOADED:
        // Diagnostic milestone only. Headers/demux admission do not prove decode.
        fileLoadedSeen = true;
        break;

    case MPV_EVENT_PROPERTY_CHANGE: {
        const auto *property =
            static_cast<const mpv_event_property *>(event->data);

        if (!property
            || event->reply_userdata != kDecodedWidthObservation
            || property->format != MPV_FORMAT_INT64
            || !property->data) {
            break;
        }

        const int64_t decodedWidth =
            *static_cast<const int64_t *>(property->data);

        if (decodedWidth <= 0)
            break;

        const qint64 elapsedMs = elapsed.elapsed();
        destroy();
        return LocalVideoAdmissionResult::success(
            generation,
            elapsedMs);
    }

    case MPV_EVENT_END_FILE: {
        const auto *end =
            static_cast<const mpv_event_end_file *>(event->data);
        const int errorCode = end ? end->error : 0;
        const QString errorText =
            errorCode < 0
                ? QString::fromUtf8(mpv_error_string(errorCode))
                : QStringLiteral("end-file before decoded-frame evidence");
        const QString diagnostic =
            QStringLiteral(
                "libmpv ended admission before decoded-frame evidence: "
                "fileLoaded=%1 reason=%2 error=%3 (%4)")
                .arg(fileLoadedSeen)
                .arg(end ? int(end->reason) : -1)
                .arg(errorCode)
                .arg(errorText);
        const qint64 elapsedMs = elapsed.elapsed();
        destroy();
        return LocalVideoAdmissionResult::failure(
            generation,
            admissionError(
                LocalMediaErrorCode::Undecodable,
                QStringLiteral("Colosseum could not decode that video."),
                diagnostic),
            QStringLiteral("end-file"),
            errorCode,
            elapsedMs);
    }

    case MPV_EVENT_SHUTDOWN: {
        const qint64 elapsedMs = elapsed.elapsed();
        destroy();
        return LocalVideoAdmissionResult::failure(
            generation,
            admissionError(
                LocalMediaErrorCode::HandlerRejected,
                QStringLiteral("Colosseum could not inspect that video."),
                QStringLiteral("libmpv shut down during admission.")),
            QStringLiteral("shutdown"),
            0,
            elapsedMs);
    }

    default:
        break;
    }
}
```

The existing r1 timeout return remains after the loop.

## Safety Invariants Preserved

1. No `SessionStore` API is reachable from the probe.
2. No shell session exists until decoded-frame admission succeeds.
3. Cancellation and timeout remain bounded.
4. A stale generation cannot create a session.
5. User configuration, scripts, audio output, and visible video output remain disabled.
6. The probe uses the source bytes read by libmpv and does not mutate the source.
7. A file-loaded event without positive decoded width is never admitted.

## Harness Corrections

Replace the r1 probe pass condition with:

- supported fixture produces `MPV_EVENT_FILE_LOADED`, then an observed `dwidth > 0`, and returns `decoded-frame`;
- corrupt, encrypted/protected, unsupported-codec, missing, and removed-mid-probe fixtures never produce successful decoded-frame admission;
- every rejected fixture returns a typed failure before any shell session exists;
- cancellation and timeout return promptly and cannot deliver stale success;
- report latency from probe start to decoded-frame admission or rejection.

Add a regression that runs the exact former P0 policy against the supported fixture and records its expected failure, so the invalid policy cannot quietly return.

## Bundle Impact

- **Code Part 01 r1:** superseded by this r2 for worker policy and success semantics.
- **Code Parts 02–04:** no design change required. They consume the unchanged typed admission result and already require admission before session creation.
- **Manifest r2:** superseded by manifest r3 only to point at code-01 r2 and record that strengthening is mandatory.
- **A1+B1:** unchanged.
- **Downloaded-file `playLocalFile()`:** unchanged.

## Stop Conditions

Return evidence to Agent 0 rather than weakening admission if:

- `dwidth > 0` occurs for a fixture that Player 1 subsequently cannot decode;
- a supported video never produces positive decoded width through `vo=null`;
- cancellation cannot interrupt the installed libmpv path within the agreed bound;
- P4 causes observable network, account, subtitle-provider, or global-progress activity;
- source replacement during admission cannot be distinguished by the existing post-probe metadata recheck.

## Exact Next Action

Agent 0 should reconstruct this r2 policy in the smallest live harness, rerun the full fixture matrix, report measured latency and event traces, and only then reconstruct the Slice 3C adapter.

## Verification Notes

- **Confirmed by Agent 0's report:** P0 is invalid; valid H.264 was rejected with error `-16`; P4 and decoded-width observation are the required direction.
- **Confirmed from the approved design:** no session before admission; cancellation, timeout, and generation guards remain mandatory.
- **Not independently verified by Preflight Architect:** P4 fixture outcomes, latency, exact installed-libmpv event ordering, compilation, or runtime behavior.
