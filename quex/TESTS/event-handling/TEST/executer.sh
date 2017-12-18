#! /usr/bin/env bash
qx_file=$1
application=${qx_file%.*}.exe
choice=$2

if [[ $choice == "--hwut-info" ]]; then
    head -n2 $qx_file | cut -b4-
    exit
fi
make $application >& /dev/null

./$application $choice &> tmp.txt
source $QUEX_PATH/TEST/quex_pathify.sh tmp.txt
