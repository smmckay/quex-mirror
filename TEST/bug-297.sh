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

rm -rf lexerCpp lexerC

case $1 in
    Cpp) make lexerCpp 
         bash ../valgrindi.sh tmp.txt ./lexerCpp
         ;;
    C)   make lexerC 
         bash ../valgrindi.sh tmp.txt ./lexerC
         ;;
esac

rm -rf lexerCpp lexerC

cat tmp.txt
rm  tmp.txt

cd $tmp
