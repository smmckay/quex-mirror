# Some functions beginning with 'def'
def defined_not_used(X):
    undefined_not_used(X)

def defined_and_used(X):
    pass

defined_and_used(X)

# An unused function that must be found
def UnusedFunctionWhichNeedsToBeFound():
    """This function exists for the sole purpose to see whether it is found by 
    the script 'function-check.sh'. If not, the script does not work properly.
    """
    pass
