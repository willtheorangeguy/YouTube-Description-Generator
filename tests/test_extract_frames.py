"""Tests for extract_frames.py"""
import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Mock cv2 before importing the module
sys.modules['cv2'] = MagicMock()

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import extract_frames


class TestExtractFrames(unittest.TestCase):
    """Test cases for extract_frames module"""

    @patch('extract_frames.cv2.VideoCapture')
    @patch('extract_frames.os.makedirs')
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

    @patch('extract_frames.cv2.VideoCapture')
    def test_extract_frames_cannot_open(self, mock_video_capture):
        """Test when video cannot be opened"""
        mock_cap = MagicMock()
        mock_video_capture.return_value = mock_cap
        mock_cap.isOpened.return_value = False
        
        # Call function - should return early
        extract_frames.extract_frames("invalid_video.mp4", "test_output")
        
        # Should not call release if not opened
        mock_cap.release.assert_not_called()

    @patch('extract_frames.cv2.VideoCapture')
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


if __name__ == '__main__':
    unittest.main()
