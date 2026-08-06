# Local Media Launch Slice 3C — Player 1/libmpv Adapter Reference Implementation Bundle r3

## Status

**Design approved; probe correction incorporated from Agent 0's compiled-and-run evidence. Reference implementation candidate only; unadopted and not independently runtime-verified by Preflight Architect.**

This immutable r3 supersedes bundle manifest r2. It changes only the canonical Code Part 01 pointer and the admission success semantics.

## Basis

- Colosseum: `master@a40333dc1fc9823ceb9decd811deeadde6ac4c2d`
- Decisions: A1+B1 remain approved.
- Agent 0 execution report: `LML-3C-MPV-05` proved P0 rejects valid media and made the strengthening branch mandatory.

## Canonical Parts

1. `handoffs/2026-08-06-colosseum-local-media-launch-slice-3c-code-01-libmpv-admission-probe-r2.md`
   - P4 option policy;
   - `MPV_EVENT_FILE_LOADED` is diagnostic only;
   - admission requires observed `dwidth > 0`;
   - cancellation, timeout, generation, and no-session-before-admission invariants preserved.

2. `handoffs/2026-08-06-colosseum-local-media-launch-slice-3c-code-02-launch-continuity-fingerprint-r1.md`
   - unchanged.

3. `handoffs/2026-08-06-colosseum-local-media-launch-slice-3c-code-03-player1-external-local-qml-r1.md`
   - unchanged.

4. `handoffs/2026-08-06-colosseum-local-media-launch-slice-3c-code-04-tests-build-adoption-r1.md`
   - unchanged except that `LML-3C-MPV-05` must apply Code Part 01 r2's decoded-frame criterion.

## Superseded Probe Rule

The following combination is prohibited:

```text
vid=no
audio=no
admit on MPV_EVENT_FILE_LOADED
```

It cannot establish video decodability and was reported to reject a valid H.264 MP4 with libmpv error `-16`.

## Canonical Admission Rule

```text
config=no
load-scripts=no
audio=no
vo=null
idle=yes
video remains enabled
observe dwidth as MPV_FORMAT_INT64
admit only when dwidth > 0
```

`MPV_EVENT_END_FILE`, timeout, cancellation, shutdown, or source metadata change before positive decoded-frame evidence produces no shell session.

## Ownership

Agent 0 owns execution, fixture discrimination, latency measurement, reconstruction, adoption decisions, divergence reporting, and runtime verification.

## Exact Next Action

Agent 0 reruns the smallest bare-libmpv harness with Code Part 01 r2 and reports the full fixture matrix, event order, latency, selected timeout, and any installed-libmpv divergence before reconstructing the adapter.

## Verification Notes

- **Test-reported:** P0 failure and the need for P4/decoded-frame evidence.
- **Designed:** the corrected immutable reference bundle.
- **Requires execution evidence:** compilation, full fixture discrimination, cancellation bounds, adoption, regressions, and user-visible runtime validation.
