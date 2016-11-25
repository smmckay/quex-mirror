import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])
from quex.engine.state_machine.core                 import StateMachine
from quex.engine.state_machine.algebra.TESTS.helper import test3, union, \
                                                           intersection, \
                                                           identity, \
                                                           add_more_DFAs
if "--hwut-info" in sys.argv:
    print "Distributivity;"
    print "HAPPY: [0-9]+;"
    sys.exit()

count = 0

def distributivity(A, B, C):
    global count
    first  = union([A, intersection([B, C])])
    second = intersection([union([A, B]), union([A,C])])
    assert identity(first, second)

    first  = intersection([A, union([B, C])])
    second = union([intersection([A, B]), intersection([A,C])])
    assert identity(first, second)

    count += 1

test3(distributivity)

print "<terminated: %i>" % count
