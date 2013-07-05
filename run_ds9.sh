#!/bin/bash

COMMAND="ds9"

echo "in $0 running $COMMAND for file $1"
echo ""

FILE=`readlink -f $1`
filename="${FILE%.*}" #gets the path/file part of path/file.ext
ext="${FILE##*.}" #gets the ext part of file.ext
folder=`dirname $FILE` #gets the directory name of the argument

echo "$folder"
# the minimum of all the .fits files is 0.0
# the maximum of all .fits files is 2.404627E+18
# average is 1.88E18
# therefore, will set maximum for all of them to 1.88E18
# for radial smoothed ones average is 2.22E22
# will use GREY color map for radial smoothed pics
# for rubble dust sims use Grey colour map and 1.7E-8 for maximum
# for sqrt scaled fits images use 1.00E18 and see how it turns out


#$COMMAND $FILE -scale limits 0.0 1.88E18 -cmap Heat -colorbar yes -smooth radius 10 -smooth yes -export $filename.png -quit
#$COMMAND $FILE -scale limits 0.0 2.22E22 -cmap Grey -colorbar yes -smooth radius 10 -smooth no -export $filename.png -quit
#$COMMAND $FILE -scale limits 6.0E-9 1.7E-8 -cmap Grey -colorbar yes -smooth radius 10 -smooth no -export $filename.png -quit
$COMMAND $FILE -scale limits 0.0 1.00E18 -cmap Heat -colorbar yes -smooth radius 10 -smooth yes -export $filename.png -quit
