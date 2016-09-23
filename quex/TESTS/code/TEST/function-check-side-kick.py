# HELPER printing a 'grep exression' for each unused function that has been
# found by 'function-check.sh'
#
# Redirect the output of 'function-check.sh' to this script in order to get
# compile-like lines jumping to the definition of unused functions.
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________

import sys
for line in open(sys.argv[1]).readlines():
    print "grep -sHIne '\\b%s(' -r --include \"*.py\""


def UnusedFunctionWhichNeedsToBeFound():
    """This function exists for the sole purpose to see whether it is found by 
    the script 'function-check.sh'. If not, the script does not work properly.
    """
    pass
