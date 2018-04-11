# "--my-tmp-txt" => user provides a list of files to be replaced in 'tmp.txt'.
# "--no-word-boundaries" => do not adapt to word boundaries.
# One might want to fill 'tmp.txt' with a dedicated list of files
# to be subject to replacement. Then set $3 to --my-tmp-txt
echo "$1 --> $2"
rm -f tmp.sh

source=$(echo $1 | sed -e 's/\//\\\//g' | sed -e 's/\./\\./g' | sed -e 's/\-/\\-/g')
replacement=$(echo $2 | sed -e 's/\//\\\//g' | sed -e 's/\./\\./g' | sed -e 's/\-/\\-/g')

if [[ $@ == **"--no-word-boundaries"** ]]; then
    echo "Word boundaries disabled."
    search=$source
else
    echo "Word boundaries enabled."
    search="\b$source\b"
fi
if [[ $@ != **"--my-tmp-txt"** ]]; then
   grep -sle "$search" . -r --exclude-dir .svn > tmp.txt
fi

echo "Files:"
for file in `cat tmp.txt`; do 
    echo "   $file";  
    echo "perl -pi.bak -e 's/$search/$replacement/g' $file" \
         | sed -e 's/(/\\(/g'                \
         | sed -e 's/)/\\)/g' >> tmp.sh
done
bash tmp.sh
for file in `cat tmp.txt`; do rm -f $file.bak;  done
#rm -f tmp.txt tmp.sh
