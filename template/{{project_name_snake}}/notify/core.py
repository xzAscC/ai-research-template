"""Core notification functionality."""

import logging
import os
import time
from pathlib import Path

import resend
from resend import exceptions

from {{ project_name_snake }}.notify.email_template import generate_html_email, generate_text_email
from {{ project_name_snake }}.notify.evidence import (
    EvidenceDirNotFoundError,
    filter_blocked_extensions,
    prepare_attachments,
    scan_evidence_dir,
)
from {{ project_name_snake }}.notify.redact import redact_sensitive

logger = logging.getLogger(__name__)


class NotificationError(Exception):
    """Raised when notification sending fails."""

    pass


def send_task_notification(
    task_name: str,
    status: str,
    logs: list[str],
    duration: float,
    attachment_paths: list[Path] | None = None,
    evidence_dir: Path | None = None,
    max_log_lines: int = 500,
) -> str:
    """Send a task completion notification via email.

    Args:
        task_name: Name of the task that was executed.
        status: Execution status (e.g., "success", "failure").
        logs: List of log lines from task execution.
        duration: Task duration in seconds.
        attachment_paths: Optional list of file paths to attach.
        evidence_dir: Optional directory to scan for evidence files.
        max_log_lines: Maximum number of log lines to include.

    Returns:
        Message ID of the sent email.

    Raises:
        NotificationError: If required environment variables are missing or
            sending fails after all retries.
    """
    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        raise NotificationError("RESEND_API_KEY environment variable is not set")

    notification_email = os.environ.get("NOTIFICATION_EMAIL")
    if not notification_email:
        raise NotificationError("NOTIFICATION_EMAIL environment variable is not set")

    truncated = len(logs) > max_log_lines
    if truncated:
        logs = logs[-max_log_lines:]
        logger.info("Logs truncated to %d lines", max_log_lines)

    redacted_logs = [redact_sensitive(line) for line in logs]

    all_attachment_paths: list[Path] = []
    if attachment_paths:
        all_attachment_paths.extend(attachment_paths)

    if evidence_dir:
        try:
            evidence_files = scan_evidence_dir(evidence_dir)
            filtered_files = filter_blocked_extensions(evidence_files)
            all_attachment_paths.extend(filtered_files)
        except EvidenceDirNotFoundError as e:
            logger.warning("Evidence directory not found: %s", e)

    attachments = prepare_attachments(all_attachment_paths) if all_attachment_paths else None

    html_content = generate_html_email(
        task_name=task_name,
        status=status,
        logs=redacted_logs,
        duration=duration,
        truncated=truncated,
    )

    text_content = generate_text_email(
        task_name=task_name,
        status=status,
        logs=redacted_logs,
        duration=duration,
        truncated=truncated,
    )

    resend.api_key = api_key

    params: dict = {
        "from": "onboarding@resend.dev",
        "to": [notification_email],
        "subject": f"Task Notification: {task_name} - {status}",
        "html": html_content,
        "text": text_content,
    }

    if attachments:
        params["attachments"] = attachments

    max_retries = 3
    backoff_delays = [1, 2, 4]

    retryable_exceptions = (exceptions.RateLimitError, exceptions.ApplicationError)

    for attempt in range(max_retries):
        try:
            email = resend.Emails.send(params)
            logger.info("Notification sent successfully: %s", email["id"])
            return email["id"]
        except (exceptions.MissingApiKeyError, exceptions.InvalidApiKeyError, exceptions.ValidationError) as e:
            logger.error("Non-retryable error sending notification: %s", e)
            raise NotificationError(f"Failed to send notification: {e}") from e
        except retryable_exceptions as e:
            if attempt < max_retries - 1:
                delay = backoff_delays[attempt]
                logger.warning(
                    "Retryable error on attempt %d/%d, waiting %ds: %s",
                    attempt + 1,
                    max_retries,
                    delay,
                    e,
                )
                time.sleep(delay)
            else:
                logger.error("All retry attempts exhausted: %s", e)
                raise NotificationError(f"Failed to send notification after {max_retries} attempts: {e}") from e

    raise NotificationError("Unexpected error in notification sending")
