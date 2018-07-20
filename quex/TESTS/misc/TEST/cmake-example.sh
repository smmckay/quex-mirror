#! /usr/bin/env bash
case $1 in
    --hwut-info)
        echo "Run with --config-by-cmake;"
        echo "HAPPY: [0-9]+;"
        ;;

    *)
        quex --cbcm -i cmake-example.qx -o Simple \
             --path-compression \
             --template-compression \
             --language C --debug-exception 
        cat Simple/Simple-configuration.h.in | grep -shoe '@[a-zA-Z0-9_]\+@' | sort 
        rm -rf Simple
        ;;
esac

