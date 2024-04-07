"""Generate ringram puzzles
Optionally with some initial words set
"""

import os
import argparse
import random
from typing import List, Tuple
from tqdm import tqdm

from puzzle import (
    flatten_puzzle,
    get_puzzle_dashdot_metrics,
    puzzle_to_str,
    words_to_puzzle_solved,
)
from puzzleyaml import main as yaml_main

WORDLISTS = {"4x4": "words_4-letters.txt", "3x3": "words_3-letters.txt"}
SAVE_TOS = {"4x4": "puzzles_4x4.txt", "3x3": "puzzles_3x3.txt"}


def size_to_num(size: str) -> str:
    """Turn "4x4" into "4" and "3x3" into "3" """
    return size[0]


def validate_words(all_words: List[str], words: List[str]) -> Tuple[bool, str]:
    """Validate words used in puzzle

    Args:
        words (List[str]): List of words

    Returns:
        Tuple[bool, str]: (valid, error)
    """
    # if non-alphanumeric characters
    if any(not word.isalpha() for word in words):
        return False, "All words must be alphabetic"
    # if not 4 letters
    if any(len(word) != 4 for word in words):
        return False, "All words must be exactly 4 letters long"
    # if not all caps
    if any(word != word.upper() for word in words):
        return False, "All words must be all caps"
    # if not in word list
    if any(word not in all_words for word in words):
        return False, "All words must be in the word list"
    return True, ""


def start_start(word1: str, word2: str):
    """Returns true if both inputs start with the same letter.
    False otherwise"""

    return word1[0] == word2[0]


def end_end(word1: str, word2: str):
    """Returns true if both inputs end with the same letter.
    False otherwise"""

    return word1[-1] == word2[-1]


def start_end(word1: str, word2: str):
    """Returns true if the first letter of word1 is the last letter of word2.
    False otherwise"""

    return word1[0] == word2[-1]


def generate(all_words: List[str], repeats: bool = False) -> List[str]:
    """Puzzle generator

    Args:
        repeats (bool, optional): Allow word repeats. Defaults to False.

    Returns:
        List[str]: List of puzzles
    """
    puzzles = []
    for word1 in tqdm(all_words):
        for word2 in all_words:
            if not repeats and word2 == word1:
                continue
            if not start_start(word1, word2):
                continue

            for word3 in all_words:
                if not repeats and (word3 == word1 or word3 == word2):
                    continue
                if not start_end(word3, word1):
                    continue

                for word4 in all_words:
                    if not repeats and (
                        word4 == word1 or word4 == word2 or word4 == word3
                    ):
                        continue
                    if not start_end(word4, word2) or not end_end(word4, word3):
                        continue

                    puzzles.append([word1, word2, word3, word4])
    return puzzles


def main(
    size: str = "4",
    words: List[str] = None,
    verbose: bool = False,
):
    """main"""
    if words is None:
        words = [None, None, None, None]
    if verbose:
        print(f"Words: {words}")

    fname = WORDLISTS[f"{size}x{size}"]
    with open(os.path.join(os.path.dirname(__file__), fname), encoding="utf-8") as f:
        all_words = f.read().splitlines()
        all_words = [word.upper() for word in all_words]

    valid, error = validate_words(all_words, [w for w in words if w])
    if not valid:
        raise ValueError(error)

    puzzles = generate(all_words)

    if verbose:
        print(f"Generated {len(puzzles)} puzzles")
        # print three random puzzles, one with morse
        for i in range(4):
            puzzle = random.choice(puzzles)
            pz = words_to_puzzle_solved(puzzle)
            metrics = get_puzzle_dashdot_metrics(pz)
            if i < 2:
                print(puzzle_to_str(pz))
                print()
            elif i < 3:
                print(puzzle_to_str(pz, metrics=metrics))
                print()
            elif i < 4:
                reveal = [random.randint(0, 11) for _ in range(4)]
                yaml = yaml_main(puzzle, reveal)
                print(yaml)

    # save as "flatten_puzzle" to SAVE_TO
    save_fname = SAVE_TOS[f"{size}x{size}"]
    with open(save_fname, "w", encoding="utf-8") as f:
        for puzzle in puzzles:
            f.write(f"{','.join(puzzle)}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        help="Dimension of puzzle, either 3 or 4",
        default="4",
    )
    parser.add_argument(
        "-w1",
        "--word1",
        help="First word (top)",
    )
    parser.add_argument(
        "-w2",
        "--word2",
        help="Second word (left)",
    )
    parser.add_argument(
        "-w3",
        "--word3",
        help="Third word (right)",
    )
    parser.add_argument(
        "-w4",
        "--word4",
        help="Fourth word (bottom)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print verbose output",
    )
    args = parser.parse_args()
    main(args.n, [args.word1, args.word2, args.word3, args.word4], args.verbose)
