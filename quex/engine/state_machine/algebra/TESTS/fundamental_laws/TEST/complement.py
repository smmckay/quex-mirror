import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])
from quex.engine.state_machine.core                 import StateMachine
from quex.engine.state_machine.algebra.TESTS.helper import test1, \
                                                           union, \
                                                           intersection, \
                                                           complement, \
                                                           identity, \
                                                           add_more_DFAs
import sys

if "--hwut-info" in sys.argv:
    print "Complement laws producing Empty and Universal;"
    print "HAPPY: [0-9]+;"
    sys.exit()

count = 0

def complement_laws(A):
    global count
    first  = union([A, complement(A)])
    assert identity(first, StateMachine.Universal())

    first  = intersection([A, complement(A)]) 
    assert identity(first, StateMachine.Empty())

    count += 1

add_more_DFAs()
test1(complement_laws)

print "<terminated: %i>" % count


