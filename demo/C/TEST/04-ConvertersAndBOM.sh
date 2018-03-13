#! /usr/bin/env bash
source ../../TEST/build-and-run.sh

hwut_info $1 \
"04-ConvertersAndBOM: Unicode Based Lexical Analyzis (Using GNU's Lib IConv);\n" \
"CHOICES:  BPC=2, BPC=2_NDEBUG, BPC=4, BPC=4_NDEBUG, BPC=wchar_t;\n" \
"SAME;"

choice=$1
first_f=$2
last_f=$3
directory="../04-ConvertersAndBOM"

case $choice in
"BPC=2" )        args="BYTES_PER_CHARACTER=2" ;;
"BPC=2_NDEBUG" ) args="BYTES_PER_CHARACTER=2 NDEBUG" ;;
"BPC=4" )        args="BYTES_PER_CHARACTER=4" ;;
"BPC=4_NDEBUG" ) args="BYTES_PER_CHARACTER=4 NDEBUG" ;;
"BPC=wchar_t" )  args="BYTES_PER_CHARACTER=wchar_t" ;;
esac

pushd $directory >& /dev/null

hwut_if_first $first_f "make clean_lexer"
bar_build lexer "$args"
bar_run   lexer 
hwut_if_last $last_f "make clean_lexer"

popd >& /dev/null
