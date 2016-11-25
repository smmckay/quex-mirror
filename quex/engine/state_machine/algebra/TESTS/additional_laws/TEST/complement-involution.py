import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])
from quex.engine.state_machine.core                 import StateMachine
from quex.engine.state_machine.algebra.TESTS.helper import test1, \
                                                           union, \
                                                           intersection, \
                                                           complement, \
                                                           identity, \
                                                           add_more_DFAs
import sys

if "--hwut-info" in sys.argv:
    print "Complement: Involution;"
    print "HAPPY: [0-9]+;"
    sys.exit()

count = 0

def involution(A):
    global count
    assert identity(complement(complement(A)), A)
    count += 1

add_more_DFAs()
test1(involution)

print "<terminated: %i>" % count



