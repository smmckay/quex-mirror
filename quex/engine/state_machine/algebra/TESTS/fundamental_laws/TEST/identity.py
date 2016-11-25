import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])
from quex.engine.state_machine.core                                       import StateMachine
from quex.engine.state_machine.algebra.TESTS.fundamental_laws.TEST.helper import test1, union, \
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
    first  = union([A, StateMachine.Empty()])
    assert identity(first, A)

    first  = intersection([A, StateMachine.Universal()]) 
    assert identity(first, A)

add_more_DFAs()
test1(identity_vs_empty_and_universal)

print "<terminated: %i>" % count

