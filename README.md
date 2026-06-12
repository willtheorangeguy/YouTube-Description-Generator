# YouTube Description Generator

A pipeline of scripts that automatically generates YouTube Shorts titles, descriptions, and hashtags from `.mp4` video files using computer vision and a local LLM.

## How it works

1. **Extract frames** — samples one frame per second from each `.mp4` file into a `{video}_frames/` folder
2. **Describe frames** — runs each frame through the [BLIP image captioning model](https://huggingface.co/Salesforce/blip-image-captioning-base) and writes a `description.txt` per folder
3. **Summarize** — feeds those frame descriptions to a local [Ollama](https://ollama.com) model (`llama3.1:8b`) which writes a YouTube Shorts title, short description, and 3–5 hashtags back to `description.txt`
4. **Collect results** — moves each `description.txt` out of its frame folder and renames it after the source video

## Requirements

- Python 3.9–3.12
- [Ollama](https://ollama.com) installed and running with `llama3.1:8b` pulled
- A CUDA-capable GPU is optional but recommended for step 2

Install Python dependencies:

```bash
pip install opencv-python pillow transformers torch
```

Pull the Ollama model:

```bash
ollama pull llama3.1:8b
```

## Usage

Place your `.mp4` files in a directory, then run the scripts in order from that directory.

### 1. Extract frames

```bash
python extract_frames.py
```

Processes all `.mp4` files in the current directory. Creates a `{video}_frames/` folder for each file containing one `frame_NNNN.jpg` per second of video.

### 2. Describe frames

```bash
python describe_frames.py [directory]
```

Walks all `*_frames/` folders under the given directory (defaults to the current directory) and writes a `description.txt` containing one caption per frame. Skips folders that already have a `description.txt`.

### 3. Summarize descriptions

```bash
python summarize_descriptions.py [directory]
```

Reads each `description.txt`, sends it to Ollama, and overwrites the file with a YouTube Shorts-ready output in this format:

```
<title>

<short description>

#tag1 #tag2 #tag3
```

Skips folders with no `description.txt`. Defaults to the current directory.

### 4. Collect results (Windows)

```bat
move_files.bat
```

Moves each `description.txt` from its `*_frames/` subfolder into the current directory, renaming it `{video}.txt`. Handles filename collisions by appending a counter.

## Running tests

```bash
python -m unittest discover -s tests -v
```

Tests run on Python 3.9–3.12 in CI via GitHub Actions on every push and pull request.

## License

MIT — see [LICENSE](LICENSE) for details.
