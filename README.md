# FikirFix — Agentic Dev CLI

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)

FikirFix is a compact developer-facing CLI demonstrating an iterative, tool-using AI agent that can inspect, run, and modify code inside a safe working directory. It is a learning sandbox — ideal for studying how agents can safely interact with local code during debugging and small refactors.

Author: Leul Tewodros Agonafer

Why this project
- Shows a minimal, auditable workflow for LLMs to use local helper functions (list/read/write/run).
- Demonstrates iterative tool use: list before read, run to validate, write to patch, and re-run to verify.
- Includes a self-contained example (`calculator/`) so you can exercise the agent end-to-end.

Highlights
- Tooling: local helpers in `functions/` (file listing, file read/write, run Python)
- Agent runtime: `main.py` — CLI that talks to a model and executes selected helper calls
- Example target: `calculator/` — a small arithmetic evaluator and renderer

Quickstart
1. Install dependencies (recommended inside a virtualenv):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt || pip install google-genai python-dotenv
```

2. Add your Gemini API key (do not commit it):

```fish
set -x GEMINI_API_KEY "your_gemini_api_key"
```

3. Run the example: evaluate an expression with the calculator

```bash
python3 calculator/main.py "3 + 7 * 2"
```

4. Ask the agent to fix the (intentional) bug or inspect files:

```bash
python3 main.py "fix the bug: 3 + 7 * 2 shouldn't be 20" --verbose
```

Design & Architecture
- `main.py` — the agent runtime and CLI glue. It exposes a limited set of tools to the model and enforces a working directory.
- `functions/` — helper utilities:
  - `get_files_info.py` — list files and read/write safely.
  - `run_python.py` — execute Python scripts and capture output.
- `calculator/` — sample project used by the agent for diagnosis and repair.

Security & Safety
- The agent operates only inside the `calculator` working directory.
- `get_file_content` truncates large files to avoid leaking huge blobs.
- Do NOT run this against sensitive repositories or with untrusted models. Treat the agent as an experimental tool.

Contribution guide
- Fork, create a branch, implement changes, open a PR with a clear description.
- Suggested improvements: add unit tests, extend safe helper functions, add CI checks.

Contact
- Leul Tewodros Agonafer — feel free to open issues or PRs.

License
- MIT

