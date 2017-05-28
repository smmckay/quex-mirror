#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "00-Minimalist;"
    exit
fi
cd ../00-Minimalist/
make       >  /dev/null
./lexer
make clean >& /dev/null
