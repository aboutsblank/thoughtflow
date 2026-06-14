# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Package manager

This project uses `uv`. Run all commands via `uv run <cmd>`.

## Commands

```bash
# Run the CLI
uv run thoughtflow <USECASE> <message> [-l|--local] [-g|--global] [-v|--verbose]

# Run tests
uv run pytest

# Run a single test
uv run pytest test/test_cli.py::test_checkConfigCorrectness1
```

## Sandbox rule

**Always test file-system changes in the `sandbox/` subdirectory**, not in the project root. Run the application from there as an independent user to avoid polluting `.thoughtflow/` storage under the repo root.

```bash
cd sandbox && uv run thoughtflow idea "my thought" --local
```

## Architecture

Three modules under `src/thoughtflow/`:

- **`dom.py`** — domain model. Defines `Element` (the stored thought), `AppSettings`, `Scope`, `Usecase` enums, and JSON serialization via `serialize()` / `encode_value()`. The `Usecase` enum is intentionally minimal — dynamic loading from `options.toml` via `core.py` is planned to replace the hardcoded values.
- **`cli.py`** — argument parsing (`argparse`) and all file I/O. Entry point is `thoughtflow.cli:main` (per `pyproject.toml`), but `main()` doesn't exist yet — logic lives in an `if __name__ == "__main__"` block that must be extracted. On each invocation it resolves the storage path, creates the `.thoughtflow/` directory if needed, and appends a serialized `Element` as a JSON line. `AUTHOR` is hardcoded as `"aboutsblank"`.
- **`core.py`** — options loading and project-root detection. `loadOptions()` (cached) reads `options.toml` using `tomllib`; `_projectRoot()` walks up from `__file__` until it finds `pyproject.toml`. Also contains a parallel `AppSettings` class — in-progress extraction from `cli.py`.

**`options.toml`** (project root) is the source of truth for valid usecases: `IDEA`, `TASK`, `FEATURE`, `PROBLEM`. These are not yet wired into `dom.Usecase` or argument validation.

**Storage format:** JSONL files. Each call appends one JSON object per line to `<scope_root>/.thoughtflow/<USECASE>`. Scope root is `~` for `--global` and `cwd` for `--local` (default).

## Pytest config

`pytest.toml` sets `--import-mode=importlib`. Tests live in `test/`.

## Planned but not yet wired

- `cli.py` `__main__` block must be extracted into `main()` to activate the `[project.scripts]` entry point
- `options.toml` usecases driving `dom.Usecase` and CLI validation (currently hardcoded)
- Business logic extraction from `cli.py` into `core.py`
- Linter, Formatter, Typechecker (no `[tool.ruff]` / `[tool.mypy]` in `pyproject.toml` yet)
