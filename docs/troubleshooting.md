# YouTube Description Generator — Troubleshooting

## `FileNotFoundError: ollama`

Ollama is not installed, or not on `PATH`. Install it from [ollama.com](https://ollama.com) and
confirm with `ollama list`.

Only `summarize` needs it — the other three steps run without.

## `Ollama failed: ...`

Ollama ran and exited non-zero; its stderr is included in the message. Usually the model is not
pulled:

```bash
ollama pull llama3.1:8b
```

## Summarize hangs forever

There is no timeout on the subprocess call, so a stalled Ollama stalls the pipeline with no
output. Check the model is loaded (`ollama ps`) and that the machine has enough memory for an 8B
model. Interrupt and retry. Recorded in
[`internal/known-issues.md`](./internal/known-issues.md).

## `describe` says "Skipping, description already exists"

Working as designed — it makes the step resumable.

If you want to re-caption, delete `description.txt` first. Note that if `summarize` has already
run, that file holds the **summary**, and the original captions are gone.

## Re-running summarize produced worse text

Because it summarised its own summary. `summarize` overwrites `description.txt`, so the second
run's input is the first run's output.

Delete `description.txt`, re-run `describe` to regenerate captions, then `summarize` once.
Recorded in [`internal/known-issues.md`](./internal/known-issues.md).

## No frames extracted

| Cause | Check |
|---|---|
| Not `.mp4` | Only `*.mp4` is globbed |
| Codec OpenCV cannot open | "Cannot open video file" in the output |
| FPS metadata missing | "Cannot determine FPS" — remux with ffmpeg |

## "Warning: Couldn't read frame at Ns"

Common at the last second — the duration calculation rounds up and the final seek can land past
the end. Harmless.

If it happens throughout, the file is likely variable-frame-rate, where per-second seeking is
unreliable. Recorded in [`internal/known-issues.md`](./internal/known-issues.md); re-encoding to
constant frame rate works around it.

## BLIP download fails

It comes from Hugging Face on first `describe`, about 1 GB, into `~/.cache/huggingface`. Behind a
proxy, set `HF_ENDPOINT` or the standard proxy variables. Delete the cache to retry a corrupt
download.

## Out of memory during describe

Use a smaller BLIP variant, or force CPU with `CUDA_VISIBLE_DEVICES=""` — slower, but it will not
run out of VRAM.

## `collect` moved a file I did not expect

It iterates **every** subdirectory looking for `description.txt`, not just `*_frames` folders.
Any unrelated subfolder containing one is collected. Recorded in
[`internal/known-issues.md`](./internal/known-issues.md).

## Output is empty

`summarize` skips empty `description.txt` files. If it is empty, `describe` produced no captions —
check there are actually frames in the folder.

## Titles lost their quotation marks

`summarize` strips every `"` from both its input and its output, so titles never come back
quoted. Deliberate, and blunt.

## Tests fail on a fresh clone

```bash
pip install -e . --no-deps
python -m unittest discover -s tests -v
```

The suite mocks the heavy dependencies, so `--no-deps` is sufficient — and is what CI uses.

## Still stuck

[Open an issue](https://github.com/willtheorangeguy/YouTube-Description-Generator/issues/new/choose)
with the command, the output, your OS and Python version, and whether a GPU is in use.
