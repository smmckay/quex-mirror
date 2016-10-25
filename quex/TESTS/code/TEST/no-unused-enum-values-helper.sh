# Helper script for 'no-unused-ops.py'
all_content=$(mktemp)
file_list=$(find $QUEX_PATH . -name "*.py")
sed -e 's/#.*$//' $file_list > $all_content

shift
echo "-- $1: No output is good output --"
shift
for value in "$@"; do
    count=$(grep -c "\b$value\b" $all_content)
    echo "## $value $count"
    if [ "$count" -lt "1" ]; then
        echo "ERROR: $value has not been used anymore!"
    fi
done

rm -f $all_content
