"""Evidence file scanning and attachment preparation."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Blocked file extensions per Resend documentation
BLOCKED_EXTENSIONS: set[str] = {
    ".exe",
    ".bat",
    ".js",
    ".ps1",
    ".cmd",
    ".com",
    ".scr",
    ".vbs",
    ".jar",
}


class EvidenceDirNotFoundError(Exception):
    """Raised when the evidence directory does not exist."""

    pass


def scan_evidence_dir(directory: Path) -> list[Path]:
    """Scan a directory for evidence files.

    Args:
        directory: Path to the evidence directory to scan.

    Returns:
        List of paths to evidence files found (top-level only, non-recursive).

    Raises:
        EvidenceDirNotFoundError: If the directory does not exist.
    """
    if not directory.exists():
        raise EvidenceDirNotFoundError(f"Evidence directory not found: {directory}")

    if not directory.is_dir():
        raise EvidenceDirNotFoundError(f"Path is not a directory: {directory}")

    files = [p for p in directory.iterdir() if p.is_file()]

    if not files:
        logger.warning("Evidence directory is empty: %s", directory)

    return files


def filter_blocked_extensions(files: list[Path]) -> list[Path]:
    """Filter out files with blocked extensions.

    Blocked extensions (per Resend documentation): .exe, .bat, .js, .ps1,
    .cmd, .com, .scr, .vbs, .jar

    Args:
        files: List of file paths to filter.

    Returns:
        List of file paths with blocked extensions removed.
    """
    return [f for f in files if f.suffix.lower() not in BLOCKED_EXTENSIONS]


def prepare_attachments(paths: list[Path]) -> list[dict[str, str | list[bytes]]]:
    """Prepare files for email attachment in Resend format.

    Args:
        paths: List of file paths to prepare.

    Returns:
        List of attachment dicts with keys:
            - filename: str - the file name
            - content: list[bytes] - file content as list of bytes
    """
    attachments: list[dict[str, str | list[bytes]]] = []

    for path in paths:
        content_bytes = path.read_bytes()
        attachments.append(
            {
                "filename": path.name,
                "content": [content_bytes],
            }
        )

    return attachments
