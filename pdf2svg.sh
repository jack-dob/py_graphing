#!/bin/bash

COMMAND="inkscape -l"

FILE=`readlink -f $1`
filename="${FILE%.*}" #gets the path/file part of path/file.ext
ext="${FILE##*.}" #gets the ext part of file.ext
folder=`dirname $FILE` #gets the directory name of the argument

$COMMAND $filename.svg $FILE