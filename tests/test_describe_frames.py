"""Tests for youtube_description_generator.describe_frames"""
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock, mock_open
from pathlib import Path

# Mock PIL, transformers, and torch before importing the module
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.Image'] = MagicMock()
sys.modules['transformers'] = MagicMock()
sys.modules['torch'] = MagicMock()

from youtube_description_generator import describe_frames


class TestDescribeFrames(unittest.TestCase):
    """Test cases for describe_frames module"""

    @patch('youtube_description_generator.describe_frames.Image.open')
    @patch('youtube_description_generator.describe_frames._load_model')
    def test_generate_description(self, mock_load_model, mock_image_open):
        """Test generating description for an image"""
        # Mock image
        mock_image = MagicMock()
        mock_image_open.return_value = mock_image
        mock_image.convert.return_value = mock_image

        # Mock processor - return object with 'to' method
        mock_processor = MagicMock()
        mock_inputs = MagicMock()
        mock_inputs.to.return_value = mock_inputs
        mock_processor.return_value = mock_inputs

        # Mock model output
        mock_model = MagicMock()
        mock_model.generate.return_value = [Mock()]
        mock_processor.decode.return_value = "A test description"

        mock_load_model.return_value = (mock_processor, mock_model, "cpu")

        # Call function
        result = describe_frames.generate_description(Path("test_image.jpg"))

        # Assertions
        self.assertEqual(result, "A test description")
        mock_image_open.assert_called_once_with(Path("test_image.jpg"))
        mock_image.convert.assert_called_once_with("RGB")

    def test_import_does_not_load_model(self):
        """Test that importing the module does not load the BLIP model"""
        self.assertIsNone(describe_frames._model)
        self.assertIsNone(describe_frames._processor)

    @patch('youtube_description_generator.describe_frames.Path.glob')
    @patch('youtube_description_generator.describe_frames.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('youtube_description_generator.describe_frames.generate_description')
    def test_describe_images_in_folder_skips_existing(self, mock_generate, mock_file,
                                                       mock_exists, mock_glob):
        """Test that existing description files are skipped"""
        mock_exists.return_value = True

        # Call function
        describe_frames.describe_images_in_folder(Path("test_folder"))

        # Should not generate descriptions if file exists
        mock_generate.assert_not_called()

    @patch('builtins.open', new_callable=mock_open)
    @patch('youtube_description_generator.describe_frames.generate_description')
    def test_describe_images_in_folder_creates_description(self, mock_generate, mock_file):
        """Test creating new description file"""
        # Create a real Path object for the test folder
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            test_folder = Path(tmpdir) / "test_folder"
            test_folder.mkdir()

            # Create mock image files
            (test_folder / "frame_0001.jpg").touch()
            (test_folder / "frame_0002.jpg").touch()

            mock_generate.side_effect = ["Description 1", "Description 2"]

            # Call function
            describe_frames.describe_images_in_folder(test_folder)

            # Assertions
            self.assertEqual(mock_generate.call_count, 2)
            mock_file.assert_called()

    @patch('youtube_description_generator.describe_frames.os.walk')
    @patch('youtube_description_generator.describe_frames.describe_images_in_folder')
    def test_find_and_process_frame_folders(self, mock_describe, mock_walk):
        """Test finding and processing frame folders"""
        # Mock directory structure
        mock_walk.return_value = [
            ("/base", ["video1_frames", "video2_frames", "other_dir"], []),
        ]

        # Call function
        describe_frames.find_and_process_frame_folders(Path("/base"))

        # Should process both frame folders
        self.assertEqual(mock_describe.call_count, 2)


if __name__ == '__main__':
    unittest.main()
