# Local Media Launch Slice 3C — Code Part 01: Bare-libmpv Admission Probe r1

## Status

**Reference implementation candidate; uncompiled, untested, unexecuted, unadopted, and runtime-unverified.**

## Proposed Locations

- Likely: `native/localmedia/LocalVideoAdmission.h`
- Likely: `native/localmedia/LibmpvAdmissionProbe.h`
- Likely: `native/localmedia/LibmpvAdmissionProbe.cpp`

The execution agent must reconcile names and paths with the adopted Slice 1 layout.

## Slice 1 Typed-Error Amendment

Add the following values to `LocalMediaErrorCode` and its name mapping:

```cpp
Player1Required,
AdmissionCancelled,
AdmissionTimedOut,
Undecodable,
ResourceChanged
```

Recommended stable names:

```text
player1-required
admission-cancelled
admission-timed-out
undecodable
resource-changed
```

`UnsupportedFormat` remains appropriate when classification rejects an extension before libmpv admission. `Undecodable` means classification accepted the resource but libmpv rejected opening it.

## `LocalVideoAdmission.h`

```cpp
#pragma once

#include "LocalMediaTypes.h"

#include <QString>
#include <QtGlobal>

namespace colosseum::localmedia {

struct LocalVideoAdmissionResult {
    bool admitted = false;
    quint64 generation = 0;
    LocalMediaError error;
    QString mpvEvent;
    int mpvError = 0;
    qint64 elapsedMs = 0;

    static LocalVideoAdmissionResult success(
        quint64 generation,
        qint64 elapsedMs)
    {
        LocalVideoAdmissionResult result;
        result.admitted = true;
        result.generation = generation;
        result.mpvEvent = QStringLiteral("file-loaded");
        result.elapsedMs = elapsedMs;
        return result;
    }

    static LocalVideoAdmissionResult failure(
        quint64 generation,
        LocalMediaError error,
        QString mpvEvent,
        int mpvError,
        qint64 elapsedMs)
    {
        LocalVideoAdmissionResult result;
        result.generation = generation;
        result.error = std::move(error);
        result.mpvEvent = std::move(mpvEvent);
        result.mpvError = mpvError;
        result.elapsedMs = elapsedMs;
        return result;
    }
};

} // namespace colosseum::localmedia

Q_DECLARE_METATYPE(colosseum::localmedia::LocalVideoAdmissionResult)
```

## `LibmpvAdmissionProbe.h`

```cpp
#pragma once

#include "LocalVideoAdmission.h"

#include <QFutureWatcher>
#include <QList>
#include <QObject>
#include <QString>

#include <atomic>
#include <memory>
#include <utility>

namespace colosseum::localmedia {

class LibmpvAdmissionProbe final : public QObject {
    Q_OBJECT

public:
    explicit LibmpvAdmissionProbe(QObject *parent = nullptr);
    ~LibmpvAdmissionProbe() override;

    void begin(const QString &canonicalPath,
               quint64 generation,
               int timeoutMs);
    void cancel();

signals:
    void finished(
        const colosseum::localmedia::LocalVideoAdmissionResult &result);

private:
    static LocalVideoAdmissionResult run(
        QString canonicalPath,
        quint64 generation,
        int timeoutMs,
        const std::shared_ptr<std::atomic_bool> &cancelled);

    struct Job {
        QFutureWatcher<LocalVideoAdmissionResult> *watcher = nullptr;
        std::shared_ptr<std::atomic_bool> cancelled;
    };

    QList<Job> m_jobs;
};

} // namespace colosseum::localmedia
```

## `LibmpvAdmissionProbe.cpp`

