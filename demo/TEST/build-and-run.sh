source $HWUT_PATH/support/bash/hwut_unit.sh

function bar_build {
    target=$1
    asserts_f=$2
    first_f=$3

    if [ "$asserts_f" == "no-asserts" ]; then 
        add_flags="-DQUEX_OPTION_ASSERTS_DISABLED"
    fi

    bash $QUEX_PATH/TEST/call-make.sh $target "ADD_FLAGS=$add_flags" 
}

function bar_run {
    app=$1
    asserts_f=$2
    shift; shift
    remainder="$*"

    bash $QUEX_PATH/TEST/valgrindi.sh tmp-log.txt ./$app $remainder > tmp-out.txt
    bar_check_assert_activation "$asserts_f" tmp-out.txt

    cat tmp-out.txt | grep -v '^##'
    cat tmp-log.txt 
    rm -f tmp-out.txt tmp-log.txt 
}

function bar_clean {
    make clean >& /dev/null
}

function bar_check_assert_activation {
    asserts_f=$1
    out_file=$2
    # Tracks the output of the lexer for the warning of 'asserts activated'.
    # => Determine whether this fits with the requirement of the test.

    asserts_active=$(grep -sHIne QUEX_OPTION_ASSERTS $out_file)
    if [ -z "$asserts_active" ]; then
        # Asserts were inactive
        if [ "$asserts_f" == "asserts" ]; then
            echo "Asserts not activated in generated lexer."
            exit
        fi
    else
        # Asserts were inactive
        if [ "$asserts_f" == "no-asserts" ]; then
            echo "Asserts not activated in generated lexer."
            exit
        fi
    fi
}
