#! /usr/bin/env bash
source ../../TEST/build-and-run.sh

hwut_info $1 \
"04-ConvertersAndBOM: Analysis with GNU IConv Converter (no asserts);\n" \
"CHOICES:  BPC=2, BPC=4, BPC=wchar_t;\n" \
"SAME;"

choice=$1
first_f=$2
last_f=$3
directory="../04-ConvertersAndBOM"

case $choice in
"BPC=2" )        args="BYTES_PER_CHARACTER=2";        asserts_f="asserts" ;;
"BPC=4" )        args="BYTES_PER_CHARACTER=4";        asserts_f="asserts" ;;
"BPC=wchar_t" )  args="BYTES_PER_CHARACTER=wchar_t";  asserts_f="asserts" ;;
esac

bar_build_and_run "$directory" "no-asserts" "$first_f" "$last_f" "$args"
