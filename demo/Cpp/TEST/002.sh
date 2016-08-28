#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "demo/002: Indentation Based Scopes"
    echo "CHOICES:  NDEBUG, DEBUG, customized;"
    echo "HAPPY:    [0-9]+;"
    echo "SAME;"
    exit
fi

case $1 in 
    NDEBUG-customized)
        cd ../002
        make clean lexer2 >& /dev/null
        $QUEX_PATH/TEST/valgrindi.sh ./lexer2 example2.txt 
        cat valgrind.log; rm -f valgrind.log
        rm -f tmp.txt
        ;;
    *)
        source core-new.sh 002 $2 $3 $1
esac

