# YouTube Description Generator — Configuration

There is no configuration file and no settings flag. One environment variable exists; everything
else is a constant in the source. That is a defensible choice for a four-function pipeline, but
worth knowing before you go looking for a config.

## `BLIP_REVISION`

The only environment variable.

```bash
BLIP_REVISION=<commit-sha> ytdg describe
```

`describe_frames.py` passes it as the `revision` argument when loading the BLIP model, defaulting
to `"main"`. Pinning a model *revision* is unusual care and worth understanding: without it, an
upstream push to the branch silently changes the weights your machine downloads and executes.
The default of `"main"` fixes the ref that gets resolved, not the commit — set an exact SHA to
lock it down.

## The prompt

In `summarize_descriptions.py`, and the thing most worth editing:

```python
prompt = f"""
You are a YouTube Shorts content assistant. Given the following frame-by-frame video
description, write a short, engaging YouTube Shorts video title and description and suggest
3-5 relevant hashtags. …

Output format:
<title>

<short description>

#tag1 #tag2 #tag3
""".strip()
```

Change the tone, the hashtag count, or the format here. The output is written to disk verbatim,
so the prompt is the only thing shaping it.

## The models

| Model | Where | Change by |
|---|---|---|
| `Salesforce/blip-image-captioning-base` | `describe_frames.py` | Editing the model id; revision via `BLIP_REVISION` |
| `llama3.1:8b` | `summarize_descriptions.py` | Editing the argv list, and `ollama pull`ing it |

Both are hardcoded. A larger BLIP variant gives better captions at proportionally more time; a
different Ollama model changes the writing style more than the prompt does.

## Sampling rate

`extract_frames.py` takes **one frame per second**, computed from the video's FPS. Not
configurable.

For Shorts this is a reasonable default — a 60-second video gives 60 captions, which is enough
signal for a summary without an unbearable `describe` step. Longer videos scale linearly and get
slow.

## Naming

| Thing | Pattern |
|---|---|
| Frame folder | `{video-stem}_frames/` |
| Frames | `frame_NNNN.jpg`, numbered by second |
| Captions and summary | `description.txt` inside the frame folder |
| Collected output | `{folder-name}.txt` — i.e. `{video}_frames.txt` |
| Collision suffix | `_1`, `_2`, … |

The collected filename keeps the `_frames` suffix because it is named after the folder. See
[`internal/known-issues.md`](./internal/known-issues.md).

## Which stages skip work

| Stage | Skips |
|---|---|
| `extract` | Nothing — re-running re-extracts, overwriting frames |
| `describe` | Folders that already have a `description.txt` |
| `summarize` | Folders with no `description.txt`, or an empty one |
| `collect` | Folders with no `description.txt` |

`describe`'s skip makes it re-runnable after an interruption. It also means it will not
regenerate captions that `summarize` has replaced — see
[`internal/known-issues.md`](./internal/known-issues.md).

## Quote stripping

`summarize` removes every `"` from both the input captions and the model's output, so titles
never come back wrapped in quotation marks. A blunt instrument, and the reason a legitimate quoted
phrase loses its quotes.

## No timeout

The Ollama call has no timeout. A hung model hangs the pipeline indefinitely; same file.
