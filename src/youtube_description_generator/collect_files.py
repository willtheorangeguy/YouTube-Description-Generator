# Cross-platform port of move_files.bat: moves each description.txt out of its
# subfolder into the base directory, renamed after the folder it came from.
import shutil
from pathlib import Path


# Function to find a target filename that doesn't collide with an existing file
def unique_target(base_dir: Path, folder_name: str) -> Path:
    target = base_dir / f"{folder_name}.txt"
    count = 1
    while target.exists():
        target = base_dir / f"{folder_name}_{count}.txt"
        count += 1
    return target


# Function to collect description.txt files from all subfolders of a directory
def collect_descriptions(base_dir: Path):
    for folder in sorted(p for p in base_dir.iterdir() if p.is_dir()):
        desc_file = folder / "description.txt"
        if not desc_file.exists():
            continue

        target = unique_target(base_dir, folder.name)
        shutil.move(str(desc_file), str(target))
        print(f"Moved and renamed: {desc_file} -> {target}")

    print("Done.")
