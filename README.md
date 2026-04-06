<div align="center">

```
  ███████╗██╗  ██╗███████╗ ██████╗██╗   ██╗████████╗██████╗  █████╗  ██████╗███████╗
  ██╔════╝╚██╗██╔╝██╔════╝██╔════╝██║   ██║╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝
  █████╗   ╚███╔╝ █████╗  ██║     ██║   ██║   ██║   ██████╔╝███████║██║     █████╗  
  ██╔══╝   ██╔██╗ ██╔══╝  ██║     ██║   ██║   ██║   ██╔══██╗██╔══██║██║     ██╔══╝  
  ███████╗██╔╝ ██╗███████╗╚██████╗╚██████╔╝   ██║   ██║  ██║██║  ██║╚██████╗███████╗
  ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝
```

# ExecuTrace

**Record, edit, and replay developer workflows**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS-purple.svg)](#)

</div>

---

## About

ExecuTrace is a Python library and CLI tool that captures developer workflows and replays them reliably.

**What it does:**
- Records terminal commands from shell history
- Tracks file system changes (create, modify, delete)
- Saves workflows in JSON or XML format
- Replays workflows with multiple execution modes

**Why use it:**
- Automate repetitive development tasks
- Share procedures with team members
- Create reproducible environment setups
- Document complex workflows reliably
- Ensure consistent deployments

---

## Installation

### From PyPI (Global Library)
```bash
# Install globally from PyPI
pip install exectrace-workflow

# Verify installation
exectrace --help
```

### From Source (Development)
```bash
git clone https://github.com/Stalin-143/ExecuTrace.git
cd ExecuTrace
pip install -e .
```

---

## Quick Usage

```bash
# Record
exectrace record my-workflow
# ... run your commands ...
exectrace stop

# Replay
exectrace replay my-workflow --explain
```

---

## License

MIT License - See [LICENSE](LICENSE) for details.

