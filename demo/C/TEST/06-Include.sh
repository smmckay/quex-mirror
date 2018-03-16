#! /usr/bin/env bash
source ../../TEST/build-and-run.sh

choice=$1
first_f=$2
last_f=$3
directory="../06-Include"
app=lexer-1

hwut_info $choice \
    "06-Include: From within reception loop (complicated);\n" \
    "CHOICES:    shallow, deep;"
    
input_file="example-$choice.txt"
bar_build_and_run_this "$directory" "no-asserts" "$first_f" "$last_f" $app "$input_file"

