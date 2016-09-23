# PURPOSE: This script searches for definitions of functions that are never
#          used at all.
#
# The result of this script is not necessarily correct. Before deleting
# functions, make sure everything is checked in. Then delete, then unit test to
# double check.
#
# NOTE: Pipe the output of this script to 'function-check-side-kick.py' in order
#       to get compile line for the editor to jump.
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
    >> pre-$functions_defined

    grep -se "\\b[a-zA-Z_0-9]\+(" $tmp_file \
         | awk '! /^ *def *[a-zA-Z_0-9]+\(/ { print; }' \
         | grep -soe "\\b[a-zA-Z_0-9]\+(" \
         | tr -d "(" \
    >> pre-$functions_called
done

wc pre-$functions_defined
wc pre-$functions_called

sort -u pre-$functions_defined           > $functions_defined
sort -u pre-$functions_called > $functions_called

wc $functions_defined
wc $functions_called

echo "Functions that are defined, but never used (?) <no output is good output>"
diff --new-line-format="" --unchanged-line-format="" \
     $functions_defined $functions_called \
> $functions_unused

# python ./function-check-side-kick.py $functions_unused > $grep_expressions
# bash $grep_expressions

rm -f $functions_defined
rm -f $functions_called
rm -f $functions_unused
rm -f $grep_expression
rm -f $tmp_file

echo "<terminated>"
