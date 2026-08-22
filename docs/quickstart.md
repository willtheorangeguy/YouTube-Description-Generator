# YouTube Description Generator — Quickstart

## 1. Install

```bash
pip install git+https://github.com/willtheorangeguy/YouTube-Description-Generator.git
```

Pulls in OpenCV, Pillow, Transformers, and PyTorch — a large download.

## 2. Get Ollama running

```bash
ollama pull llama3.1:8b
```

[Ollama](https://ollama.com) must be installed and running before the summarize step. The other
three steps do not need it.

## 3. Run it

```bash
ytdg run path/to/videos
```

Or `cd` into the folder and run `ytdg run` — every command defaults to the current directory.

The first `describe` downloads the BLIP model (~1 GB) from Hugging Face, once.

## 4. What you get

For `myvideo.mp4`:

```text
myvideo.mp4
myvideo_frames/          frame_0000.jpg, frame_0001.jpg, …
myvideo_frames.txt       the finished title, description, and hashtags
```

Note the output is named after the **frames folder**, so `myvideo_frames.txt`.

## Running steps individually

Useful, because the stages cost very different amounts:

```bash
ytdg extract      # fast
ytdg describe     # slow — one BLIP pass per frame
ytdg summarize    # one Ollama call per video
ytdg collect      # instant
```

`describe` skips folders that already have a `description.txt`, so it is safe to re-run after an
interruption.

> **`summarize` is not safe to re-run.** It replaces `description.txt` with its own output, so a
> second run summarises the summary — and `describe` will not regenerate the captions, because
> the file exists. Delete `description.txt` first to start that video over. See
> [`internal/known-issues.md`](./internal/known-issues.md).

## Tuning the output

The prompt is a string in `summarize_descriptions.py`. Editing it is the intended way to change
tone or format — there is no configuration file. See [Configuration](./configuration.md).

## Speed

`describe` dominates. It runs BLIP once per extracted frame, so a 60-second video is 60 model
passes. A CUDA GPU makes a large difference; on a CPU, expect minutes per video.
