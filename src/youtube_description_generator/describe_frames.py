# This module processes image frames in folders ending with "_frames"
# and generates descriptions using the BLIP model.
import os
from pathlib import Path

from PIL import Image

# Loaded lazily on first use so importing this module doesn't download the model
_processor = None
_model = None
_device = None

_BLIP_MODEL = "Salesforce/blip-image-captioning-base"
# Pin the model revision so an upstream change to the branch cannot silently
# swap the weights we execute. Set BLIP_REVISION to an exact commit SHA to
# lock this down fully; "main" only fixes the ref that gets resolved.
_BLIP_REVISION = os.environ.get("BLIP_REVISION", "main")


# Function to load the BLIP model and processor (once, on first use)
def _load_model():
    global _processor, _model, _device
    if _model is None:
        import torch
        from transformers import BlipProcessor, BlipForConditionalGeneration

        _device = "cuda" if torch.cuda.is_available() else "cpu"
        _processor = BlipProcessor.from_pretrained(
            _BLIP_MODEL, revision=_BLIP_REVISION
        )
        _model = BlipForConditionalGeneration.from_pretrained(
            _BLIP_MODEL, revision=_BLIP_REVISION
        ).to(_device)
    return _processor, _model, _device


# Function to generate a description for a single image
def generate_description(image_path: Path) -> str:
    processor, model, device = _load_model()
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)
    out = model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True)

# Function to describe all images in a folder
def describe_images_in_folder(folder: Path):
    output_file = folder / "description.txt"
    if output_file.exists():
        print(f"Skipping {folder}, description already exists.")
        return

    print(f"Describing frames in: {folder}")
    descriptions = []
    image_files = sorted(folder.glob("*.jpg")) + sorted(folder.glob("*.png"))

    # Check if there are no images
    for img_file in image_files:
        caption = generate_description(img_file)
        descriptions.append(f"{img_file.name}: {caption}")
        print(f"  {img_file.name} -> {caption}")

    # Write all descriptions to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(descriptions))

# Function to find and process all frame folders in a base directory
def find_and_process_frame_folders(base_dir: Path):
    for root, dirs, files in os.walk(base_dir):
        for d in dirs:
            if d.endswith("_frames"):
                describe_images_in_folder(Path(root) / d)

# Main entry point to process all frame folders
if __name__ == "__main__":
    import sys

    base_directory = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    find_and_process_frame_folders(base_directory)
