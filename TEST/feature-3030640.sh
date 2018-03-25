#! /usr/bin/env bash
bug=3030640
if [[ $1 == "--hwut-info" ]]; then
    echo "ymarkovitch: $bug 0.50.1 Adding .hpp extension to generated headers"
    echo "CHOICES: pp, ++, xx, cc, PlainC, PlainCpp, ErrorC, ErrorCpp;"
    exit
fi

tmp=`pwd`
cd $bug/ 

if [[ $1 == "PlainC" ]]; then
    quex -i simple.qx --language C --debug-exception -o Lexer
elif [[ $1 == "ErrorC" ]]; then
    quex -i simple.qx --language C --fes foo -o Lexer # --debug-exception
elif [[ $1 == "PlainCpp" ]]; then
    quex -i simple.qx -o Lexer
elif [[ $1 == "ErrorCpp" ]]; then
    quex -i simple.qx --fes foo -o Lexer
else
    quex -i simple.qx --fes $1 -o Lexer --debug-exception
fi

# Display the generated files
cd Lexer
echo "||||"
ls Lexer* 
echo "||||"
cd ..

rm -rf Lexer*

cd $tmp
