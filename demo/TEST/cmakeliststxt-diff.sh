#! /usr/bin/env bash
# 
# PURPOSE: Compares CMakeLists.txts of the C and C++ Demo Applications.
#
# A minimal process is applied to unify the content of CMakeLists.txts for C and C++.
# Then, the content is compared. All demo application directories are checked.
#
# At the end of the file in comments it is shown how a single directory can be
# considered independently.
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________
source helper.sh

hwut_info $1 \
    "Demo Consistency: C and C++ CMakeLists.txt-s;\n" \
    "HAPPY: [0-9]+"

count=0
cpp_dir="../Cpp/"
c_dir="../C/"
demo_directories=$(ls ../C/[0-9][0-9]* -d | sort)
## demo_directories=$(echo ../C/14*)                       ## DEBUG: uncomment this.

function compare_CMakeListsTxts {
    subdir=$1
    c_CMakeListsTxt=$c_dir/$subdir/CMakeLists.txt
    cpp_CMakeListsTxt=$cpp_dir/$subdir/CMakeLists.txt
    c_tmp=$(mktemp)
    cpp_tmp=$(mktemp)
    if [[ "$subdir" =~ "14" ]]; then
         cat $c_CMakeListsTxt   | grep -v A_B_C | grep -ve '--token-class' > prepaded_C.txt
         cat $cpp_CMakeListsTxt | sed -e 's/max\/Lexer/max\/max/g'  \
                           | sed -e 's/moritz\/Lexer/moritz\/moritz/g'  \
                           | sed -e 's/boeck\/Lexer/boeck\/boeck/g'  \
                           | grep -v A_B_C | grep -ve '--token-class' \
                           | sed -e 's/::/_/g'                             > prepaded_Cpp.txt
         c_CMakeListsTxt=prepaded_C.txt
         cpp_CMakeListsTxt=prepaded_Cpp.txt
    fi
    if [[ "$subdir" =~ "13" ]]; then
         cat $cpp_CMakeListsTxt | sed -e 's/lexer:://g' > prepaded_Cpp.txt
         cpp_CMakeListsTxt=prepaded_Cpp.txt
    fi
    cat $c_CMakeListsTxt   | grep -v A_B_C | sed -e 's/\.h//g' | sed -e 's/gcc/g++/g' | sed -e 's/\-\-language *C//g' > $c_tmp
    cat $cpp_CMakeListsTxt | grep -v A_B_C | sed -e 's/\.\([chy]\)pp/\.\1/g' | sed -e 's/\.h//g' > $cpp_tmp
    helper_diff $c_tmp $cpp_tmp $subdir/CMakeLists.txt

    rm -rf $c_tmp $cpp_tmp prepaded_Cpp.txt prepaded_C.txt ## DEBUG: comment this
    ## echo $c_tmp $cpp_tmp                                ## DEBUG: uncomment this.
}

for subdir in $demo_directories; do compare_CMakeListsTxts $(basename $subdir); done
echo "<terminated $count>"
