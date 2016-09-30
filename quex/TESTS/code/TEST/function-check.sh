# PURPOSE: This script searches for definitions of functions that are never
#          used at all.
#
# The result of this script is not necessarily correct. Before deleting
# functions, make sure everything is checked in. Then delete, then unit test to
# double check.
#
# $1 --> generate output in 'gcc compile' format to be handled by an editor
#        to jump to the correct position
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________

if [[ "$1" = "--hwut-info" ]]; then
    echo "Checking for defined but unused functions."
    exit
fi

# Find all function definitions 
functions_defined=$(mktemp)
functions_called=$(mktemp)
functions_unused=$(mktemp)
grep_expression=$(mktemp)
tmp_file=$(mktemp)

file_list=$(find $QUEX_PATH . -name "*.py")

for file in $file_list; do
    sed -e 's/#.*$//' $file > $tmp_file
    grep -soe "^ *def *[a-zA-Z_0-9]\+(" $tmp_file \
         | tr -d "(" \
         | awk '{ print $2; }' \
    >> $functions_defined

    grep -se "\\b[a-zA-Z_0-9]\+(" $tmp_file \
         | awk '! /^ *def *[a-zA-Z_0-9]+\(/ { print; }' \
         | grep -soe "\\b[a-zA-Z_0-9]\+(" \
         | tr -d "(" \
    >> $functions_called
done

wc $functions_defined
wc $functions_called

sort -u $functions_defined > $tmp_file; mv $tmp_file $functions_defined
sort -u $functions_called  > $tmp_file; mv $tmp_file $functions_called

wc $functions_defined
wc $functions_called

echo "Functions that are defined, but never used (?) <no output is good output>"
diff --new-line-format="" --unchanged-line-format="" \
     $functions_defined $functions_called \
> $functions_unused

if [[ "$1" = "compile" ]]; then
    cat $functions_unused | awk '{ print "def *" $1 "("; }' > $tmp_file
    grep -f $tmp_file $QUEX_PATH -r --include "*.py"
else
    cat $functions_unused
fi

# python ./function-check-side-kick.py $functions_unused > $grep_expressions
# bash $grep_expressions

rm -f $functions_defined
rm -f $functions_called
rm -f $functions_unused
rm -f $grep_expression
rm -f $tmp_file

echo "<terminated>"
