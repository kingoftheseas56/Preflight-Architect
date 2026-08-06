# Local Media Launch Slice 1 — Reference Code Part

**Status:** implementable reference code; uncompiled, untested, unexecuted, unadopted, and unverified.

**Colosseum basis:** `master@bb8eecb40eb8a50b7ded62f79035c555972c3fef`

This is one canonical segment of the interim Slice 1 bundle. The execution agent must inspect, adapt, compile, test, and runtime-validate before adoption.

## `native/localmedia/LocalMediaTypes.h`

```cpp
#pragma once

#include <QDateTime>
#include <QString>
#include <QUrl>
#include <QVariantMap>
#include <QtGlobal>

#include <utility>

namespace colosseum::localmedia {

enum class LocalMediaKind {
    Unknown,
    Book,
    ComicArchive,
    Video
};

enum class LocalMediaErrorCode {
    None,
    EmptyResource,
    UnsupportedScheme,
    NotFound,
    NotReadable,
    DirectoryNotSupported,
    UnsupportedFormat,
    AmbiguousFormat,
    HandlerUnavailable,
    AmbiguousHandler,
    InvalidSessionDescriptor,
    HandlerRejected
};

struct LocalMediaError {
    LocalMediaErrorCode code = LocalMediaErrorCode::None;
    QString userMessage;
    QString diagnostic;

    bool isError() const { return code != LocalMediaErrorCode::None; }

    static LocalMediaError make(LocalMediaErrorCode code,
                                QString userMessage,
                                QString diagnostic = {})
    {
        return LocalMediaError{
            code,
            std::move(userMessage),
            std::move(diagnostic)
        };
    }
};

struct LocalMediaResource {
    QUrl source;
    QString canonicalPath;
    QString displayName;
    QString extension;
    qint64 sizeBytes = -1;
    QDateTime modifiedAt;
};

struct LocalMediaInspectionResult {
    bool ok = false;
    LocalMediaResource resource;
    LocalMediaError error;

    static LocalMediaInspectionResult succeeded(LocalMediaResource resource)
    {
        LocalMediaInspectionResult result;
        result.ok = true;
        result.resource = std::move(resource);
        return result;
    }

    static LocalMediaInspectionResult failed(LocalMediaError error)
    {
        LocalMediaInspectionResult result;
        result.error = std::move(error);
        return result;
    }
};

struct LocalMediaClassificationResult {
    bool ok = false;
    LocalMediaKind kind = LocalMediaKind::Unknown;
    LocalMediaError error;

    static LocalMediaClassificationResult succeeded(LocalMediaKind kind)
    {
        LocalMediaClassificationResult result;
        result.ok = true;
        result.kind = kind;
        return result;
    }

    static LocalMediaClassificationResult failed(LocalMediaError error)
    {
        LocalMediaClassificationResult result;
        result.error = std::move(error);
        return result;
    }
};

struct LocalMediaOpenRequest {
    LocalMediaResource resource;
    LocalMediaKind kind = LocalMediaKind::Unknown;
    QString intakeSource;
};

struct LocalMediaPrepareResult {
    bool ok = false;
    QVariantMap sessionDescriptor;
    LocalMediaError error;

    static LocalMediaPrepareResult succeeded(QVariantMap descriptor)
    {
        LocalMediaPrepareResult result;
        result.ok = true;
        result.sessionDescriptor = std::move(descriptor);
        return result;
    }

    static LocalMediaPrepareResult failed(LocalMediaError error)
    {
        LocalMediaPrepareResult result;
        result.error = std::move(error);
        return result;
    }
};

struct LocalMediaRouteResult {
    bool ok = false;
    LocalMediaResource resource;
    LocalMediaKind kind = LocalMediaKind::Unknown;
    QString handlerId;
    QVariantMap sessionDescriptor;
    LocalMediaError error;

    static LocalMediaRouteResult succeeded(LocalMediaResource resource,
                                           LocalMediaKind kind,
                                           QString handlerId,
                                           QVariantMap descriptor)
    {
        LocalMediaRouteResult result;
        result.ok = true;
        result.resource = std::move(resource);
        result.kind = kind;
        result.handlerId = std::move(handlerId);
        result.sessionDescriptor = std::move(descriptor);
        return result;
    }

    static LocalMediaRouteResult failed(LocalMediaError error)
    {
        LocalMediaRouteResult result;
        result.error = std::move(error);
        return result;
    }
};

QString localMediaKindName(LocalMediaKind kind);
QString localMediaErrorCodeName(LocalMediaErrorCode code);

} // namespace colosseum::localmedia
```

