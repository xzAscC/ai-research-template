"""Email template generation for task notifications."""

import html


def format_duration(seconds: float) -> str:
    """Format a duration in seconds to a human-readable string.

    Args:
        seconds: Duration in seconds.

    Returns:
        Human-readable duration string (e.g., "2h 30m 15s", "2m 5s", "30s").
    """
    if seconds < 0:
        seconds = 0

    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")

    return " ".join(parts)


def generate_html_email(
    task_name: str,
    status: str,
    logs: list[str],
    duration: float,
    truncated: bool = False,
    attachment_info: list[dict] | None = None,
) -> str:
    """Generate an HTML email body for task notification.

    Args:
        task_name: Name of the task that was executed.
        status: Execution status (e.g., "success", "failure").
        logs: List of log lines from task execution.
        duration: Task duration in seconds.
        truncated: Whether the logs were truncated.
        attachment_info: Optional list of attachment metadata dicts.

    Returns:
        HTML string for the email body.
    """
    # Security: Escape user-provided content to prevent XSS
    escaped_task_name = html.escape(task_name)
    escaped_status = html.escape(status.upper())
    escaped_logs = [html.escape(line) for line in logs]

    status_colors = {
        "success": "#28a745",
        "failure": "#dc3545",
    }
    status_color = status_colors.get(status.lower(), "#6c757d")

    duration_str = format_duration(duration)

    logs_html = "<br>".join(escaped_logs) if escaped_logs else "No logs available."

    truncated_notice = ""
    if truncated:
        truncated_notice = '<p style="color: #856404; background-color: #fff3cd; padding: 10px; border-radius: 4px; margin: 10px 0;">⚠️ Output was truncated due to size limits.</p>'

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Notification</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <table style="width: 100%; border-collapse: collapse; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <tr>
            <td style="padding: 20px; border-bottom: 1px solid #eee;">
                <h1 style="margin: 0; font-size: 24px; color: #333;">Task Notification</h1>
            </td>
        </tr>
        <tr>
            <td style="padding: 20px;">
                <table style="width: 100%;">
                    <tr>
                        <td style="padding: 8px 0; font-weight: bold; width: 120px;">Task:</td>
                        <td style="padding: 8px 0;">{escaped_task_name}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; font-weight: bold;">Status:</td>
                        <td style="padding: 8px 0;"><span style="background-color: {status_color}; color: white; padding: 4px 12px; border-radius: 4px; font-weight: bold;">{escaped_status}</span></td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; font-weight: bold;">Duration:</td>
                        <td style="padding: 8px 0;">{duration_str}</td>
                    </tr>
                </table>
                {truncated_notice}
                <h2 style="font-size: 18px; margin-top: 20px; margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 10px;">Logs</h2>
                <pre style="background-color: #f8f9fa; padding: 15px; border-radius: 4px; overflow-x: auto; font-size: 13px; white-space: pre-wrap; word-wrap: break-word;">{logs_html}</pre>
            </td>
        </tr>
    </table>
</body>
</html>"""

    return html_content


def generate_text_email(
    task_name: str,
    status: str,
    logs: list[str],
    duration: float,
    truncated: bool = False,
    attachment_info: list[dict] | None = None,
) -> str:
    """Generate a plain text email body for task notification.

    Args:
        task_name: Name of the task that was executed.
        status: Execution status (e.g., "success", "failure").
        logs: List of log lines from task execution.
        duration: Task duration in seconds.
        truncated: Whether the logs were truncated.
        attachment_info: Optional list of attachment metadata dicts.

    Returns:
        Plain text string for the email body.
    """
    duration_str = format_duration(duration)

    lines = [
        "=" * 50,
        "TASK NOTIFICATION",
        "=" * 50,
        "",
        f"Task:     {task_name}",
        f"Status:   {status.upper()}",
        f"Duration: {duration_str}",
        "",
    ]

    if truncated:
        lines.append("⚠️ Output was truncated due to size limits.")
        lines.append("")

    lines.append("-" * 50)
    lines.append("LOGS")
    lines.append("-" * 50)

    if logs:
        lines.extend(logs)
    else:
        lines.append("No logs available.")

    lines.append("")
    lines.append("=" * 50)

    return "\n".join(lines)
