#! /usr/bin/env bash
# 
# PURPOSE: Compares Build Results of the C and C++ Demo Applications.
#
# Compare the build results of Makefile-s and CMakeLists.txt-files.
# Both must produce the exact same applications.
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________
source helper.sh

hwut_info $1 \
    "Demo Consistency: Same build results Makefile vs. CMakeLists.txt;\n" \
    "HAPPY: [0-9]+"


function find_executables {
    for file in $(find  -maxdepth 1 -type f -executable); do
        basename $file
    done | sort -bd | tr '\n' ' '
}

function compare_build_results { directory=$1
    pushd $directory         >& /dev/null
    make $(find_executables) >& /dev/null
    make all -j 1024         >& /dev/null
    MAKE_results=$(find_executables)

    rm -rf build
    mkdir build  >& /dev/null
    cd build     >& /dev/null
    cmake ..     >& /dev/null
    make -j 1024 >& /dev/null
    CMAKE_results=$(find_executables)
    
    if [[ "$MAKE_results" != "$CMAKE_results" ]]; then
        echo "[FAIL] $directory"
        echo "       ($MAKE_results) <-> ($CMAKE_results)" 
    else
        good=true
        for app in $CMAKE_results; do
            if [[ -z "$(diff $app ../$app)" ]]; then
                echo "[FAIL] $directory"
                echo "       $app <-> ../$app"
                good=false
            fi
        done
        if [[ "$good" = "true" ]]; then
            echo "[OK]   $directory ($CMAKE_results)"
        fi
    fi
    popd  >& /dev/null
}

function iterate { base_dir=$1
    echo "-- $base_dir -----------------------------------------------------"
    echo
    pushd ../$base_dir >& /dev/null
    # demo_directories=$(ls 04* -d | sort)
    demo_directories=$(ls [0-9][0-9]* -d | sort)
    for subdir in $demo_directories; do 
        compare_build_results $(basename $subdir); 
    done
    popd >& /dev/null
    echo
}

count=0
iterate C
iterate Cpp

echo "<terminated $count>"
