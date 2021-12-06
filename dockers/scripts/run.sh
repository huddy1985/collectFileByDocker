#!/bin/bash

function newrepo()
{
	echo $1 $2
}


function start()
{
	echo "repos list: $1"
	i=0
	for type in `cat $1`; do
		t=$type
		types[$i]=$t
		((i++))
	done

	lenrepo=`expr $i - 1`

	for t in `seq 0 $lenrepo`; do
		newrepo $2 $t
	done
}

start $1 $2
