import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])
from quex.engine.state_machine.core                 import DFA
from quex.engine.state_machine.algebra.TESTS.helper import test2, union, \
                                                           intersection, \
                                                           identity, \
                                                           difference, \
                                                           add_more_DFAs

if "--hwut-info" in sys.argv:
    print "Intersection by Difference;"
    print "HAPPY: [0-9]+;"
    sys.exit()

count = 0

def intersection_by_difference(A, B):
    global count
    assert identity(intersection([A, B]), 
                    difference(A, difference(A, B)))


    count += 1

test2(intersection_by_difference)

print "<terminated: %i>" % count

