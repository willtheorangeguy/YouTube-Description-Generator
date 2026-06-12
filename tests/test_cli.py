"""Tests for youtube_description_generator.cli"""
import unittest
from unittest.mock import patch
from pathlib import Path

from youtube_description_generator import cli


class TestCli(unittest.TestCase):
    """Test cases for the ytdg command-line interface"""

    def test_each_subcommand_dispatches_to_its_handler(self):
        """Test that each subcommand calls the matching handler with the directory"""
        for command, handler in [
            ("extract", "cmd_extract"),
            ("describe", "cmd_describe"),
            ("summarize", "cmd_summarize"),
            ("collect", "cmd_collect"),
        ]:
            with patch.object(cli, handler) as mock_handler:
                cli.main([command, "some/dir"])
                mock_handler.assert_called_once_with(Path("some/dir"))

    def test_directory_defaults_to_cwd(self):
        """Test that the directory argument defaults to the current directory"""
        with patch.object(cli, "cmd_collect") as mock_handler:
            cli.main(["collect"])
            mock_handler.assert_called_once_with(Path("."))

    def test_run_invokes_full_pipeline(self):
        """Test that `ytdg run` calls all four steps in order"""
        with patch.object(cli, "cmd_extract") as m_extract, \
             patch.object(cli, "cmd_describe") as m_describe, \
             patch.object(cli, "cmd_summarize") as m_summarize, \
             patch.object(cli, "cmd_collect") as m_collect:
            cli.cmd_run(Path("some/dir"))

            m_extract.assert_called_once_with(Path("some/dir"))
            m_describe.assert_called_once_with(Path("some/dir"))
            m_summarize.assert_called_once_with(Path("some/dir"))
            m_collect.assert_called_once_with(Path("some/dir"))

    def test_no_command_exits_with_error(self):
        """Test that running with no subcommand exits with an error"""
        with self.assertRaises(SystemExit):
            cli.main([])


if __name__ == '__main__':
    unittest.main()
