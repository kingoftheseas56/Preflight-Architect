# Local Media Launch Slice 3C — Code Part 01: Bare-libmpv Admission Probe r3

## Status

**Execution evidence incorporated. Immutable evidence amendment only; not independently compiled, run, adopted, or runtime-validated by Preflight Architect.**

This r3 supersedes `2026-08-06-colosseum-local-media-launch-slice-3c-code-01-libmpv-admission-probe-r2.md` only for measured fixture outcomes, reference error taxonomy, timeout guidance, and regression notes. The r2 P4 option policy, decoded-frame success condition, cancellation, generation, TOCTOU, typed-error, and no-session-before-admission contracts remain unchanged.

## Evidence Received

Agent 0 reconstructed the r2 policy in a standalone MSVC harness using the repository's installed libmpv client API, with no Qt or Colosseum mutation, and reported the following results on issue #1:

| Fixture | Verdict | Total | Evidence / failure |
|---|---:|---:|---|
| supported H.264 MP4 | Admit | 151 ms | `FILE_LOADED`, then `dwidth=320` |
| truncated MP4 | Reject | 27 ms | error `-16` after `FILE_LOADED`, no decoded width |
| garbage MKV | Reject | 103 ms | error `-17` |
| corrupt payload after first frame | Admit | 49 ms | one genuine decoded frame, `dwidth=320` |
| encrypted MP4 | Reject | 32 ms | error `-16` after `FILE_LOADED`, no decoded width |
| missing file | Reject | 14 ms | error `-13` |
| empty MP4 | Reject | 23 ms | error `-17` |

Agent 0 also reported:

- `FILE_LOADED` always preceded positive decoded-width evidence for admitted video;
- truncated and encrypted fixtures reached `FILE_LOADED` but never produced decoded-frame evidence;
- cancellation returned within 14 ms without stale success;
- stale-generation and timeout guards prevented session creation;
- the former prohibited P0 policy with `vid=no` still rejected valid H.264 with error `-16`;
- observed local-disk latency across repeated runs was 34–180 ms, including a real 1080p MP4 with audio.

This is **test-reported execution evidence from Agent 0**, not a rerun by Preflight Architect.

## Accepted Outcome

**Accept. Code Part 01 r2 is test-reported as behaving exactly as designed against the installed libmpv.**

The canonical admission contract is now:

> Admission proves that libmpv can open the source and decode at least one real video frame through null output. It does not prove that the entire file is free of later corruption.

A source that decodes one valid frame and fails later is correctly admitted. Later corruption is a playback failure, preserves the shell session, and routes to the recovery behavior owned by later Local Media Launch slices.

## Reference Error Taxonomy

Record the following installed-libmpv observations as diagnostic reference data, not as a promise that every libmpv build or every malformed source will produce the same numeric code:

| libmpv error | Observed meaning | Observed fixtures |
|---:|---|---|
| `-16` | no audio or video data played / nothing playable before decoded-frame evidence | prohibited P0 valid-video case, truncated MP4, encrypted MP4 |
| `-17` | unrecognized file format | garbage MKV, empty MP4 |
| `-13` | loading failed | missing file |

Typed product errors remain authoritative. Raw libmpv codes belong in diagnostics and test traces; product behavior must not branch solely on these three values unless a later implementation decision explicitly adopts that mapping.

## Timeout Guidance

Use **3000 ms** as the default local-video admission timeout.

Measured local-disk probes completed within 180 ms, so 3000 ms provides substantial headroom. Do not reduce the default to a few hundred milliseconds based on these measurements. A timeout is a fail-closed rejection of a potentially valid file, so an aggressive value recreates the same user-visible failure class as the invalid r1 policy.

The following source classes were **not measured**:

- removable drives;
- network mounts;
- slow or sleeping disks;
- very large 4K or unusually complex containers.

Per-source-class budgets, a slow-source retry, or richer timeout recovery belong to the later recovery slice. They are not grounds for weakening the current pre-session admission contract.

Recommended implementation constant:

```cpp
constexpr int kDefaultLocalVideoAdmissionTimeoutMs = 3000;
```

## Permanent Regression Guards

Keep the following gates in the executable harness:

1. The prohibited `vid=no` plus `audio=no` policy must reject the supported H.264 fixture, proving the original r1 failure remains detectable.
2. `FILE_LOADED` without `dwidth > 0` must never admit.
3. Supported video must admit only after positive decoded-width evidence.
4. Truncated and encrypted fixtures that reach `FILE_LOADED` but never decode must reject without session creation.
5. Cancellation, timeout, and stale-generation results must never create a session.
6. Latency reports must distinguish cold-process and warm-process runs.
7. Slow-source testing must not justify silently lowering the default timeout.

## Bundle Impact

- **Code Part 01 r1:** falsified as adoption input by execution evidence.
- **Code Part 01 r2:** policy and code shape remain authoritative; r3 adds measured evidence and operational guidance.
- **Code Parts 02–04:** unchanged and still approved as design.
- **Manifest r3:** remains the governing bundle index unless later revised to point explicitly at this evidence amendment.
- **A1+B1, opaque `localId`, QML isolation, downloaded-file `playLocalFile()`, TOCTOU checks, fingerprint sequencing:** unchanged.

## Exact Next Action

Agent 0 owns reconstruction and adoption of the Slice 3C adapter in Colosseum, followed by the live-window gates for Player 1 session creation, external-local progress isolation, subtitle-provider silence, and source-unavailable session preservation.

## Verification Notes

- **Test-reported:** r2 fixture discrimination, event ordering, guard behavior, and 34–180 ms measured local-disk latency.
- **Confirmed from repository artifacts:** r2 requires P4 null-output decode with `dwidth > 0`, not `FILE_LOADED`, and preserves no-session-before-admission.
- **Not independently verified by Preflight Architect:** compilation, installed-libmpv behavior, timing measurements, adapter adoption, or user-visible playback.
- **Requires runtime validation:** the original local-video workflow in the running Colosseum window and the remaining MPV isolation/source-unavailable gates.
