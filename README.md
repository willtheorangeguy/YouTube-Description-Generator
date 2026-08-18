<!-- Logo -->
<h1 align="center">YouTube Description Generator</h1>

<!-- Copy -->
<h4 align="center">Turns a folder of Shorts into upload-ready titles, descriptions, and hashtags — entirely on your own machine.</h4>

<!-- Badges -->
<div align="center">
  <img alt="Tests" src="https://github.com/willtheorangeguy/YouTube-Description-Generator/actions/workflows/tests.yml/badge.svg">
  <img alt="GitHub Issues" src="https://img.shields.io/github/issues/willtheorangeguy/YouTube-Description-Generator">
  <img alt="GitHub Pull Requests" src="https://img.shields.io/github/issues-pr/willtheorangeguy/YouTube-Description-Generator">
  <img alt="License" src="https://img.shields.io/github/license/willtheorangeguy/YouTube-Description-Generator">
</div>

<!-- Navigation -->
<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#support">Support</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

## Key Features

- Samples one frame per second, captions each with [BLIP](https://huggingface.co/Salesforce/blip-image-captioning-base), and has a local [Ollama](https://ollama.com) model write the result up.
- **No API keys and no cloud services** — both models run locally, and nothing about your unpublished videos leaves the machine.
- Four steps you can run individually, so a failed stage is re-runnable without repeating the expensive one.
- One `.txt` per video, ready to paste.

```
Epic Sunset Timelapse

Watch the sky transform in 30 seconds of pure color.

#sunset #timelapse #shorts
```

## Installation

```bash
pip install git+https://github.com/willtheorangeguy/YouTube-Description-Generator.git
ollama pull llama3.1:8b
```

Python 3.9+, plus Ollama running. PyTorch and Transformers are large downloads. See [`docs/installation.md`](docs/installation.md).

## Usage

```bash
ytdg run path/to/videos      # the whole pipeline
ytdg extract [directory]     # .mp4 → {video}_frames/frame_NNNN.jpg
ytdg describe [directory]    # frames → description.txt
ytdg summarize [directory]   # description.txt → title, description, hashtags
ytdg collect [directory]     # */description.txt → {folder}.txt
```

Every command defaults to the current directory.

> **`summarize` overwrites `description.txt` with its output**, replacing the frame captions — and `describe` skips folders that already have the file. Read [`docs/internal/known-issues.md`](docs/internal/known-issues.md) before re-running a stage.

## Documentation

Full documentation lives in [`docs/`](docs/README.md):
[Quickstart](docs/quickstart.md) · [Installation](docs/installation.md) · [Configuration](docs/configuration.md) · [Architecture](docs/architecture.md) · [API](docs/api.md) · [Development](docs/development.md) · [FAQ](docs/faq.md) · [Troubleshooting](docs/troubleshooting.md) · [Roadmap](docs/roadmap.md)

## Support

Open a [GitHub Discussion](https://github.com/willtheorangeguy/YouTube-Description-Generator/discussions/new) or file an [issue](https://github.com/willtheorangeguy/YouTube-Description-Generator/issues/new/choose).

## Contributing

Contributions welcome. See the org-wide [Contributing Guide](https://github.com/willtheorangeguy/.github/blob/main/CONTRIBUTING.md) and [Code of Conduct](https://github.com/willtheorangeguy/.github/blob/main/CODE_OF_CONDUCT.md).

## Credits

Captioning by [BLIP](https://huggingface.co/Salesforce/blip-image-captioning-base) via [Transformers](https://huggingface.co/docs/transformers); summarising by [Ollama](https://ollama.com); frames by [OpenCV](https://opencv.org/).

## License

MIT — see [`LICENSE.md`](LICENSE.md).
