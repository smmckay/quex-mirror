function build {
    target=$1
    asserts_f=$2
    first_f=$3
    if [ "$first_f" == "FIRST" ] || [ -z "$first_f"  ]; then 
        make clean >& /dev/null
    fi
    if [ "$asserts_f" == "no-asserts" ]; then 
        $add_flags=-DQUEX_OPTION_ASSERTS_DISABLED
    fi
    make $target ADD_FLAGS="$add_flags"
}

function run {
    app=$1
    bash $QUEX_PATH/TEST/valgrind-executer.sh $app |& grep -v '^##'
}

function clean {
    last_f=$1
    if [ "$last_f" == "LAST" ] || [ -z "$last_f" ]; then 
        make clean >& /dev/null
    fi
}

