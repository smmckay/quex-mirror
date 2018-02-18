# Challenges with Buffer Size 5
# CHOICES: x, long-way-x, pc-x, pc-long-way-x, dtc-x, dtc-long-way-x;
# 
# PRE_X      --> lexeme of length two 'x'.
# PRE_LONG_X --> lexeme of length two 'x' preceeded by a long pre-context.
# *_POST     --> same with post context.
# *_DTC      --> same with dangerous trailing content. 
#
# (C) Frank-Rene Schaefer
#_____________________________________________________________________________
choice=$1

if [[ $choice == "--hwut-info" ]]; then
    echo "Challenges with Buffer Size 5;"
    echo "CHOICES: PRE_X, PRE_X_PC, PRE_X_DTC, PRE_LONG_X, PRE_LONG_X_PC, PRE_LONG_X_DTC;"
    exit
fi

if [ "$2" == "FIRST" ] || [ -z "$2"  ]; then 
    quex -i challenge-with-tiny-buffer-sizes.qx -o Simple --language C
    gcc -I$QUEX_PATH -I. lexer.c Simple.c -o lexer -DQUEX_SETTING_BUFFER_SIZE=5
fi

function test_this {
    mode="$1"
    content="$2"
    tmp=$(mktemp)
    echo "---------------------------------------------------------------------"
    echo "content: [$content]; mode: $mode;"
    echo
    printf "$content" > $tmp
    ./lexer $mode $tmp |& grep -v '^##'
    echo
    rm -f $tmp >& /dev/null
}

case $choice in
    x)     # lexeme of length 2
        test_this PRE_X "xx "
        test_this PRE_X " xx"
        test_this PRE_X "xx    "
        test_this PRE_X "     xx"
        test_this PRE_X "xx xx  xx   xx    xx"
    ;;
    dtc-x) # lexemes with a dangerous trailing context
        test_this PRE_X_DTC "xx "
        test_this PRE_X_DTC " xx"
        test_this PRE_X_DTC "xx    "
        test_this PRE_X_DTC "     xx"
        test_this PRE_X_DTC "xx xx  xx   xx    xx"
    ;;
    long-way-x) # long sequential pre-context
        test_this PRE_LONG_X "xxlong-way-back"
        test_this PRE_LONG_X "long-way-backxx"
        test_this PRE_LONG_X "xxlong-way-back"
        test_this PRE_LONG_X "long-way-backxx"
        ;;
    dtc-long-way-x) # lexemes with dangerous trailing context and long pre-context
        test_this PRE_LONG_DTC "xxlong-way-back"
        test_this PRE_LONG_DTC "long-way-backxx"
        test_this PRE_LONG_DTC "xxlong-way-back"
        test_this PRE_LONG_DTC "long-way-backxx"
        ;;
    pc-x) # lexemes with post context
        test_this PRE_X_PC "xy "
        test_this PRE_X_PC " xy"
        test_this PRE_X_PC "xy    "
        test_this PRE_X_PC "     xy"
        test_this PRE_X_PC "xy xy  xy   xy    xy"
        ;;
    pc-long-way-x) # lexemes with post context and long sequential pre-context
        test_this PRE_LONG_X_PC "xylong-way-back"
        test_this PRE_LONG_X_PC "long-way-backxy"
        test_this PRE_LONG_X_PC "xylong-way-back"
        test_this PRE_LONG_X_PC "long-way-backxy"
        ;;
esac

if [ "$3" == "LAST" ] || [ -z "$3" ]; then 
    rm -f Simple* ./lexer
fi


