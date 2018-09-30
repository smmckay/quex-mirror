#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.regular_expression.engine      as regex
import quex.engine.state_machine.algorithm.beautifier as beautifier
import quex.engine.state_machine.algebra.complement as complement
import quex.engine.state_machine.algebra.intersection  as intersection
import quex.engine.state_machine.algebra.union   as union
from   quex.engine.state_machine.core            import DFA
import quex.engine.state_machine.check.identity  as identity
import quex.engine.state_machine.check.superset  as superset

if "--hwut-info" in sys.argv:
    print "Complementary DFAs"
    print "CHOICES: Sequence, Branches, Loops, BranchesLoops, Misc;"
    sys.exit(0)

def commonality(A, B):
    return superset.do(A, B) or superset.do(B, A) 

def test(A_str):
    print "_____________________________________________________________________"
    if isinstance(A_str, (str, unicode)):
        print ("A = " + A_str).replace("\n", "\\n").replace("\t", "\\t")
        sm = regex.do(A_str, {}).extract_sm()
    else:
        sm = A_str
        print "A = ", sm

    ## print "##sm:", sm.get_string(NormalizeF=False)
    result_1st    = complement.do(sm)
    print "complement(A):", result_1st # .get_string(NormalizeF=False)
    result_2nd    = complement.do(result_1st)
    ## print "##2nd:", result_2nd.get_string(NormalizeF=False)
    print
    print "union(A, complement(A)):            All  =", DFA.is_Universal(union.do([sm, result_1st]))
    print "intersection(A, complement(A)):     None =", DFA.is_Empty(intersection.do([sm, result_1st]))
    print "identity(A, complement(complement(A)):",     identity.do(sm, result_2nd)
    assert not commonality(sm, result_1st)
    assert not commonality(result_1st, result_2nd)

if "Sequence" in sys.argv:
    test('[0-9]')
    test('[0-9][0-9]')
    test('[0-9][0-9][0-9]')
    test('a(b?)')
    test('ab(c?)')
    test('ab|abcd')

elif "Branches" in sys.argv:
    test('12|AB')
    test('x(12|AB)')
    test('(12|AB)x')
    test('x(12|AB)x')
    test('x(1?2|A?B)x')
    test('x(1?2?|A?B?)x')

elif "Loops" in sys.argv:
    test('A+')
    test('A(B*)')
    test('A((BC)*)')
    test('((A+)B+)C+')
    test('(ABC|BC|C)+')

elif "BranchesLoops" in sys.argv:
    test('(AB|XY)+')
    test('(AB|XY)((DE|FG)*)')
    test('(((AB|XY)+)(DE|FG)+)(HI|JK)+')
    test('((AB|XY)(DE|FG)(HI|JK)|(DE|FG)(HI|JK)|(HI|JK))+')

elif "Misc" in sys.argv:
    test('((((((((p+)r)+i)+)n)+t)+e)+r)+')
    test('(printer|rinter|inter|nter|ter|er|r)+')
    test('(p?r?i?n?t?e?r|rinter|inter|nter|ter|er|r)+')
    test('(((((((((p+)r)+i)+)p)+r)+i)+n)+|(priprin|riprin|iprin|prin|rin|in|n)+)x?')

elif "Special" in sys.argv:
    test(DFA.Empty())
    test(DFA.Universal())
    sm = DFA.Universal()
    sm.get_init_state().set_acceptance(True)
    sm = beautifier.do(sm)
    test(sm)
else:
    test('a|ab')

