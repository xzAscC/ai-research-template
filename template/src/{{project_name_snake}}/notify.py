"""Email when an experiment finishes or fails.

Wrap an entry point with :func:`notify_on_exit` to get one email when the
wrapped block finishes or raises::

    from <package>.notify import notify_on_exit

    with notify_on_exit("exp1", log_file="logs/exp1/run.log"):
        main()

Credentials come from the environment or from a gitignored ``.env`` at the repo
root (see ``.env.example``); real environment variables win over ``.env``:

    NOTIFY_GMAIL_USER=<sender>@gmail.com
    NOTIFY_GMAIL_APP_PASSWORD=<16-character Gmail app password>
    NOTIFY_TO=<comma-separated recipients; default: the sender>

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
        return {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
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


def _ensure_env() -> None:
    for key, value in _load_dotenv().items():
        os.environ.setdefault(key, value)


def configured() -> bool:
    _ensure_env()
    return bool(os.environ.get("NOTIFY_GMAIL_USER")) and bool(
        os.environ.get("NOTIFY_GMAIL_APP_PASSWORD")
    )


def _recipients() -> list[str]:
    raw = os.environ.get("NOTIFY_TO") or os.environ.get("NOTIFY_GMAIL_USER", "")
    return [addr.strip() for addr in raw.split(",") if addr.strip()]


def send_email(subject: str, body: str, *, to: list[str] | None = None) -> None:
    """Send a plain-text email through Gmail SMTP; raise on any failure."""
    _ensure_env()
    user = os.environ.get("NOTIFY_GMAIL_USER", "")
    password = os.environ.get("NOTIFY_GMAIL_APP_PASSWORD", "").replace(" ", "")
    if not user or not password:
        raise RuntimeError(
            "notify is not configured: set NOTIFY_GMAIL_USER and NOTIFY_GMAIL_APP_PASSWORD"
        )
    recipients = to if to is not None else _recipients()
    if not recipients:
        raise RuntimeError("notify has no recipients (NOTIFY_TO is empty)")

    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.set_content(body)

    stage = "before-send"
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=SMTP_TIMEOUT) as server:
            server.starttls(context=ssl.create_default_context())
            server.login(user, password)
            stage = "send"
            server.send_message(msg)
    except Exception as exc:
        # After the message went out, a failure does not tell whether it arrived.
        if stage == "send":
            raise AmbiguousDeliveryError("SMTP send outcome is unknown") from exc
        raise


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
    try:
        content = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ""
    return "\n".join(content[-lines:]) if lines > 0 else ""


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

    start = time.monotonic()
    host = socket.gethostname()
    try:
        yield
    except BaseException:
        status = "FAILED"
        body = [
            f"task: {task}",
            f"host: {host}",
            f"status: FAILED after {time.monotonic() - start:,.0f}s",
            "",
            traceback.format_exc(),
        ]
        raise
    else:
        status = "done"
        body = [
            f"task: {task}",
            f"host: {host}",
            f"status: completed in {time.monotonic() - start:,.0f}s",
        ]
    finally:
        if log_file is not None:
            body += ["", f"--- tail of {log_file} (last {tail_lines} lines) ---"]
            body.append(_tail(log_file, tail_lines))
        _try_send(f"[{PROJECT}] {status}: {task}", "\n".join(body))


__all__ = ["AmbiguousDeliveryError", "configured", "notify_on_exit", "send_email"]
