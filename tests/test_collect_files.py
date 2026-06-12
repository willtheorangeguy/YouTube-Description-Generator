"""Tests for youtube_description_generator.collect_files"""
import tempfile
import unittest
from pathlib import Path

from youtube_description_generator import collect_files


class TestCollectFiles(unittest.TestCase):
    """Test cases for collect_files module"""

    def test_moves_and_renames_descriptions(self):
        """Test that description.txt files are moved up and renamed after their folder"""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            folder = base / "video1_frames"
            folder.mkdir()
            (folder / "description.txt").write_text("summary text", encoding="utf-8")

            collect_files.collect_descriptions(base)

            target = base / "video1_frames.txt"
            self.assertTrue(target.exists())
            self.assertEqual(target.read_text(encoding="utf-8"), "summary text")
            self.assertFalse((folder / "description.txt").exists())

    def test_skips_folders_without_description(self):
        """Test that folders with no description.txt are left alone"""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            (base / "video1_frames").mkdir()

            collect_files.collect_descriptions(base)

            self.assertEqual(list(base.glob("*.txt")), [])

    def test_collision_appends_counter(self):
        """Test that an existing target file gets a _1, _2 suffix"""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            folder = base / "video1_frames"
            folder.mkdir()
            (folder / "description.txt").write_text("new", encoding="utf-8")
            (base / "video1_frames.txt").write_text("existing", encoding="utf-8")
            (base / "video1_frames_1.txt").write_text("existing 1", encoding="utf-8")

            collect_files.collect_descriptions(base)

            target = base / "video1_frames_2.txt"
            self.assertTrue(target.exists())
            self.assertEqual(target.read_text(encoding="utf-8"), "new")
            self.assertEqual((base / "video1_frames.txt").read_text(encoding="utf-8"), "existing")


if __name__ == '__main__':
    unittest.main()
