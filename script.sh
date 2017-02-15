#!/bin/bash
file="test.txt"
while IFS= read -r line
do
        # display $line or do somthing with $line
	printf '%s\n' "$line"
	sed -e 's/[.] \s*/. \n/g'
	#sentences=$(echo $line | tr "\. " "\n")
	for sentence in $sentences
	do
	    echo "> [$sentence]"
	done
done <"$file"


