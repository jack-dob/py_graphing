#!/bin/bash

COMMAND="$HOME/Documents/Scripts/c_progs/dust_calc"

echo "in $0 running $COMMAND for file $1"
echo ""

FILE=`readlink -f $1`
#echo "$FILE"
filename="${FILE%.*}" #gets the path/file part of path/file.ext
ext="${FILE##*.}" #gets the ext part of file.ext
#echo "$ext"
#echo "$filename"
folder=`dirname $FILE` #gets the directory name of the argument
#echo "$folder"

#ok, using this for ss.00010000 files, therefore want to keep the extension
#first, make sure that $folder/analysis directory is there

if [ -d $folder/analysis ]; then
	outdir="$folder/analysis/$ext"
	#echo "mkdir $outdir" #make a directory to contain output
	if [ ! -d $outdir ]; then
		mkdir $outdir
	fi
	#echo "cd $outdir" #change to the output directory
	cd $outdir
	#echo "$COMMAND $FILE '!$filename.fits'" #run the program
	$COMMAND $FILE !./$ext.fits
else
	echo "ERROR: Could not find folder $folder/analysis"
	echo "exiting....."
fi