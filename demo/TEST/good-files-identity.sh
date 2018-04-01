#! /usr/bin/env bash
if [[ "$1" == "--hwut-info" ]]; then
    echo "List all GOOD files which are identical;"
    exit
fi

pushd ../C/TEST/GOOD > /dev/null

echo "List off differing files: (no output is good output)"
echo
for file in *.txt; do 
    if [[ "$file" =~ "no-references-to-cpp" ]]; then 
        continue; 
    fi
    # Special treatment of 'command line' where 'getline()' in C delivers an
    # extra newline character. C++ does not.
    if [[ "$file" =~ "10-SocketsAndTerminal.sh--command-line" ]]; then
        result=$(diff $file ../../../Cpp/TEST/GOOD/$file | grep -e 'VALGRIND|WHITESPACE|read|---|[0-9cd]+')
        if [ -z "$result" ]; then
            result="identical"
        fi
    else
        result=$(diff -srqbB $file ../../../Cpp/TEST/GOOD/$file)
    fi

    if [[ "$result" =~ "identical" ]]; then
        echo "[OK]      $file"
    else
        echo "[DIFFERS] $file"
    fi    

done | sort 
echo
echo "<terminated>"

popd >& /dev/null
