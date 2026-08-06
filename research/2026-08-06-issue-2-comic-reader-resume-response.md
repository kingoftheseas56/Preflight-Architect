---
artifact_class: issue-response
status: reviewed
date: 2026-08-06
issue: https://github.com/kingoftheseas56/Preflight-Architect/issues/2
subject_repository: https://github.com/kingoftheseas56/Colosseum
source_revision: a40333dc1fc9823ceb9decd811deeadde6ac4c2d
---

# Issue Response: Comic reader resets to page 1 after resume

## Verdict

Choose **Option A** as the primary fix. The Long-Strip surface must not publish state-authoring tracking signals while inactive.

Guard both scheduling and delivery of the delayed signal:

1. do not schedule a tracking emit while inactive;
2. re-check `active` when the timer fires, because the surface may become inactive after scheduling.

Option B is suitable only as defense-in-depth. Option C is too lifecycle-specific unless runtime tracing proves the active Long-Strip restore path needs a separate suppression gate.

## Evidence

Issue #2 reports that the correct resume record is present, `_resumeArmed` has been consumed, `currentPage` nevertheless ends at 1, paged surfaces do not write it back, and a prior store/load guard did not resolve the symptom.

At Colosseum revision `a40333d`, `ComicReaderShell.qml` keeps the strip mounted, binds its `active` state to visibility, and consumes strip outputs without active checks. `ComicReaderStripSurface.qml` already uses `active` as a boundary for viewport reporting, but the delayed state-tracking path scheduled from `onContentYChanged` does not visibly enforce the same rule at the inspected call site.

This supports treating the missing gate as an ownership inconsistency rather than introducing a new architecture.

## Durable invariant

> An inactive surface may remain mounted and receive positioning commands, but it must not publish state-authoring tracking signals such as `scrolled`, `pageInView`, `visiblePages`, or presentation state.

## Recommended implementation shape

```qml
function _scheduleEmit() {
    if (!active)
        return

    _emitPending = true
    if (!emitTimer.running)
        emitTimer.start()
}

function _flushEmit() {
    if (!_emitPending)
        return

    _emitPending = false

    if (!active)
        return

    _emitUserScroll()
}

onActiveChanged: {
    if (!active) {
        emitTimer.stop()
        _emitPending = false
        return
    }

    _scheduleReport()
    Qt.callLater(root._emitPresented)
}
```

A final `if (!active) return` inside `_emitUserScroll()` is also reasonable as defense-in-depth.

## Why not Option B alone

A shell-only `onPageInView` guard protects `currentPage`, but the inactive surface could still emit other state-authoring outputs. It also duplicates the mount contract in the orchestrator instead of enforcing it at the source.

## Why not Option C first

Holding `_programmatic` across `openEntry()` couples suppression to one lifecycle event and may hide unrelated transitions. Prefer a separate named gate such as `trackingEnabled` only if runtime evidence shows the active Long-Strip restore path also emits stale tracking.

## Runtime blind spot

An `active` guard addresses the reported paged-mode mechanism because the strip is inactive there. It may not address a similar race when Long Strip itself is active and model rebuilding occurs before delayed restore. That remains a hypothesis and needs tracing.

## Required regression evidence

The execution agent should prove that:

1. paged resume emits no stale strip tracking after inactive model reset;
2. a timer scheduled while active cannot publish after deactivation;
3. an inactive change cannot become stale merely because activation occurs before the timer expires;
4. Long-Strip wheel, keyboard, scrub, Home/End, and auto-scroll tracking still work;
5. paged and Long-Strip resume remain on the saved page after delayed tracking, restore, and progress debounce windows;
6. reopening does not degrade the saved resume record to page 1;
7. tracing captures the originating `contentYChanged`, `_programmatic`, active state at schedule and delivery, emitted page, and later progress write.

## Status

- **Confirmed:** the strip remains mounted, `active` is tied to visibility, and shell handlers accept its outputs without active checks.
- **Confirmed:** viewport reporting already rejects inactive operation, while delayed tracking does not visibly enforce the same rule at the inspected call site.
- **Inferred:** Option A is the smallest coherent ownership repair.
- **Hypothesis:** the inactive strip model reset is the observed runtime overwrite.
- **Unknown:** whether active Long-Strip opening has a related pre-restore stale emit.
- **Not verified:** no implementation or runtime fix has been executed or validated here.

## Sources

- https://github.com/kingoftheseas56/Preflight-Architect/issues/2
- https://raw.githubusercontent.com/kingoftheseas56/Colosseum/a40333dc1fc9823ceb9decd811deeadde6ac4c2d/qml/comicreader/ComicReaderShell.qml
- https://raw.githubusercontent.com/kingoftheseas56/Colosseum/a40333dc1fc9823ceb9decd811deeadde6ac4c2d/qml/comicreader/ComicReaderStripSurface.qml
