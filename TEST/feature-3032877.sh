#! /usr/bin/env bash
bug=3032877
if [[ $1 == "--hwut-info" ]]; then
    echo "alexeevm: $bug -b, --buffer-element-size enhancement"
    # One converter is enough to test here
    echo "CHOICES: normal, codec;"
    exit
fi

case $1 in
    normal) converter="";;
    codec)  converter="--encoding utf8";;
esac

tmp=`pwd`
cd $bug/ 

function perform_test() {
    echo "_____________________________________________________________________"
    echo "ARGUMENT_LIST: $argument_list"
    echo
    quex -i simple.qx -o EasyLexer $argument_list # --debug-exception
    cd EasyLexer
    if [ -e EasyLexer-configuration ]; then
        awk ' /_lexatom_t/ && /typedef/ ' EasyLexer-configuration \
            >& tmp.txt
        cat tmp.txt
        rm -f tmp.txt
    else
        echo "File EasyLexer-configuration does not exist."
    fi
    cd ..
    rm -rf EasyLexer*
    rm -rf Lexer*
    echo
}

for option in {u8,u16,u32,uint8_t,uint16_t,uint32_t,wchar_t,UChar}; do
    argument_list="--bet $option $converter"
    perform_test
done

argument_list="--bet $option $converter"
perform_test

if [[ $1 == "codec" ]]; then
    for bes in {1,2}; do
        argument_list="--bet $option $converter -b $bes"
        perform_test
    done
fi

cd $tmp
