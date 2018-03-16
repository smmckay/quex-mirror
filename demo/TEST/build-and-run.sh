source $HWUT_PATH/support/bash/hwut_unit.sh

function bar_build {
    target=$1
    asserts_f=$2  # 'no-asserts' => disable asserts
    #             # 'asserts'    => leave asserts enabled
    shift; shift; shift;
    make_flags="$@"

    if [ "$asserts_f" == "no-asserts" ]; then 
        add_flags="-DQUEX_OPTION_ASSERTS_DISABLED"
    elif [ "$asserts_f" == "asserts" ]; then  
        add_flags=""
    fi

    echo "[$target] [$add_flags] [$make_flags]"
    bash $QUEX_PATH/TEST/call-make.sh $target "ADD_FLAGS=$add_flags" $make_flags
    # make $target "ADD_FLAGS=$add_flags" $make_flags
}

function bar_run {
    app=$1
    asserts_f=$2
    shift; shift
    remainder="$@"

    ## echo "#run: [$app][$asserts_f][$remainder]"

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
            echo "Error: asserts not activated in generated lexer."
            exit
        fi
    else
        # Asserts were active
        if [ "$asserts_f" == "no-asserts" ]; then
            echo "Error: asserts activated in generated lexer."
            exit
        fi
    fi
}

function bar_build_always_and_run {
    directory=$1
    app=$2
    asserts_f=$3  # 'asserts/no-asserts'

    pushd $directory >& /dev/null

    # Clean always, because there is w/ and wo/ 'asserts'
    bar_clean 
    bar_build $app "$asserts_f" 
    bar_run   $app 
    bar_clean 

    popd >& /dev/null
}

function bar_build_and_run {
    directory=$1
    asserts_f=$2
    first_f=$3
    last_f=$4
    shift; shift; shift; shift;
    command_line_arguments="$@"

    pushd $directory >& /dev/null

    hwut_if_first $first_f "make clean_lexer"
    bar_build lexer "$asserts_f" "$command_line_arguments"
    bar_run   lexer 
    hwut_if_last $last_f "make clean_lexer"

    popd >& /dev/null
}

function bar_build_and_run_this {
    directory=$1
    asserts_f=$2
    first_f=$3
    last_f=$4
    app=$5
    shift; shift; shift; shift; shift;
    command_line_arguments="$@"

    pushd $directory >& /dev/null

    hwut_if_first "$first_f" "make clean_$app"
    bar_build     "$app"     "$asserts_f" 
    bar_run       "$app"     "$asserts_f" $command_line_arguments
    hwut_if_last  "$last_f"  "make clean_$app"

    popd >& /dev/null
}
