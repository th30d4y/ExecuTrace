"""XML-based workflow storage backend for ExecuTrace."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Set
from xml.etree import ElementTree as ET

from exectrace.core.models import Action, Workflow


class XmlStorage:
    """Store and retrieve workflows in XML format."""

    def __init__(self, base_dir: str | None = None) -> None:
        home = os.environ.get("EXECTRACE_HOME") or str(Path.home() / ".exectrace")
        self.base_dir = Path(base_dir or home)
        self.workflows_dir = self.base_dir / "workflows"
        self.state_dir = self.base_dir / "state"
        self.workflows_dir.mkdir(parents=True, exist_ok=True)
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def workflow_path(self, name: str) -> Path:
        """Get the file path for a workflow."""
        return self.workflows_dir / f"{name}.xml"

    def save_workflow(self, workflow: Workflow) -> Path:
        """Save a workflow to XML file."""
        path = self.workflow_path(workflow.name)
        
        # Create root element
        root = ET.Element("workflow")
        root.set("name", workflow.name)
        root.set("version", workflow.version)
        root.set("created_at", workflow.created_at)
        root.set("updated_at", workflow.updated_at)
        
        # Add actions
        actions_elem = ET.SubElement(root, "actions")
        for action in workflow.actions:
            action_elem = ET.SubElement(actions_elem, "action")
            action_elem.set("type", action.action_type)
            action_elem.set("timestamp", action.timestamp)
            
            # Add payload as child elements
            for key, value in action.payload.items():
                payload_elem = ET.SubElement(action_elem, "payload")
                payload_elem.set("key", key)
                payload_elem.text = str(value)
        
        # Write to file with pretty printing
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        with open(path, "wb") as f:
            tree.write(f, encoding="utf-8", xml_declaration=True)
        
        return path

    def load_workflow(self, name: str) -> Workflow:
        """Load a workflow from XML file."""
        path = self.workflow_path(name)
        if not path.exists():
            raise FileNotFoundError(f"Workflow '{name}' was not found")
        
        tree = ET.parse(path)
        root = tree.getroot()
        
        workflow = Workflow(
            name=root.get("name", name),
            version=root.get("version", "1.0"),
            created_at=root.get("created_at"),
            updated_at=root.get("updated_at"),
        )
        
        # Load actions
        actions_elem = root.find("actions")
        if actions_elem is not None:
            for action_elem in actions_elem.findall("action"):
                action_type = action_elem.get("type", "")
                timestamp = action_elem.get("timestamp", "")
                
                # Load payload
                payload: Dict[str, object] = {}
                for payload_elem in action_elem.findall("payload"):
                    key = payload_elem.get("key", "")
                    value = payload_elem.text or ""
                    payload[key] = value
                
                action = Action(action_type=action_type, timestamp=timestamp, payload=payload)
                workflow.actions.append(action)
        
        return workflow

    def list_workflows(self) -> List[str]:
        """List all available workflow names (XML format)."""
        return sorted(file.stem for file in self.workflows_dir.glob("*.xml"))

    def active_recording_path(self) -> Path:
        """Get path for active recording state file."""
        return self.state_dir / "active_recording.json"

    def save_active_recording(self, data: Dict[str, object]) -> None:
        """Save active recording state (uses JSON for simplicity)."""
        import json
        with open(self.active_recording_path(), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_active_recording(self) -> Dict[str, object]:
        """Load active recording state (uses JSON for simplicity)."""
        import json
        path = self.active_recording_path()
        if not path.exists():
            raise FileNotFoundError("No active recording found. Start one with 'exectrace record <name>'.")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def clear_active_recording(self) -> None:
        """Clear active recording state."""
        path = self.active_recording_path()
        if path.exists():
            path.unlink()

    def replay_state_path(self, workflow_name: str) -> Path:
        """Get path for replay state file."""
        return self.state_dir / f"replay_state_{workflow_name}.json"

    def load_replay_state(self, workflow_name: str) -> Set[str]:
        """Load replay state for smart replays (uses JSON for simplicity)."""
        import json
        path = self.replay_state_path(workflow_name)
        if not path.exists():
            return set()
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return set(data.get("completed_signatures", []))

    def save_replay_state(self, workflow_name: str, signatures: Set[str]) -> None:
        """Save replay state for smart replays (uses JSON for simplicity)."""
        import json
        path = self.replay_state_path(workflow_name)
        data = {"completed_signatures": sorted(signatures)}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
