"""Storage factory for selecting appropriate backend."""

from __future__ import annotations

from typing import Literal, Union

from exectrace.storage.json_storage import JsonStorage
from exectrace.storage.xml_storage import XmlStorage

StorageBackend = Union[JsonStorage, XmlStorage]


def get_storage(format_type: Literal["json", "xml"] = "json", base_dir: str | None = None) -> StorageBackend:
    """Get storage backend by format type."""
    if format_type == "xml":
        return XmlStorage(base_dir)
    else:  # default to json
        return JsonStorage(base_dir)
