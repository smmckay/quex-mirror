import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])
from quex.engine.state_machine.core                 import DFA
from quex.engine.state_machine.algebra.TESTS.helper import test2, union, \
                                                           intersection, \
                                                           identity, \
                                                           add_more_DFAs

if "--hwut-info" in sys.argv:
    print "Commutativity;"
    print "HAPPY: [0-9]+;"
    sys.exit()

count = 0

def commutativity(A, B):
    global count
    first  = union([A.clone(), B.clone()])
    second = union([B.clone(), A.clone()])
    assert identity(first, second)

    first  = intersection([A.clone(), B.clone()]) 
    second = intersection([B.clone(), A.clone()]) 
    assert identity(first, second)

    count += 1

test2(commutativity)

print "<terminated: %i>" % count
