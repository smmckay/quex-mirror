import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])
from quex.engine.state_machine.core                 import StateMachine
from quex.engine.state_machine.algebra.TESTS.helper import test3, \
                                                           union, \
                                                           intersection, \
                                                           complement, \
                                                           identity, \
                                                           superset, \
                                                           sample_DFAs
import sys

if "--hwut-info" in sys.argv:
    print "Transitivity;"
    print "HAPPY: [0-9]+;"
    sys.exit()

count = 0

def transitivity(A, B, C):
    global count
    Bnew = union([A.clone(), B.clone()])    # => Bnew = superset of A
    Cnew = union([Bnew.clone(), C.clone()]) # => Cnew = superset of Bnew
    assert superset(Bnew.clone(), A.clone())
    assert superset(Cnew.clone(), Bnew.clone())
    assert superset(Cnew.clone(), A.clone())

    count += 1

sample_DFAs(2)
test3(transitivity)

print "<terminated: %i>" % count


