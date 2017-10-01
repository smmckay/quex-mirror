#! /usr/bin/env python
"""PURPOSE: Test the '\CutBegin' operations.

CutBegin{P Q} provides a pattern that matches on pruned lexemes of 'P'. That is, 

   * lexemes matched by `P` which *do not start* with something that matches `Q`. 

   * the 'tail' of lexemes matched by `P` which start with something `Q`. The
     'tail' of a lexeme is what comes after what is matched by `Q`.
   
For example, let `P` be defined as `("Mr. "|"Mrs. ")"Bone"` which matches `Mr.
Bone` and `Mrs. Bone`. Then, the pruned pattern `\\CutBegin{{P} "Mr. "} matches
`Bone` and `Mrs. Bone`.

NOTE: The operation ensures that no lexeme starts with `Q`. Thus, the any cut
      operation with `Q` is equivalent to the cutting of `Q+`.  The additional 
      test '\CutBegin{P Q} == \CutBegin{P Q+}' is a very strong additional test 
      to verify the functionality!

ADDITIONAL TESTS: 

    () \CutBegin{Q Q}                   = \Empty
    () \CutBegin{P          \Empty}     = P
    () \CutBegin{P          \Universal} = \Empty
    () \CutBegin{\Empty     P}          = \Empty

    (not) \CutBegin{\Universal P}          = \Universal  # Does not hold 'p = 1+'
    (not) \CutBegin{Q*P Q}                 = Q*P    => Does not hold if P starts with Q
                                                    and 

    () \Intersection{Q \CutBegin{P Q+}} = \Empty
    () \NotBegin{\CutBegin{P Q+}} Q}    = \CutBegin{P Q+} 
    () \IsBegin{\CutBegin{P Q+}} Q}     = \Empty

AUTHOR: Frank-Rene Schaefer
"""
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.regular_expression.engine               as regex
from   quex.engine.state_machine.core                     import DFA
import quex.engine.state_machine.construction.repeat      as repeat
import quex.engine.state_machine.construction.sequentialize as sequentialize
from   quex.engine.state_machine.TEST.helper_state_machine_shapes import get_sm_list

import quex.engine.state_machine.algebra.cut              as cut      
import quex.engine.state_machine.algebra.union            as union
import quex.engine.state_machine.algebra.intersection     as intersection
import quex.engine.state_machine.algebra.derived          as derived
import quex.engine.state_machine.check.identity           as identity
import quex.engine.state_machine.check.superset           as superset
import quex.engine.state_machine.algorithm.beautifier     as beautifier

if "--hwut-info" in sys.argv:
    print "Cut Begin: Cut P so that it does not start with Q."
    print "CHOICES: 0, 0b, 1, 2, 3, 4, 5, wild;"
    sys.exit(0)

def __operation(P, Q):
    result = cut.cut_begin(P, Q)
    result = beautifier.do(result)
    result.clean_up()
    return result

    # NOT: complement_begin(cut_begin(P Q) Q) == cut_begin(P Q))
    #      assert identity.do(complement_begin.do(result, cutter), result)

def core(P, Q, Q_repeated, Q_repeated_P):
    cut_P_Q         = __operation(P, Q)
    cut_Q_Q         = __operation(Q, Q)
    cut_P_Empty     = __operation(P, DFA.Empty())
    cut_P_Universal = __operation(P, DFA.Universal())
    cut_Empty_P     = __operation(DFA.Empty(), P)
    cut_Universal_P = __operation(DFA.Universal(), P)
    cut_P_Qp        = __operation(P, Q_repeated)
    cut_QpP_Q       = __operation(Q_repeated_P, Q)

    # \CutBegin{Q          Q}          = \Empty
    assert cut_Q_Q.is_Empty()

    # \CutBegin{P          \Empty}     = P
    assert identity.do(cut_P_Empty, P)

    # \CutBegin{P          \Universal} = \Empty
    assert cut_P_Universal.is_Empty()

    # \CutBegin{\Empty     P}          = \Empty
    assert cut_Empty_P.is_Empty()

    # \Intersection{Q \CutBegin{P Q+}} == \Empty
    assert intersection.do([Q, cut_P_Qp]).is_Empty()

    # \NotBegin{\CutBegin{P Q+} Q} == \CutBegin{P Q+}
    assert identity.do(derived.not_begin(cut_P_Qp, Q), cut_P_Qp)

    # \IsBegin{\CutBegin{P Q+} Q} == \Empty
    assert derived.is_begin(cut_P_Qp, Q).is_Empty()

    return cut_P_Qp

