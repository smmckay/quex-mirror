
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
    print "Domination;"
    print "HAPPY: [0-9]+;"
    sys.exit()

count = 0

def domination(A):
    global count
    first  = union([A, StateMachine.Universal()])
    assert identity(first, StateMachine.Universal())

    first  = intersection([A, StateMachine.Empty()]) 
    assert identity(first, StateMachine.Empty())

    count += 1

add_more_DFAs()
test1(domination)

print "<terminated: %i>" % count


