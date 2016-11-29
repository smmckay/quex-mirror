import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])
from quex.engine.state_machine.core                 import StateMachine
from quex.engine.state_machine.algebra.TESTS.helper import test1, \
                                                           union, \
                                                           intersection, \
                                                           complement, \
                                                           identity, \
                                                           superset, \
                                                           add_more_DFAs
import sys

if "--hwut-info" in sys.argv:
    print "Reflexivity;"
    print "HAPPY: [0-9]+;"
    sys.exit()

count = 0

def reflexivity(A):
    global count
    assert superset(A, A)

    count += 1

add_more_DFAs()
test1(reflexivity)

print "<terminated: %i>" % count


