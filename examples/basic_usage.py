"""Basic programmatic usage of ExecuTrace.

This example demonstrates how to use ExecuTrace programmatically
to record workflows, edit them, and replay them.
"""

from exectrace.core.editor import WorkflowEditor
from exectrace.core.replayer import Replayer
from exectrace.recorder.session import RecorderSession
from exectrace.storage.factory import get_storage


def example_record():
    """Example: Record a workflow."""
    print("=== Recording Example ===")
    
    # Create a recorder session with JSON format
    recorder = RecorderSession(storage_format="json", storage_path=".exectrace_demo")
    
    # Start recording
    state = recorder.start(name="demo-workflow", root_dir=".")
    print(f"Recording started: {state['name']}")
    print(f"Root directory: {state['root_dir']}")
    print("(In a real scenario, user would execute commands here)")
    
    # Stop recording
    workflow = recorder.stop()
    print(f"Recording stopped. Captured {len(workflow.actions)} actions.")
    print()


def example_edit():
    """Example: Edit a workflow programmatically."""
    print("=== Edit Example ===")
    
    storage = get_storage("json", ".exectrace_demo")
    editor = WorkflowEditor(storage)
    
    try:
        # Load the workflow
        workflow = editor.load("demo-workflow")
        print(f"Loaded workflow: {workflow.name}")
        print(f"Current actions: {len(workflow.actions)}")
        
        # Add a manual command action
        workflow.add_action("command", {"command": "echo 'Hello, ExecuTrace!'", "cwd": "."})
        print("Added manual action")
        
        # Save the updated workflow
        editor.save(workflow)
        print("Workflow saved")
    except FileNotFoundError as e:
        print(f"Note: {e}")
    print()


def example_list():
    """Example: List available workflows."""
    print("=== List Example ===")
    
    json_storage = get_storage("json")
    xml_storage = get_storage("xml")
    
    json_workflows = json_storage.list_workflows()
    xml_workflows = xml_storage.list_workflows()
    
    all_workflows = sorted(set(json_workflows + xml_workflows))
    
    print("Available workflows:")
    for name in all_workflows:
        formats = []
        if name in json_workflows:
            formats.append("json")
        if name in xml_workflows:
            formats.append("xml")
        print(f"  - {name} [{', '.join(formats)}]")
    
    if not all_workflows:
        print("  (No workflows found)")
    print()


def example_xml_storage():
    """Example: Use XML storage format."""
    print("=== XML Storage Example ===")
    
    from exectrace.storage.xml_storage import XmlStorage
    
    # Create a workflow using XML storage
    xml_storage = XmlStorage(".exectrace_demo/xml")
    
    # You can use it with RecorderSession
    recorder = RecorderSession(storage=xml_storage)
    print("XML storage configured for RecorderSession")
    print()


if __name__ == "__main__":
    print("ExecuTrace Examples\n")
    
    # Uncomment to run examples:
    # example_record()
    # example_edit()
    example_list()
    # example_xml_storage()
    
    print("For CLI usage, run:")
    print("  exectrace record <name>       - Start recording a workflow")
    print("  exectrace stop                 - Stop and save recording")
    print("  exectrace replay <name>        - Replay a workflow")
    print("  exectrace list                 - List workflows")
    print("  exectrace edit <name>          - Edit a workflow")
    print("  exectrace delete <name>        - Delete a workflow")
    print("\nFor more info: exectrace --help")
