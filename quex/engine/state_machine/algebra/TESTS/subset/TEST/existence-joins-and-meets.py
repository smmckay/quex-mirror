import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])
from quex.engine.state_machine.core                 import StateMachine
from quex.engine.state_machine.algebra.TESTS.helper import test2, \
                                                           union, \
                                                           intersection, \
                                                           complement, \
                                                           identity, \
                                                           superset, \
                                                           sample_DFAs
import sys

if "--hwut-info" in sys.argv:
    print "Existence: Joins and Meets;"
    print "HAPPY: [0-9]+;"
    sys.exit()

count = 0

def join_and_meets(A, B):
    global count
    Join = union([A, B])    
    assert superset(Join, A)
    assert superset(Join, B)

    Meet = intersection([A, B])    
    assert superset(A, Meet)
    assert superset(B, Meet)
    count += 1

test2(join_and_meets)

print "<terminated: %i>" % count



