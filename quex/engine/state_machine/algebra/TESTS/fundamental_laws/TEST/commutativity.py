from   quex.engine.state_machine.algebra.TESTS.fundamental_laws.TEST.helper import test2
import sys

if "--hwut-info" in sys.argv:
    print "Commutativity"
    sys.exit()

count = 0

def commutativity(A, B):
    first  = union(A, B)
    second = union(B, A)
    assert identity(first, second)

    first  = intersection(A, B) 
    second = intersection(B, A)
    assert identity(first, second)

    count += 1

test2(commutativity)

print "<terminated: %i>" % count
