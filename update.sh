#!/bin/bash
# update the website with new puzzles!

set -e

echo [update.sh] > /dev/stderr
date > /dev/stderr

THREE_REVEAL="1 8"
FOUR_REVEAL="1 12"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

current=$(cat $SCRIPT_DIR/current.txt)
next=$(cat $SCRIPT_DIR/next.txt)

echo "current: ${current}" > /dev/stderr
echo "next: ${next}" > /dev/stderr

next3x3=$(echo "${next}" | head -n1)
next4x4=$(echo "${next}" | tail -n1)
current3x3=$(echo "${current}" | head -n1)
current4x4=$(echo "${current}" | tail -n1)

yaml=""
echo "generating yaml..."

py=$SCRIPT_DIR/generation/env/bin/python
gen=$SCRIPT_DIR/generation/puzzleyaml.py
yaml="${yaml}$( $py $gen -w $(echo $next3x3 | sed 's/,/ /g') -r $THREE_REVEAL )\n"
yaml="${yaml}$( $py $gen -w $(echo $next4x4 | sed 's/,/ /g') -r $FOUR_REVEAL )\n"
yaml="${yaml}$( $py $gen -w $(echo $current3x3 | sed 's/,/ /g') -r -1 )\n"
yaml="${yaml}$( $py $gen -w $(echo $current4x4 | sed 's/,/ /g') -r -1 )\n"

echo "generated yaml"
echo -e "${yaml}" > /dev/stderr

echo "moving yaml to website..."
echo -e "${yaml}" > $SCRIPT_DIR/website/_data/puzzles.yaml

echo "installing npm"
export NVM_DIR="/usr/alifeee/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm use 20

echo "regenerating website..."
(cd $SCRIPT_DIR/website; npm run build)

echo "moving NEXT to CURRENT"
mv $SCRIPT_DIR/next.txt $SCRIPT_DIR/current.txt
