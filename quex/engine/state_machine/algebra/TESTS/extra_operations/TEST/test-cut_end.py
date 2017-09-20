#! /usr/bin/env python
"""PURPOSE: Test the '\CutEnd' operations.

CutEnd{P Q} provides a pattern that matches on pruned lexemes of 'P'. That is, 

   * lexemes matched by `P` which *do not start* with something that matches `Q`. 

   * the 'tail' of lexemes matched by `P` which start with something `Q`. The
     'tail' of a lexeme is what comes after what is matched by `Q`.
   
For example, let `P` be defined as `("Mr. "|"Mrs. ")"Bone"` which matches `Mr.
Bone` and `Mrs. Bone`. Then, the pruned pattern `\\CutEnd{{P} "Mr. "} matches
`Bone` and `Mrs. Bone`.

NOTE: The operation ensures that no lexeme starts with `Q`. Thus, the any cut
      operation with `Q` is equivalent to the cutting of `Q+`.  The additional 
      test '\CutEnd{P Q} == \CutEnd{P Q+}' is a very strong additional test 
      to verify the functionality!

ADDITIONAL TESTS: 

    * \CutEnd{P Q}                  = \CutEnd{P Q+} 
    * \Intersection{Q \CutEnd{P Q}} = \Empty
    * \NotEnd{\CutEnd{P Q}} Q}      = \CutEnd{P Q} 
    * \IsEnd{\CutEnd{P Q}} Q}       = \Empty

AUTHOR: Frank-Rene Schaefer
"""
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.regular_expression.engine               as regex
import quex.engine.state_machine.construction.repeat      as repeat
import quex.engine.state_machine.algebra.cut              as cut
import quex.engine.state_machine.algebra.union            as union
import quex.engine.state_machine.algebra.intersection     as intersection
from   quex.engine.state_machine.TEST.helper_state_machine_shapes import get_sm_list
import quex.engine.state_machine.algebra.derived          as derived
import quex.engine.state_machine.check.identity           as identity
import quex.engine.state_machine.check.superset           as superset
import quex.engine.state_machine.algorithm.beautifier     as beautifier

if "--hwut-info" in sys.argv:
    print "Cut End: Cut P so that it does not end with Q."
    print "CHOICES: 0, 1, 2, 3, 4, 5, wild;"
    sys.exit(0)

def clean(SM):
    result = beautifier.do(SM)
    result.clean_up()
    return result

def operation(P, Q):
    return clean(cut.cut_end(P, Q))

    # NOT: complement_begin(cut_begin(P Q) Q) == cut_begin(P Q))
    #      assert identity.do(complement_begin.do(result, cutter), result)

def test(A_txt, B_txt):
    """Performs: \CutEnd{P Q} and prints the result!

    """
    print "---------------------------"

    print ("Original = " + A_txt).replace("\n", "\\n").replace("\t", "\\t")
    print ("Cutter   = " + B_txt).replace("\n", "\\n").replace("\t", "\\t")

    A = regex.do(A_txt, {}).sm
    B = regex.do(B_txt, {}).sm

    result_0, result_1 = core(A, B)

    print
    print "result = ", result_0.get_string(NormalizeF=True)

    assertion_checks(result_0, result_1, B)

def assertion_checks(result_0, result_1, B):
    # \CutEnd{P Q} == \CutEnd{P Q+}
    assert identity.do(result_0, result_1)

    # \Intersection{Q \CutEnd{P Q}} == \Empty
    assert intersection.do([result_0, B]).is_Empty()

    # \NotEnd{\CutEnd{P Q} Q} == \CutEnd{P Q}
    assert identity.do(derived.not_end(result_0, B), result_0)

    # \IsEnd{\CutEnd{P Q} Q} == \CutEnd{P Q}
    assert derived.is_end(result_0, B).is_Empty()


def core(A, B):
    result_0  = operation(A, B)
    Brepeated = repeat.do(B, min_repetition_n=1)
    result_1  = operation(A, B)
    return result_0, result_1

if "0" in sys.argv:
    test('otto_mueller', 'mueller')
    test('otto',         'otto')
    test('otto|fritz',   'otto')
    test('[01]{1,3}',    '0')
    test('[01]{1,3}',    '0+')
    test('[01]+',        '0')
    test('[01]+',        '0+')
    test('1[01]*',       '10')
    test('1[01]*',       '10+')
    test('[0-9]{2,}',    '01')
    test('123',          '123(4?)')
    test('12',           '1(2?)')
    test('1',            '1(2?)')
    test('"123"|"ABC"',  '"123"')
    test('\\n',          '(\\r\\n)|\\n')

elif "1" in sys.argv:
    test('[a-n]',          '[m-z]')
    test('"1234"|"ABC"',   '123')
    test('"12"|"A"',       '2')
    test('12',             '2')
    test('"1BAC"|"1BBC"',  '1ABC')
    test('alb|albertikus', 'albertiku')

elif "2" in sys.argv:
    test('"123"+',  '"123"')
    test('X"123"?', 'X"123"')
    test('"123"?X', '"123"X')
    test('1*X',     '1X')
    test('"123"*X', '"123"X')
    test('X"123"*', 'X"123"')

elif "3" in sys.argv:
    test('ab("12"+)yz',      'abz')
    test('a("12"|"AB")z',    'a1Bz')
    test('ab("12"|"AB")yz',  'ab1Byz')
    test('ab("12"|"ABD")yz', 'abAByc')

elif "4" in sys.argv:
    test('ab"12"+',          '1212')
    test('ab"12"+',          'ab1212')
    test('ab("12"+)yz',      'ab1212yz')
    test('ab("12"?)yz',      'abyz')
    test('ab("12"*)yz',      'abyz')
    test('ab("12"|"AB")?yz', 'abyz')
    test('ab("12"|"AB")?yz', 'abAByz')
    test('ab("12"|"AB")*yz', 'abyz')
    test('ab("12"|"AB")*yz', 'abAB12yz')

elif "5" in sys.argv:
    test('X("a"|"x"?|"e"|"g")', 'X')
    test('X("a"|"x"?|"e"|"g")', 'Xx')
    test('"a"|"x"+|"e"|"g"',    'x{5}')
    test('X("a"|"x"*|"e"|"g")', 'X')
    test('X("a"|"x"*|"e"|"g")', 'Xx{5}')

elif "wild" in sys.argv:
    def iterable():
        sm_list = get_sm_list()
        for i, sm_0 in enumerate(sm_list):
            for k, sm_1 in enumerate(sm_list):
                if i == k: continue
                yield sm_0, sm_1

    count = 0
    for a_sm, b_sm in iterable():
        result_0, result_1 = core(a_sm, b_sm)
        assertion_checks(result_0, result_1, b_sm)
        count += 1

    print "<terminated: %i>" % count

