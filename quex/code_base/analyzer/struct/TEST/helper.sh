if [[ "$2" = "--hwut-info" ]]; then
   ./$1 --hwut-info
else
   ./$1 $2 |& awk ' /terminated/ ' 
fi
