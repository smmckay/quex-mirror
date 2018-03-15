#! /usr/bin/env bash
source ../../TEST/build-and-run.sh

hwut_info $1 \
   "04-ConvertersAndBOM-bom: Lexer with converter that detects BOM;\n" \
   "CHOICES:  Without, UTF8, UTF16BE, EBCDIC, UTF7;"

choice=$1
first_f=$2
last_f=$3
directory="../04-ConvertersAndBOM"
app=lexer-with-bom

case $1 in
"Without" ) args="example.txt";;
"EBCDIC" )  args="example-bom-ebcdic.txt";;
"UTF8" )    args="example-bom-utf8.txt";;
"UTF16BE" ) args="example-bom-utf16be.txt";;
"UTF7" )    args="example-bom-utf7.txt";;
esac

bar_build_and_run_this "$directory" "no-asserts" "$first_f" "$last_f" $app "$args"




