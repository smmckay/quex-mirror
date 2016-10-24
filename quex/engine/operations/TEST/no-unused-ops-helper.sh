# Helper script for 'no-unused-ops.py'
all_content=$(mktemp)
file_list=$(find $QUEX_PATH . -name "*.py" | grep -v '\bTEST\b' )
sed -e 's/#.*$//' $file_list > $all_content

echo "No output is good output"
shift
for value in "$@"; do
    count=$(grep -c "\bOp\.$value(" $all_content)
    echo "## $value $count"
    if [ "$count" -lt "1" ]; then
        echo "ERROR: Op $value has not been used anymore!"
    fi
done

rm -f $all_content
