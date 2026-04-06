from __future__ import annotations

from datetime import datetime, timezone


ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def utc_now_iso() -> str:
    """Return a UTC timestamp in ISO-8601 format."""
    return datetime.now(tz=timezone.utc).strftime(ISO_FORMAT)
