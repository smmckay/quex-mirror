import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])
from quex.engine.state_machine.core                 import StateMachine
from quex.engine.state_machine.algebra.TESTS.helper import test2, union, \
                                                           intersection, \
                                                           identity, \
                                                           complement, \
                                                           add_more_DFAs

if "--hwut-info" in sys.argv:
    print "Complement: DeMorgan's Law;"
    print "HAPPY: [0-9]+;"
    sys.exit()

count = 0

def de_morgan(A, B):
    global count
    assert identity(complement(union([A, B])), 
                    intersection([complement(A), complement(B)]))
    assert identity(complement(intersection([A, B])), 
                    union([complement(A), complement(B)]))
    count += 1

test2(de_morgan)

print "<terminated: %i>" % count
