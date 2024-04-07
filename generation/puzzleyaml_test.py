"""Tests for puzzleyaml.py"""

import unittest
from puzzleyaml import main as puzzleyaml


class TestYamlGeneration(unittest.TestCase):
    """Test yaml generation from start to finish"""

    def test_main_4x4(self):
        """Test the YAML generation as it would be used via the CLI"""
        words = ["BIRD", "BORN", "DOVE", "NOSE"]
        reveal = [1, 12]
        expected_data = {
            "dots-top": [6, 2, 5, 6],
            "dots-left": [9, 0, 5, 5],
            "dashes-right": [3, 6, 2, 4],
            "dashes-bottom": [6, 3, 1, 5],
            "letters": [["B", "", "", ""], ["", ""], ["", ""], ["", "", "", "E"]],
        }

        actual_data = puzzleyaml(words, reveal)

        self.assertEqual(actual_data, expected_data)

    def test_bad_inputs_4x4(self):
        """Test various bad inputs"""
        words = ["BIRD", "BORN", "DOVE", "NOSE"]
        reveal = [1, 12]

        # not enough words
        with self.assertRaises(ValueError):
            puzzleyaml(["BIRD", "BORN", "DOVE"], reveal)
        # words not in caps
        with self.assertRaises(ValueError):
            puzzleyaml(["BIRD", "BORN", "dove"], reveal)
        # words not all the same length
        with self.assertRaises(ValueError):
            puzzleyaml(["BIRD", "BORN", "DOVES", "NOSE"], reveal)

    def test_bad_puzzle_4x4(self):
        """A non-formatted puzzle should be denied"""
        words = ["BIRD", "BORN", "DOVE", "HOSE"]
        reveal = [1, 12]

        with self.assertRaises(ValueError):
            puzzleyaml(words, reveal)
