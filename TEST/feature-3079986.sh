#! /usr/bin/env bash
bug=3079986
if [[ $1 == "--hwut-info" ]]; then
    echo "rmanoj-oss: $bug Allow namespace delimiter in --token-id-prefix for C++"
    echo "CHOICES: nnn, nnc, ncc, ccc;"
    echo "SAME;"
    exit
fi

tmp=`pwd`
cd $bug/ 

testcase=$1

make clean
make check   TESTCASE=$testcase
make compile TESTCASE=$testcase
make clean

cd $tmp
