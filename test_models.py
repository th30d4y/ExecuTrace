"""Regression tests for reading corrupt workflow files (#25)."""

import pytest

from exectrace.core.models import Action, Workflow


def test_action_from_dict_missing_fields_names_them():
    with pytest.raises(ValueError, match="action_type"):
        Action.from_dict({"timestamp": "2026-01-01T00:00:00Z"})
    with pytest.raises(ValueError, match="timestamp"):
        Action.from_dict({"action_type": "file_read"})
    with pytest.raises(ValueError, match="action_type, timestamp"):
        Action.from_dict({})


def test_action_from_dict_still_accepts_valid_actions():
    action = Action.from_dict(
        {"action_type": "file_read", "timestamp": "2026-01-01T00:00:00Z"}
    )
    assert action.action_type == "file_read"
    assert action.payload == {}
    assert Action.from_dict(
        {"action_type": "file_read", "timestamp": "2026-01-01T00:00:00Z", "payload": {"p": 1}}
    ).payload == {"p": 1}


def test_workflow_from_dict_missing_name_names_it():
    with pytest.raises(ValueError, match="name"):
        Workflow.from_dict({"actions": []})


def test_workflow_from_dict_still_accepts_a_valid_workflow():
    workflow = Workflow.from_dict(
        {
            "name": "demo",
            "actions": [{"action_type": "file_read", "timestamp": "2026-01-01T00:00:00Z"}],
        }
    )
    assert workflow.name == "demo"
    assert workflow.actions[0].action_type == "file_read"
