"""ranking ringram puzzles by different metrics"""

import argparse
from typing import List
from puzzle import flatten_puzzle, puzzle_solved_to_words, words_to_puzzle_solved


def by_unique_letters(puzzle: List[List[str]]) -> int:
    """Rank by number of unique letters"""
    return len(set(flatten_puzzle(puzzle)))

def main(puzzles_wordy: List[str]):
    """main"""
    ranks = [by_unique_letters]
    puzzles = [words_to_puzzle_solved(words) for words in puzzles_wordy]

    print(f"Ranking by unique letters")
    sorted_puzzles = sorted(puzzles, key=by_unique_letters, reverse=True)
    for i, puzzle in enumerate(sorted_puzzles[:10]):
        print(f"{i+1}. {by_unique_letters(puzzle)}")
        print(", ".join(puzzle_solved_to_words(puzzle)))

    print(f"Ranking by unique letters, skipping used words")
    used_words = set()
    sorted_puzzles = sorted(puzzles, key=by_unique_letters, reverse=True)
    puzzles_freq_filtered = []
    for puzzle in sorted_puzzles:
        words = puzzle_solved_to_words(puzzle)
        if not any(word in used_words for word in words):
            puzzles_freq_filtered.append(puzzle)
            used_words.update(words)
    for i, puzzle in enumerate(puzzles_freq_filtered[:10]):
        print(f"{i+1}. {by_unique_letters(puzzle)}")
        print(", ".join(puzzle_solved_to_words(puzzle)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w",
        "--words",
        nargs="+",
        help="List of words to convert to puzzle",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Input file with words",
    )
    args = parser.parse_args()
    if args.input:
        words = []
        with open(args.input, "r", encoding="utf-8") as f:
            for line in f:
                words.append(line.strip().split(",")) # csv
    else:
        words = [args.words]
    main(words)
