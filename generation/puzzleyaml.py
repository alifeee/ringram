#!/bin/python
"""Convert a list of puzzle words to a puzzle input
i.e., with the input
  ["BIRD", "BORN", "DOVE", "NOSE"]
...shown in solved and unsolved puzzle form (where "-" is blank), respectively, as
  B I R D    B - - -
  O     O    -     -
  R     V    -     -
  N O S E    - - - E
to the yaml:
  - dots-top: [6, 2, 5, 6]
    dots-left: [9, 0, 5, 5]
    dashes-bottom: [6, 3, 1, 5]
    dashes-right: [3, 6, 2, 4]
    letters: [
      ["B", "", "", "" ],
      ["" ,         "" ],
      ["" ,         "" ],
      ["" , "", "", "E"],
    ]
"""
import os
import argparse
from typing import Dict, List, Tuple
import yaml

# load morse.yaml
with open(
    os.path.join(os.path.dirname(__file__), "morse.yaml"), "r", encoding="utf-8"
) as f:
    morse = yaml.safe_load(f)


def validate_words(words: List[str]) -> Tuple[bool, str]:
    """Validate words for puzzle generation

    Args:
        words (List[str]): List of words

    Returns:
        Tuple[bool, str]: (valid, error)
    """
    # if not 4 words
    if len(words) != 4:
        return False, "There must be exactly 4 words"
    # if any word has non-alphabetic characters
    if any(not word.isalpha() for word in words):
        return False, "All words must be alphabetic"
    # if any word is not 4 letters
    if any(len(word) != 4 for word in words):
        return False, "All words must be exactly 4 letters long"
    # if any word is not all caps
    if any(word != word.upper() for word in words):
        return False, "All words must be all caps"
    # if words are not a valid puzzle
    #  word 0 first and word 1 first are equal
    #  word 0 last  and word 2 first are equal
    #  word 3 first and word 1 last are equal
    #  word 3 last and word 2 last are equal
    if (
        words[0][0] != words[1][0]
        or words[0][-1] != words[2][0]
        or words[3][0] != words[1][-1]
        or words[3][-1] != words[2][-1]
    ):
        return False, "Words must form a valid puzzle"
    return True, ""


def validate_reveal(reveal: List[int]) -> Tuple[bool, str]:
    """Validate reveal for puzzle generation

    Args:
        reveal (List[int]): List of reveal indices

    Returns:
        Tuple[bool, str]: (valid, error)
    """
    # for each reveal index
    for index in reveal:
        # if not an integer
        if not isinstance(index, int):
            return False, "All reveal indices must be integers"
        # if not in grid (1-12)
        if not -1 <= index <= 12:
            return (
                False,
                "All reveal indices must be between (inc.) 1 and 12, or 0 for none, or -1 for all",
            )
    return True, ""


def word_and_letter_to_rowcol(word_index: int, letter_index: int) -> Tuple[int, int]:
    """Convert word and letter index to row and column
    So, given the words ["BIRD", "BORN", "DOVE", "NOSE"],
      the wordIndex 1 (BORN) and letterIndex 2 (R), we return
    (2, 0) as the R is in row 2 and column 0:
      B I R D
      O     O
     <R>    V
      N O S E
    """
    if word_index == 0:  # BIRD
        row = 0
        col = letter_index
    elif word_index == 1:  # BORN
        row = letter_index
        col = 0
    elif word_index == 2:  # DOVE
        row = letter_index
        col = 2
    elif word_index == 3:  # NOSE
        row = 3
        col = letter_index
    return row, col


def flatten_puzzle(puzzle_full: List[List[str]]) -> List[str]:
    """Flatten a puzzle to a list of strings
    input
      [
        ["B", "I", "R", "D"],
        ["O",           "O"],
        ["R",           "V"],
        ["N", "O", "S", "E"],
      ]
    output
      ["B", "I", "R", "D", "O", "O", "R", "V", "N", "O", "S", "E"]
    """
    return [letter for row in puzzle_full for letter in row]


