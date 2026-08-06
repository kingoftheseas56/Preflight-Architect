# Local Media Launch Slice 1 — Reference Code Part

**Status:** implementable reference code; uncompiled, untested, unexecuted, unadopted, and unverified.

**Colosseum basis:** `master@bb8eecb40eb8a50b7ded62f79035c555972c3fef`

This is one canonical segment of the interim Slice 1 bundle. The execution agent must inspect, adapt, compile, test, and runtime-validate before adoption.

## `native/localmedia/LocalMediaRouter.h`

```cpp
#pragma once

#include "LocalMediaClassifier.h"
#include "LocalMediaHandler.h"
#include "LocalMediaInspector.h"

#include <QList>

namespace colosseum::localmedia {

class LocalMediaRouter {
public:
    LocalMediaRouteResult route(
        const QUrl &source,
        const QString &intakeSource,
        const LocalMediaClassifier &classifier,
        const QList<const LocalMediaHandler *> &handlers) const;

private:
    static LocalMediaError validateSessionDescriptor(
        const QVariantMap &descriptor);
};

} // namespace colosseum::localmedia
```

## `native/localmedia/LocalMediaRouter.cpp`

```cpp
#include "LocalMediaRouter.h"

#include <QStringList>

namespace colosseum::localmedia {

LocalMediaRouteResult LocalMediaRouter::route(
    const QUrl &source,
    const QString &intakeSource,
    const LocalMediaClassifier &classifier,
    const QList<const LocalMediaHandler *> &handlers) const
{
    const LocalMediaInspector inspector;
    const LocalMediaInspectionResult inspection = inspector.inspect(source);
    if (!inspection.ok)
        return LocalMediaRouteResult::failed(inspection.error);

    const LocalMediaClassificationResult classification =
        classifier.classify(inspection.resource);
    if (!classification.ok)
        return LocalMediaRouteResult::failed(classification.error);

    QList<const LocalMediaHandler *> matches;
    for (const LocalMediaHandler *handler : handlers) {
        if (handler != nullptr && handler->supports(classification.kind))
            matches.append(handler);
    }

    if (matches.isEmpty()) {
        return LocalMediaRouteResult::failed(LocalMediaError::make(
            LocalMediaErrorCode::HandlerUnavailable,
            QStringLiteral("Colosseum cannot open this file yet."),
            QStringLiteral("No handler supports local-media kind '%1'.")
                .arg(localMediaKindName(classification.kind))));
    }

    if (matches.size() != 1) {
        QStringList ids;
        for (const LocalMediaHandler *handler : std::as_const(matches))
            ids << handler->id();

        return LocalMediaRouteResult::failed(LocalMediaError::make(
            LocalMediaErrorCode::AmbiguousHandler,
            QStringLiteral("Colosseum cannot choose how to open this file."),
            QStringLiteral("Multiple handlers support kind '%1': %2.")
                .arg(localMediaKindName(classification.kind),
                     ids.join(QStringLiteral(", "))));
    }

    const LocalMediaHandler *handler = matches.constFirst();
    const QString handlerId = handler->id().trimmed();
    if (handlerId.isEmpty()) {
        return LocalMediaRouteResult::failed(LocalMediaError::make(
            LocalMediaErrorCode::HandlerRejected,
            QStringLiteral("Colosseum cannot open this file yet."),
            QStringLiteral("The selected local-media handler has an empty id.")));
    }

    LocalMediaOpenRequest request;
    request.resource = inspection.resource;
    request.kind = classification.kind;
    request.intakeSource = intakeSource.trimmed();

    const LocalMediaPrepareResult prepared = handler->prepare(request);
    if (!prepared.ok) {
        if (prepared.error.isError())
            return LocalMediaRouteResult::failed(prepared.error);

        return LocalMediaRouteResult::failed(LocalMediaError::make(
            LocalMediaErrorCode::HandlerRejected,
            QStringLiteral("Colosseum could not prepare that file."),
            QStringLiteral("Handler '%1' failed without a typed error.").arg(handlerId)));
    }

    const LocalMediaError descriptorError =
        validateSessionDescriptor(prepared.sessionDescriptor);
    if (descriptorError.isError())
        return LocalMediaRouteResult::failed(descriptorError);

    return LocalMediaRouteResult::succeeded(
        inspection.resource,
        classification.kind,
        handlerId,
        prepared.sessionDescriptor);
}

LocalMediaError LocalMediaRouter::validateSessionDescriptor(
    const QVariantMap &descriptor)
{
    const QString appType = descriptor.value(QStringLiteral("appType")).toString().trimmed();
    const QString contentKind =
        descriptor.value(QStringLiteral("contentKind")).toString().trimmed();
    const QString title = descriptor.value(QStringLiteral("title")).toString().trimmed();
    const QVariantMap target = descriptor.value(QStringLiteral("target")).toMap();

    if (appType.isEmpty() || contentKind.isEmpty() || title.isEmpty() || target.isEmpty()) {
        return LocalMediaError::make(
            LocalMediaErrorCode::InvalidSessionDescriptor,
            QStringLiteral("Colosseum could not prepare that file."),
            QStringLiteral("A#SessionStore descriptor requires non-empty appType, contentKind, title, and target fields."));
    }

    const QStringList identityKeys {
        QStringLiteral("showKey"),
        QStringLiteral("id"),
        QStringLiteral("path"),
        QStringLiteral("infoHash")
    };

    for (const QString &key : identityKeys) {
        if (!target.value(key).toString().trimmed().isEmpty())
            return {};
    }

    return LocalMediaError::make(
        LocalMediaErrorCode::InvalidSessionDescriptor,
        QStringLiteral("Colosseum could not prepare that file."),
        QStringLiteral("The SessionStore target requires showKey, id, path, or infoHash as a provisional identity."));
}

} // namespace colosseum::localmedia
```
