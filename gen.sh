#!/bin/bash

CAFFE_ROOT=../caffe;

if [ $# -ne 2 ]; then
	echo "usage: $0 [inkml_dir_name] [output_db_name]"
	exit 1
fi

if [[ "$1" == *"/"* ]]; then
	echo "$1 contains slash"
	exit 1
fi

if [[ "$2" == *"/"* ]]; then
	echo "$2 contains slash"
	exit 1
fi

if [ -e "$2" ]; then
	echo "$2 already exists"
	exit 1
fi

echo "using $1"

mkdir "$1-png"
python inkml2img.py "$1" "$1-png"
if [ $? -ne 0 ]; then
	exit 1
fi

$CAFFE_ROOT/build/tools/convert_imageset -gray "$1"-png/ "$1"-png/listfile.txt "$2"

