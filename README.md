# FikirFix — Agentic Dev CLI

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)

FikirFix is a working, developer-facing coding agent CLI that accepts a natural-language prompt, uses a small set of auditable helper tools (list, read, run, write), and iterates until it has evidence to recommend or apply fixes. It is designed to be safe-by-default, testable, and installable for real developer workflows.

Author: Leul Tewodros Agonafer — maintainer


Why this project
- A practical, auditable agent that developers can run locally to help find and fix small bugs.
- Safe-by-default: write operations are gated behind explicit flags, and the agent includes dry-run and audit modes.
- Testable: includes unit tests and integration patterns that run the agent loop deterministically via a model stub (see `DEPLOY_PLAN.md`).

Highlights
- Tooling: local helpers in `functions/` (file listing, file read/write, run Python)
- Agent runtime: `main.py` — an agent loop that exposes safe helpers to an LLM
- CLI: `fikirfix` — polished Typer + Rich-based wrapper for convenient developer use


Quickstart (production-ready)
-----------------------------

1) Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Install the package (editable mode during development) and runtime deps:

```bash
python -m pip install -e .
```

3) Configure a model key (Gemini) securely. Example (Fish):

```fish
set -x GEMINI_API_KEY "your_gemini_api_key"
```

4) Recommended workflow examples

- Run a dry-run fix (safe default):

```bash
fikirfix run "fix the bug: 3 + 7 * 2 shouldn't be 20" --dry-run
```

- Run and apply fixes (explicitly opt-in):

```bash
fikirfix run "fix the bug: ..." --allow-writes --confirm
```

- Evaluate an expression using the bundled calculator (no model required):

```bash
fikirfix calc "3 + 7 * 2"
```

- Inspect repository or working directory:

```bash
fikirfix inspect .
```

- Diagnose environment and connectivity:

```bash
fikirfix doctor
```

Security and safety (must read)
--------------------------------
- By default the agent runs in **safe/dry-run mode** and will not apply writes.
- To perform writes you MUST pass `--allow-writes` and `--confirm` to opt in.
- All tool calls are auditable; consider enabling persistent logs for your environment.

Testing and CI
---------------
- The `DEPLOY_PLAN.md` contains a targeted plan to add deterministic model stubs and CI workflows so the agent loop can be tested in automation without live LLM calls.

Where to go next
----------------
- Run `pytest` locally to verify the CLI and core modules.
- If you want, I can add a GitHub Actions CI workflow now that runs unit tests, integration tests with the model stub, and packaging checks.

Run without installing
-----------------------

If you prefer not to install the package, you can invoke the CLI module directly:

```bash
python -m fikirfix.cli calc "3 + 7 * 2"
python -m fikirfix.cli run "fix the bug: ..." --verbose
```

Troubleshooting
---------------

- If `fikirfix` is not found after installation, ensure your virtualenv is activated and the installation succeeded.
- If Typer or Rich imports fail, install required runtime deps:

```bash
python -m pip install "typer[all]>=0.9.0" rich
```

- The agent requires a Gemini API key for the model client. If you do not have a key, use `fikirfix calc ...` or run the calculator examples.

Development & testing
---------------------

- Run tests with `pytest`:

```bash
pytest -q
```

- Run a single CLI test during development:

```bash
pytest -q tests/test_cli.py::test_calc_expression -q
```

Security & Safety
-----------------

- The agent's helpers are intentionally constrained to operate inside a working directory (the `calculator` example by default).
- `get_file_content` truncates large files to avoid leaking huge blobs.
- Avoid running the agent on sensitive repositories or with untrusted models.

Contributing
------------

- Fork, create a feature branch, implement changes, and open a PR with a clear description and tests.

Contact
-------

Leul Tewodros Agonafer — open issues or PRs on the repository.

License
-------

MIT

