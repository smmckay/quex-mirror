#! /usr/bin/env bash
bug=299
if [[ $1 == "--hwut-info" ]]; then
    echo "patrikj-kt: $bug LoopRestartP -- generated code does not compile"
    echo "CHOICES: original, with-derivation, without-derivation;"
    exit
fi

tmp=`pwd`
pushd $bug/ >& /dev/null

case $1 in
    original)           app=lexer;   file=example.txt; ;;
    with-derivation)    app=with;    file=minimal.txt; ;;
    without-derivation) app=without; file=minimal.txt; ;;
esac

make $app >& tmp.txt
cat tmp.txt | awk '(/[Ww][Aa][Rr][Nn][Ii][Nn][Gg]/ || /[Ee][Rr][Rr][Oo][Rr]/) && ! /ASSERTS/ '
rm tmp.txt
bash ../valgrindi.sh tmp.txt ./$app $file
rm -rf with without lexer Simple 
cat tmp.txt
rm tmp.txt

popd >& /dev/null
