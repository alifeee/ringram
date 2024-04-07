"""Tests for puzzle.py"""

import unittest
from puzzle import (
    flatten_puzzle,
    get_col,
    get_puzzle_dashdot_metrics,
    get_row,
    inflate_puzzle,
    n_dashes,
    n_dots,
    puzzle_solved_to_words,
    puzzle_to_puzzle_unsolved,
    words_to_puzzle_solved,
    list_to_morse,
)


class TestFlattenPuzzle(unittest.TestCase):
    """Tests for flattening and inflating puzzles
    Note that "FLAT" means read from top left to bottom right, rightwards, then downwards
    """

    flat_4x4 = ["B", "I", "R", "D", "O", "O", "R", "V", "N", "O", "S", "E"]
    full_4x4 = [
        ["B", "I", "R", "D"],
        ["O", "O"],
        ["R", "V"],
        ["N", "O", "S", "E"],
    ]

    flat_3x3 = ["H", "I", "T", "U", "O", "M", "A", "P"]
    full_3x3 = [
        # (format comment)
        ["H", "I", "T"],
        ["U", "O"],
        ["M", "A", "P"],
    ]

    def test_inflate(self):
        """inflate_puzzle should inflate a puzzle"""
        for flat_puzzle, full_puzzle in [
            (self.flat_3x3, self.full_3x3),
            (self.flat_4x4, self.full_4x4),
        ]:
            with self.subTest(flat_puzzle=flat_puzzle, full_puzzle=full_puzzle):
                inflated_puzzle = inflate_puzzle(flat_puzzle)

                self.assertEqual(inflated_puzzle, full_puzzle)

    def test_flatten(self):
        """flatten_puzzle should flatten a puzzle"""
        for flat_puzzle, full_puzzle in [
            (self.flat_3x3, self.full_3x3),
            (self.flat_4x4, self.full_4x4),
        ]:
            with self.subTest(flat_puzzle=flat_puzzle, full_puzzle=full_puzzle):
                flattened_puzzle = flatten_puzzle(full_puzzle)

                self.assertEqual(flattened_puzzle, flat_puzzle)


class TestWordsToPuzzle(unittest.TestCase):
    """Tests creating puzzles from word lists and vice versa
    This is not the same as flattening the puzzles
    """

    words_4x4 = ["BIRD", "BORN", "DOVE", "NOSE"]
    puzzle_4x4 = [
        ["B", "I", "R", "D"],
        ["O", "O"],
        ["R", "V"],
        ["N", "O", "S", "E"],
    ]

    words_3x3 = ["HIT", "HUM", "TOP", "MAP"]
    puzzle_3x3 = [
        # (format comment)
        ["H", "I", "T"],
        ["U", "O"],
        ["M", "A", "P"],
    ]

    def test_words_to_puzzle_solved(self):
        """words_to_puzzle_solved should create a puzzle from four 4 letter words"""
        for words, puzzle in [
            (self.words_4x4, self.puzzle_4x4),
            (self.words_3x3, self.puzzle_3x3),
        ]:
            with self.subTest(words=words, puzzle=puzzle):
                puzzle_solved = words_to_puzzle_solved(words)

                self.assertEqual(puzzle_solved, puzzle)

    def test_puzzle_solved_to_words(self):
        """puzzle_solved_to_words should create a list of 4 words from a puzzle"""
        for words, puzzle in [
            (self.words_4x4, self.puzzle_4x4),
            (self.words_3x3, self.puzzle_3x3),
        ]:
            with self.subTest(words=words, puzzle=puzzle):
                words_from_puzzle = puzzle_solved_to_words(puzzle)

                self.assertEqual(words_from_puzzle, words)


