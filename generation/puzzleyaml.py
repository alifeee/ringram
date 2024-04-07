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
import argparse
from typing import List, Tuple
import yaml
from puzzle import (
    get_puzzle_dashdot_metrics,
    puzzle_to_puzzle_unsolved,
    puzzle_to_str,
    words_to_puzzle_solved,
)


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
    # if any word is a different length to the others
    if len(set(len(word) for word in words)) > 1:
        return False, "All words must be the same length"
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


def main(words: List[str], reveal: List[int], verbose: bool = False):
    """main"""
    # validate input
    words_valid, words_error = validate_words(words)
    reveal_valid, reveal_error = validate_reveal(reveal)
    if not words_valid:
        raise ValueError(f"{words_error}. words: {words}")
    if not reveal_valid:
        raise ValueError(f"{reveal_error}. reveal: {reveal}")

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
    if verbose:
        print(yaml_data)
    return yaml_data


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

    data = main(args.words, args.reveal, args.verbose)
    print(yaml.dump([data], default_flow_style=None))
