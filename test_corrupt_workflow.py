"""Unit tests for corrupt workflow validation and error handling (fixes issue #25)."""

import json
import os
import tempfile
import unittest
from pathlib import Path

from exectrace.cli import main
from exectrace.core.models import Action, Workflow
from exectrace.storage.json_storage import JsonStorage
from exectrace.storage.xml_storage import XmlStorage


class CorruptWorkflowTests(unittest.TestCase):
    def test_action_from_dict_non_dict(self):
        with self.assertRaises(ValueError) as ctx:
            Action.from_dict("not-a-dict")
        self.assertIn("must be a dictionary", str(ctx.exception))

    def test_action_from_dict_missing_action_type(self):
        with self.assertRaises(ValueError) as ctx:
            Action.from_dict({"timestamp": "2026-01-01T00:00:00Z"})
        self.assertIn("missing required field 'action_type'", str(ctx.exception))

    def test_action_from_dict_missing_timestamp(self):
        with self.assertRaises(ValueError) as ctx:
            Action.from_dict({"action_type": "command"})
        self.assertIn("missing required field 'timestamp'", str(ctx.exception))

    def test_workflow_from_dict_non_dict(self):
        with self.assertRaises(ValueError) as ctx:
            Workflow.from_dict(None)
        self.assertIn("must be a dictionary", str(ctx.exception))

    def test_workflow_from_dict_missing_name(self):
        with self.assertRaises(ValueError) as ctx:
            Workflow.from_dict({"version": "1.0", "actions": []})
        self.assertIn("missing required field 'name'", str(ctx.exception))

    def test_json_storage_load_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            storage = JsonStorage(tmp)
            bad_file = storage.workflow_path("broken")
            bad_file.write_text("{ unclosed json: ", encoding="utf-8")

            with self.assertRaises(ValueError) as ctx:
                storage.load_workflow("broken")
            self.assertIn("Corrupt workflow file", str(ctx.exception))
            self.assertIn("invalid JSON", str(ctx.exception))

    def test_json_storage_load_missing_action_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            storage = JsonStorage(tmp)
            bad_file = storage.workflow_path("corrupt_action")
            bad_content = {
                "name": "corrupt_action",
                "actions": [
                    {"payload": {"command": "ls"}}  # missing action_type and timestamp
                ],
            }
            bad_file.write_text(json.dumps(bad_content), encoding="utf-8")

            with self.assertRaises(ValueError) as ctx:
                storage.load_workflow("corrupt_action")
            self.assertIn("Corrupt workflow file", str(ctx.exception))
            self.assertIn("missing required field 'action_type'", str(ctx.exception))

    def test_xml_storage_load_invalid_xml(self):
        with tempfile.TemporaryDirectory() as tmp:
            storage = XmlStorage(tmp)
            bad_file = storage.workflow_path("broken_xml")
            bad_file.write_text("<workflow><unclosed>", encoding="utf-8")

            with self.assertRaises(ValueError) as ctx:
                storage.load_workflow("broken_xml")
            self.assertIn("Corrupt workflow file", str(ctx.exception))
            self.assertIn("invalid XML", str(ctx.exception))

    def test_xml_storage_load_missing_attributes(self):
        with tempfile.TemporaryDirectory() as tmp:
            storage = XmlStorage(tmp)
            bad_file = storage.workflow_path("no_name")
            bad_file.write_text("<workflow></workflow>", encoding="utf-8")

            with self.assertRaises(ValueError) as ctx:
                storage.load_workflow("no_name")
            self.assertIn("missing required attribute 'name'", str(ctx.exception))

    def test_cli_handles_corrupt_file_cleanly(self):
        with tempfile.TemporaryDirectory() as tmp:
            old_home = os.environ.get("EXECTRACE_HOME")
            os.environ["EXECTRACE_HOME"] = tmp
            try:
                storage = JsonStorage(tmp)
                bad_file = storage.workflow_path("cli_corrupt")
                bad_file.write_text(json.dumps({"actions": []}), encoding="utf-8")

                # Running CLI replay against corrupt workflow returns exit code 2
                exit_code = main(["replay", "cli_corrupt", "--dry-run"])
                self.assertEqual(exit_code, 2)
            finally:
                if old_home is not None:
                    os.environ["EXECTRACE_HOME"] = old_home
                else:
                    os.environ.pop("EXECTRACE_HOME", None)


if __name__ == "__main__":
    unittest.main()
