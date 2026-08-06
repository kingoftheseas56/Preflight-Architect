# Local Media Launch Slice 1 — Reference Code Part

**Status:** implementable reference code; uncompiled, untested, unexecuted, unadopted, and unverified.

**Colosseum basis:** `master@bb8eecb40eb8a50b7ded62f79035c555972c3fef`

This is one canonical segment of the interim Slice 1 bundle. The execution agent must inspect, adapt, compile, test, and runtime-validate before adoption.

## `tests/local_media_contract_harness.cpp`

```cpp
#include "localmedia/LocalMediaClassifier.h"
#include "localmedia/LocalMediaHandler.h"
#include "localmedia/LocalMediaRouter.h"

#include <QByteArray>
#include <QCoreApplication>
#include <QDir>
#include <QFile>
#include <QFileInfo>
#include <QHash>
#include <QTemporaryDir>

#include <cstdlib>
#include <iostream>
#include <utility>

using namespace colosseum::localmedia;

namespace {

void require(bool condition, const char *message)
{
    if (!condition) {
        std::cerr << "FAIL: " << message << '\n';
        std::exit(1);
    }
}

void requireCode(const LocalMediaRouteResult &result,
                 LocalMediaErrorCode expected,
                 const char *message)
{
    if (result.ok || result.error.code != expected) {
        std::cerr << "FAIL: " << message
                  << " (expected=" << localMediaErrorCodeName(expected).toStdString()
                  << ", actual=" << localMediaErrorCodeName(result.error.code).toStdString()
                  << ")\n";
        std::exit(1);
    }
}

QString writeFile(const QTemporaryDir &temporary,
                  const QString &name,
                  const QByteArray &payload = QByteArrayLiteral("fixture"))
{
    const QString path = temporary.filePath(name);
    QFile file(path);
    require(file.open(QIODevice::WriteOnly), "fixture file opens for writing");
    require(file.write(payload) == payload.size(), "fixture payload is written");
    file.close();
    return path;
}

class FakeHandler final : public LocalMediaHandler {
public:
    enum class Mode {
        Valid,
        InvalidDescriptor,
        Reject
    };

    FakeHandler(QString handlerId, LocalMediaKind kind, Mode mode = Mode::Valid)
        : m_handlerId(std::move(handlerId))
        , m_kind(kind)
        , m_mode(mode)
    {
    }

    QString id() const override { return m_handlerId; }

    bool supports(LocalMediaKind kind) const override
    {
        return kind == m_kind;
    }

    LocalMediaPrepareResult prepare(const LocalMediaOpenRequest &request) const override
    {
        if (m_mode == Mode::Reject) {
            return LocalMediaPrepareResult::failed(LocalMediaError::make(
                LocalMediaErrorCode::HandlerRejected,
                QStringLiteral("The fixture handler rejected the file."),
                QStringLiteral("Intentional test rejection.")));
        }

        if (m_mode == Mode::InvalidDescriptor) {
            return LocalMediaPrepareResult::succeeded(
                QVariantMap{{QStringLiteral("appType"), QStringLiteral("biblio")}});
        }

        QString appType;
        QString contentKind;
        switch (request.kind) {
        case LocalMediaKind::Book:
            appType = QStringLiteral("biblio");
            contentKind = QStringLiteral("book");
            break;
        case LocalMediaKind::ComicArchive:
            appType = QStringLiteral("tankoban");
            contentKind = QStringLiteral("comic");
            break;
        case LocalMediaKind::Video:
            appType = QStringLiteral("theatre");
            contentKind = QStringLiteral("movie");
            break;
        case LocalMediaKind::Unknown:
            break;
        }

        QVariantMap target;
        target.insert(QStringLiteral("path"), request.resource.canonicalPath);

        QVariantMap descriptor;
        descriptor.insert(QStringLiteral("appType"), appType);
        descriptor.insert(QStringLiteral("contentKind"), contentKind);
        descriptor.insert(QStringLiteral("title"), request.resource.displayName);
        descriptor.insert(QStringLiteral("target"), target);
        return LocalMediaPrepareResult::succeeded(descriptor);
    }

private:
    QString m_handlerId;
    LocalMediaKind m_kind = LocalMediaKind::Unknown;
    Mode m_mode = Mode::Valid;
};

void runSuite()
{
    QTemporaryDir temporary;
    require(temporary.isValid(), "temporary fixture directory exists");

    const QString bookPath = writeFile(temporary, QStringLiteral("Example.EPUB"));
    const QString comicPath = writeFile(temporary, QStringLiteral("Issue.CBZ"));
    const QString videoPath = writeFile(temporary, QStringLiteral("Clip.MKV"));
    const QString unknownPath = writeFile(temporary, QStringLiteral("notes.bin"));
    const QString extensionlessPath = writeFile(temporary, QStringLiteral("README"));
    const QString missingPath = temporary.filePath(QStringLiteral("missing.epub"));
    const QString folderPath = temporary.filePath(QStringLiteral("folder"));
    require(QDir().mkpath(folderPath), "directory fixture is created");

    QHash<QString, LocalMediaKind> mappings;
    mappings.insert(QStringLiteral(".epub"), LocalMediaKind::Book);
    mappings.insert(QStringLiteral("cbz"), LocalMediaKind::ComicArchive);
    mappings.insert(QStringLiteral("mkv"), LocalMediaKind::Video);
    const ExtensionMediaClassifier classifier(mappings);
    const LocalMediaRouter router;

    requireCode(
        router.route(QUrl(), QStringLiteral("test"), classifier, {}),
        LocalMediaErrorCode::EmptyResource,
        "empty input is rejected");

    requireCode(
        router.route(QUrl(QStringLiteral("https://example.com/video.mkv")),
                     QStringLiteral("test"), classifier, {}),
        LocalMediaErrorCode::UnsupportedScheme,
        "remote URL is rejected");

    requireCode(
        router.route(QUrl::fromLocalFile(missingPath),
                     QStringLiteral("test"), classifier, {}),
        LocalMediaErrorCode::NotFound,
        "missing file is rejected");

    requireCode(
        router.route(QUrl::fromLocalFile(folderPath),
                     QStringLiteral("test"), classifier, {}),
        LocalMediaErrorCode::DirectoryNotSupported,
        "directory is rejected");

    requireCode(
        router.route(QUrl::fromLocalFile(unknownPath),
                     QStringLiteral("test"), classifier, {}),
        LocalMediaErrorCode::UnsupportedFormat,
        "unregistered extension is rejected");

    requireCode(
        router.route(QUrl::fromLocalFile(extensionlessPath),
                     QStringLiteral("test"), classifier, {}),
        LocalMediaErrorCode::UnsupportedFormat,
        "extensionless file is rejected");

    requireCode(
        router.route(QUrl::fromLocalFile(bookPath),
                     QStringLiteral("test"), classifier, {}),
        LocalMediaErrorCode::HandlerUnavailable,
        "classified file without a handler is rejected");

    const FakeHandler bookHandler(QStringLiteral("reader2"), LocalMediaKind::Book);
    const LocalMediaRouteResult bookRoute =
        router.route(QUrl::fromLocalFile(bookPath),
                     QStringLiteral("taskbar"), classifier, {&bookHandler});

    require(bookRoute.ok, "book route succeeds");
    require(bookRoute.kind == LocalMediaKind::Book,
            "extension classification is case-insensitive");
    require(bookRoute.handlerId == QStringLiteral("reader2"),
            "selected handler id is returned");
    require(bookRoute.resource.canonicalPath == QFileInfo(bookPath).canonicalFilePath(),
            "resource path is canonical");
    require(bookRoute.resource.sizeBytes == QByteArrayLiteral("fixture").size(),
            "resource size is captured");
    require(bookRoute.sessionDescriptor.value(QStringLiteral("appType")).toString()
                == QStringLiteral("biblio"),
            "handler descriptor is preserved");
    require(bookRoute.sessionDescriptor.value(QStringLiteral("target")).toMap()
                .value(QStringLiteral("path")).toString()
                == bookRoute.resource.canonicalPath,
            "SessionStore target carries provisional path identity");

    const FakeHandler secondBookHandler(
        QStringLiteral("reader2-secondary"),
        LocalMediaKind::Book);
    requireCode(
        router.route(QUrl::fromLocalFile(bookPath),
                     QStringLiteral("test"), classifier, {&bookHandler, &secondBookHandler}),
        LocalMediaErrorCode::AmbiguousHandler,
        "multiple matching handlers fail closed");

    const FakeHandler invalidHandler(
        QStringLiteral("invalid"),
        LocalMediaKind::Book,
        FakeHandler::Mode::InvalidDescriptor);
    requireCode(
        router.route(QUrl::fromLocalFile(bookPath),
                     QStringLiteral("test"), classifier, {&invalidHandler}),
        LocalMediaErrorCode::InvalidSessionDescriptor,
        "invalid SessionStore descriptor is rejected");

    const FakeHandler rejectingHandler(
        QStringLiteral("rejecting"),
        LocalMediaKind::Book,
        FakeHandler::Mode::Reject);
    requireCode(
        router.route(QUrl::fromLocalFile(bookPath),
                     QStringLiteral("test"), classifier, {&rejectingHandler}),
        LocalMediaErrorCode::HandlerRejected,
        "typed handler error is preserved");

    const FakeHandler comicHandler(
        QStringLiteral("comic-import"),
        LocalMediaKind::ComicArchive);
    const LocalMediaRouteResult comicRoute =
        router.route(QUrl::fromLocalFile(comicPath),
                     QStringLiteral("test"), classifier, {&comicHandler});
    require(comicRoute.ok && comicRoute.kind == LocalMediaKind::ComicArchive,
            "comic archive routes through an explicit handler");

    const FakeHandler videoHandler(
        QStringLiteral("player1"),
        LocalMediaKind::Video);
    const LocalMediaRouteResult videoRoute =
        router.route(QUrl::fromLocalFile(videoPath),
                     QStringLiteral("test"), classifier, {&videoHandler});
    require(videoRoute.ok && videoRoute.kind == LocalMediaKind::Video,
            "video routes through an explicit handler");
}

} // namespace

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    runSuite();
    std::cout << "Local media Slice 1 contract tests passed.\n";
    return 0;
}
```
