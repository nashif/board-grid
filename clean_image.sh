#!/bin/sh

for i in `find boards/  -name \*.yaml  -mindepth 3`; do
	board=$(basename $i .yaml)
	d=$(dirname $i)
	dd=$(basename $d)
	if [ $dd != $board ]; then
		continue
	fi
	if [ -f "$d/doc/img/$board.jpg" -o -f "$d/doc/img/$board.png" ]; then
		echo "image available for $board: $d/doc/img/$board.png"
	else
		if [ -d "$d/doc" ]; then
			pushd $d/doc
			for ff in `find -name *.jpg -o -name *.png`; do
				if [ -f "index.rst" ]; then
					fig=$(grep ".. image::" index.rst)
					if [ $? == "0" ]; then
						echo
						echo "Fixing $board"
						echo
						img=$(echo $fig | cut -d' ' -f3)
						imgdir=$(dirname $img)
						extension="${img##*.}"
						mv $img $imgdir/$board.$extension
						sed -i "s@$img@$imgdir/$board.$extension@" index.rst
					fi
				fi
				break
			done
			popd
		fi
	fi

done

