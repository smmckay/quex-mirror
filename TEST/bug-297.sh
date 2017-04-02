#! /usr/bin/env bash
bug=297
if [[ $1 == "--hwut-info" ]]; then
    echo "fschaef: $bug r4678(trunk): Memory leak in Token Class;"
    echo "CHOICES: C, Cpp;"
    echo "SAME;"
    exit
fi

tmp=`pwd`
cd $bug/ 

includes="-I$QUEX_PATH/quex/code_base/extra/test_environment/ -I$QUEX_PATH"
defines="-DQUEX_OPTION_TOKEN_POLICY_SINGLE -DQUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER"
case $1 in
    Cpp)
        sources="lexer.cpp $QUEX_PATH/quex/code_base/extra/test_environment/TestAnalyzer-dummy.cpp"
        g++ $includes $defines $sources -o lexer  
        ;;
    C)
        sources="lexer.c $QUEX_PATH/quex/code_base/extra/test_environment/TestAnalyzer-dummy.c"
        gcc $includes $defines -D__QUEX_OPTION_PLAIN_C $sources -o lexer  
        ;;
esac

bash ../valgrindi.sh tmp.txt ./lexer
rm  -f lexer
cat tmp.txt
rm  tmp.txt

cd $tmp
