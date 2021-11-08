#!/usr/bin/env bash

#
#usage:
# $0 <sondfontfile.sf>
#output:
# output csv to stdout: bank,tone,name
#


echo 'inst 1' | fluidsynth -a 'alsa'  $1 | grep '^[0-9]' | grep -v '^$' |\
    while true; do
	read line

	if [ "x$line" = "x" ]; then
	    break;
	else
	    bank=`echo $line | cut -c 1-3 | awk '{printf("%d",$1)}'`
	    pg=`echo $line | cut -c 5-7 | awk '{printf("%d",$1)}'`
	    name=`echo $line | cut -c 9-`
	    printf "%u,%u,'$name'\n" $bank $pg;
	fi
    done

