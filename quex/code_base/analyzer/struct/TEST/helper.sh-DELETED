if [[ "$2" = "--hwut-info" ]]; then
   ./$1 --hwut-info
else
    valgrind --leak-check=full ./$1 $2 \
        |& awk ' /terminated/ || /possible/ || /still reachable/ || /ERROR SUMMARY/ ' \
        | tr -d = \
        | sed -e 's/^[0-9]\+//g'
fi
