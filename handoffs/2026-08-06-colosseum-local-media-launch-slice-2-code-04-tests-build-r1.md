
# Slice 2 Reference Code — Harness and Build Registration r1

**Status:** implementable reference code; uncompiled, untested, unexecuted, unadopted, and unverified.

## `tests/local_media_continuity_store_harness.cpp`

```cpp
#include "localmedia/LocalMediaContinuityStore.h"

#include <QCoreApplication>
#include <QFile>
#include <QJsonDocument>
#include <QJsonObject>
#include <QTemporaryDir>

#include <cstdlib>
#include <iostream>

using namespace colosseum::localmedia;

namespace {

void require(bool condition, const char *message)
{
    if (!condition) {
        std::cerr << "FAIL: " << message << '\n';
        std::exit(1);
    }
}

QString writeFixture(const QTemporaryDir &temporary, const QString &name)
{
    const QString path = temporary.filePath(name);
    QFile file(path);
    require(file.open(QIODevice::WriteOnly), "fixture opens");
    require(file.write("fixture") == 7, "fixture writes");
    file.close();
    return path;
}

LocalMediaContinuityRecord prototype(const QString &path,
                                     LocalMediaFamily family,
                                     const QString &title)
{
    LocalMediaContinuityRecord record;
    record.family = family;
    record.displayTitle = title;
    record.currentLocator.canonicalPath = path;
    record.currentLocator.opaqueAccessToken = QStringLiteral("opaque-test-token");
    record.fingerprints.append({
        QStringLiteral("sha256"),
        QStringLiteral("same-fingerprint"),
        7,
        1234
    });
    record.stateLinks.insert(QStringLiteral("reader2.pathKey"),
                             QStringLiteral("legacy-path-key"));
    record.identification.insert(QStringLiteral("provider"),
                                 QStringLiteral("test-provider"));
    record.subtitleReferences.append({
        {QStringLiteral("path"), QStringLiteral("/derived/subtitle.srt")},
        {QStringLiteral("source"), QStringLiteral("manual")}
    });
    return record;
}

void writeJson(const QString &path, const QJsonObject &root)
{
    QFile file(path);
    require(file.open(QIODevice::WriteOnly | QIODevice::Truncate), "json fixture opens");
    const QByteArray bytes = QJsonDocument(root).toJson(QJsonDocument::Compact);
    require(file.write(bytes) == bytes.size(), "json fixture writes");
}

void runSuite()
{
    QTemporaryDir temporary;
    require(temporary.isValid(), "temporary directory exists");

    const QString storePath = temporary.filePath(QStringLiteral("local-media.json"));
    const QString firstPath = writeFixture(temporary, QStringLiteral("first.epub"));
    const QString relocatedPath = writeFixture(temporary, QStringLiteral("relocated.epub"));
    const QString copyPath = writeFixture(temporary, QStringLiteral("copy.epub"));

    LocalMediaStoreError error;
    LocalMediaContinuityStore store(storePath);
    require(store.load(&error), "missing store loads as empty");
    require(store.all().isEmpty(), "first run contains no records");

    const QString firstId =
        store.create(prototype(firstPath, LocalMediaFamily::Book, QStringLiteral("First")),
                     &error);
    require(!firstId.isEmpty(), "first record is created");
    require(QFile::exists(firstPath), "create leaves source media untouched");
    require(store.markOpened(firstId, 100, &error), "record is marked opened");
    require(store.recents().size() == 1, "opened record appears in recents");

    LocalMediaContinuityStore restarted(storePath);
    require(restarted.load(&error), "store reloads after restart");
    const auto loaded = restarted.record(firstId);
    require(loaded.has_value(), "stable identity survives restart");
    require(loaded->stateLinks.value(QStringLiteral("reader2.pathKey")).toString()
                == QStringLiteral("legacy-path-key"),
            "Reader 2 state link survives restart");
    require(!loaded->identification.isEmpty(), "identification survives restart");
    require(loaded->subtitleReferences.size() == 1, "subtitle reference survives restart");
    require(loaded->currentLocator.opaqueAccessToken
                == QStringLiteral("opaque-test-token"),
            "opaque access token survives restart");

    LocalMediaLocator relocated;
    relocated.canonicalPath = relocatedPath;
    relocated.opaqueAccessToken = QStringLiteral("new-opaque-token");
    require(restarted.relocate(firstId, relocated, &error), "relocation succeeds");
    require(restarted.findByPath(relocatedPath) == firstId,
            "new path resolves to stable identity");
    require(restarted.findByPath(firstPath) == firstId,
            "historical path resolves to stable identity");
    require(QFile::exists(firstPath) && QFile::exists(relocatedPath),
            "relocation does not mutate source files");

    const QString copyId =
        restarted.create(prototype(copyPath, LocalMediaFamily::Book, QStringLiteral("Copy")),
                         &error);
    require(!copyId.isEmpty() && copyId != firstId, "copy has distinct local identity");
    require(restarted.findByFingerprint(QStringLiteral("sha256"),
                                        QStringLiteral("same-fingerprint")).size() == 2,
            "shared fingerprint does not merge identities");
    require(restarted.setRelationship(copyId,
                                      LocalMediaRelationshipKind::CopyOf,
                                      firstId,
                                      &error),
            "copy relationship is explicit");

    require(restarted.markOpened(copyId, 200, &error), "copy is marked opened");
    require(restarted.recents().first().localId == copyId,
            "recents are ordered newest first");
    require(restarted.clearRecents(&error), "clear recents succeeds");
    require(restarted.recents().isEmpty(), "clear recents removes only recency");
    require(restarted.record(firstId).has_value()
                && restarted.record(firstId)->stateLinks.contains(
                    QStringLiteral("reader2.pathKey")),
            "clear recents preserves continuity state");

    const auto removed = restarted.forget(copyId, &error);
    require(removed.has_value(), "forget returns cleanup references");
    require(!restarted.record(copyId).has_value(), "forgotten metadata is removed");
    require(QFile::exists(copyPath), "forget never removes source media");
    require(restarted.findByFingerprint(QStringLiteral("sha256"),
                                        QStringLiteral("same-fingerprint"))
                == QStringList{firstId},
            "forget removes only the forgotten fingerprint link");

    LocalMediaContinuityStore secondRestart(storePath);
    require(secondRestart.load(&error), "post-mutation store reloads");
    require(secondRestart.record(firstId).has_value(), "remaining record survives restart");

    writeJson(storePath, {
        {QStringLiteral("schemaVersion"), 99},
        {QStringLiteral("records"), QJsonArray{}}
    });
    LocalMediaContinuityStore unsupported(storePath);
    require(!unsupported.load(&error), "unknown schema fails closed");
    require(error.code == LocalMediaStoreErrorCode::UnsupportedVersion,
            "unknown schema returns typed error");

    writeJson(storePath, {
        {QStringLiteral("schemaVersion"), 1},
        {QStringLiteral("records"), QJsonArray{
            QJsonObject{
                {QStringLiteral("localId"), QString()},
                {QStringLiteral("family"), QStringLiteral("unknown")}
            }
        }}
    });
    LocalMediaContinuityStore quarantining(storePath);
    require(quarantining.load(&error), "malformed row does not reject whole store");
    require(quarantining.all().isEmpty(), "malformed row is quarantined");
    require(!quarantining.loadWarnings().isEmpty(), "quarantine is observable");
}

} // namespace

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    runSuite();
    std::cout << "Local media continuity store tests passed.\n";
    return 0;
}
```