## `native/localmedia/LocalMediaTypes.cpp`

```cpp
#include "LocalMediaTypes.h"

namespace colosseum::localmedia {

QString localMediaKindName(LocalMediaKind kind)
{
    switch (kind) {
    case LocalMediaKind::Book:
        return QStringLiteral("book");
    case LocalMediaKind::ComicArchive:
        return QStringLiteral("comic-archive");
    case LocalMediaKind::Video:
        return QStringLiteral("video");
    case LocalMediaKind::Unknown:
        break;
    }
    return QStringLiteral("unknown");
}

QString localMediaErrorCodeName(LocalMediaErrorCode code)
{
    switch (code) {
    case LocalMediaErrorCode::None:
        return QStringLiteral("none");
    case LocalMediaErrorCode::EmptyResource:
        return QStringLiteral("empty-resource");
    case LocalMediaErrorCode::UnsupportedScheme:
        return QStringLiteral("unsupported-scheme");
    case LocalMediaErrorCode::NotFound:
        return QStringLiteral("not-found");
    case LocalMediaErrorCode::NotReadable:
        return QStringLiteral("not-readable");
    case LocalMediaErrorCode::DirectoryNotSupported:
        return QStringLiteral("directory-not-supported");
    case LocalMediaErrorCode::UnsupportedFormat:
        return QStringLiteral("unsupported-format");
    case LocalMediaErrorCode::AmbiguousFormat:
        return QStringLiteral("ambiguous-format");
    case LocalMediaErrorCode::HandlerUnavailable:
        return QStringLiteral("handler-unavailable");
    case LocalMediaErrorCode::AmbiguousHandler:
        return QStringLiteral("ambiguous-handler");
    case LocalMediaErrorCode::InvalidSessionDescriptor:
        return QStringLiteral("invalid-session-descriptor");
    case LocalMediaErrorCode::HandlerRejected:
        return QStringLiteral("handler-rejected");
    }
    return QStringLiteral("unknown-error");
}

} // namespace colosseum::localmedia
```

## `native/localmedia/LocalMediaClassifier.h`

```cpp
#pragma once

#include "LocalMediaTypes.h"

#include <QHash>

namespace colosseum::localmedia {

class LocalMediaClassifier {
public:
    virtual ~LocalMediaClassifier() = default;
    virtual LocalMediaClassificationResult classify(
        const LocalMediaResource &resource) const = 0;
};

class ExtensionMediaClassifier final : public LocalMediaClassifier {
public:
    explicit ExtensionMediaClassifier(
        QHash<QString, LocalMediaKind> extensionKinds);

    LocalMediaClassificationResult classify(
        const LocalMediaResource &resource) const override;

private:
    static QString normalizeExtension(QString extension);

    QHash<QString, LocalMediaKind> m_extensionKinds;
};

} // namespace colosseum::localmedia
```

## `native/localmedia/LocalMediaClassifier.cpp`

```cpp
#include "LocalMediaClassifier.h"

namespace colosseum::localmedia {

ExtensionMediaClassifier::ExtensionMediaClassifier(
    QHash<QString, LocalMediaKind> extensionKinds)
{
    for (auto it = extensionKinds.cbegin(); it != extensionKinds.cend(); ++it) {
        const QString extension = normalizeExtension(it.key());
        if (extension.isEmpty() || it.value() == LocalMediaKind::Unknown)
            continue;
        m_extensionKinds.insert(extension, it.value());
    }
}

LocalMediaClassificationResult ExtensionMediaClassifier::classify(
    const LocalMediaResource &resource) const
{
    const QString extension = normalizeExtension(resource.extension);
    if (extension.isEmpty()) {
        return LocalMediaClassificationResult::failed(LocalMediaError::make(
            LocalMediaErrorCode::UnsupportedFormat,
            QStringLiteral("This file type is not supported."),
            QStringLiteral("The inspected resource has no file extension.")));
    }

    const auto it = m_extensionKinds.constFind(extension);
    if (it == m_extensionKinds.cend()) {
        return LocalMediaClassificationResult::failed(LocalMediaError::make(
            LocalMediaErrorCode::UnsupportedFormat,
            QStringLiteral("This file type is not supported."),
            QStringLiteral("No local-media kind is registered for extension '%1'.")
                .arg(extension)));
    }

    return LocalMediaClassificationResult::succeeded(it.value());
}

QString ExtensionMediaClassifier::normalizeExtension(QString extension)
{
    extension = extension.trimmed().toLower();
    while (extension.startsWith(QLatin1Char('.')))
        extension.remove(0, 1);
    return extension;
}

} // namespace colosseum::localmedia
```
