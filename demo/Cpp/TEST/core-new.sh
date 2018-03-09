test_dir=../$1
asserts_f=$2
first_f=$3
last_f=$4
current_dir=`pwd`

echo "ARGS:" $*
echo $1 $2 $3 >> tmp.txt

cd $test_dir

if [ "$first_f" == "FIRST" ] || [ -z "$first_f"  ]; then 
    make clean >& /dev/null
fi

# Make the test program _______________________________________________________
echo "## make lexer $4 $5 $6 $7"
if [[ "$args_to_make" != "" ]]; then
    $QUEX_PATH/TEST/call-make.sh $args_to_make >& tmp-make.txt
else
    $QUEX_PATH/TEST/call-make.sh lexer $4 $5 $6 $7 >& tmp-make.txt
fi

# Run the test ________________________________________________________________
# (including the check for memory leaks)
if [[ "$lexer_name" == "" ]]; then
    lexer_name="./lexer"
fi

bash $QUEX_PATH/TEST/valgrindi.sh tmp-valgrind.log $lexer_name $args_to_lexer
cat tmp-valgrind.log; rm -f tmp-valgrind.log

# -- use a 'side-kick' to filter additional lines
#    (caller may copy his side-kick over this one, but
#     note: this file deletes the side-kick.sh!)
if [[ -f $current_dir/side-kick.sh ]]; then
    source $current_dir/side-kick.sh tmp-make.txt  
    source $current_dir/side-kick.sh tmp-stdout.txt 
    # No side-kick.sh of another application shall interfer
    rm -f  $current_dir/side-kick.sh
else
    cat tmp-make.txt  
    #cat tmp-stdout.txt 
fi

rm -f tmp-stdout.txt tmp-stdout0.txt
rm -f tmp-make.txt   tmp-make0.txt

# Clean up ____________________________________________________________________
if [ "$last_f" == "LAST" ] || [ -z "$last_f" ]; then 
    make clean >& /dev/null
fi

cd $current_dir
