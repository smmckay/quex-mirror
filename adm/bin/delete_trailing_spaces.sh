for file in $(find -name "*.py"); do sed -i $file -e's/[ \t]*$//'; done