def inflate_puzzle(puzzle_flat: List[str]) -> List[List[str]]:
    """Inflate a puzzle from a list of strings
    input
      ["B", "I", "R", "D", "O", "O", "R", "V", "N", "O", "S", "E"]
    output
      [
        ["B", "I", "R", "D"],
        ["O",           "O"],
        ["R",           "V"],
        ["N", "O", "S", "E"],
      ]
    """
    return [puzzle_flat[0:4], puzzle_flat[4:6], puzzle_flat[6:8], puzzle_flat[8:12]]


def words_to_puzzle_solved(words: List[str]) -> List[List[str]]:
    """Convert words to a puzzle, e.g.,
    input
      ["BIRD", "BORN", "DOVE", "NOSE"]
    output (visual)
      B I R D
      O     O
      R     V
      N O S E
    output (python)
      [
        ["B", "I", "R", "D"],
        ["O",           "O"],
        ["R",           "V"],
        ["N", "O", "S", "E"],
      ]
    """
    return inflate_puzzle(
        [
            words[0][0],
            words[0][1],
            words[0][2],
            words[0][3],
            words[1][1],
            words[2][1],
            words[1][2],
            words[2][2],
            words[3][0],
            words[3][1],
            words[3][2],
            words[3][3],
        ]
    )


def puzzle_to_puzzle_unsolved(
    puzzle: List[List[str]], reveal: List[int]
) -> List[List[str]]:
    """Conceal all elements of a puzzle apart from those in reveal
    input puzzle, and reveal [1, 12]
      B I R D
      O     O
      R     V
      N O S E
    output [visual]
      B - - -
      -     -
      -     -
      - - - E
    output [python]
      [
        ["B", "", "", ""],
        ["",       ""],
        ["",       ""],
        ["", "", "", "E"],
      ]
    """
    flat = flatten_puzzle(puzzle)
    unsolved = []
    for i, letter in enumerate(flat):
        if i + 1 in reveal or -1 in reveal:
            unsolved.append(letter)
        else:
            unsolved.append("")
    return inflate_puzzle(unsolved)


def puzzle_to_str(puzzle: List[str], metrics: Dict[str, List[int]] = None) -> str:
    """Pretty print a puzzle, i.e., turn this
      [
        ["B", "", "", ""],
        ["",       ""],
        ["",       ""],
        ["", "", "", "E"],
      ]
    into this
      B - - -
      -     -
      -     -
      - - - E
    """
    puzzle = inflate_puzzle(
        [letter if letter else "-" for letter in flatten_puzzle(puzzle)]
    )
    _str = ""
    pad_c = "  "  # corner padding
    pad_m = "   "  # middle padding
    if metrics is None:
        _str += f'{" ".join(puzzle[0])}\n'
        _str += f"{puzzle[1][0]} {pad_m} {puzzle[1][1]}\n"
        _str += f"{puzzle[2][0]} {pad_m} {puzzle[2][1]}\n"
        _str += f'{" ".join(puzzle[3])}'
    else:
        topdots = [str(n) for n in metrics["dots-top"]]
        ld = metrics["dots-left"]
        rd = metrics["dashes-right"]
        bottomdashes = [str(n) for n in metrics["dashes-bottom"]]
        _str += f'{pad_c}{" ".join(topdots)}{pad_c}\n'
        _str += f'{ld[0]} {" ".join(puzzle[0])} {rd[0]}\n'
        _str += f"{ld[1]} {puzzle[1][0]} {pad_m} {puzzle[1][1]} {rd[1]}\n"
        _str += f"{ld[2]} {puzzle[2][0]} {pad_m} {puzzle[2][1]} {rd[2]}\n"
        _str += f'{ld[3]} {" ".join(puzzle[3])} {rd[3]}'
        _str += f'\n{pad_c}{" ".join(bottomdashes)}{pad_c}'
    return _str


def get_row(puzzle: List[List[str]], row: int) -> List[str]:
    """Get a row from a puzzle
    e.g., given the puzzle
      B I R D
      O     O
      R     V
      N O S E
    get_row(puzzle, 0) -> ["B", "I", "R", "D]
    get_row(puzzle, 2) -> ["R", "V"]
    """
    return puzzle[row]


