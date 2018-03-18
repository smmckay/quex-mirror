#! /usr/bin/env bash
if [[ "$1" == "--hwut-info" ]]; then
    echo "List all GOOD files which are identical;"
    exit
fi

pushd ../C/TEST/GOOD > /dev/null

echo "List off differing files: (no output is good output)"
echo
count=0
for file in *.txt; do 
    if [[ "$file" =~ "no-references-to-cpp" ]]; then 
        continue; 
    fi
    result=$(diff -srqbB $file ../../../Cpp/TEST/GOOD/$file)
    if [[ "$result" =~ "identical" ]]; then
        let count++
    else
        echo "File: $file differs!"
    fi    
done | sort 
echo
echo "<terminated: $count>"

popd >& /dev/null
