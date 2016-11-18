from quex.engine.state_machine.algebra.TESTS.fundamental_laws.TEST.helper import test1, \
                                                                                 union, \
                                                                                 complement, \
                                                                                 identity
import sys

if "--hwut-info" in sys.argv:
    print "Complement laws producing Empty and Universal;"
    print "HAPPY: [0-9]+;"
    sys.exit()

count = 0

def complement_laws(A):
    first  = union(A, complement(A))
    assert identity(first, Universal)
    first  = union(complement(A), A)
    assert identity(first, Universal)

    first  = intersection(A, complement(A)) 
    assert identity(first, Empty)
    first  = intersection(complement(A), A) 
    assert identity(first, Empty)

    count += 1

test1(complement_laws)

print "<terminated: %i>" % count


