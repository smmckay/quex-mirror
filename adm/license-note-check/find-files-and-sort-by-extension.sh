grep -L MIT . -r --exclude-dir .svn | while read line; do file=${line:1}; root=${file%.*}; ext="${file#"$root"}"; echo "'$ext'" $line; done | sort
