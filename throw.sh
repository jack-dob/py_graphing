#!/bin/bash

if [ $# -eq 0 ]; then
	echo "Usage: grab.sh [n] [m] [file]"
	echo "[n]: the inital line to cut out"
	echo "[m]: the final line to cut out"
	echo "[file]: the file you wish to operate on"
	exit 0
fi

if [ $1 == "-h" ]; then
	echo "Usage: grab.sh [n] [m] [file]"
	echo "[n]: the inital line to cut out"
	echo "[m]: the final line to cut out"
	echo "[file]: the file you wish to operate on"
	exit 0
fi
#echo "$1 $2 $3"
#STRIP_PATH="$HOME/Documents/Scripts/graphing"
FILE="${3:-/dev/stdin}"
DIFF1=$((`wc -l <$FILE` - $1))
DIFF2=$((`wc -l <$FILE` - $2))
if [ $DIFF1 -lt 0 ]; then
	echo "n is too large"
	exit 0
fi
if [ $DIFF2 -lt 0 ]; then
	echo "m is too large"
	exit 0
fi
#echo "THROW"
#echo $FILE
#echo $DIFF
TEMP=./temp.txt
head -$1 $FILE >$TEMP
tail -$DIFF2 $FILE >> $TEMP
cat $TEMP
rm -f $TEMP
