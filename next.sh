#!/bin/bash
# picks new puzzles from the puzzle list
# saves them to puzzles.txt for later use
# notifies me via pushbullet of the puzzles

# fail on error :)
set -e

echo "" > /dev/stderr
echo "[update.sh]" > /dev/stderr
date > /dev/stderr

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# the puzzles are sorted by letter uniqueness, so we don't want the bottom of that
SELECT_TOP_FROM_THREES=48640
SELECT_TOP_FROM_FOURS=221438

# generate these files with the python in /generation
# i.e. (and the same with 4x4s),
# python puzzlegen.py -n 3
# python puzzlerank.py -i puzzles_3x3.txt -o unique > puzzles_3x3_sorted.txt
# probably on a good machine (on my server, process gets killed, presumably memory problems)
maxrand=32767

# 3x3
rangeswithin=$((($SELECT_TOP_FROM_THREES / $maxrand) + 1))
rangerange=$(($SELECT_TOP_FROM_THREES / rangeswithin))
three_select=$((1 + $RANDOM % $rangerange + $RANDOM % $rangeswithin * $rangerange))
echo "selecting line $three_select of $SELECT_TOP_FROM_THREES" > /dev/stderr
threepuzzle=$(awk 'NR == '"${three_select}"' {print} NR > '"${three_select}"' {exit}' $SCRIPT_DIR/generation/puzzles_3x3_sorted.txt)
echo "selected: $threepuzzle" > /dev/stderr

# 4x4
rangeswithin=$((($SELECT_TOP_FROM_FOURS / $maxrand) + 1))
rangerange=$(($SELECT_TOP_FROM_FOURS / rangeswithin))
four_select=$((1 + $RANDOM % $rangerange + $RANDOM % $rangeswithin * $rangerange))
echo "selecting line $four_select of $SELECT_TOP_FROM_FOURS" > /dev/stderr
fourpuzzle=$(awk 'NR == '"${four_select}"' {print} NR > '"${four_select}"' {exit}' $SCRIPT_DIR/generation/puzzles_4x4_sorted.txt)
echo "selected: $fourpuzzle" > /dev/stderr

# save generated to file (next puzzles)
echo $threepuzzle > $SCRIPT_DIR/next.txt
echo $fourpuzzle >> $SCRIPT_DIR/next.txt

source $SCRIPT_DIR/.env
curl -H 'Access-Token: '"${PUSHBULLET_API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data-binary '{"body": "'"${threepuzzle}; ${fourpuzzle}"'", "title": "next ringram puzzles", "type": "note"}' \
  --request POST \
  -o /dev/stderr \
  https://api.pushbullet.com/v2/pushes
