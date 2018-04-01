#! /usr/bin/env bash
# PURPOSE:
# 
# This tests checks whether the sequence of occurrence of members of the
# user defined token type is the same in the generated code. Only then,
# the packaging of member variables can be controlled and is stable 
# over different versions of quex and python.
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________
bug=185
if [[ $1 == "--hwut-info" ]]; then
    echo "raphamiard: $bug 0.66.5 Stable output for distinct token fields"
    exit
fi

tmp=`pwd`
cd $bug/ 
quex -i token-type.qx --token-class-only  --debug-exception
cat Lexer/Lexer-token | grep -e "position_[0123456789]\+;$" | awk '{ print substr($0, index($0, "position")+9); }' | tr -d ';' > occurrence_sequence.txt
wc occurrence_sequence.txt
sort -n occurrence_sequence.txt > sorted_by_occurrence.txt
echo "Verify that the occurrence sequence is equal the sequence "
echo "how it occurred in generated code. (no output is good output)"
diff occurrence_sequence.txt sorted_by_occurrence.txt
rm -rf Lexer*
rm *.txt
cd $tmp
echo "<terminated>"
