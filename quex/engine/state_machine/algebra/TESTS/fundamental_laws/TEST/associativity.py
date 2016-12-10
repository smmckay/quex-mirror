import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])
from quex.engine.state_machine.core                 import StateMachine
from quex.engine.state_machine.algebra.TESTS.helper import test3, union, \
                                                           intersection, \
                                                           identity, \
                                                           add_more_DFAs

if "--hwut-info" in sys.argv:
    print "Associativity;"
    print "HAPPY: [0-9]+;"
    sys.exit()

count = 0

def associativity(A, B, C):
    global count
    first  = union([union([A.clone(), B.clone()]), C.clone()])
    second = union([A.clone(), union([B.clone(), C.clone()])])
    assert identity(first, second), \
             "First: %s;\nSecond: %s;\n" % (first, second) \
           + "A: %s;\nB: %s;\nC: %s;\n" % (A, B, C)
    first  = intersection([intersection([A.clone(), B.clone()]), C.clone()])
    second = intersection([A, intersection([B.clone(), C.clone()])])
    assert identity(first, second), \
           "A: %s;\nB: %s;\nC: %s;\n" % (A, B, C)
    count += 1


test3(associativity)

print "<terminated: %i>" % count
