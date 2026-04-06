from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from exectrace.utils.sensitive_filter import redact_text


def detect_history_file() -> Path | None:
    candidates = [Path.home() / ".bash_history", Path.home() / ".zsh_history"]
    for path in candidates:
        if path.exists() and path.is_file():
            return path
    return None


def history_line_count(history_file: Path) -> int:
    with open(history_file, "r", encoding="utf-8", errors="ignore") as f:
        return sum(1 for _ in f)


def capture_commands_since(history_file: Path, start_line: int) -> Tuple[List[str], int]:
    with open(history_file, "r", encoding="utf-8", errors="ignore") as f:
        lines = [line.rstrip("\n") for line in f]

    new_lines = lines[start_line:]
    commands = []
    for line in new_lines:
        cmd = line
        # zsh can store lines as ": <epoch>:<duration>;<command>"
        if line.startswith(": ") and ";" in line:
            cmd = line.split(";", 1)[1]
        commands.append(redact_text(cmd))

    return commands, len(lines)
