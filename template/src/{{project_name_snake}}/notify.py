"""Email when an experiment finishes or fails.

Wrap an entry point with :func:`notify_on_exit` to get one email when the
wrapped block finishes or raises::

    from <package>.notify import notify_on_exit

    with notify_on_exit("exp1", log_file="logs/exp1/run.log"):
        main()

Credentials come from the environment or from a gitignored ``.env`` at the repo
root (see ``.env.example``); real environment variables win over ``.env``, and
``.env`` is never copied into ``os.environ``, so child processes do not see it:

    NOTIFY_GMAIL_USER=<sender>@gmail.com
    NOTIFY_GMAIL_APP_PASSWORD=<16-character Gmail app password>
    NOTIFY_TO=<comma-separated recipients; default: the sender>

``.env`` must be a file you own that group and others cannot write
(``chmod 600 .env``); otherwise it is ignored with a warning when the run starts.

A failed notification (missing credentials, SMTP down, no network) never stops
the run; it prints a warning to stderr.
"""

from __future__ import annotations

import os
import smtplib
import socket
import ssl
import stat
import sys
import time
import traceback
from collections import deque
from collections.abc import Iterator
from contextlib import contextmanager
from email.message import EmailMessage
from pathlib import Path

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_TIMEOUT = 30

# Subject prefix: the package name.
PROJECT = __name__.partition(".")[0]
# Only these keys are read from .env, so it cannot set PYTHONPATH, LD_PRELOAD, ...
DOTENV_KEYS = frozenset({"NOTIFY_GMAIL_USER", "NOTIFY_GMAIL_APP_PASSWORD", "NOTIFY_TO"})


class AmbiguousDeliveryError(RuntimeError):
    """The SMTP server may have accepted the message; do not retry it."""


def _dotenv_path() -> Path:
    # src/<package>/notify.py -> repo root
    return Path(__file__).resolve().parents[2] / ".env"


def _trusted(path: Path) -> bool:
    # A regular file (not a symlink) that we own and nobody else can write.
    try:
        info = path.lstat()
    except OSError:
        return False
    return stat.S_ISREG(info.st_mode) and info.st_uid == os.getuid() and not info.st_mode & 0o022


def _load_dotenv(path: Path | None = None) -> dict[str, str]:
    path = path if path is not None else _dotenv_path()
    if not _trusted(path):
        if os.path.lexists(path):
            print(
                f"[notify] ignoring {path}: it must be a regular file that you own and that "
                "group and others cannot write (chmod 600)",
                file=sys.stderr,
            )
        return {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        print(f"[notify] cannot read {path}: {exc}", file=sys.stderr)
        return {}
    values: dict[str, str] = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip("'\"")
        if key in DOTENV_KEYS:
            values[key] = value
    return values


def _settings() -> dict[str, str]:
    # Read on every use, so edits to .env during a run count. Real environment
    # variables win; nothing is written back to os.environ.
    values = _load_dotenv()
    values.update({key: os.environ[key] for key in DOTENV_KEYS if key in os.environ})
    return values


def configured() -> bool:
    settings = _settings()
    return bool(settings.get("NOTIFY_GMAIL_USER")) and bool(
        settings.get("NOTIFY_GMAIL_APP_PASSWORD")
    )


def _recipients(settings: dict[str, str]) -> list[str]:
    raw = settings.get("NOTIFY_TO") or settings.get("NOTIFY_GMAIL_USER", "")
    return [addr.strip() for addr in raw.split(",") if addr.strip()]


def send_email(subject: str, body: str, *, to: list[str] | None = None) -> None:
    """Send a plain-text email through Gmail SMTP; raise on any failure."""
    settings = _settings()
    user = settings.get("NOTIFY_GMAIL_USER", "")
    password = settings.get("NOTIFY_GMAIL_APP_PASSWORD", "").replace(" ", "")
    if not user or not password:
        raise RuntimeError(
            "notify is not configured: set NOTIFY_GMAIL_USER and NOTIFY_GMAIL_APP_PASSWORD"
        )
    recipients = to if to is not None else _recipients(settings)
    if not recipients:
        raise RuntimeError("notify has no recipients (NOTIFY_TO is empty)")

    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.set_content(body)

    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=SMTP_TIMEOUT)
    try:
        server.starttls(context=ssl.create_default_context())
        server.login(user, password)
        try:
            server.send_message(msg)
        except (smtplib.SMTPSenderRefused, smtplib.SMTPRecipientsRefused, smtplib.SMTPDataError):
            # The server refused the message, so it was not delivered.
            raise
        except Exception as exc:
            # The connection failed while sending: the message may or may not have arrived.
            raise AmbiguousDeliveryError("SMTP send outcome is unknown") from exc
    finally:
        # QUIT only ends the session. Its errors say nothing about the message, so they
        # must not replace the result above (a `with` block would let them).
        try:
            server.quit()
        except Exception:
            server.close()


def _try_send(subject: str, body: str) -> None:
    try:
        send_email(subject, body)
    except AmbiguousDeliveryError as exc:
        print(f"[notify] AMBIGUOUS send for '{subject}': {exc}", file=sys.stderr)
    except Exception as exc:  # a notification must never kill the run
        print(f"[notify] FAILED to send '{subject}': {exc}", file=sys.stderr)
    else:
        print(f"[notify] sent: {subject}", file=sys.stderr)


def _tail(path: str | Path, lines: int) -> str:
    if lines <= 0:
        return ""
    try:
        # deque keeps only the last lines, so a log of several GB needs no more memory
        with open(path, encoding="utf-8", errors="replace") as handle:
            return "".join(deque(handle, maxlen=lines)).rstrip("\n")
    except OSError:
        return ""


@contextmanager
def notify_on_exit(
    task: str,
    *,
    log_file: str | Path | None = None,
    tail_lines: int = 40,
    enabled: bool = True,
) -> Iterator[None]:
    """Email whether ``task`` finished or failed when the wrapped block exits.

    On an exception the traceback (and the tail of ``log_file`` when given) is
    emailed and the exception re-raised. ``enabled=False`` keeps the block but
    sends nothing.
    """
    if not enabled:
        yield
        return

    # Check .env now, so a problem with it shows when the run starts, not at its end.
    # The email reads it again when it is sent.
    _load_dotenv()
    start = time.monotonic()
    host = socket.gethostname()
    failure = ""
    try:
        yield
    except SystemExit as exc:
        # sys.exit() or sys.exit(0) after the work is a clean finish
        if exc.code not in (0, None):
            failure = traceback.format_exc()
        raise
    except BaseException:
        failure = traceback.format_exc()
        raise
    finally:
        seconds = f"{time.monotonic() - start:,.0f}s"
        body = [f"task: {task}", f"host: {host}"]
        if failure:
            status = "FAILED"
            body += [f"status: FAILED after {seconds}", "", failure]
        else:
            status = "done"
            body.append(f"status: completed in {seconds}")
        if log_file is not None:
            body += ["", f"--- tail of {log_file} (last {tail_lines} lines) ---"]
            body.append(_tail(log_file, tail_lines))
        _try_send(f"[{PROJECT}] {status}: {task}", "\n".join(body))


__all__ = ["AmbiguousDeliveryError", "configured", "notify_on_exit", "send_email"]
