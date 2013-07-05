#!/bin/bash

#do stuff to a list of files

#$filename="${FILE%.*}" #internet magic, chops off file extension

command=$1
args=("$@") #put arguments into an array
rest=("${args[@]:1}") #chop off the first element (as this is the command)
#echo "$command"
#echo "${rest[@]}"
#echo "${rest[@]:1}"
#echo $command ${rest[@]:1}

for element in ${rest[@]}; do
	#filename="${element%.*}"
	#echo "$command $filename"
	$command $element
	echo "-------------------------------------------------------------------"
done
echo " "
echo -e "Finished looping command: $command \a"
