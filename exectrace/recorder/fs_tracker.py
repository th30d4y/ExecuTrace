from __future__ import annotations

import base64
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

from exectrace.utils.hash_utils import sha256_bytes


@dataclass
class FileSnapshotEntry:
    sha256: str
    size: int


def snapshot_directory(root_dir: Path) -> Dict[str, FileSnapshotEntry]:
    """Capture a file snapshot for deterministic change detection."""
    snapshot: Dict[str, FileSnapshotEntry] = {}
    for path in root_dir.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            rel = str(path.relative_to(root_dir))
            content = path.read_bytes()
            snapshot[rel] = FileSnapshotEntry(sha256=sha256_bytes(content), size=len(content))
    return snapshot


def encode_file_content(path: Path) -> Tuple[str, bool]:
    content = path.read_bytes()
    try:
        content.decode("utf-8")
        is_binary = False
    except UnicodeDecodeError:
        is_binary = True
    return base64.b64encode(content).decode("ascii"), is_binary


def diff_snapshots(
    root_dir: Path,
    before: Dict[str, FileSnapshotEntry],
    after: Dict[str, FileSnapshotEntry],
) -> List[dict]:
    actions: List[dict] = []

    before_paths = set(before.keys())
    after_paths = set(after.keys())

    created = sorted(after_paths - before_paths)
    deleted = sorted(before_paths - after_paths)
    possibly_modified = sorted(before_paths & after_paths)

    for rel_path in created:
        file_path = root_dir / rel_path
        encoded, is_binary = encode_file_content(file_path)
        actions.append(
            {
                "action_type": "file_create",
                "payload": {
                    "path": rel_path,
                    "content_b64": encoded,
                    "is_binary": is_binary,
                },
            }
        )

    for rel_path in possibly_modified:
        if before[rel_path].sha256 != after[rel_path].sha256:
            file_path = root_dir / rel_path
            encoded, is_binary = encode_file_content(file_path)
            actions.append(
                {
                    "action_type": "file_modify",
                    "payload": {
                        "path": rel_path,
                        "content_b64": encoded,
                        "is_binary": is_binary,
                    },
                }
            )

    for rel_path in deleted:
        actions.append(
            {
                "action_type": "file_delete",
                "payload": {
                    "path": rel_path,
                },
            }
        )

    return actions
