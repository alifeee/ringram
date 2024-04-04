"""Generate ringram puzzles
Optionally with some initial words set
"""

import os
import argparse
import random
from typing import List, Tuple
from tqdm import tqdm

from puzzle import flatten_puzzle, get_puzzle_dashdot_metrics, puzzle_to_str, words_to_puzzle_solved
from puzzleyaml import main as yaml_main

WORDLIST = "words_4-letters.txt"

with open(os.path.join(os.path.dirname(__file__), WORDLIST), encoding="utf-8") as f:
    WORDS = f.read().splitlines()
    WORDS = [word.upper() for word in WORDS]

SAVE_TO = "puzzles.txt"


def validate_words(words: List[str]) -> Tuple[bool, str]:
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
    if any(word not in WORDS for word in words):
        return False, "All words must be in the word list"
    return True, ""


def generate(repeats: bool = False) -> List[str]:
    """Puzzle generator

    Args:
        repeats (bool, optional): Allow word repeats. Defaults to False.

    Returns:
        List[str]: List of puzzles
    """
    puzzles = []
    for word1 in tqdm(WORDS):
        for word2 in WORDS:
            if not repeats and word2 == word1:
                continue
            if word2[0] != word1[0]:
                continue

            for word3 in WORDS:
                if not repeats and (word3 == word1 or word3 == word2):
                    continue
                if word3[0] != word1[3]:
                    continue

                for word4 in WORDS:
                    if not repeats and (word4 == word1 or word4 == word2 or word4 == word3):
                        continue
                    if word4[0] != word2[3] or word4[3] != word3[3]:
                        continue

                    puzzles.append([word1, word2, word3, word4])
    return puzzles


def main(
    w1: str = None,
    w2: str = None,
    w3: str = None,
    w4: str = None,
    verbose: bool = False,
):
    """main"""
    words = [w1, w2, w3, w4]
    if verbose:
        print(f"Words: {words}")

    valid, error = validate_words([w for w in words if w])
    if not valid:
        raise ValueError(error)
    
    puzzles = generate()
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
    with open(SAVE_TO, "w", encoding="utf-8") as f:
        for puzzle in puzzles:
            f.write(f"{','.join(puzzle)}\n")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
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
    main(args.word1, args.word2, args.word3, args.word4, args.verbose)
