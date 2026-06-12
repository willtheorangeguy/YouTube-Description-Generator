# YouTube Description Generator

[![Tests](https://github.com/willtheorangeguy/YouTube-Description-Generator/actions/workflows/tests.yml/badge.svg)](https://github.com/willtheorangeguy/YouTube-Description-Generator/actions/workflows/tests.yml)

Automatically generate YouTube Shorts titles, descriptions, and hashtags from `.mp4` video files — entirely on your own machine. Frames are sampled from each video, captioned with a computer vision model, and summarized into upload-ready text by a local LLM. No API keys, no cloud services.

## How it works

The `ytdg` command runs a four-step pipeline over a directory of videos:

| Step | Command | What it does |
|------|---------|--------------|
| 1. Extract | `ytdg extract` | Samples one frame per second from each `.mp4` into a `{video}_frames/` folder |
| 2. Describe | `ytdg describe` | Captions every frame with the [BLIP image captioning model](https://huggingface.co/Salesforce/blip-image-captioning-base) and writes a `description.txt` per folder |
| 3. Summarize | `ytdg summarize` | Feeds the captions to a local [Ollama](https://ollama.com) model (`llama3.1:8b`), which rewrites `description.txt` as a Shorts title, short description, and 3–5 hashtags |
| 4. Collect | `ytdg collect` | Moves each `description.txt` out of its frame folder, renamed `{video}.txt` |

The end result: one ready-to-paste `.txt` file per video, like

```
Epic Sunset Timelapse

Watch the sky transform in 30 seconds of pure color.

#sunset #timelapse #shorts
```

## Installation

Requires **Python 3.9+**.

```bash
pip install git+https://github.com/willtheorangeguy/YouTube-Description-Generator.git
```

This installs the `ytdg` command along with its Python dependencies (OpenCV, Pillow, Transformers, PyTorch — the latter two are large downloads). A CUDA-capable GPU is optional but makes the describe step much faster.

For the summarize step you also need [Ollama](https://ollama.com) installed and running, with the model pulled:

```bash
ollama pull llama3.1:8b
```

The BLIP captioning model (~1 GB) is downloaded automatically from Hugging Face the first time you run `ytdg describe`.

## Usage

Run the whole pipeline against a directory of `.mp4` files:

```bash
ytdg run path/to/videos
```

Every command takes an optional directory argument and defaults to the current directory, so you can also `cd` into your video folder and just run `ytdg run`.

Or run the steps individually — useful when re-running a single stage:

```bash
ytdg extract [directory]     # .mp4 → {video}_frames/frame_NNNN.jpg
ytdg describe [directory]    # frames → description.txt (skips folders that already have one)
ytdg summarize [directory]   # description.txt → title, description, hashtags
ytdg collect [directory]     # */description.txt → {video}.txt (collisions get _1, _2, …)
```

`python -m youtube_description_generator <command>` works as an alternative to `ytdg`.

> **Tip:** to tweak the tone or format of the generated text, edit the prompt in `summarize_descriptions.py`.

On Windows, `move_files.bat` is also included as a standalone alternative to `ytdg collect`.

## Using it as a library

All pipeline steps are importable functions:

```python
from pathlib import Path

from youtube_description_generator.extract_frames import extract_all
from youtube_description_generator.describe_frames import find_and_process_frame_folders
from youtube_description_generator.summarize_descriptions import process_frame_folders
from youtube_description_generator.collect_files import collect_descriptions

videos = Path("path/to/videos")
extract_all(videos)
find_and_process_frame_folders(videos)
process_frame_folders(videos)
collect_descriptions(videos)
```

Lower-level pieces are available too, e.g. `extract_frames(video_path, output_dir)` for a single video, `generate_description(image_path)` for a single frame, or `summarize_description(text)` to summarize arbitrary caption text.

## Development

```bash
git clone https://github.com/willtheorangeguy/YouTube-Description-Generator.git
cd YouTube-Description-Generator
pip install -e .
python -m unittest discover -s tests -v
```

The test suite mocks all heavy dependencies (OpenCV, PyTorch, Transformers), so `pip install -e . --no-deps` is enough to run it — that's what CI does, on Python 3.9–3.12, for every push and pull request.

## License

MIT — see [LICENSE](LICENSE) for details.
