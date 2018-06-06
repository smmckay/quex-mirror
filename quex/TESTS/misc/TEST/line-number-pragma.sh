#! /usr/bin/env bash

if [ "$2" == "FIRST" ] || [ -z "$2"  ]; then 
    quex -i line-number-pragma.qx -o LineNumberPragma
fi

file_list='LineNumberPragma LineNumberPragma-token LineNumberPragma.cpp'
cd LineNumberPragma

case $1 in
    --hwut-info)
        echo "Testing the implementation of line number pragmas;"
        echo "CHOICES: qx, source;"
        echo "HAPPY:   :[0-9]+:;"
        exit;
        ;;

    qx)
        echo __________________________________________________________________
        echo Pragmas from within .qx file
        echo
        tmp_file=$(mktemp)
        cat $file_list > $tmp_file
        grep -sHIne '# *line' $tmp_file | grep -soe '[0-9]\+ \+\"line-number-pragma.qx\"' | sort -nu;
        rm -f $tmp_file
        ;;

    source)
        echo __________________________________________________________________
        echo Pragmas to set-back the file internal line numbers.
        echo
        for file in $file_list; do
            echo $file
            # * Extract line number pragmas about the file itself!
            #              OUTPUT: => file:N: #line M "file"
            # * Delete everything except N and M of each line
            #              OUTPUT: => N M
            # * Ensure that:
            #              N = M - 1
            # * No output is good output
            echo "   <no output is good output/print only errors>"
            grep -sHIne "# *line \+[0-9]\+ \+\"LineNumberPragma/$file\"" $file \
            | sed -e "s/$file//g" \
            | sed -e "s/line//g"  \
            | tr -d "\"#:"        \
            | awk 'BEGIN { n = 0; } { n += 1; if( $1 != $2 ) print $1 "!=" $2 "- 1"; } END { print "   count: " n; }'
        done
        
        ;;
esac

echo __________________________________________________________________
cd ..
if [ "$3" == "LAST" ] || [ -z "$3" ]; then 
    # echo "Do not forget to 'remove'"
    rm -rf LineNumberPragma*
fi
echo "<terminated>"
