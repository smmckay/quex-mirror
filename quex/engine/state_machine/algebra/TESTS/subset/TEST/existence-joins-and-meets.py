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
    Join = union([A.clone(), B.clone()])    
    assert superset(Join.clone(), A.clone())
    assert superset(Join.clone(), B.clone())

    Meet = intersection([A.clone(), B.clone()])    
    assert superset(A.clone(), Meet.clone())
    assert superset(B.clone(), Meet.clone())
    count += 1

test2(join_and_meets)

print "<terminated: %i>" % count



