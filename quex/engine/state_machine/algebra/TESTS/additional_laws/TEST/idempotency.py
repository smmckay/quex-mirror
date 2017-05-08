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
    print "Idempotency;"
    print "HAPPY: [0-9]+;"
    sys.exit()

count = 0

def idempotency(A):
    global count
    assert identity(A, union([A, A]))
    assert identity(A, intersection([A, A]))

    count += 1

add_more_DFAs()
test1(idempotency)

print "<terminated: %i>" % count



