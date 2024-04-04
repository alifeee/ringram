"""Helpers for ringram puzzles"""

from typing import Dict, List

morse = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
}


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
    # check dimension is 2
    if not all(isinstance(row, list) for row in puzzle_full):
        raise ValueError("Puzzle must be a list of lists")
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
