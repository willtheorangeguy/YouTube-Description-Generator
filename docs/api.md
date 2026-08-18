# YouTube Description Generator — API

Every pipeline step is an importable function. There is no network API.

## The four stages

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

Each takes a directory and reports progress on stdout. All four default to the current directory
when given `None`.

## Lower-level pieces

### `extract_frames(video_path, output_dir)`

One video, one output directory. Takes strings, not `Path`s — it is the oldest function here.

### `generate_description(image_path) -> str`

A caption for a single image. Loads BLIP on first call and keeps it in module globals, so
repeated calls do not reload.

```python
from youtube_description_generator.describe_frames import generate_description
print(generate_description(Path("frame_0007.jpg")))
```

Useful on its own as a captioner, independent of the rest of the pipeline.

### `summarize_description(text) -> str`

Sends arbitrary text to Ollama with the Shorts prompt and returns the response.

```python
from youtube_description_generator.summarize_descriptions import summarize_description
print(summarize_description("a dog running on a beach\na wave breaking\n"))
```

Raises `RuntimeError` with Ollama's stderr on a non-zero exit, and `FileNotFoundError` when
Ollama is not installed. **No timeout** — see
[`internal/known-issues.md`](./internal/known-issues.md).

### `unique_target(base_dir, folder_name) -> Path`

The collision-avoiding name `collect` uses: `{folder_name}.txt`, then `_1`, `_2`, and so on.

## Composing your own pipeline

Because the stages communicate through files, you can substitute one:

```python
extract_all(videos)
find_and_process_frame_folders(videos)

# ...then read the captions yourself, instead of calling process_frame_folders
for folder in videos.glob("*_frames"):
    captions = (folder / "description.txt").read_text(encoding="utf-8")
    my_summary = my_own_model(captions)
    (folder / "summary.txt").write_text(my_summary, encoding="utf-8")
```

Writing to a **different filename** — as above — also avoids destroying the captions, which is
what the built-in summarize step does.

## Import cost

`describe_frames` imports `torch` and `transformers` inside `_load_model`, so importing the module
is cheap and downloads nothing. Importing does not require the model to exist.

## Not importable

The prompt and the model names are literals inside their functions, so changing either means
editing the source rather than passing an argument. See [Configuration](./configuration.md).
