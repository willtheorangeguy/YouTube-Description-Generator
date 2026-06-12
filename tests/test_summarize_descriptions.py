"""Tests for youtube_description_generator.summarize_descriptions"""
import unittest
from unittest.mock import Mock, patch
from pathlib import Path

from youtube_description_generator import summarize_descriptions


class TestSummarizeDescriptions(unittest.TestCase):
    """Test cases for summarize_descriptions module"""

    @patch('youtube_description_generator.summarize_descriptions.subprocess.run')
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

    @patch('youtube_description_generator.summarize_descriptions.subprocess.run')
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

    @patch('youtube_description_generator.summarize_descriptions.os.walk')
    @patch('youtube_description_generator.summarize_descriptions.Path.exists')
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

    @patch('youtube_description_generator.summarize_descriptions.os.walk')
    @patch('youtube_description_generator.summarize_descriptions.Path.exists')
    @patch('youtube_description_generator.summarize_descriptions.Path.read_text')
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

    @patch('youtube_description_generator.summarize_descriptions.os.walk')
    @patch('youtube_description_generator.summarize_descriptions.Path.exists')
    @patch('youtube_description_generator.summarize_descriptions.Path.read_text')
    @patch('youtube_description_generator.summarize_descriptions.Path.write_text')
    @patch('youtube_description_generator.summarize_descriptions.summarize_description')
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
