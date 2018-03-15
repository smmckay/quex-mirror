#! /usr/bin/env bash
source ../../TEST/build-and-run.sh

hwut_info $1 \
   "04-ConvertersAndBOM: Analysis with IBM's ICU Converter (asserts);\n" \
   "CHOICES:  BPC=2, BPC=4, BPC=wchar_t;\n" \
   "SAME;"

choice=$1
first_f=$2
last_f=$3
directory="../04-ConvertersAndBOM"
app=lexer-icu

case $choice in
"BPC=2" )        args="BYTES_PER_CHARACTER=2" ;;
"BPC=4" )        args="BYTES_PER_CHARACTER=4" ;;
"BPC=wchar_t" )  args="BYTES_PER_CHARACTER=wchar_t" ;;
esac

pushd $directory >& /dev/null

hwut_if_first "$first_f" "make clean_$app"
bar_build     "$app"     "asserts" $args
bar_run       "$app"     "asserts" $command_line_arguments
hwut_if_last  "$last_f"  "make clean_$app"

popd >& /dev/null
