# Command-line interface for the YouTube Shorts description pipeline.
import argparse
from pathlib import Path

from youtube_description_generator import __version__


# Heavy dependencies (cv2, torch, transformers) are imported inside each
# handler so commands that don't need them stay fast.
def cmd_extract(directory: Path):
    from youtube_description_generator.extract_frames import extract_all

    extract_all(directory)


def cmd_describe(directory: Path):
    from youtube_description_generator.describe_frames import find_and_process_frame_folders

    find_and_process_frame_folders(directory)


def cmd_summarize(directory: Path):
    from youtube_description_generator.summarize_descriptions import process_frame_folders

    process_frame_folders(directory)


def cmd_collect(directory: Path):
    from youtube_description_generator.collect_files import collect_descriptions

    collect_descriptions(directory)


def cmd_run(directory: Path):
    cmd_extract(directory)
    cmd_describe(directory)
    cmd_summarize(directory)
    cmd_collect(directory)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ytdg",
        description="Generate YouTube Shorts titles, descriptions, and hashtags from .mp4 files.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    commands = {
        "extract": (cmd_extract, "Extract one frame per second from each .mp4 file"),
        "describe": (cmd_describe, "Caption frames in *_frames/ folders with the BLIP model"),
        "summarize": (cmd_summarize, "Turn frame captions into a title, description, and hashtags via Ollama"),
        "collect": (cmd_collect, "Move each description.txt out of its folder, renamed after the video"),
        "run": (cmd_run, "Run the full pipeline: extract, describe, summarize, collect"),
    }
    for name, (handler, help_text) in commands.items():
        sub = subparsers.add_parser(name, help=help_text)
        sub.add_argument(
            "directory",
            nargs="?",
            default=".",
            type=Path,
            help="Directory to process (default: current directory)",
        )
        sub.set_defaults(handler=handler)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.handler(args.directory)


if __name__ == "__main__":
    main()