def test(A_txt, B_txt):
    """Performs: \CutBegin{P Q} and prints the result!

    """
    print "---------------------------"

    A, B                     = parse_REs(A_txt, B_txt)
    B_repeated, B_repeated_A = more_DFAs(A, B)

    result = core(A, B, B_repeated, B_repeated_A)

    print
    print "result = ", result.get_string(NormalizeF=True)

def parse_REs(A_txt, B_txt):
    print ("Original = " + A_txt).replace("\n", "\\n").replace("\t", "\\t")
    print ("Cutter   = " + B_txt).replace("\n", "\\n").replace("\t", "\\t")
    A = regex.do(A_txt, {}).sm
    B = regex.do("%s" % B_txt, {}).sm
    return A, B

def more_DFAs(A, B):
    B_repeated   = repeat.do(B)
    B_repeated0  = repeat.do(B, min_repetition_n=0)
    B_repeated_A = beautifier.do(sequentialize.do([B_repeated0, A]))
    return beautifier.do(B_repeated), B_repeated_A

if False: # Selected Test
    test('1*X',     '1X')
    sys.exit()
    # test('\Universal', '1')
    # test('A(11|22|33|44|55|66|77|88|99|AA|BB|CC|DD|EE|FF|GG|HH|II|JJ|KK|LL|MM|NN|OO|PP|QQ|RR|SS)+C', 'ABBC')
    # test('1*01',          '0')
    # A = regex.do("1+2", {}).sm
    # B = regex.do("1", {}).sm
    A = DFA.Universal()
    B = regex.do("1+", {}).sm
    print __operation(A, B)
    # print "#result:", result.get_string("hex")
    sys.exit()

if "0b" in sys.argv:
    test('[1]',          '0')
    test('[0]',          '0')
    test('[01]',         '0')
    test('[1][01]',      '0')
    test('[0][01]',      '0')
    test('[01][01]',     '0')
    test('[1][01][01]',  '0')
    test('[0][01][01]',  '0')
    test('[01][01][01]', '0')
    test('[01][1][01]',  '0')
    test('[01][0][01]',  '0')

if "0" in sys.argv:
    test('otto_mueller', 'otto')
    test('otto',         'otto')
    test('otto|fritz',   'otto')
    test('[01]{1,3}',    '0')
    test('[01]+',        '0')
    test('1[01]*',       '10')
    test('[0-9]{2,}',    '01')
    test('123',          '123(4?)')
    test('12',           '1(2?)')
    test('1',            '1(2?)')
    test('"123"|"ABC"',  '"123"')
    test('\\n',          '(\\r\\n)|\\n')
    test('[ab]+',        '"b"')
    test('[ab]+',        '"bb"')

elif "1" in sys.argv:
    test('[a-n]', '[m-z]')
    test('"1234"|"ABC"', '"123"')
    test('"12"|"A"', '"1"')
    test('12', '1')
    test('"1BAC"|"1BBC"', '"1ABC"')
    test('alb|albertikus', 'albert')

elif "2" in sys.argv:
    test('"123"+',  '"123"')
    test('X"123"?', 'X"123"')
    test('"123"?X', '"123"X')
    test('1*X',     '1X')
    test('"123"*X', '"123"X')
    test('X"123"*', 'X"123"')

elif "3" in sys.argv:
    test('ab("12"+)yz',      'abz')
    test('a("12"|"AB")z',    'a1B3z')
    test('ab("12"|"AB")yz',  'ab1B3yz')
    test('ab("12"|"ABD")yz', 'abAByc')

elif "4" in sys.argv:
    test('"12"+yz',          '1212')
    test('"12"+yz',          '1212yz')
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
        B_repeated, B_repeated_A = more_DFAs(a_sm, b_sm)
        core(a_sm, b_sm, B_repeated, B_repeated_A)
        count += 1

    print "<terminated: %i>" % count


