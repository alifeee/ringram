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
    """Flatten a puzzle to a list of strings,
    from top left to bottom right, rightwards, then downwards
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
    # 4x4
    if len(puzzle_flat) == 12:
        return [puzzle_flat[0:4], puzzle_flat[4:6], puzzle_flat[6:8], puzzle_flat[8:12]]
    # 3x3
    if len(puzzle_flat) == 8:
        return [puzzle_flat[0:3], puzzle_flat[3:5], puzzle_flat[5:8]]
    raise ValueError("Only 4x4 and 3x3 puzzles implemented")


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
    if len(words[0]) == 4:
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
    if len(words[0]) == 3:
        return inflate_puzzle(
            [
                words[0][0],
                words[0][1],
                words[0][2],
                words[1][1],
                words[2][1],
                words[3][0],
                words[3][1],
                words[3][2],
            ]
        )
    raise ValueError("Only 4x4 and 3x3 puzzles implemented")


def puzzle_solved_to_words(puzzle: List[List[str]]) -> List[str]:
    """Convert a solved puzzle to words
    input (visual)
      B I R D
      O     O
      R     V
      N O S E
    input (python)
      [
        ["B", "I", "R", "D"],
        ["O",           "O"],
        ["R",           "V"],
        ["N", "O", "S", "E"],
      ]
    output
      ["BIRD", "BORN", "DOVE", "NOSE"]
    """
    if len(puzzle) == 4:
        return [
            "".join([puzzle[0][0], puzzle[0][1], puzzle[0][2], puzzle[0][3]]),
            "".join([puzzle[0][0], puzzle[1][0], puzzle[2][0], puzzle[3][0]]),
            "".join([puzzle[0][3], puzzle[1][1], puzzle[2][1], puzzle[3][3]]),
            "".join([puzzle[3][0], puzzle[3][1], puzzle[3][2], puzzle[3][3]]),
        ]
    if len(puzzle) == 3:
        return [
            "".join([puzzle[0][0], puzzle[0][1], puzzle[0][2]]),
            "".join([puzzle[0][0], puzzle[1][0], puzzle[2][0]]),
            "".join([puzzle[0][2], puzzle[1][1], puzzle[2][2]]),
            "".join([puzzle[2][0], puzzle[2][1], puzzle[2][2]]),
        ]
    raise ValueError("Only 4x4 and 3x3 puzzles implemented")


def puzzle_to_puzzle_unsolved(
    puzzle: List[List[str]], reveal: List[int]
) -> List[List[str]]:
    """Conceal all elements of a puzzle apart from those in reveal
    if reveal contains "-1", show all elements
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
    or with metrics into this
      6 2 5 6
    9 B - - - 3
    0 -     - 6
    5 -     - 2
    5 - - - E 4
      6 3 1 5
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
    # do not do negative indexing for now
    if row < 0:
        raise IndexError("Cannot negatively index puzzles (yet...)")
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
    # not sure intimately how this logic works, but the tests pass
    maxindex = len(puzzle) - 1
    extrema = [0, maxindex]
    if col == 0:
        return [puzzle[i][0] for i in range(maxindex + 1)]
    if 0 < col < maxindex:
        return [puzzle[i][col] for i in extrema]
    if col == maxindex:
        return [puzzle[i][maxindex if i in extrema else 1] for i in range(maxindex + 1)]
    raise IndexError(f"Column must be between 0 and {maxindex}")


def list_to_morse(letters: List[str]) -> List[str]:
    """Convert a list of letters to morse
    e.g., ["B", "I", "R", "D"] -> ["-...", "..", ".-.", "-.."]
    """
    if isinstance(letters, str):
        raise ValueError("letters should be a list")
    return [morse[letter] for letter in letters]


def n_dots(sequence: str) -> int:
    """Get the number of dots in a morse sequence
    e.g., "-..." -> 3
    """
    if isinstance(sequence, list):
        raise ValueError("sequence must be a string")
    return sequence.count(".")


def n_dashes(sequence: str) -> int:
    """Get the number of dashes in a morse sequence
    e.g., "-..." -> 1
    """
    if isinstance(sequence, list):
        raise ValueError("sequence must be a string")
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
    puzzle_size = len(puzzle)  # hopefully 3 or 4
    dots_top = [
        n_dots("".join(list_to_morse(get_col(puzzle, i)))) for i in range(puzzle_size)
    ]
    dots_left = [
        n_dots("".join(list_to_morse(get_row(puzzle, i)))) for i in range(puzzle_size)
    ]
    dashes_right = [
        n_dashes("".join(list_to_morse(get_row(puzzle, i)))) for i in range(puzzle_size)
    ]
    dashes_bottom = [
        n_dashes("".join(list_to_morse(get_col(puzzle, i)))) for i in range(puzzle_size)
    ]
    return {
        "dots-top": dots_top,
        "dots-left": dots_left,
        "dashes-right": dashes_right,
        "dashes-bottom": dashes_bottom,
    }
