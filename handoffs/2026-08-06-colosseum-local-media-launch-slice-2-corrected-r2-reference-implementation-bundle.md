# Local Media Launch Slice 2 — Corrected r2 Reference Implementation Bundle

## Status

**Reviewed reference correction bundle; uncompiled, untested, unexecuted, unadopted, and runtime-unverified.**

This immutable r2 supersedes the r1 manifest as the canonical Slice 2 adoption input. It composes the four immutable r1 code parts and applies only the amendments below.

## Basis and Composition

- Colosseum: `master@a40333dc1fc9823ceb9decd811deeadde6ac4c2d`
- Review: `kingoftheseas56/Preflight-Architect#1`
- Supersedes: `handoffs/2026-08-06-colosseum-local-media-launch-slice-2-manifest-r1.md`
- Retains unchanged:
  - `...slice-2-code-01-types-store-header-r1.md`
  - `...slice-2-code-02-store-implementation-a-r1.md`
  - `...slice-2-code-03-store-implementation-b-r1.md`
  - `...slice-2-code-04-tests-build-r1.md`

## Fix Traceability

| Review finding | r2 correction |
|---|---|
| `#ifnndef` | Replace with `#ifndef`. |
| `toOObject()` | Replace with `toObject()`. |
| Missing `QJsonArray` | Add the direct include to the harness. |
| Windows path case contract | Case-fold every normalized comparison/storage key under `Q_OS_WIN`, including absent-path fallback. |
| Relationship inconsistency | Separate structural record validation from referential validation; validate references before mutation and after all rows load. |

## Exact Amendments

### 1. Header guard and helper declaration

Target: proposed `native/localmedia/LocalMediaContinuityStore.h`.

```diff
-#ifnndef COLOSSEUM_LOCALMEDIA_CONTINUITY_STORE_H
+#ifndef COLOSSEUM_LOCALMEDIA_CONTINUITY_STORE_H
 #define COLOSSEUM_LOCALMEDIA_CONTINUITY_STORE_H
@@
     bool validateRecord(const LocalMediaContinuityRecord &record,
                         LocalMediaStoreError *error) const;
+    bool validateRelationshipTargets(
+        const LocalMediaContinuityRecord &record,
+        LocalMediaStoreError *error) const;
```

### 2. JSON typo

Target: proposed `native/localmedia/LocalMediaContinuityStore.cpp`, record deserialization.

```diff
-const QJsonObject relationship = value.toOObject();
+const QJsonObject relationship = value.toObject();
```

### 3. Windows normalization

Replace the r1 `normalizePath()` implementation with:

```cpp
QString LocalMediaContinuityStore::normalizePath(const QString &path)
{
    const QString trimmed = path.trimmed();
    if (trimmed.isEmpty())
        return {};

    const QFileInfo info(trimmed);
    QString normalized = info.canonicalFilePath();
    if (normalized.isEmpty())
        normalized = info.absoluteFilePath();

    normalized = QDir::cleanPath(QDir::fromNativeSeparators(normalized));
#ifdef Q_OS_WIN
    normalized = normalized.toCaseFolded();
#endif
    return normalized;
}
```

**Decision:** the store persists the normalized locator key. On Windows that key is case-folded. Source media is never renamed or modified. If original display casing is required later, it must be a separate presentation field rather than identity data.

### 4. Referential validation semantics

`validateRecord()` remains intrinsic and order-independent: it checks required identity/family/locator fields, fingerprints, non-empty relationship targets, and no self-reference. It must not inspect `m_records`.

Add:

```cpp
bool LocalMediaContinuityStore::validateRelationshipTargets(
    const LocalMediaContinuityRecord &record,
    LocalMediaStoreError *error) const
{
    for (const auto &relationship : record.relationships) {
        const QString otherId = relationship.otherLocalId.trimmed();
        if (!m_records.contains(otherId)) {
            setError(error,
                     LocalMediaStoreErrorCode::NotFound,
                     QStringLiteral("A related local media item could not be found."),
                     otherId);
            return false;
        }
    }
    return true;
}
```

In `upsert()`, before any mutation or persistence:

```cpp
if (!validateRecord(record, error))
    return false;
if (!validateRelationshipTargets(record, error))
    return false;
```

`setRelationship()` retains its existing direct target-existence check.

In `load()`, first parse every structurally valid row. Then audit references against the complete in-memory set. Quarantine dangling records and repeat until stable so removing one bad target cannot leave a newly dangling record:

```cpp
bool removed = false;
do {
    removed = false;
    const QStringList ids = m_order;
    for (const QString &id : ids) {
        const auto it = m_records.constFind(id);
        if (it == m_records.constEnd()
            || validateRelationshipTargets(it.value(), nullptr))
            continue;

        m_records.remove(id);
        m_order.removeAll(id);
        m_loadWarnings.append(
            QStringLiteral("Quarantined record '%1' because a relationship target is missing.")
                .arg(id));
        removed = true;
    }
} while (removed);
```

A dangling persisted relationship quarantines the affected row; it does not reject the whole store.

### 5. Harness include and coverage

Target: proposed `tests/local_media_continuity_store_harness.cpp`.

```diff
 #include <QFile>
+#include <QJsonArray>
 #include <QJsonDocument>
 #include <QJsonObject>
```

Add hermetic cases proving:

1. Upserting a record whose relationship target is absent returns `NotFound` and leaves the snapshot unchanged.
2. Loading a row with a dangling relationship succeeds overall, quarantines that row, and emits a warning.
3. On Windows, two missing paths differing only by case normalize equally; creating the second returns `DuplicateLocation`.
4. Existing create/restart, relocation, recents, clear-recents, forget, shared-fingerprint, malformed-row, and schema-version cases still pass.

The Windows case must use nonexistent paths so the `absoluteFilePath()` fallback is exercised.

## Build Registration

Retain the r1 proposed CMake target and CTest registration. The execution agent must locate the current source/harness insertion points at adoption time rather than apply stale context markers blindly.

## Required Execution Verification

1. Reconcile r2 with the actually adopted Slice 1 contract.
2. Apply in an isolated branch/worktree.
3. Build the continuity harness and affected application target.
4. Run the harness directly and through CTest (`unit` and `local-media` labels).
5. Run existing `ProgressStore`, Reader 2 store/bridge, and comic-ledger regressions.
6. Run the Windows absent-path case-fold test on Windows.
7. Prove failed relationship mutations and failed saves roll back in-memory state.
8. Prove source media is never opened for write or deletion.
9. Prove local-media records never appear in `ProgressStore::recent()`.

## Stop Conditions

Return evidence instead of forcing adoption if the adopted Slice 1 record contract is incompatible, another current store owns these semantics, Reader 2 relocation requires an unapproved migration, opaque access tokens cannot be persisted safely, Windows callers require original casing in the identity field, or baseline regressions make results ambiguous.

## Verification Notes

- **Confirmed:** all five issue findings are addressed in this r2.
- **Inferred:** public API compatibility with r1; only one private helper is added.
- **Requires execution evidence:** compilation, tests, Windows behavior, regressions, adoption, and runtime integration.
