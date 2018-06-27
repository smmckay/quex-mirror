#! /usr/bin/env bash
qx_file=$1
application=${qx_file%.*}.exe
choice=$2

if [[ $choice == "--hwut-info" ]]; then
    head -n2 $qx_file | cut -b4-
    echo "HAPPY: 0x0000|0xFFFF;"
    exit
fi

if [ "$3" == "FIRST" ] || [ -z "$3"  ]; then 
    rm -f $application
    make $application >& /dev/null
fi

# Not 'valgrind', used '-fsanitize=address'
# export LSAN_OPTIONS=verbosity=1:log_threads=1
./$application $choice &> tmp.txt
source $QUEX_PATH/TEST/quex_pathify.sh tmp.txt

if [ "$4" == "LAST" ] || [ -z "$4" ]; then 
    make clean >& /dev/null
fi
