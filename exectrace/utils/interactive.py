"""Interactive CLI utilities for user input and selection."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal


def prompt_storage_location(default: str | None = None) -> str:
    """Prompt user for storage location with optional default."""
    if default is None:
        default = str(Path.home() / ".exectrace" / "workflows")
    
    prompt_text = f"Enter storage path (press Enter for default: {default}): "
    user_input = input(prompt_text).strip()
    
    if not user_input:
        return default
    
    # Expand home directory
    path = Path(user_input).expanduser()
    
    # Create directory if it doesn't exist
    path.mkdir(parents=True, exist_ok=True)
    
    return str(path)


def prompt_file_format() -> Literal["json", "xml"]:
    """Prompt user to choose file format (JSON or XML)."""
    while True:
        print("Choose file format:")
        print("  1) JSON (default)")
        print("  2) XML")
        
        choice = input("Enter choice (1 or 2, default: 1): ").strip().lower()
        
        if not choice or choice == "1":
            return "json"
        elif choice == "2":
            return "xml"
        else:
            print("Invalid choice. Please enter 1 or 2.")


def prompt_confirmation(message: str) -> bool:
    """Prompt user for yes/no confirmation."""
    while True:
        response = input(f"{message} (y/n): ").strip().lower()
        if response in ("y", "yes"):
            return True
        elif response in ("n", "no"):
            return False
        else:
            print("Please enter 'y' or 'n'.")


def list_directories(base_path: str | None = None) -> list[str]:
    """List subdirectories in a path for selection (future feature)."""
    if base_path is None:
        base_path = str(Path.home())
    
    try:
        base = Path(base_path)
        dirs = sorted([d.name for d in base.iterdir() if d.is_dir()])
        return dirs
    except (OSError, PermissionError):
        return []
