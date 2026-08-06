# Qt Test + Qt Quick Test Integration Guide

## Decision

Use four evidence layers:

1. Qt Test for deterministic C++ contracts, models, signals, persistence, and state transitions.
2. Qt Quick Test for deterministic QML component behavior, bindings, focus, input, and UI state.
3. Lanista for isolated assembled-application workflows, semantic state, and pixels.
4. Human review for aesthetic verdicts.

A green native or QML test is Test-reported, not Runtime-validated, for a user-visible slice.

## Colosseum integration

- Keep `native/CMakeLists.txt` as the application build root.
- Add `tests/CMakeLists.txt` for test targets and CTest registration.
- Request `Qt6::Test` and `Qt6::QuickTest` only under `BUILD_TESTING`.
- Never link test modules into the shipping `colosseum` executable.
- Register a small pilot set of existing deterministic harnesses before rewriting them.
- Use CTest labels such as `unit`, `qml`, `integration`, `legacy`, `lanista`, `windows`, and `visual`.

First native candidate:

```text
tests/window_state_policy_harness.cpp
```

Convert it into independent Qt Test functions/data rows while preserving temporary settings isolation. Keep the old harness until parity is demonstrated.

Create one shared Qt Quick Test runner/setup and register existing files first:

```text
tests/qml/tst_comicreader_title_controls.qml
tests/qml/tst_search_history_flow.qml
```

Then migrate:

```text
tests/comicreader_resume_race_harness.qml
```

Use `TestCase`, `SignalSpy`, `tryCompare`, and `tryVerify`. Fixed sleeps are not correctness signals.

Every test must use isolated settings, app-data, cache, databases, progress, downloads, and artifacts. Default deterministic gates must not use live user data or uncontrolled network.

Add a small read-only, versioned reader-state snapshot. Do not expose arbitrary QObject reflection, raw pointers, volatile QML paths, secrets, or live library contents.

First vertical regression:

```text
open work
→ navigate to non-default page
→ minimize
→ restore
→ retain same session, work identity, and page
```

Proof ownership:

- Qt Test: authoritative persistence/state transition and signal ordering.
- Qt Quick Test: restored-state consumption and stale page-one overwrite prevention.
- Lanista: actual isolated application workflow and real minimize/restore evidence.

## Brotherhood skills

Do not create another workflow skill. Add one shared reference: `references/colosseum-test-layers.md`.

### Brainstorming

Add a `Verification Architecture` section covering behavior invariants, Qt Test, Qt Quick Test, Lanista, isolation, negative controls, human-only verdicts, and test-seam gaps.

### Writing Plans

Read both `docs/colosseum-test-verification.md` and `docs/colosseum-lanista-verification.md`.

Each relevant slice must include:

```text
Qt Test
Qt Quick Test
Existing harnesses
Negative control
Test seam status: available / migration required / test blocked / not applicable
Bridge status: available / bridge blocked / not applicable
```

Test seam status is distinct from Lanista bridge status.

### Executing Plans

Run in this order:

```text
baseline
→ implement smallest approved change
→ build selected tests
→ run Qt Test
→ run Qt Quick Test
→ run named legacy harnesses
→ preserve machine-readable results
→ replay Lanista
→ inspect state/events/probes/pixels
→ report exact supported status
```

Keep existing overall statuses:

- Runtime-validated
- Test-reported
- Implemented, verification pending
- Bridge blocked
- Verification failed
- Plan contradicted

Add a per-layer result matrix.

### UI Audit

Add a protection seam to every finding:

```text
Qt Test / Qt Quick Test / Lanista / combined / human-only / unknown
```

End with a regression protection map.

## Ordered slices

1. Create `docs/colosseum-test-verification.md`.
2. Add a small CTest registration seam.
3. Convert the window-state harness with parity.
4. Add the shared Qt Quick Test runner.
5. Register existing `tst_*.qml` files.
6. Migrate the reader resume-race QML harness.
7. Add reader-state snapshot v1.
8. Run the three-layer minimize/restore regression.
9. Update Brotherhood skills and pressure tests.
10. Reconcile both verification ledgers.

## First action

Inventory existing runners and create `docs/colosseum-test-verification.md` before changing CMake or test sources.
