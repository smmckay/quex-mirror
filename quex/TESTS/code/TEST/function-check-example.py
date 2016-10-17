# Some functions beginning with 'def'
def BAD_defined_but_not_used(X):
    undefined_not_used(X)

def GOOD_defined_and_called(X):
    pass

def GOOD_defined_and_used_as_callback(X):
    pass

def GOOD_defined_and_used_on_same_line_as_definition(X):
    pass

def GOOD_function(X): return GOOD_defined_and_used_on_same_line_as_definition(X)

GOOD_defined_and_called(X)
function(x, GOOD_defined_and_used_as_callback, z)
GOOD_function(X)

# An unused function that must be found
def UnusedFunctionWhichNeedsToBeFound():
    """This function exists for the sole purpose to see whether it is found by 
    the script 'function-check.sh'. If not, the script does not work properly.
    """
    pass
