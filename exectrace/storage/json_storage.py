from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List, Set

from exectrace.core.models import Workflow


class JsonStorage:
    def __init__(self, base_dir: str | None = None) -> None:
        home = os.environ.get("EXECTRACE_HOME") or str(Path.home() / ".exectrace")
        self.base_dir = Path(base_dir or home)
        self.workflows_dir = self.base_dir / "workflows"
        self.state_dir = self.base_dir / "state"
        self.workflows_dir.mkdir(parents=True, exist_ok=True)
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def workflow_path(self, name: str) -> Path:
        return self.workflows_dir / f"{name}.json"

    def save_workflow(self, workflow: Workflow) -> Path:
        path = self.workflow_path(workflow.name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(workflow.to_dict(), f, indent=2)
        return path

    def load_workflow(self, name: str) -> Workflow:
        path = self.workflow_path(name)
        if not path.exists():
            raise FileNotFoundError(f"Workflow '{name}' was not found")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Workflow.from_dict(data)

    def list_workflows(self) -> List[str]:
        return sorted(file.stem for file in self.workflows_dir.glob("*.json"))

    def active_recording_path(self) -> Path:
        return self.state_dir / "active_recording.json"

    def save_active_recording(self, data: Dict[str, object]) -> None:
        with open(self.active_recording_path(), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_active_recording(self) -> Dict[str, object]:
        path = self.active_recording_path()
        if not path.exists():
            raise FileNotFoundError("No active recording found. Start one with 'exectrace record <name>'.")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def clear_active_recording(self) -> None:
        path = self.active_recording_path()
        if path.exists():
            path.unlink()

    def replay_state_path(self, workflow_name: str) -> Path:
        return self.state_dir / f"replay_state_{workflow_name}.json"

    def load_replay_state(self, workflow_name: str) -> Set[str]:
        path = self.replay_state_path(workflow_name)
        if not path.exists():
            return set()
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return set(data.get("completed_signatures", []))

    def save_replay_state(self, workflow_name: str, signatures: Set[str]) -> None:
        path = self.replay_state_path(workflow_name)
        data = {"completed_signatures": sorted(signatures)}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
