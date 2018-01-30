if [[ "$2" = "--hwut-info" ]]; then
   ./$1 --hwut-info
else
    tmp_file=$(mktemp)
    app=$1
    shift
    bash $QUEX_PATH/TEST/valgrindi.sh $tmp_file ./$app "$@" | grep -v '^##'
    cat $tmp_file | grep -v '^##'
    rm -f $tmp_file
fi
