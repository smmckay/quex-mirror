if [[ "$2" = "--hwut-info" ]]; then
   ./$1 --hwut-info
else
    echo "||||"
    valgrind ./$1 $2 \
        |& awk ' /terminated/ || /possible/ || /still reachable/ ' \
        | tr -d = \
        | sed -e 's/^[0-9]\+//g'
    echo "||||"
fi
