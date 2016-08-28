# Unit test for different demos. This is the core file
# All tests follow this structure.
#
#   $1     directory where to find the makefile
#   $2, $3 arguments passed to the makefile
#
# See 000.sh, 001.sh, 002,sh for examples of tests based on this.
# 
# (C) 2006 Frank-Rene Schäfer
#
#______________________________________________________________________
cd $QUEX_PATH/demo/Cpp/$1 
if [[ $2 == "NDEBUG" ]]; then
    arg1=""
else
    arg1="ASSERTS_ENABLED_F=YES"
fi
echo "makefile =" Makefile
echo "cleaning ..."
make clean   >& /dev/null
echo "make $arg1 $3 ##"
make  $arg1 $3 >& tmp.txt
cat tmp.txt | awk '(/[Ww][Aa][Rr][Nn][Ii][Nn][Gg]/ || /[Ee][Rr][Rr][Oo][Rr]/) && ! /ASSERTS/ && ! /deprecated since quex/ && ! /QUEX_ERROR_EXIT/ && ! /QUEX_ERROR_DEPRECATED/'
rm tmp.txt
echo "executing ..."
if [[ -z $application ]]; then
    if [[ $no_valgrind != "YES" ]]; then
        $QUEX_PATH/TEST/valgrindi.sh stdout.txt ./lexer $args_to_lexer
        cat stdout.txt
    else
        ./lexer $args_to_lexer
    fi
else
    if [[ $no_valgrind != "YES" ]]; then
        $QUEX_PATH/TEST/valgrindi.sh stdout.txt ./lexer $args_to_lexer
        cat stdout.txt
    else
       $application $args_to_lexer
    fi
fi
rm -f stdout.txt
rm -f tmp.txt
echo "cleaning ..."
make clean   >& /dev/null

