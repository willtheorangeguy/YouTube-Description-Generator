# YouTube Description Generator — Roadmap

Direction, not a schedule. Defects are tracked in
[`internal/known-issues.md`](./internal/known-issues.md); this page is about what the tool is
*for*.

## Where it is

All four steps work, run independently, and are tested with the heavy dependencies mocked so CI
needs no models. Both models run locally.

## Considered

**Writing the summary to its own file.** The most valuable change. `summarize` overwrites
`description.txt`, destroying the captions and making the step unsafe to re-run — in a pipeline
whose whole shape is about re-running stages independently. A `summary.txt` beside the captions
fixes it, and makes `collect` pick the right file.

**A timeout on the Ollama call.** A stalled model currently stalls the run indefinitely.

**Scoping `collect` to `*_frames` folders.** It currently walks every subdirectory.

**Naming the output after the video.** `{video}_frames.txt` is what the folder-based naming
produces; `{video}.txt` is what people expect.

**Sequential frame reading.** Per-second seeking is unreliable on variable-frame-rate footage.

**Configurable models and sampling rate.** Both are literals. Command-line flags would not cost
much.

**Audio.** Captions describe pictures, so a video whose content is what is said produces poor
descriptions. Local transcription is a natural addition — and the sibling `whisper-captions`
already does it.

## Non-goals

**Cloud models.** The reason to use this is that unpublished footage stays on your machine. A
hosted captioning or summarising API would remove the only real advantage.

**Uploading to YouTube.** It generates text; you paste it. Automating uploads means OAuth,
quotas, and a tool that acts on your channel.

**Editing video.** Frames are read, never written.

**Thumbnail selection, SEO scoring, trend analysis.** Each is a different product, and each needs
data this tool does not have.

**Guaranteeing the output is good.** It is a small local model working from image captions. The
text is a starting point, and the documentation says so rather than implying otherwise.

## Contributing

Issues and pull requests welcome — see the
[Contributing Guide](https://github.com/willtheorangeguy/.github/blob/main/CONTRIBUTING.md).
Writing the summary to a separate file is small, and it is the change that makes the rest of the
pipeline's design actually work.