```cpp
#include "LibmpvAdmissionProbe.h"

#include <QElapsedTimer>
#include <QFile>
#include <QtConcurrent>

#include <mpv/client.h>

namespace colosseum::localmedia {
namespace {

LocalMediaError admissionError(
    LocalMediaErrorCode code,
    const QString &userMessage,
    const QString &diagnostic)
{
    return LocalMediaError::make(code, userMessage, diagnostic);
}

bool setOption(mpv_handle *ctx, const char *name, const char *value)
{
    return mpv_set_option_string(ctx, name, value) >= 0;
}

} // namespace

LibmpvAdmissionProbe::LibmpvAdmissionProbe(QObject *parent)
    : QObject(parent)
{
    qRegisterMetaType<LocalVideoAdmissionResult>();
}

LibmpvAdmissionProbe::~LibmpvAdmissionProbe()
{
    cancel();
    for (const Job &job : std::as_const(m_jobs))
        job.watcher->waitForFinished();
}

void LibmpvAdmissionProbe::begin(
    const QString &canonicalPath,
    quint64 generation,
    int timeoutMs)
{
    // Superseding a launch never blocks the GUI thread waiting for the old
    // worker. The old generation is cancelled and allowed to retire.
    cancel();

    Job job;
    job.watcher =
        new QFutureWatcher<LocalVideoAdmissionResult>(this);
    job.cancelled =
        std::make_shared<std::atomic_bool>(false);

    QFutureWatcher<LocalVideoAdmissionResult> *watcher =
        job.watcher;
    const auto cancelled = job.cancelled;
    m_jobs.append(job);

    connect(watcher,
            &QFutureWatcher<LocalVideoAdmissionResult>::finished,
            this,
            [this, watcher] {
                const LocalVideoAdmissionResult result =
                    watcher->result();

                for (int i = 0; i < m_jobs.size(); ++i) {
                    if (m_jobs.at(i).watcher == watcher) {
                        m_jobs.removeAt(i);
                        break;
                    }
                }

                watcher->deleteLater();
                emit finished(result);
            });

    watcher->setFuture(QtConcurrent::run(
        [canonicalPath, generation, timeoutMs, cancelled] {
            return run(canonicalPath,
                       generation,
                       timeoutMs,
                       cancelled);
        }));
}

void LibmpvAdmissionProbe::cancel()
{
    for (const Job &job : std::as_const(m_jobs))
        job.cancelled->store(true, std::memory_order_release);
}

LocalVideoAdmissionResult LibmpvAdmissionProbe::run(
    QString canonicalPath,
    quint64 generation,
    int timeoutMs,
    const std::shared_ptr<std::atomic_bool> &cancelled)
{
    QElapsedTimer elapsed;
    elapsed.start();

    if (canonicalPath.trimmed().isEmpty()) {
        return LocalVideoAdmissionResult::failure(
            generation,
            admissionError(
                LocalMediaErrorCode::NotFound,
                QStringLiteral("That video is no longer available."),
                QStringLiteral("Admission received an empty canonical path.")),
            QStringLiteral("precondition"),
            0,
            elapsed.elapsed());
    }

    mpv_handle *ctx = mpv_create();
    if (!ctx) {
        return LocalVideoAdmissionResult::failure(
            generation,
            admissionError(
                LocalMediaErrorCode::HandlerRejected,
                QStringLiteral("Colosseum could not inspect that video."),
                QStringLiteral("mpv_create returned null.")),
            QStringLiteral("create"),
            0,
            elapsed.elapsed());
    }

    auto destroy = [&ctx] {
        if (ctx) {
            mpv_terminate_destroy(ctx);
            ctx = nullptr;
        }
    };

    // Isolated admission: no user config, scripts, audio output, or visual surface.
    // This is the Brotherhood-approved baseline. The live fixture gate below
    // decides whether it is sufficiently discriminating for the installed libmpv.
    const bool optionsOk =
        setOption(ctx, "config", "no")
        && setOption(ctx, "load-scripts", "no")
        && setOption(ctx, "audio", "no")
        && setOption(ctx, "vid", "no")
        && setOption(ctx, "vo", "null")
        && setOption(ctx, "idle", "yes");

    if (!optionsOk || mpv_initialize(ctx) < 0) {
        destroy();
        return LocalVideoAdmissionResult::failure(
            generation,
            admissionError(
                LocalMediaErrorCode::HandlerRejected,
                QStringLiteral("Colosseum could not inspect that video."),
                QStringLiteral("libmpv admission initialization failed.")),
            QStringLiteral("initialize"),
            0,
            elapsed.elapsed());
    }

    // libmpv's client API accepts UTF-8 paths; do not narrow Windows
    // Unicode paths through the local 8-bit codec.
    const QByteArray encodedPath = canonicalPath.toUtf8();
    const char *command[] = {
        "loadfile",
        encodedPath.constData(),
        "replace",
        nullptr
    };

    const int commandResult = mpv_command_async(ctx, 1, command);
    if (commandResult < 0) {
        const QString diagnostic =
            QStringLiteral("mpv_command_async(loadfile) failed: %1")
                .arg(QString::fromUtf8(mpv_error_string(commandResult)));
        destroy();
        return LocalVideoAdmissionResult::failure(
            generation,
            admissionError(
                LocalMediaErrorCode::Undecodable,
                QStringLiteral("Colosseum could not open that video."),
                diagnostic),
            QStringLiteral("command"),
            commandResult,
            elapsed.elapsed());
    }

    while (elapsed.elapsed() < timeoutMs) {
        if (cancelled->load(std::memory_order_acquire)) {
            destroy();
            return LocalVideoAdmissionResult::failure(
                generation,
                admissionError(
                    LocalMediaErrorCode::AdmissionCancelled,
                    QString(),
                    QStringLiteral("Admission was superseded or cancelled.")),
                QStringLiteral("cancelled"),
                0,
                elapsed.elapsed());
        }

        mpv_event *event = mpv_wait_event(ctx, 0.05);
        switch (event->event_id) {
        case MPV_EVENT_FILE_LOADED: {
            const qint64 elapsedMs = elapsed.elapsed();
            destroy();
            return LocalVideoAdmissionResult::success(
                generation,
                elapsedMs);
        }
        case MPV_EVENT_END_FILE: {
            const auto *end =
                static_cast<const mpv_event_end_file *>(event->data);
            const int errorCode = end ? end->error : 0;
            const QString errorText =
                errorCode < 0
                    ? QString::fromUtf8(mpv_error_string(errorCode))
                    : QStringLiteral("end-file before file-loaded");
            const QString diagnostic =
                QStringLiteral("libmpv rejected admission: reason=%1 error=%2 (%3)")
                    .arg(end ? int(end->reason) : -1)
                    .arg(errorCode)
                    .arg(errorText);
            const qint64 elapsedMs = elapsed.elapsed();
            destroy();
            return LocalVideoAdmissionResult::failure(
                generation,
                admissionError(
                    LocalMediaErrorCode::Undecodable,
                    QStringLiteral("Colosseum could not decode that video."),
                    diagnostic),
                QStringLiteral("end-file"),
                errorCode,
                elapsedMs);
        }
        case MPV_EVENT_SHUTDOWN: {
            const qint64 elapsedMs = elapsed.elapsed();
            destroy();
            return LocalVideoAdmissionResult::failure(
                generation,
                admissionError(
                    LocalMediaErrorCode::HandlerRejected,
                    QStringLiteral("Colosseum could not inspect that video."),
                    QStringLiteral("libmpv shut down during admission.")),
                QStringLiteral("shutdown"),
                0,
                elapsedMs);
        }
        default:
            break;
        }
    }

    destroy();
    return LocalVideoAdmissionResult::failure(
        generation,
        admissionError(
            LocalMediaErrorCode::AdmissionTimedOut,
            QStringLiteral("Colosseum took too long to inspect that video."),
            QStringLiteral("libmpv admission exceeded %1 ms.")
                .arg(timeoutMs)),
        QStringLiteral("timeout"),
        0,
        elapsed.elapsed());
}

} // namespace colosseum::localmedia
```

## Mandatory Probe Experiment

Before reconstructing the launch adapter, run a tiny live harness against:

1. one supported local video;
2. a truncated/corrupt container;
3. an encrypted/protected fixture;
4. a valid container carrying an unsupported video codec;
5. a missing path;
6. a path removed while admission is running.

Pass condition:

- supported fixture reaches `MPV_EVENT_FILE_LOADED`;
- every required rejection fixture produces a typed failure before any shell session exists;
- cancellation and timeout return promptly and cannot deliver a stale success.

### Strengthening branch

`MPV_EVENT_FILE_LOADED` means headers were read and decoding is beginning; it does not by itself prove a frame rendered. If the baseline `vid=no` probe admits an unsupported-codec fixture that Player 1 later rejects, replace only the worker policy with a bounded null-output decode:

```text
video enabled
vo=null
audio=no
frames=1
admit only after first decoded-frame evidence
```

Keep the public probe contract unchanged. Do not weaken the acceptance criterion.

## Completion Criterion

This part is ready for adoption only when the live harness proves the installed libmpv discriminates the agreed fixtures, cancellation is bounded, and no session API is reachable from the probe.
