import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])
from quex.engine.state_machine.core                 import StateMachine
from quex.engine.state_machine.algebra.TESTS.helper import test2, test1, test3, union, \
                                                           intersection, \
                                                           identity, \
                                                           complement, \
                                                           difference, \
                                                           add_more_DFAs, sample_DFAs

if "--hwut-info" in sys.argv:
    print "Complement: Relativity in difference operations;"
    print "CHOICES: 1, 2, 3;"
    print "HAPPY: [0-9]+;"
    sys.exit()

count = 0

def one(A):
    global count
    assert identity(difference(A, A), StateMachine.Empty())
    assert identity(difference(StateMachine.Empty(), A), StateMachine.Empty())
    assert identity(difference(A, StateMachine.Empty()), A) 
    assert identity(difference(StateMachine.Universal(), A), complement(A))
    assert identity(difference(A, StateMachine.Universal()), StateMachine.Empty()) 
    count += 1

def two(A, B):
    global count
    assert identity(difference(B, A),             intersection([complement(A), B]))
    assert identity(complement(difference(B, A)), union([A, complement(B)]))
    count += 1

def three(A, B, C):
    global count
    diff_C_B = difference(C, B)
    diff_C_A = difference(C, A)
    diff_B_A = difference(B, A)
    assert identity(difference(C, intersection([A, B])),
                    union([diff_C_A, diff_C_B]))
    assert identity(difference(C, union([A, B])),
                    intersection([diff_C_A, diff_C_B]))

    assert identity(difference(C, diff_B_A),
                    union([intersection([A, C]), diff_C_B]))

    tmp = intersection([diff_B_A, C])
    assert identity(tmp, difference(intersection([B, C]), A))
    assert identity(tmp, intersection([B, diff_C_A]))

    assert identity(union([diff_B_A, C]), 
                    difference(union([B, C]), difference(A, C)))
    count += 1

if   "1" in sys.argv: 
    add_more_DFAs()
    test1(one)
elif "2" in sys.argv: 
    test2(two)
elif "3" in sys.argv: 
    sample_DFAs(3)
    test3(three)


print "<terminated: %i>" % count


