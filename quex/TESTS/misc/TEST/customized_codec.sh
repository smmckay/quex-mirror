#! /usr/bin/env bash

case $1 in
    --hwut-info)
        echo "Customized codec files (option --encoding-file);"
        ;;

    *)
        rm -f Simple*
        quex -i           customized_codec.qx  \
             --encoding-file customized_codec.dat \
             -o           Simple --debug-exception
        awk '/customized_codec/' Simple-*customized_codec*
        rm -f Simple*
        ;;
esac
