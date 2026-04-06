# ExecuTrace - GitHub Repository

## 📦 Project Overview

**ExecuTrace** is a Python library and CLI tool that captures, records, and replays developer workflows reliably. This repository contains the complete source code for the project.

## 🚀 Available on PyPI

This project is published on PyPI and can be installed globally:

```bash
pip install exectrace-workflow
```

**PyPI Link:** https://pypi.org/project/exectrace-workflow/

## 📋 Latest Release

**Version:** 1.0.1  
**Release Date:** April 6, 2026  
**PyPI:** https://pypi.org/project/exectrace-workflow/1.0.1/

## 🎯 Core Features

### Recording
- Captures terminal commands from shell history (bash, zsh)
- Tracks file system changes (create, modify, delete)
- Saves workflow metadata (timestamps, user, environment)

### Storage
- **Dual Format Support:**
  - JSON (human-readable, version control friendly)
  - XML (structured, enterprise-compatible)
- Flexible storage paths
- Automatic backup support

### Replay Modes
- **Dry-run:** Preview changes without executing
- **Explain:** Show what will happen step-by-step
- **Smart:** Execute with intelligent error handling

### CLI Interface
Commands available:
- `exectrace record <name>` - Start recording a workflow
- `exectrace stop` - Stop recording
- `exectrace replay <name>` - Replay a workflow
- `exectrace list` - Show all workflows
- `exectrace edit <name>` - Edit a workflow
- `exectrace delete <name>` - Delete a workflow

## 📁 Repository Structure

```
ExecuTrace/
├── exectrace/              # Main package
│   ├── cli.py             # CLI interface
│   ├── core/              # Core modules
│   │   ├── editor.py
│   │   ├── models.py
│   │   └── replayer.py
│   ├── recorder/          # Recording functionality
│   │   ├── command_capture.py
│   │   ├── fs_tracker.py
│   │   └── session.py
│   ├── storage/           # Storage backends
│   │   ├── json_storage.py
│   │   ├── xml_storage.py
│   │   └── factory.py
│   └── utils/             # Utility modules
│       ├── hash_utils.py
│       ├── logger.py
│       ├── sensitive_filter.py
│       └── time_utils.py
├── examples/              # Example usage
│   └── basic_usage.py
├── pyproject.toml         # Package configuration
├── README.md              # User documentation
└── GITHUB.md              # This file
```

## 🛠️ Development Setup

### Prerequisites
- Python 3.9 or higher
- pip or pip3

### Clone and Install
```bash
git clone https://github.com/Stalin-143/ExecuTrace.git
cd ExecuTrace
pip install -e .
```

### Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Or test individual modules:
```bash
python -c "from exectrace.cli import main; main()"
```

## 📝 Usage Examples

### Record a Workflow
```bash
# Start recording
exectrace record my-setup

# Run your commands
npm install
python -m build

# Stop recording
exectrace stop
```

### Replay a Workflow
```bash
# Dry run (preview)
exectrace replay my-setup --dry-run

# Explain mode (step-by-step)
exectrace replay my-setup --explain

# Smart mode (execute with error handling)
exectrace replay my-setup --smart
```

### List All Workflows
```bash
exectrace list
```

Shows workflows with storage format tags:
```
my-setup [json]
build-process [xml]
deploy-prod [json]
```

## 🔧 Features & Architecture

### Workflow Model
Each workflow contains:
- **Name:** Unique identifier
- **Actions:** List of recorded commands and file changes
- **Metadata:** Timestamps, user info, environment variables
- **Format:** JSON or XML storage

### Storage Factory Pattern
Dynamic storage backend selection:
```python
from exectrace.storage.factory import get_storage

# Get storage backend
storage = get_storage("json", "/path/to/workflows")
```

### Interactive CLI
User-friendly prompts for:
- Storage location selection
- File format preference (JSON/XML)
- Workflow editing
- Confirmation dialogs

## 📊 Python Requirements

- **Minimum:** Python 3.9
- **Tested:** Python 3.9, 3.10, 3.11, 3.12
- **Dependencies:** None (stdlib only)

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-thing`)
3. Commit your changes (`git commit -m "Add amazing thing"`)
4. Push to the branch (`git push origin feature/amazing-thing`)
5. Open a Pull Request

## 📞 Support

For issues, questions, or suggestions:
- **GitHub Issues:** https://github.com/Stalin-143/ExecuTrace/issues
- **PyPI Project:** https://pypi.org/project/exectrace-workflow/

## 🎓 Learn More

- [README.md](README.md) - User guide and quick start
- [examples/basic_usage.py](examples/basic_usage.py) - Code examples

---

**Version:** 1.0.1  
**Last Updated:** April 6, 2026  
**Status:** Production Ready ✅
