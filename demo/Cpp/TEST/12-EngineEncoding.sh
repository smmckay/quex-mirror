#! /usr/bin/env bash
source ../../TEST/build-and-run.sh

hwut_info $1 \
    "12-EngineEncoding: Engine Encoding (Example ISO8859-7);\n" \
    "CHOICES:  iso8859-7, utf8, utf16-be, utf16-le;\n" \
    "SAME;"

choice=$1
special=''

case $choice in 
   "utf16-le") choice="utf16"; special="LE";;
   "utf16-be") choice="utf16"; special="BE";;
esac


pushd ../12-EngineEncoding >& /dev/null

$QUEX_PATH/TEST/call-make.sh clean $choice-lexer | grep -v greek.qx 
$QUEX_PATH/TEST/valgrindi.sh tmp.txt ./$choice-lexer $special 
cat tmp.txt; rm -f tmp.txt

popd >& /dev/null
