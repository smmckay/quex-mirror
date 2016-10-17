#! /usr/bin/env bash
test_dir=../$1
first_f=$2
last_f=$3

if [[ "$first_f" != "FIRST" && "$first_f" != "NOT-FIRST" ]]; then
    echo "## Warning: \$2 is not FIRST or NOT-FIRST as HWUT would ask"
fi
if [[ "$second_f" != "LAST" && "$second_f" != "NOT-LAST" ]]; then
    echo "## Warning: \$3 is not FIRST or NOT-FIRST as HWUT would ask"
fi

current_dir=`pwd`

cd $test_dir

if [[ "$first_f" == "FIRST" ]]; then
    make clean >& /dev/null
fi
# In any case delete existing object files, and executables
rm -f *.o *.exe

# Make the test program _______________________________________________________
echo "## make lexer $4 $5 $6 $7"
if [[ "$args_to_make" != "" ]]; then
    $QUEX_PATH/TEST/call-make.sh $args_to_make >& tmp-make.txt
else
    $QUEX_PATH/TEST/call-make.sh lexer $4 $5 $6 $7 >& tmp-make.txt
fi

# echo "DEBUG: BEGIN"
# cat tmp-make.txt
# echo "DEBUG: END"

# Run the test ________________________________________________________________
# (including the check for memory leaks)
if [[ "$lexer_name" == "" ]]; then
    lexer_name="./lexer"
fi

chmod a+rx $QUEX_PATH/TEST/valgrindi.sh
$QUEX_PATH/TEST/valgrindi.sh tmp-valgrind.log $lexer_name $args_to_lexer
cat tmp-valgrind.log; rm -f tmp-valgrind.log

# -- use a 'side-kick' to filter additional lines
#    (caller may copy his side-kick over this one, but
#     note: this file deletes the side-kick.sh!)
if [[ -f $current_dir/side-kick.sh ]]; then
    source $current_dir/side-kick.sh tmp-make.txt  
    source $current_dir/side-kick.sh tmp-stdout.txt 
    # No side-kick.sh of another application shall interfer
    rm -f  $current_dir/side-kick.sh
fi

rm -f tmp-stdout.txt tmp-stdout0.txt
rm -f tmp-make.txt   tmp-make0.txt

# Clean up ____________________________________________________________________
if [[ $last_f == "LAST" ]]; then
    make clean >& /dev/null
fi

cd $current_dir
