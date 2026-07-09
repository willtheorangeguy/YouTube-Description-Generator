# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install for development (no heavy deps needed to run tests)
pip install -e . --no-deps

# Install with all dependencies (large: torch, transformers ~1 GB)
pip install -e .

# Run all tests
python -m unittest discover -s tests -v

# Run a single test file
python -m unittest tests.test_extract_frames -v

# Lint (not in CI, but recommended)
pylint src/youtube_description_generator/

# Run the CLI
ytdg run path/to/videos
python -m youtube_description_generator run path/to/videos
```

CI installs with `--no-deps` and mocks all heavy dependencies, so the test suite runs without OpenCV, PyTorch, or Transformers installed.

## Architecture

This is a four-step pipeline CLI that generates YouTube Shorts descriptions from `.mp4` files entirely locally (no cloud APIs). Source lives in `src/youtube_description_generator/`.

**Pipeline steps — each is independently callable:**

| Module | Public entry point | What it does |
|---|---|---|
| `extract_frames.py` | `extract_all(directory)` | Samples 1 frame/second from each `.mp4` → `{video}_frames/frame_NNNN.jpg` |
| `describe_frames.py` | `find_and_process_frame_folders(directory)` | Captions each frame with BLIP (Hugging Face), writes `description.txt` per folder |
| `summarize_descriptions.py` | `process_frame_folders(directory)` | Feeds captions to local Ollama (`llama3.1:8b`), rewrites `description.txt` as title + description + hashtags |
| `collect_files.py` | `collect_descriptions(directory)` | Moves `*/description.txt` → `{video}.txt` in the parent directory |

**`cli.py`** wires these into `ytdg` subcommands (`extract`, `describe`, `summarize`, `collect`, `run`). It lazy-imports each module's handler so heavy deps are only loaded when that step is actually invoked.

**Key design constraints:**

- `describe_frames.py` caches the BLIP model in module-level globals (`_model`, `_processor`) — loaded once per process, supports optional CUDA.
- `describe_frames.py` skips frame folders that already contain a `description.txt` (idempotent re-runs).
- `summarize_descriptions.py` calls Ollama via `subprocess` — Ollama must be running locally with `llama3.1:8b` pulled. The prompt is hardcoded in that file; edit it there to change output tone/format.
- `collect_files.py` handles filename collisions by appending `_1`, `_2`, etc.

## Testing conventions

Tests use `unittest` and mock all heavy dependencies at the **module level** before importing the code under test:

```python
sys.modules['cv2'] = MagicMock()
sys.modules['torch'] = MagicMock()
sys.modules['transformers'] = MagicMock()
```

This pattern must be maintained for any new modules that import OpenCV, PyTorch, or Transformers. Test files go in `tests/` and are named `test_*.py`. Test functions are named `test_*`. Use `tempfile.TemporaryDirectory` for filesystem tests.

## Naming conventions

- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Docstrings: required on all modules, functions, classes, and methods (Google style with `Args:` / `Returns:`)

## Boundaries

- Ask before adding dependencies or modifying `.github/workflows/tests.yml`.
- The `move_files.bat` is a Windows-only standalone alternative to `ytdg collect` — keep it in sync when `collect_files.py` logic changes.
