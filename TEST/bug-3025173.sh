#! /usr/bin/env bash
bug=3025173
if [[ $1 == "--hwut-info" ]]; then
    echo "alexeevm: $bug 0.49.2 Custom Token struct for quex"
    echo "HAPPY: :[0-9]+:"
    exit
fi

tmp=`pwd`
cd $bug/ 

make clean >& /dev/null

echo "(1) Generate 'OK-Sources' and Compile"
make check | bash ../quex_pathify.sh

./check

make clean >& /dev/null

echo "(2) Mix member assignments with manually written token class."
make mixMemberAssignWithManualTokenClass
make clean >& /dev/null

echo "(3) Provide a 'token_type' definition together with a manually written class."
make tokenTypeAlongWithManualTokenClass
make clean >& /dev/null

echo "(4) Manually written token class without '--token-class' definition"
make tokenTypeWithoutTokenClassSpecification
make clean >& /dev/null

cd $tmp
