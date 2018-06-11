#! /usr/bin/env bash
#
bug=2095970
if [[ $1 == "--hwut-info" ]]; then
    echo "sphericalcow: $bug 0.31.3 Mode change without immediate return"
    echo "CHOICES: CONTINUE_w_Asserts, CONTINUE, RETURN_w_Asserts, RETURN, DEFAULT_w_Asserts, DEFAULT;"
    echo "HAPPY:   Simple.cpp:[0-9]+:;"
    exit
fi

tmp=`pwd`
cd $bug/ 
make clean >& /dev/null


case $1 in 
    CONTINUE_w_Asserts)
    echo "The sequence of tokens is supposed to be messed up!"
    echo "Assertion is supposed to trigger!"
    make EXT_MODE_FILE=CONTINUE.qx                  >& /dev/null
    ./lexer
    make clean
    cd $tmp
    exit
    ;;
    CONTINUE)
    echo "The sequence of tokens is supposed to be messed up!"
    make EXT_MODE_FILE=CONTINUE.qx                  \
         EXT_CFLAGS=-DQUEX_OPTION_ASSERTS_EXT_DISABLED_EXT  >& /dev/null
    ;;
    RETURN_w_Asserts)
    make EXT_MODE_FILE=RETURN.qx                    >& /dev/null
    ;;
    RETURN)
    make EXT_MODE_FILE=RETURN.qx                    \
         EXT_CFLAGS=-DQUEX_OPTION_ASSERTS_EXT_DISABLED_EXT  >& /dev/null
    ;;
    DEFAULT_w_Asserts)
    make EXT_MODE_FILE=DEFAULT.qx                   >& /dev/null
    ;;
    DEFAULT)
    make EXT_MODE_FILE=DEFAULT.qx                   \
         EXT_CFLAGS=-DQUEX_OPTION_ASSERTS_EXT_DISABLED_EXT  >& /dev/null
    ;;
esac

bash ../valgrindi.sh tmp.txt ./lexer 
cat tmp.txt
rm tmp.txt
# cleansening
make clean
cd $tmp
