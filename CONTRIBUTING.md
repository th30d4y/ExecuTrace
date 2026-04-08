# Contributing to ExecuTrace

Thank you for your interest in contributing to **ExecuTrace**! Whether you're fixing a bug, proposing a new feature, improving the docs, or just sharing feedback, every contribution is welcome.

Please take a moment to read this guide before you start.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [Coding Standards](#coding-standards)
- [Commit Message Conventions](#commit-message-conventions)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Documentation](#documentation)
- [Security Vulnerabilities](#security-vulnerabilities)
- [Hall of Fame](#hall-of-fame)

---

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating you agree to uphold its standards. Please report unacceptable behaviour to **w4nn4d133@gmail.com**.

---

## Ways to Contribute

| Type | How |
|---|---|
| 🐛 Bug fix | Open an issue first, then submit a PR |
| ✨ New feature | Open a feature-request issue to discuss scope |
| 📖 Documentation | Edit Markdown files or the `website/` source |
| 🧪 Tests | Add or improve tests in `test_comprehensive.py` |
| 🔐 Security | See [Security Vulnerabilities](#security-vulnerabilities) |

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- `git`

### Fork & clone

```bash
git clone https://github.com/<your-username>/ExecuTrace.git
cd ExecuTrace
```

### Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### Install in editable mode

```bash
pip install -e .
```

### Verify the installation

```bash
exectrace --help
```

---

## Project Structure

```
ExecuTrace/
├── exectrace/            # Core library
│   ├── cli.py            # Command-line interface
│   ├── core/             # Replayer and workflow models
│   ├── recorder/         # Session recording logic
│   ├── storage/          # JSON & XML storage backends
│   └── utils/            # Logging, interactive prompts
├── website/              # Documentation website (GitHub Pages)
│   ├── index.html
│   └── data/
│       ├── contributors.json
│       └── security_hof.json
├── test_comprehensive.py # Test suite
├── pyproject.toml        # Build & packaging configuration
├── CONTRIBUTING.md       # This file
├── CODE_OF_CONDUCT.md
├── SECURITY.md
└── README.md
```

---

## Running Tests

```bash
python test_comprehensive.py
```

All tests must pass before submitting a pull request. If you add new functionality, please add corresponding tests.

---

## Coding Standards

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code style.
- Use type annotations for all public functions and methods (Python 3.9+ syntax).
- Keep functions focused and small — prefer multiple simple functions over one large one.
- Use the `get_logger` utility from `exectrace.utils.logger` for logging rather than `print` in library code.
- Do not introduce new dependencies without prior discussion in an issue.

---

## Commit Message Conventions

Use short, imperative messages in the present tense:

```
fix: handle missing workflow file gracefully
feat: add --timeout flag to replay command
docs: add contribution guide
test: cover XML storage edge cases
refactor: extract prompt helpers into utils module
```

Prefix categories: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`.

---

## Pull Request Process

1. **Branch** off `main` with a descriptive name:
   ```bash
   git checkout -b fix/replay-dry-run-output
   ```
2. **Make your changes** in small, focused commits.
3. **Run the tests** and confirm everything passes.
4. **Push** your branch and open a Pull Request against `main`.
5. Fill in the PR description explaining *what* changed and *why*.
6. A maintainer will review your PR. Please respond to feedback promptly.
7. Once approved, the PR will be merged by a maintainer.

> For large changes, open an issue for discussion **before** writing code to avoid wasted effort.

---

## Reporting Bugs

1. Search [existing issues](https://github.com/Stalin-143/ExecuTrace/issues) to check whether the bug has already been reported.
2. If not, open a new issue and include:
   - ExecuTrace version (`pip show exectrace-workflow`)
   - Python version and OS
   - Steps to reproduce
   - Expected vs. actual behaviour
   - Relevant error output or logs

---

## Suggesting Features

1. Search existing issues for similar requests.
2. Open an issue with the label **enhancement** and describe:
   - The problem you're trying to solve
   - Your proposed solution
   - Any alternatives you've considered

---

## Documentation

The project documentation website lives in `website/`. It is a static HTML site deployed via GitHub Pages.

- To add yourself to the contributors list, update `website/data/contributors.json`.
- For content changes, edit `website/index.html` and open a PR.

---

## Security Vulnerabilities

Please **do not** open a public issue for security bugs. Follow the responsible-disclosure process described in [SECURITY.md](SECURITY.md).

---

## Hall of Fame

Contributors and responsible security reporters are credited on the project website. Thank you for helping make ExecuTrace better!
