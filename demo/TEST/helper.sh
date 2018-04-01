source $HWUT_PATH/support/bash/hwut_unit.sh

function helper_diff {
    file=$1
    cmp_file=$2
    name=$3
    if [ -z "$cmp_file" ]; then cmp_file="$file"; fi

    result=$(diff -srqbB $file $cmp_file)
    if [[ "$result" =~ "identical" ]]; then
        echo "  [OK]   $name ($(wc $file -l | cut -f1 -d' ') lines)"
        let count++
    else
        echo "  [DIFF] $name"
    fi
}

function compare_QxFiles {
 for file in $(ls *.qx); do
    helper_diff $file 
 done
}

function compare_ExampleFiles {
 for file in $(ls example*.txt); do
    helper_diff $file 
 done
}

function compare_LexerFiles {
 function compare_ExampleFiles {
     for file in $(ls lexer*.c); do
         helper_diff $file $(echo $file | sed -e 's/\.c/\.cpp/')
     done
 }
}
