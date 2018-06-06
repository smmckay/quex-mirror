#! /usr/bin/env bash

case $1 in
    --hwut-info)
        echo "Customized codec files (option --encoding-file);"
        ;;

    *)
        rm -rf Simple*
        quex -i              customized_codec.qx  \
             --encoding-file customized_codec.dat \
             -o              Simple --debug-exception
        awk '/_lexeme_/' Simple/converter-from-lexeme
        rm -rf Simple*
        ;;
esac
