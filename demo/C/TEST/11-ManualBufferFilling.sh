#! /usr/bin/env bash
source ../../TEST/build-and-run.sh

hwut_info $1 \
"11-ManualBufferFilling: Manual Buffer Filling (w/o Converter);\n" \
"CHOICES:  feeder-plain, feeder-converter, gavager-plain, gavager-converter, point-plain;"

directory="../11-ManualBufferFilling"
app=$1.exe

bar_build_always_and_run "$directory" "$app" "asserts"


