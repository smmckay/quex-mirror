from quex.engine.state_machine.algebra.TESTS.fundamental_laws.TEST.helper import test3
import sys

if "--hwut-info" in sys.argv:
    print "Associativity"
    sys.exit()

count = 0

def associativity(A, B, C):
    first  = union(union(A, B), C)
    second = union(A, union(B, C))
    assert identity(first, second)

    first  = intersection(intersection(A, B), C) 
    second = intersection(A, intersection(B, C))
    assert identity(first, second)

    count += 1

test3(associativity)

print "<terminated: %i>" % count
