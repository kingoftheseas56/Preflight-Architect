# Local Media Launch Slice 1 — Reference Code Part

**Status:** implementable reference code; uncompiled, untested, unexecuted, unadopted, and unverified.

**Colosseum basis:** `master@bb8eecb40eb8a50b7ded62f79035c555972c3fef`

This is one canonical segment of the interim Slice 1 bundle. The execution agent must inspect, adapt, compile, test, and runtime-validate before adoption.

## `native/localmedia/LocalMediaInspector.h`

```cpp
#pragma once

#include "LocalMediaTypes.h"

namespace colosseum::localmedia {

class LocalMediaInspector {
public:
    LocalMediaInspectionResult inspect(const QUrl &source) const;
};

} // namespace colosseum::localmedia
```

## `native/localmedia/LocalMediaInspector.cpp`

```cpp
#include "LocalMediaInspector.h"

#include <QDir>
#include <QFileInfo>

namespace colosseum::localmedia {

LocalMediaInspectionResult LocalMediaInspector::inspect(const QUrl &source) const
{
    if (!source.isValid() || source.isEmpty()) {
        return LocalMediaInspectionResult::failed(LocalMediaError::make(
            LocalMediaErrorCode::EmptyResource,
            QStringLiteral("Choose a file to open."),
            QStringLiteral("The intake URL is empty or invalid.")));
    }

    if (!source.isLocalFile()) {
        return LocalMediaInspectionResult::failed(LocalMediaError::make(
            LocalMediaErrorCode::UnsupportedScheme,
            QStringLiteral("This location cannot be opened as local media."),
            QStringLiteral("Only file: URLs are accepted by Slice 1.")));
    }

    const QString localPath = QDir::cleanPath(source.toLocalFile());
    QFileInfo info(localPath);

    if (!info.exists()) {
        return LocalMediaInspectionResult::failed(LocalMediaError::make(
            LocalMediaErrorCode::NotFound,
            QStringLiteral("This file is no longer available."),
            QStringLiteral("No file exists at '%1'.").arg(info.absoluteFilePath())));
    }

    if (!info.isFile()) {
        return LocalMediaInspectionResult::failed(LocalMediaError::make(
            LocalMediaErrorCode::DirectoryNotSupported,
            QStringLiteral("Choose a file, not a folder."),
            QStringLiteral("The intake path is not a regular file.")));
    }

    if (!info.isReadable()) {
        return LocalMediaInspectionResult::failed(LocalMediaError::make(
            LocalMediaErrorCode::NotReadable,
            QStringLiteral("Colosseum cannot read this file."),
            QStringLiteral("The file exists but is not readable.")));
    }

    const QString canonicalPath = info.canonicalFilePath();
    if (canonicalPath.isEmpty()) {
        return LocalMediaInspectionResult::failed(LocalMediaError::make(
            LocalMediaErrorCode::NotReadable,
            QStringLiteral("Colosseum cannot resolve this file."),
            QStringLiteral("Canonical path resolution returned an empty path.")));
    }

    LocalMediaResource resource;
    resource.source = QUrl::fromLocalFile(canonicalPath);
    resource.canonicalPath = canonicalPath;
    resource.displayName = info.fileName();
    resource.extension = info.suffix().toLower();
    resource.sizeBytes = info.size();
    resource.modifiedAt = info.lastModified();
    return LocalMediaInspectionResult::succeeded(std::move(resource));
}

} // namespace colosseum::localmedia
```

## `native/localmedia/LocalMediaHandler.h`

```cpp
#pragma once

#include "LocalMediaTypes.h"

namespace colosseum::localmedia {

class LocalMediaHandler {
public:
    virtual ~LocalMediaHandler() = default;

    virtual QString id() const = 0;
    virtual bool supports(LocalMediaKind kind) const = 0;
    virtual LocalMediaPrepareResult prepare(
        const LocalMediaOpenRequest &request) const = 0;
};

} // namespace colosseum::localmedia
```
