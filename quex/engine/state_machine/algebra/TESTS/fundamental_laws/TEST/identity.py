from quex.engine.state_machine.algebra.TESTS.fundamental_laws.TEST.helper import test2
import sys

if "--hwut-info" in sys.argv:
    print "Identity with. Empty and Universal"
    print "HAPPY: [0-9]+;"
    sys.exit()

count = 0

def identity_vs_empty_and_universal(A):
    first  = union(A, Empty)
    assert identity(first, A)

    first  = intersection(A, Universal) 
    assert identity(first, A)

    count += 1

test1(identity_vs_empty_and_universal)

print "<terminated: %i>" % count

