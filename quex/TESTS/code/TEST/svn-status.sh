# PURPOSE: Check that there are no (not too many) trailing files which
#          are not under SVN source control.
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________

if [[ "$1" = "--hwut-info" ]]; then
    echo "Checking SVN status;"
    exit
fi

original_dir=$PWD
example=file-that-must-be-detected-as-not-under-source-control.txt

date > $example

cd $QUEX_PATH
hwut make clean    >& /dev/null

cd $QUEX_PATH/demo
bash make_clean.sh >& /dev/null

cd $QUEX_PATH
echo "Almost no output is good output:"
svn status \
| grep '^?' \
| awk ' ! /quex\/engine\/analyzer\/examine\/doc\// && ! /demo\/C\/000\/CMakeLists.txt/'

cd $original_dir
rm -f $example

echo "<terminated>"
