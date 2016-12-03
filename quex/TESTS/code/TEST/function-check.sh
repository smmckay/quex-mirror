# PURPOSE: This script searches for definitions of functions that are never
#          used at all.
#
# The result of this script is not necessarily correct. Before deleting
# functions, make sure everything is checked in. Then delete, then unit test to
# double check.
#
# ./function-check.sh example 
#
#  => Treat file 'function-check-example.py' as an example.
#
# ./function-check.sh compile 
#
#  => generate output in 'gcc compile' format to be handled by an editor to 
#     jump to the correct position.
#     in shell: "> bash function-check.sh compile > tmp.log"
#     in vim:   ":set makeprg=cat"
#               ":make tmp.log"
#
# CHOICS: 'example' --> self test of this bash script
#         'real'    --> run on the total code base
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________

if [[ "$1" = "--hwut-info" ]]; then
    echo "Checking for defined but unused functions."
    echo "CHOICES: example, real;"
    exit
fi

# Find all function definitions 
tmp_file=$(mktemp)
#debug=true
#show=true

if [[ "$1" = "example" ]]; then
    file_list=function-check-example.py
else
    file_list=$(find $QUEX_PATH . \( -iname "*.py" ! -iname "GetPot.py" ! -iname "interval_handling.py" \) )
fi

all_content=$(mktemp)

sed -e 's/#.*$//' $file_list > $all_content

functions_defined=$(grep -soe "^ *def *[a-zA-Z_0-9]\+(" $all_content \
                    | tr -d "(" \
                    | awk '{ print $2; }')


# 'interval handling.py' must be considered for the search of used functions.
sed -e 's/#.*$//' $(find $QUEX_PATH -name interval_handling.py) >> $all_content

functions_unused=()
for name in $(echo $functions_defined); do
    count=$(grep -c "\b$name\b" $all_content)
    if [ "$count" -lt "2" ]; then
        functions_unused+=($name)
    fi
done

if [[ "$show" = "true" ]]; then
    echo "-( defined )----------"
    echo $functions_defined
    echo "----------------------"
    echo "-( called )-----------"
    echo ${functions_unused[@]}
    echo "----------------------"
fi

if [[ "$1" = "compile" ]] || [[ "$2" = "compile" ]]; then
    echo ${functions_unused[@]} | tr " " "\n" | awk '{ print "\\\\bdef *" $1 "("; }' > $tmp_file
    while read fdef; do
        grep -sHIne "$fdef" $QUEX_PATH -r --include "*.py"
    done < $tmp_file
else
    echo "||||"
    echo ${functions_unused[@]} | tr " " "\n" | sort
    echo "||||"
fi

# python ./function-check-side-kick.py $functions_unused > $grep_expressions
# bash $grep_expressions

rm -f $tmp_file
rm -f $all_content

echo "<terminated>"
