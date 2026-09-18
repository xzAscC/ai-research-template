"""Sensitive data redaction for logs and content."""

import re


def redact_sensitive(text: str) -> str:
    """Redact sensitive information from text.

    Detects and redacts patterns like:
        - API keys (sk-xxx, api_key=xxx, Bearer xxx)
        - Passwords (password=xxx, passwd xxx)
        - Tokens (token=xxx, auth=xxx)

    Args:
        text: Input text that may contain sensitive data.

    Returns:
        Text with sensitive information replaced by [REDACTED].
    """
    patterns = [
        # API keys - preserve key name, redact value
        (r"(api_key[=:]\s*)\S+", r"\1[REDACTED]"),
        (r"(Bearer\s+)\S+", r"\1[REDACTED]"),
        # Passwords - preserve key name, redact value
        (r"(password[=:]\s*)\S+", r"\1[REDACTED]"),
        (r"(passwd\s+)\S+", r"\1[REDACTED]"),
        # Tokens - preserve key name, redact value
        (r"(token[=:]\s*)\S+", r"\1[REDACTED]"),
        (r"(auth[=:]\s*)\S+", r"\1[REDACTED]"),
        # Standalone API keys (OpenAI-style)
        (r"sk-[a-zA-Z0-9]+", "[REDACTED]"),
    ]

    result = text
    for pattern, replacement in patterns:
        result = re.sub(pattern, replacement, result)

    return result
