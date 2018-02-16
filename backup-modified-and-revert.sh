for file in $(svn status | grep '^M' | cut -f8-20 -d' '); do 
    echo $file
    cp $file $file-modified; 
done
svn revert -R . >& /dev/null
