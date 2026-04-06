from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from exectrace.utils.time_utils import utc_now_iso


@dataclass
class Action:
    action_type: str
    timestamp: str
    payload: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_type": self.action_type,
            "timestamp": self.timestamp,
            "payload": self.payload,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Action":
        return cls(
            action_type=data["action_type"],
            timestamp=data["timestamp"],
            payload=data.get("payload", {}),
        )


@dataclass
class Workflow:
    name: str
    version: str = "1.0"
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)
    actions: List[Action] = field(default_factory=list)

    def add_action(self, action_type: str, payload: Dict[str, Any]) -> None:
        self.actions.append(Action(action_type=action_type, timestamp=utc_now_iso(), payload=payload))
        self.updated_at = utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "actions": [action.to_dict() for action in self.actions],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Workflow":
        return cls(
            name=data["name"],
            version=data.get("version", "1.0"),
            created_at=data.get("created_at", utc_now_iso()),
            updated_at=data.get("updated_at", utc_now_iso()),
            actions=[Action.from_dict(item) for item in data.get("actions", [])],
        )
