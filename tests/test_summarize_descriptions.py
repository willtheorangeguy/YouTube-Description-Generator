"""Tests for summarize_descriptions.py"""
import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock, mock_open
from pathlib import Path

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import summarize_descriptions


class TestSummarizeDescriptions(unittest.TestCase):
    """Test cases for summarize_descriptions module"""

    @patch('summarize_descriptions.subprocess.run')
    def test_summarize_description_success(self, mock_run):
        """Test successful description summarization"""
        # Mock successful subprocess result
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = b"Test Title\n\nTest Description\n\n#test #video"
        mock_run.return_value = mock_result
        
        # Call function
        result = summarize_descriptions.summarize_description("Test input text")
        
        # Assertions
        self.assertEqual(result, "Test Title\n\nTest Description\n\n#test #video")
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        self.assertEqual(call_args[0][0][0], "ollama")
        self.assertEqual(call_args[0][0][1], "run")

    @patch('summarize_descriptions.subprocess.run')
    def test_summarize_description_failure(self, mock_run):
        """Test handling of subprocess failure"""
        # Mock failed subprocess result
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = b"Error message"
        mock_run.return_value = mock_result
        
        # Call function - should raise RuntimeError
        with self.assertRaises(RuntimeError) as context:
            summarize_descriptions.summarize_description("Test input text")
        
        self.assertIn("Ollama failed", str(context.exception))

    @patch('summarize_descriptions.os.walk')
    @patch('summarize_descriptions.Path.exists')
    def test_process_frame_folders_skips_missing_description(self, mock_exists, mock_walk):
        """Test skipping folders without description.txt"""
        # Mock directory structure
        mock_walk.return_value = [
            ("/base", ["video1_frames"], []),
        ]
        mock_exists.return_value = False
        
        # Call function - should skip without error
        summarize_descriptions.process_frame_folders(Path("/base"))
        
        # Should check if file exists
        mock_exists.assert_called()

    @patch('summarize_descriptions.os.walk')
    @patch('summarize_descriptions.Path.exists')
    @patch('summarize_descriptions.Path.read_text')
    def test_process_frame_folders_skips_empty_description(self, mock_read, 
                                                            mock_exists, mock_walk):
        """Test skipping empty description files"""
        # Mock directory structure
        mock_walk.return_value = [
            ("/base", ["video1_frames"], []),
        ]
        mock_exists.return_value = True
        mock_read.return_value = "   \n  "  # Empty/whitespace only
        
        # Call function - should skip without error
        summarize_descriptions.process_frame_folders(Path("/base"))
        
        # Should read the file
        mock_read.assert_called()

    @patch('summarize_descriptions.os.walk')
    @patch('summarize_descriptions.Path.exists')
    @patch('summarize_descriptions.Path.read_text')
    @patch('summarize_descriptions.Path.write_text')
    @patch('summarize_descriptions.summarize_description')
    def test_process_frame_folders_processes_valid_description(self, mock_summarize, 
                                                                 mock_write, mock_read, 
                                                                 mock_exists, mock_walk):
        """Test processing valid description file"""
        # Mock directory structure
        mock_walk.return_value = [
            ("/base", ["video1_frames"], []),
        ]
        mock_exists.return_value = True
        mock_read.return_value = "Valid description text"
        mock_summarize.return_value = "Summary output"
        
        # Call function
        summarize_descriptions.process_frame_folders(Path("/base"))
        
        # Should call summarize and write
        mock_summarize.assert_called_once_with("Valid description text")
        mock_write.assert_called_once()


if __name__ == '__main__':
    unittest.main()
