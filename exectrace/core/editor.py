from __future__ import annotations

from typing import Union

from exectrace.core.models import Workflow
from exectrace.storage.factory import get_storage
from exectrace.storage.json_storage import JsonStorage
from exectrace.storage.xml_storage import XmlStorage


class WorkflowEditor:
    """Load, modify, and save workflows programmatically."""

    def __init__(self, storage: Union[JsonStorage, XmlStorage] | None = None) -> None:
        self.storage = storage or get_storage("json")

    def load(self, name: str) -> Workflow:
        return self.storage.load_workflow(name)

    def save(self, workflow: Workflow) -> None:
        self.storage.save_workflow(workflow)

    def remove_action(self, workflow: Workflow, index: int) -> None:
        if index < 0 or index >= len(workflow.actions):
            raise IndexError("Action index out of range")
        workflow.actions.pop(index)
