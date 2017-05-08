
import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])
from quex.engine.state_machine.core                 import DFA
from quex.engine.state_machine.algebra.TESTS.helper import test2, union, \
                                                           intersection, \
                                                           identity, \
                                                           add_more_DFAs

if "--hwut-info" in sys.argv:
    print "Absorbtion;"
    print "HAPPY: [0-9]+;"
    sys.exit()

count = 0

def absorbtion(A, B):
    global count
    assert identity(union([A, intersection([A.clone(), B.clone()])]), A.clone())
    assert identity(intersection([A, union([A.clone(), B.clone()])]), A.clone())


    count += 1

test2(absorbtion)

print "<terminated: %i>" % count
