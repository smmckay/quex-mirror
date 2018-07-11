#! /usr/bin/env bash
case $1 in
    --hwut-info)
        echo "Respect max. recursion depth upon base mode inclusion."
        ;;

    *)
        echo "No output is good output:"
        quex --cbm -i huge-inheritance.qx -o Simple \
             --debug-limit-recursion 64 \
             --debug-exception
        echo "<terminated>"
        rm Simple*
        ;;
esac
