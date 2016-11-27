import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])
from quex.engine.state_machine.core                 import StateMachine
from quex.engine.state_machine.algebra.TESTS.helper import test1, union, \
                                                           intersection, \
                                                           identity, \
                                                           complement, \
                                                           difference, \
                                                           add_more_DFAs

if "--hwut-info" in sys.argv:
    print "Complement: Uniqueness and Involution;"
    print "HAPPY: [0-9]+;"
    sys.exit()

count = 0

def uniqueness(A):
    """Uniqueness of complement:
        
              A u B = Universal   and    A n B = Empty

           => A = complement B  and vice versa

       Involution:
            
              A = complement(complement(A))
    """
    global count

    B = difference(StateMachine.Universal(), A)
    # => A u B = Universal   and    A n B = Empty
    assert identity(union([A, B]), StateMachine.Universal())
    assert identity(intersection([A, B]), StateMachine.Empty())

    # Uniqueness of complement
    assert identity(A, complement(B))
    assert identity(B, complement(A))

    # Involution/Double Complement
    assert identity(A, complement(complement(A)))
    assert identity(B, complement(complement(B)))
    count += 1

add_more_DFAs()
test1(uniqueness)

print "<terminated: %i>" % count


