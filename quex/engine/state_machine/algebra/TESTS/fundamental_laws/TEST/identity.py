import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])
from quex.engine.state_machine.core                 import StateMachine
from quex.engine.state_machine.algebra.TESTS.helper import test1, union, \
                                                           intersection, \
                                                           identity, \
                                                           add_more_DFAs

if "--hwut-info" in sys.argv:
    print "Identity with. Empty and Universal;"
    print "HAPPY: [0-9]+;"
    sys.exit()

count = 0

def identity_vs_empty_and_universal(A):
    global count
    count += 1
    # if count != 3: return
    first  = union([A.clone(), StateMachine.Empty()])
    assert identity(first, A.clone())

    first  = intersection([A.clone(), StateMachine.Universal()]) 
    assert identity(first, A)

add_more_DFAs()
test1(identity_vs_empty_and_universal)

print "<terminated: %i>" % count

