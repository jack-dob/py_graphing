#!/bin/bash

if [ $# -eq 0 ]; then
	echo "Usage: grab.sh [n] [m] [file]"
	echo "[n]: the inital line to start readout from"
	echo "[m]: the final line in the readout"
	echo "[file]: the file you wish to operate on"
	exit 0
fi

if [ $1 == "-h" ]; then
	echo "Usage: grab.sh [n] [m] [file]"
	echo "[n]: the inital line to start readout from"
	echo "[m]: the final line in the readout"
	echo "[file]: the file you wish to operate on"
	exit 0
fi
#echo "$1 $2 $3"
STRIP_PATH="$HOME/Documents/Scripts/graphing"
FILE="${3:-/dev/stdin}"
DIFF1=$((`wc -l < $FILE` - $1))
DIFF2=$((`wc -l < $FILE` - $2))
if [ $DIFF1 -lt 0 ]; then
	echo "n is too large"
	exit 0
fi
if [ $DIFF2 -lt 0 ]; then
	echo "m is too large"
	exit 0
fi
#echo "GRAB"
#echo $FILE
#echo $DIFF
TEMP=./temp.txt
$STRIP_PATH/strip.sh $1 $FILE >$TEMP
$STRIP_PATH/strip.sh -$DIFF2 $TEMP
rm -f $TEMP
