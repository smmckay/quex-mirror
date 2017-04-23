# PURPOSE: The analyzer class depends on a template for C and C++. Check that
#          the main data members are exactly the same.
#
# Files under consideration:
#
#            $QUEX_PATH/quex/code_base/analyzer/TXT-C
#            $QUEX_PATH/quex/code_base/analyzer/TXT-Cpp
#
# The sections from those files which are extracted are surrounded by markers:                
#
#  "__( Data Members )_______________________________________________________"
#  "__( END: Data Members )__________________________________________________"
#
# The content in between those markes is compared in this test.
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________

if [[ "$1" = "--hwut-info" ]]; then
    echo "Main data member consistency for C and C++;"
    exit
fi
tmpC=$(mktemp)
tmpCpp=$(mktemp)

awk -e 'BEGIN{ok=0} / Data Members \)/ { ok = !ok; } { if(ok) { print; } }'  \
    $QUEX_PATH/quex/code_base/analyzer/TXT-C > $tmpC

awk -e 'BEGIN{ok=0} / Data Members \)/ { ok = !ok; } { if(ok) { print; } }'  \
    $QUEX_PATH/quex/code_base/analyzer/TXT-Cpp > $tmpCpp

echo "(*) Check: extracted content != 0  (else verdict 'same' is meaningless)"
wc $tmpC -l   | cut -f 1 -d ' '
wc $tmpCpp -l | cut -f 1 -d ' '

echo "(*) Check: content same?"
diff -srq $tmpC $tmpCpp \
     | awk '/identical/ { print "identical"; } ! /identical/ { print "differ"; }'
