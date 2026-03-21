"""Notification module for sending task completion emails."""

from {{ project_name_snake }}.notify.core import NotificationError, send_task_notification
from {{ project_name_snake }}.notify.evidence import EvidenceDirNotFoundError

__all__ = [
    "send_task_notification",
    "NotificationError",
    "EvidenceDirNotFoundError",
]
