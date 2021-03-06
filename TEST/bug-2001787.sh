#! /usr/bin/env bash
bug=2001787
if [[ $1 == "--hwut-info" ]]; then
    echo "attardi: $bug RE Problem with inverted whitespace"
    echo "CHOICES: iconv, icu;"
    echo "HAPPY: cpp:[0-9]+:;"
    exit
fi

echo "** Please note, that '.' in an RE stands for 'anything but newline'   **"
echo "** Thus, it does not match newline, and the lexer triggers on newline **"
echo "** to the default terminal.                                           **"
tmp=`pwd`
cd $bug/ 

if [ "$2" == "FIRST" ] || [ -z "$2"  ]; then 
    make clean
fi

make lexer-$1  >& /dev/null
./lexer-$1 example.txt 2> tmp.txt
cat tmp.txt
rm -f tmp.txt

# cleansening
if [ "$3" == "LAST" ] || [ -z "$3" ]; then 
   make clean
fi

cd $tmp
