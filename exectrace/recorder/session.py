from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Literal, Union

from exectrace.core.models import Workflow
from exectrace.recorder.command_capture import (
    capture_commands_since,
    detect_history_file,
    history_line_count,
)
from exectrace.recorder.fs_tracker import FileSnapshotEntry, diff_snapshots, snapshot_directory
from exectrace.storage.factory import get_storage
from exectrace.storage.json_storage import JsonStorage
from exectrace.storage.xml_storage import XmlStorage
from exectrace.utils.logger import get_logger
from exectrace.utils.time_utils import utc_now_iso

logger = get_logger(__name__)


class RecorderSession:
    def __init__(
        self,
        storage: Union[JsonStorage, XmlStorage] | None = None,
        storage_format: Literal["json", "xml"] = "json",
        storage_path: str | None = None,
    ) -> None:
        if storage:
            self.storage = storage
        else:
            self.storage = get_storage(storage_format, storage_path)

    def start(self, name: str, root_dir: str | None = None) -> Dict[str, Any]:
        root = Path(root_dir or ".").resolve()
        history_file = detect_history_file()
        history_start_line = history_line_count(history_file) if history_file else 0

        snapshot = snapshot_directory(root)

        state = {
            "name": name,
            "started_at": utc_now_iso(),
            "root_dir": str(root),
            "history_file": str(history_file) if history_file else None,
            "history_start_line": history_start_line,
            "snapshot": {k: {"sha256": v.sha256, "size": v.size} for k, v in snapshot.items()},
        }

        self.storage.save_active_recording(state)
        logger.info("Recording started: %s", name)
        return state

    def stop(self) -> Workflow:
        state = self.storage.load_active_recording()
        workflow = Workflow(name=str(state["name"]))
        workflow.created_at = str(state["started_at"])

        root_dir = Path(str(state["root_dir"]))
        before_snapshot = {
            path: FileSnapshotEntry(sha256=entry["sha256"], size=entry["size"])
            for path, entry in dict(state["snapshot"]).items()
        }
        after_snapshot = snapshot_directory(root_dir)

        history_file_value = state.get("history_file")
        if history_file_value:
            commands, _ = capture_commands_since(Path(str(history_file_value)), int(state["history_start_line"]))
            for command in commands:
                if command.strip():
                    workflow.add_action("command", {"command": command, "cwd": str(root_dir)})

        file_actions = diff_snapshots(root_dir, before_snapshot, after_snapshot)
        for item in file_actions:
            workflow.add_action(item["action_type"], item["payload"])

        self.storage.save_workflow(workflow)
        self.storage.clear_active_recording()
        logger.info("Recording stopped: %s (%d actions)", workflow.name, len(workflow.actions))
        return workflow