class TestPuzzleUnsolved(unittest.TestCase):
    """Tests that puzzles can be hidden properly"""

    puzzle_4x4 = [
        ["B", "I", "R", "D"],
        ["O", "O"],
        ["R", "V"],
        ["N", "O", "S", "E"],
    ]
    puzzle_3x3 = [
        # (format comment)
        ["H", "I", "T"],
        ["U", "O"],
        ["M", "A", "P"],
    ]

    def test_hide_none_4x4(self):
        """puzzle_to_puzzle_unsolved should hide all letters when nothing is in reveal"""
        puzzle = self.puzzle_4x4
        reveal = []
        expected = [
            # (comment for formatting)
            ["", "", "", ""],
            ["", ""],
            ["", ""],
            ["", "", "", ""],
        ]

        puzzle_hidden = puzzle_to_puzzle_unsolved(puzzle, reveal)

        self.assertEqual(puzzle_hidden, expected)

    def test_hide_some_4x4(self):
        """puzzle_to_puzzle_unsolved should hide the relevant elements in reveal,
        ignoring those above the size of the puzzle"""
        puzzle = self.puzzle_4x4
        reveal = [1, 3, 6, 10, 13]
        expected = [
            # (comment for formatting)
            ["B", "", "R", ""],
            ["", "O"],
            ["", ""],
            ["", "O", "", ""],
        ]

        puzzle_hidden = puzzle_to_puzzle_unsolved(puzzle, reveal)

        self.assertEqual(puzzle_hidden, expected)

    def test_hide_all_4x4(self):
        """puzzle_to_puzzle_unsolved should hide no letters when -1 is in reveal"""
        puzzle = self.puzzle_4x4
        reveal = [-1, 0, 1]

        puzzle_hidden = puzzle_to_puzzle_unsolved(puzzle, reveal)

        self.assertEqual(puzzle_hidden, puzzle)

    def test_hide_none_3x3(self):
        """puzzle_to_puzzle_unsolved should hide all letters when nothing is in reveal"""
        puzzle = self.puzzle_3x3
        reveal = []
        expected = [
            # (comment for formatting)
            ["", "", ""],
            ["", ""],
            ["", "", ""],
        ]

        puzzle_hidden = puzzle_to_puzzle_unsolved(puzzle, reveal)

        self.assertEqual(puzzle_hidden, expected)

    def test_hide_some_3x3(self):
        """puzzle_to_puzzle_unsolved should hide the relevant elements in reveal,
        ignoring those above the size of the puzzle"""
        puzzle = self.puzzle_3x3
        reveal = [1, 3, 6, 10, 13]
        expected = [
            # (comment for formatting)
            ["H", "", "T"],
            ["", ""],
            ["M", "", ""],
        ]

        puzzle_hidden = puzzle_to_puzzle_unsolved(puzzle, reveal)

        self.assertEqual(puzzle_hidden, expected)

    def test_hide_all_3x3(self):
        """puzzle_to_puzzle_unsolved should hide no letters when -1 is in reveal"""
        puzzle = self.puzzle_3x3
        reveal = [-1, 0, 1]

        puzzle_hidden = puzzle_to_puzzle_unsolved(puzzle, reveal)

        self.assertEqual(puzzle_hidden, puzzle)


class TestPuzzleIndexing(unittest.TestCase):
    """Test indexing rows/columns for puzzles"""

    puzzle_4x4 = [
        ["B", "I", "R", "D"],
        ["O", "O"],
        ["R", "V"],
        ["N", "O", "S", "E"],
    ]
    puzzle_3x3 = [
        # (format comment)
        ["H", "I", "T"],
        ["U", "O"],
        ["M", "A", "P"],
    ]

    def test_get_row_4x4(self):
        """get_row should get the asked-for row"""
        puzzle = self.puzzle_4x4
        row0 = ["B", "I", "R", "D"]
        row1 = ["O", "O"]
        row2 = ["R", "V"]
        row3 = ["N", "O", "S", "E"]

        computed_rows = [get_row(puzzle, row_index) for row_index in range(4)]

        with self.assertRaises(IndexError):
            get_row(puzzle, -1)
        with self.assertRaises(IndexError):
            get_row(puzzle, 4)

        for computed_row, row in zip(computed_rows, [row0, row1, row2, row3]):
            self.assertEqual(computed_row, row)

    def test_get_col_4x4(self):
        """get_col should get the asked-for column"""
        puzzle = self.puzzle_4x4
        col0 = ["B", "O", "R", "N"]
        col1 = ["I", "O"]
        col2 = ["R", "S"]
        col3 = ["D", "O", "V", "E"]

        computed_cols = [get_col(puzzle, col_index) for col_index in range(4)]

        with self.assertRaises(IndexError):
            get_col(puzzle, -1)
        with self.assertRaises(IndexError):
            get_col(puzzle, 4)

        for computed_col, col in zip(computed_cols, [col0, col1, col2, col3]):
            self.assertEqual(computed_col, col)

    def test_get_row_3x3(self):
        """get_row should get the asked-for row"""
        puzzle = self.puzzle_3x3
        row0 = ["H", "I", "T"]
        row1 = ["U", "O"]
        row2 = ["M", "A", "P"]

        computed_rows = [get_row(puzzle, row_index) for row_index in range(3)]

        with self.assertRaises(IndexError):
            get_row(puzzle, -1)
        with self.assertRaises(IndexError):
            get_row(puzzle, 3)

        for computed_row, row in zip(computed_rows, [row0, row1, row2]):
            self.assertEqual(computed_row, row)

    def test_get_col_3x3(self):
        """get_col should get the asked-for column"""
        puzzle = self.puzzle_3x3
        col0 = ["H", "U", "M"]
        col1 = ["I", "A"]
        col2 = ["T", "O", "P"]

        computed_cols = [get_col(puzzle, col_index) for col_index in range(3)]

        with self.assertRaises(IndexError):
            get_col(puzzle, -1)
        with self.assertRaises(IndexError):
            get_col(puzzle, 3)

        for computed_col, col in zip(computed_cols, [col0, col1, col2]):
            self.assertEqual(computed_col, col)


