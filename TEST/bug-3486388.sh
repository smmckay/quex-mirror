#! /usr/bin/env bash
# PURPOSE: Prior to version 0.70.1, there were tremendous trouble using multiple
#          lexical analyzers in the same name space. The problems are avoided
#          completely with recent versions, due to the removal of macro code
#          generation.
# 
# Nevertheless, this test is left in place as a sample application using multiple analyzers.
bug=3486388
if [[ $1 == "--hwut-info" ]]; then
    echo "clemwang: $bug 0.61.2 Need better errmsg when incorrectly using 2 Lexers at once"
    exit
fi

tmp=`pwd`
cd $bug/ 
echo "Code Generation: Two lexers in the same name space"
quex --cbm -i simple.qx -o Otto  --language C
quex --cbm -i simple.qx -o Fritz --language C
echo "Compilation: No output is good output"
gcc  -c lexer.c >& tmp.txt -I.
cat tmp.txt | awk '(/[Ww][Aa][Rr][Nn][Ii][Nn][Gg]/ || /[Ee][Rr][Rr][Oo][Rr]/) && ! /ASSERTS/ ' | head -n 1
rm -rf tmp.txt Fritz* Otto*

# cleansening
make clean >& /dev/null
cd $tmp
