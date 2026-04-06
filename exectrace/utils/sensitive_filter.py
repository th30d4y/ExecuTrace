from __future__ import annotations

import re
from typing import Iterable

DEFAULT_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key\s*[=:]\s*)([^\s]+)"),
    re.compile(r"(?i)(token\s*[=:]\s*)([^\s]+)"),
    re.compile(r"(?i)(password\s*[=:]\s*)([^\s]+)"),
    re.compile(r"(?i)(secret\s*[=:]\s*)([^\s]+)"),
    re.compile(r"(?i)(Authorization:\s*Bearer\s+)([^\s]+)"),
]


def redact_text(text: str, patterns: Iterable[re.Pattern] | None = None) -> str:
    """Redact common secrets from captured command text."""
    active_patterns = list(patterns) if patterns is not None else DEFAULT_PATTERNS
    result = text
    for pattern in active_patterns:
        result = pattern.sub(r"\1<REDACTED>", result)
    return result
