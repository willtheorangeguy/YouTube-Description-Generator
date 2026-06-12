"""Tests for youtube_description_generator.extract_frames"""
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock

# Mock cv2 before importing the module
sys.modules['cv2'] = MagicMock()

from youtube_description_generator import extract_frames


class TestExtractFrames(unittest.TestCase):
    """Test cases for extract_frames module"""

    @patch('youtube_description_generator.extract_frames.cv2.VideoCapture')
    @patch('youtube_description_generator.extract_frames.os.makedirs')
    def test_extract_frames_success(self, mock_makedirs, mock_video_capture):
        """Test successful frame extraction"""
        # Mock video capture
        mock_cap = MagicMock()
        mock_video_capture.return_value = mock_cap
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = [30.0, 90]  # FPS and total frames
        mock_cap.read.return_value = (True, Mock())

        # Call function
        extract_frames.extract_frames("test_video.mp4", "test_output")

        # Assertions
        mock_video_capture.assert_called_once_with("test_video.mp4")
        mock_makedirs.assert_called_once_with("test_output", exist_ok=True)
        mock_cap.release.assert_called_once()

    @patch('youtube_description_generator.extract_frames.cv2.VideoCapture')
    def test_extract_frames_cannot_open(self, mock_video_capture):
        """Test when video cannot be opened"""
        mock_cap = MagicMock()
        mock_video_capture.return_value = mock_cap
        mock_cap.isOpened.return_value = False

        # Call function - should return early
        extract_frames.extract_frames("invalid_video.mp4", "test_output")

        # Should not call release if not opened
        mock_cap.release.assert_not_called()

    @patch('youtube_description_generator.extract_frames.cv2.VideoCapture')
    def test_extract_frames_invalid_fps(self, mock_video_capture):
        """Test when FPS cannot be determined"""
        mock_cap = MagicMock()
        mock_video_capture.return_value = mock_cap
        mock_cap.isOpened.return_value = True
        mock_cap.get.return_value = 0  # Invalid FPS

        # Call function - should return early
        extract_frames.extract_frames("test_video.mp4", "test_output")

        # Should not call release if FPS is invalid
        mock_cap.release.assert_not_called()

    @patch('youtube_description_generator.extract_frames.extract_frames')
    def test_extract_all_processes_each_video(self, mock_extract):
        """Test extract_all finds .mp4 files and derives output dirs"""
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "video1.mp4").touch()
            (Path(tmpdir) / "video2.mp4").touch()
            (Path(tmpdir) / "notes.txt").touch()

            extract_frames.extract_all(tmpdir)

            self.assertEqual(mock_extract.call_count, 2)
            _, first_output = mock_extract.call_args_list[0][0]
            self.assertTrue(first_output.endswith("video1_frames"))

    @patch('youtube_description_generator.extract_frames.extract_frames')
    def test_extract_all_no_videos(self, mock_extract):
        """Test extract_all with no .mp4 files"""
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            extract_frames.extract_all(tmpdir)
            mock_extract.assert_not_called()


if __name__ == '__main__':
    unittest.main()
