file=$1
license_header_file=$2

tmp=$(mktemp)

shebang_f=0
done_f=false

cat $file | while read line; do 
    echo "[$line]"
    if [[ "$line" == "#!"* ]]; then 
        echo "<<$line>>"
    elif [ "$done_f" = false ]; then
        cat $license_header_file 
        done_f=true
    else
        echo $line 
    fi
done # > $tmp

cat $tmp

rm $tmp -f
