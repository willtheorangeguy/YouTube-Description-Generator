# This script summarizes video descriptions for YouTube Shorts using an Ollama model.
import os
from pathlib import Path
import subprocess

# You can change this to any folder, defaults to current directory
BASE_DIR = Path.cwd()

# Function to summarize a video description using an Ollama model
def summarize_description(text: str) -> str:
    prompt = f"""
You are a YouTube Shorts content assistant. Given the following frame-by-frame video description, write a short, 
engaging YouTube Shorts video description and suggest 3-5 relevant hashtags. Do not include user pleasantries or any other prompt. Just provide the output in the specified format.

Descriptions:
{text}

Output format:
<short description>

#tag1 #tag2 #tag3
""".strip() # Edit the prompt as needed

    # Use Ollama (assumes model is already pulled)
    result = subprocess.run(
        ["ollama", "run", "llama3.1:8b"],
        input=prompt.encode("utf-8"),
        capture_output=True,
        check=True
    )

    if result.returncode != 0:
        raise RuntimeError("Ollama failed:\n" + result.stderr.decode())
    return result.stdout.decode().strip()

# Function to process all frame folders in a base directory
def process_frame_folders(base_dir: Path):
    for root, dirs, files in os.walk(base_dir):
        for d in dirs:
            if d.endswith("_frames"):
                folder = Path(root) / d
                desc_file = folder / "description.txt"
                if not desc_file.exists():
                    print(f"Skipping {folder} (no description.txt)")
                    continue

                print(f"Processing {desc_file}...")
                text = desc_file.read_text(encoding="utf-8")
                text = text.replace('"', '')
                if not text.strip():
                    print(f"  Skipping (empty description.txt)")
                    continue

                try:
                    summarized = summarize_description(text)
                    summarized = summarized.replace('"', '') # Clean up quotes
                    desc_file.write_text(summarized, encoding="utf-8")
                    print(f"  ✅ Updated with YouTube Shorts summary and hashtags.")
                except Exception as e:
                    print(f"  ❌ Failed to summarize: {e}")

# Main entry point to process all frame folders
if __name__ == "__main__":
    import sys
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE_DIR
    process_frame_folders(base)