class TestMorse(unittest.TestCase):
    """Tests about morse conversion and dot/dash counting"""

    def test_list_to_morse(self):
        """list_to_morse should successfully convert a list of letters to
        a list of Morse representation
        """
        letters_fine = ["B", "I", "R", "D"]
        letters_morse = ["-...", "..", ".-.", "-.."]
        letters_actually_words = ["BIRD", "WHEN"]
        letters_lowercase = ["b", "i", "r", "d"]
        letters_with_blanks = ["B", "I", "", ""]
        letters_not_a_list = "BIRD"

        computed_morse = list_to_morse(letters_fine)

        self.assertEqual(computed_morse, letters_morse)
        with self.assertRaises(KeyError):
            list_to_morse(letters_actually_words)
        with self.assertRaises(KeyError):
            list_to_morse(letters_lowercase)
        with self.assertRaises(KeyError):
            list_to_morse(letters_with_blanks)
        with self.assertRaises(ValueError):
            list_to_morse(letters_not_a_list)

    def test_count_dots(self):
        """n_dots counts dots correctly"""
        sequence = "-......-.-.."
        sequence_as_list = ["-...", "..", ".-.", "-.."]
        actual_dots = 9

        computed_dots = n_dots(sequence)

        self.assertEqual(computed_dots, actual_dots)
        with self.assertRaises(ValueError):
            n_dots(sequence_as_list)

    def test_count_dashes(self):
        """n_dashes counts dashes correctly"""
        sequence = "-......-.-.."
        sequence_as_list = ["-...", "..", ".-.", "-.."]
        actual_dashes = 3

        computed_dashes = n_dashes(sequence)

        self.assertEqual(computed_dashes, actual_dashes)
        with self.assertRaises(ValueError):
            n_dashes(sequence_as_list)


class TestMetrics(unittest.TestCase):
    """Tests for the metrics for row/col dot/dash count"""

    def test_get_puzzle_dashdot_metrics_4x4(self):
        """get_puzzle_dashdot_metrics should get the right metrics for a 4x4 puzzle"""
        puzzle = [
            ["B", "I", "R", "D"],
            ["O", "O"],
            ["R", "V"],
            ["N", "O", "S", "E"],
        ]
        expected_metrics = {
            "dots-top": [6, 2, 5, 6],
            "dots-left": [9, 0, 5, 5],
            "dashes-right": [3, 6, 2, 4],
            "dashes-bottom": [6, 3, 1, 5],
        }

        computed_metrics = get_puzzle_dashdot_metrics(puzzle)

        self.assertEqual(computed_metrics, expected_metrics)

    def test_get_puzzle_dashdot_metrics_3x3(self):
        """get_puzzle_dashdot_metrics should get the right metrics for a 3x3 puzzle"""
        puzzle = [
            # (format comment)
            ["H", "I", "T"],
            ["U", "O"],
            ["M", "A", "P"],
        ]
        expected_metrics = {
            "dots-top": [6, 3, 2],
            "dots-left": [6, 2, 3],
            "dashes-right": [1, 4, 5],
            "dashes-bottom": [3, 1, 6]
        }

        computed_metrics = get_puzzle_dashdot_metrics(puzzle)

        self.assertEqual(computed_metrics, expected_metrics)
