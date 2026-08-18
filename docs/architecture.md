# YouTube Description Generator — Architecture

Four independent steps, chained by files on disk rather than by function calls.

```
{video}.mp4
   └── extract    → {video}_frames/frame_NNNN.jpg
          └── describe  → {video}_frames/description.txt   (BLIP captions)
                 └── summarize → description.txt            (replaced by the LLM output)
                        └── collect → {video}_frames.txt
```

Each step scans a directory and does its work, so any of them can be run alone. That is the main
design decision here, and a good one: the stages cost wildly different amounts, and a failure in
the cheap last step should not mean repeating the expensive second one.

## 1. `extract_frames.py`

OpenCV opens each `.mp4`, reads its FPS and frame count, and writes one JPEG per second into
`{stem}_frames/`.

Frames are reached by seeking — `cap.set(CAP_PROP_POS_FRAMES, second * fps)` — rather than by
reading sequentially and keeping every *n*th frame. Seeking is simpler, and less reliable on
variable-frame-rate footage and long-GOP codecs, where a seek lands on the nearest keyframe. See
[`internal/known-issues.md`](./internal/known-issues.md).

## 2. `describe_frames.py`

BLIP captions every frame, one line each, into `description.txt`.

Two details worth keeping:

**The model loads lazily.** `_processor`, `_model`, and `_device` are module globals populated on
first use, and `torch` and `transformers` are imported *inside* `_load_model`. So importing the
module — as the CLI and the tests do — costs nothing and downloads nothing.

**The revision is pinned.** The model is loaded with `revision=_BLIP_REVISION`, from
`BLIP_REVISION` or `"main"`. Naming a revision when loading third-party weights is unusual care:
without it, an upstream push silently changes the model your machine executes.

CUDA is used when available, CPU otherwise.

**A folder with an existing `description.txt` is skipped**, which makes this re-runnable after an
interruption — and is also half of the problem below.

## 3. `summarize_descriptions.py`

Walks for `*_frames` folders, reads `description.txt`, and sends the captions to Ollama with a
prompt asking for a title, a description, and 3–5 hashtags.

```python
ollama_path = shutil.which("ollama") or "ollama"
result = subprocess.run(
    [ollama_path, "run", "llama3.1:8b"],
    input=prompt.encode("utf-8"),
    capture_output=True,
    check=False,
)
```

The binary is resolved to an absolute path so `PATH` ordering cannot substitute it, argv is a
list so nothing is shell-interpreted, and the prompt goes in on stdin rather than as an argument.
The `# nosec` comments record why. This is the right way to shell out.

Two things it does not do: set a timeout, and preserve the captions. The result is written
**back over `description.txt`**, and since `describe` skips folders that have that file, the
captions cannot be regenerated. Both are in
[`internal/known-issues.md`](./internal/known-issues.md).

Failures are caught per folder and printed, so one bad video does not stop the batch.

## 4. `collect_files.py`

Moves each `description.txt` up into the base directory, named after its folder, with `_1`, `_2`
suffixes on collision.

It iterates **every** subdirectory, not only `*_frames` — unlike the other three steps. And
because the name comes from the folder, the output is `{video}_frames.txt`. Both are in the
known-issues file.

A faithful port of `move_files.bat`, which is still included for Windows.

## The CLI

`cli.py` maps each step to a subcommand plus `run` for all four, each taking an optional
directory that defaults to the current one. `__main__.py` makes
`python -m youtube_description_generator` equivalent.

## Why files, not function calls

Because the steps are expensive and unequal. Frames on disk mean `describe` can be re-run without
re-extracting; captions on disk mean the LLM can be re-prompted without re-captioning.

The design would be fully realised if `summarize` wrote to a different filename. As it stands,
the one stage that most needs re-running is the one that destroys its own input.

## Testing

The suite mocks OpenCV, PyTorch, and Transformers, so `pip install -e . --no-deps` is enough to
run it and CI needs no model downloads. That is possible because the heavy imports are inside
`_load_model` rather than at module scope.
