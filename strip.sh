#!/bin/bash

if [ $# -eq 0 ]; then
	echo "Usage: [lines to split] [file]"
	echo "[lines to split]: if +ve will remove from beginning of file if -ve will remove from end"
	echo "[file]: the file you wish to operate on"
	exit 0
fi

if [ $1 == "-h" ]; then
	echo "Usage: [lines to split] [file]"
	echo "[lines to split]: if +ve will remove from beginning of file if -ve will remove from end"
	echo "[file]: the file you wish to operate on"
	exit 0
fi
FILE=`readlink -f "${2:-/dev/stdin}"`
#echo "STRIP: $FILE"
#cat $FILE
nlines=`wc -l < $FILE`
command="tail"
clines=$(($nlines - $1))
if [ $1 -lt 0 ]; then
	command="head"
	clines=$(($nlines + $1))
fi

#echo "$nlines $command $clines"
#echo $FILE
#cat $FILE
"$command" -"$clines" < "$FILE"
