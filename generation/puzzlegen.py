"""Generate ringram puzzles
Optionally with some initial words set
"""

import os
import argparse
from typing import List, Tuple

WORDLIST = "words_4-letters.txt"
with open(os.path.join(os.path.dirname(__file__), WORDLIST), encoding="utf-8") as f:
    WORDS = f.read().splitlines()
    WORDS = [word.upper() for word in WORDS]


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


def generate():
    """recursive generator"""
    # to-do


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