def get_col(puzzle: List[List[str]], col: int) -> List[str]:
    """Get a column from a puzzle
    e.g., given the puzzle
      B I R D
      O     O
      R     V
      N O S E
    get_col(puzzle, 0) -> ["B", "O", "R", "N]
    get_col(puzzle, 2) -> ["R", "S"]
    """
    # have to be careful here since middle rows are shorter
    if col == 0:
        return [puzzle[0][0], puzzle[1][0], puzzle[2][0], puzzle[3][0]]
    if col == 1:
        return [puzzle[0][1], puzzle[3][1]]
    if col == 2:
        return [puzzle[0][2], puzzle[3][2]]
    if col == 3:
        return [puzzle[0][3], puzzle[1][1], puzzle[2][1], puzzle[3][3]]
    raise IndexError("Column must be between 0 and 3")


def list_to_morse(letters: List[str]) -> List[str]:
    """Convert a list of letters to morse
    e.g., ["B", "I", "R", "D"] -> ["-...", "..", ".-.", "-.."]
    """
    return [morse[letter] for letter in letters]


def n_dots(sequence: str) -> int:
    """Get the number of dots in a morse sequence
    e.g., "-..." -> 3
    """
    return sequence.count(".")


def n_dashes(sequence: str) -> int:
    """Get the number of dashes in a morse sequence
    e.g., "-..." -> 1
    """
    return sequence.count("-")


def get_puzzle_dashdot_metrics(puzzle: List[List[str]]) -> Dict[str, List[int]]:
    """Get top/left dots, and right/bottom dashes for a puzzle
    Puzzle should be solved
    e.g., given the puzzle
      B I R D
      O     O
      R     V
      N O S E
    get_puzzle_dashdot_metrics(puzzle) -> {
        'dots-top': [6, 2, 5, 6],
        'dots-left': [9, 0, 5, 5],
        'dashes-right': [3, 6, 2, 4]
        'dashes-bottom': [6, 3, 1, 5],
    }
    """
    dots_top = [n_dots("".join(list_to_morse(get_col(puzzle, i)))) for i in range(4)]
    dots_left = [n_dots("".join(list_to_morse(get_row(puzzle, i)))) for i in range(4)]
    dashes_right = [
        n_dashes("".join(list_to_morse(get_row(puzzle, i)))) for i in range(4)
    ]
    dashes_bottom = [
        n_dashes("".join(list_to_morse(get_col(puzzle, i)))) for i in range(4)
    ]
    return {
        "dots-top": dots_top,
        "dots-left": dots_left,
        "dashes-right": dashes_right,
        "dashes-bottom": dashes_bottom,
    }


def main(words: List[str], reveal: List[int], verbose: bool = False):
    """main"""
    # validate input
    words_valid, words_error = validate_words(words)
    reveal_valid, reveal_error = validate_reveal(reveal)
    if not words_valid:
        raise ValueError(words_error)
    if not reveal_valid:
        raise ValueError(reveal_error)

    # create solved puzzle
    solved = words_to_puzzle_solved(words)
    if verbose:
        print("Solved:")
        print(puzzle_to_str(solved))

    # create unsolved puzzle
    unsolved = puzzle_to_puzzle_unsolved(solved, reveal)
    if verbose:
        print()
        print("Unsolved:")
        print(puzzle_to_str(unsolved))

    metrics = get_puzzle_dashdot_metrics(solved)
    if verbose:
        print()
        print("Metrics:")
        print(f"Dots top: {metrics['dots-top']}")
        print(f"Dots left: {metrics['dots-left']}")
        print(f"Dashes right: {metrics['dashes-right']}")
        print(f"Dashes bottom: {metrics['dashes-bottom']}")

    if verbose:
        print()
        print("Unsolved:")
        print(puzzle_to_str(unsolved, metrics))

    # create yaml
    yaml_data = {
        "dots-top": metrics["dots-top"],
        "dots-left": metrics["dots-left"],
        "dashes-right": metrics["dashes-right"],
        "dashes-bottom": metrics["dashes-bottom"],
        "letters": unsolved,
    }
    print(yaml.dump([yaml_data], default_flow_style=None))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w",
        "--words",
        nargs="+",
        help="List of words to convert to puzzle",
        required=True,
    )
    parser.add_argument(
        "-r",
        "--reveal",
        nargs="+",
        type=int,
        help="List of indices to reveal. -1 for all. 0 for none.",
        required=True,
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print verbose output"
    )
    args = parser.parse_args()
    main(args.words, args.reveal, args.verbose)
