#! /usr/bin/env bash
# 
# PURPOSE: Compares Makefiles of the C and C++ Demo Applications.
#
# A minimal process is applied to unify the content of Makefiles for C and C++.
# Then, the content is compared. All demo application directories are checked.
#
# At the end of the file in comments it is shown how a single directory can be
# considered independently.
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________
source helper.sh

hwut_info $1 \
    "Demo Consistency: C and C++ Makefiles;\n" \
    "HAPPY: [0-9]+"

count=0
cpp_dir="../Cpp/"
c_dir="../C/"
demo_directories=$(ls ../C/[0-9][0-9]* -d | sort)

function compare_Makefiles {
    subdir=$1
    c_Makefile=$c_dir/$subdir/Makefile
    cpp_Makefile=$cpp_dir/$subdir/Makefile
    c_tmp=$(mktemp)
    cpp_tmp=$(mktemp)
    if [[ "$subdir" =~ "14" ]]; then
         cat $c_Makefile   | grep -v A_B_C | grep -ve '--token-class' > prepaded_C.txt
         cat $cpp_Makefile | grep -v A_B_C | grep -ve '--token-class' > prepaded_Cpp.txt
         c_Makefile=prepaded_C.txt
         cpp_Makefile=prepaded_Cpp.txt
    fi
    cat $c_Makefile   | grep -v A_B_C | sed -e 's/\.h//g' | sed -e 's/gcc/g++/g' | sed -e 's/\-\-language *C//g' > $c_tmp
    cat $cpp_Makefile | grep -v A_B_C | sed -e 's/\.\([chy]\)pp/\.\1/g' | sed -e 's/\.h//g' > $cpp_tmp
    helper_diff $c_tmp $cpp_tmp $subdir/Makefile
    rm -rf $c_tmp $cpp_tmp prepaded_Cpp.txt prepaded_C.txt
}

for subdir in $demo_directories; do compare_Makefiles $(basename $subdir); done
# echo "-- special --"
# compare_Makefiles 02-ModesAndStuff
echo "<terminated $count>"