## `native/CMakeLists.txt` candidate changes

```diff
@@
     SessionStore.h
+    localmedia/LocalMediaContinuityStore.h
+    localmedia/LocalMediaContinuityStore.cpp
@@
+add_executable(local_media_continuity_store_harness
+    ../tests/local_media_continuity_store_harness.cpp
+    localmedia/LocalMediaContinuityStore.cpp
+)
+target_include_directories(local_media_continuity_store_harness
+    PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
+target_link_libraries(local_media_continuity_store_harness PRIVATE Qt6::Core)
```

The execution agent must place these insertions in the repository's actual source and
standalone-harness sections, not apply the context markers blindly.

## `tests/CMakeLists.txt` candidate change

```diff
@@
 colosseum_register_harness(biblio_catalog_logic_harness unit)
+colosseum_register_harness(
+    local_media_continuity_store_harness
+    unit
+    local-media
+)
```

## Required verification

1. Compile the harness and the affected application target.
2. Run the harness directly.
3. Run its registered CTest entry and the `unit` and `local-media` labels.
4. Run existing `ProgressStore`, Reader 2 store/bridge, and comic-ledger regressions.
5. Confirm the store file is isolated from existing online/Continue persistence.
6. Add a write-failure test using a non-writable or injectable persistence seam if the
   platform test environment can make it deterministic.
7. Confirm source files remain unchanged after create, relocate, clear recents, and forget.
