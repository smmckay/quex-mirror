# One might want to fill 'tmp.txt' with a dedicated list of files
# to be subject to replacement. Then set $3 to --my-tmp-txt
echo "$1 --> $2"
if [[ $3 != "--my-tmp-txt" ]]; then
   grep -sle "$1" . -r --exclude-dir .svn > tmp.txt
fi
echo "Files:"
rm -f tmp.sh
source=$(echo $1 | sed -e 's/\//\\\//g' | sed -e 's/\./\\./g' | sed -e 's/\-/\\-/g')
replacement=$(echo $2 | sed -e 's/\//\\\//g' | sed -e 's/\./\\./g' | sed -e 's/\-/\\-/g')
for file in `cat tmp.txt`; do 
    echo "   $file";  
    echo "perl -pi.bak -e 's/$source/$replacement/g' $file" \
         | sed -e 's/(/\\(/g'                \
         | sed -e 's/)/\\)/g' >> tmp.sh
done
bash tmp.sh
for file in `cat tmp.txt`; do rm -f $file.bak;  done
#rm -f tmp.txt tmp.sh
