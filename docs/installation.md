# YouTube Description Generator — Installation

## Requirements

| | |
|---|---|
| Python | 3.9 or newer |
| Ollama | Installed and running, for the summarize step |
| Disk | ~1 GB for BLIP, ~5 GB for `llama3.1:8b`, plus PyTorch |
| GPU | Optional; makes `describe` far faster |

## Install

```bash
pip install git+https://github.com/willtheorangeguy/YouTube-Description-Generator.git
```

This provides the `ytdg` command and pulls in OpenCV, Pillow, Transformers, and PyTorch. The last
two are the bulk of it.

From source:

```bash
git clone https://github.com/willtheorangeguy/YouTube-Description-Generator.git
cd YouTube-Description-Generator
pip install -e .
```

## Ollama

```bash
ollama pull llama3.1:8b
```

Only the **summarize** step needs it. Extract, describe, and collect run without it, so you can
do most of a run and add Ollama later.

The model name is hardcoded in `summarize_descriptions.py`; a different one means editing that
line. The binary is resolved with `shutil.which("ollama")` to an absolute path, so a shadowed
`ollama` earlier on `PATH` cannot be substituted.

## The BLIP model

Downloaded automatically from Hugging Face on the first `ytdg describe`, to the standard
Transformers cache (`~/.cache/huggingface`). About 1 GB, once.

## GPU

`describe` is the expensive step and benefits most. If pip installed the CPU-only PyTorch build,
replace it per [PyTorch's instructions](https://pytorch.org/get-started/locally/).

```python
import torch; print(torch.cuda.is_available())
```

CPU-only works; it is simply slow.

## Verify

```bash
ytdg --help
ollama list                  # llama3.1:8b present
ytdg extract path/with/one/video
```

Extract needs neither model, so it is the quickest check that the install works.

## Alternative entry point

```bash
python -m youtube_description_generator <command>
```

Identical to `ytdg`.

## Windows

`move_files.bat` is included as a standalone equivalent of `ytdg collect`, from before the
cross-platform port. `ytdg collect` does the same thing and is preferred.

## Uninstall

```bash
pip uninstall youtube-description-generator
rm -rf ~/.cache/huggingface     # the BLIP weights
ollama rm llama3.1:8b
```
