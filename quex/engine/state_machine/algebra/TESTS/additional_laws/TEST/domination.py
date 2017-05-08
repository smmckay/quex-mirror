
import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])
from quex.engine.state_machine.core                 import DFA
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
    first  = union([A, DFA.Universal()])
    assert identity(first, DFA.Universal())

    first  = intersection([A, DFA.Empty()]) 
    assert identity(first, DFA.Empty())

    count += 1

add_more_DFAs()
test1(domination)

print "<terminated: %i>" % count


