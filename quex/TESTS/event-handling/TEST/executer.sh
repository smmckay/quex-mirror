#! /usr/bin/env bash
# $1 application
# $2 choice
./$1 $2 &> tmp.txt
source $QUEX_PATH/TEST/quex_pathify.sh tmp.txt
