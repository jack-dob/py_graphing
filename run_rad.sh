#!/bin/bash

COMMAND="$HOME/Documents/Scripts/c_progs/rad_dust"

echo "in $0 running $COMMAND for file $1"
echo ""

FILE=`readlink -f $1`
#echo "$FILE"
filename="${FILE%.*}" #gets the path/file part of path/file.ext
ext="${FILE##*.}" #gets the ext part of file.ext
mid="${filename##*.}"
#echo "$ext"
#echo "$filename"
folder=`dirname $FILE` #gets the directory name of the argument
#echo "$folder"

#ok, using this for ss.00010000.dust files, therefore want to keep the middle bit
#first, make sure that $folder/analysis directory is there

if [ -d $folder/analysis ]; then
	outdir="$folder/analysis/$mid"
	#echo "mkdir $outdir" #make a directory to contain output
	if [ -d $outdir ]; then
		:
	else
		mkdir $outdir
	fi
	#echo "cd $outdir" #change to the output directory
	cd $outdir
	#echo "$COMMAND $FILE '!$filename.fits'" #run the program
	$COMMAND $FILE !./ann_$mid.fits
else
	echo "ERROR: Could not find folder $folder/analysis"
	echo "exiting....."
fi