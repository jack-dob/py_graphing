#!/bin/bash

CMD1="$HOME/Documents/Scripts/graphing/surf_density.py"
CMD2="$HOME/Documents/Scripts/graphing/mVa_graph.py"
CMD3="$HOME/Documents/Scripts/graphing/eVa_graph.py"
echo "in $0 running $COMMAND for file $1"
echo ""

FILE=`readlink -f $1`
filename="${FILE%.*}" #gets the path/file part of path/file.ext
ext="${FILE##*.}" #gets the ext part of file.ext
folder=`dirname $FILE` #gets the directory name of the argument

echo "$folder"
outdir1="$folder/analysis/surf_d"
outdir2="$folder/analysis/mVa"
outdir3="$folder/analysis/eVa"
if [ -d $outdir1 ]; then
	$CMD1 $FILE $outdir1
else
	mkdir $outdir1
	$CMD1 $FILE $outdir1
fi
#
if [ -d $outdir2 ]; then
	$CMD2 $FILE $outdir2
else
	mkdir $outdir2
	$CMD2 $FILE $outdir2
fi
#
if [ -d $outdir3 ]; then
	$CMD3 $FILE $outdir3
else
	mkdir $outdir3
	$CMD3 $FILE $outdir3
fi

