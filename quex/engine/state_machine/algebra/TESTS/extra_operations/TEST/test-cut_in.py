#! /usr/bin/env python
"""PURPOSE: Test the '\CutIn' operations.

CutIn{P Q} provides a pattern that matches on pruned lexemes of 'P'. That is, 

   * lexemes matched by `P` which *do not start* with something that matches `Q`. 

   * the 'tail' of lexemes matched by `P` which start with something `Q`. The
     'tail' of a lexeme is what comes after what is matched by `Q`.
   
For example, let `P` be defined as `("Mr. "|"Mrs. ")"Bone"` which matches `Mr.
Bone` and `Mrs. Bone`. Then, the pruned pattern `\\CutIn{{P} "Mr. "} matches
`Bone` and `Mrs. Bone`.

NOTE: The operation ensures that no lexeme starts with `Q`. Thus, the any cut
      operation with `Q` is equivalent to the cutting of `Q+`.  The additional 
      test '\CutIn{P Q} == \CutIn{P Q+}' is a very strong additional test 
      to verify the functionality!

ADDITIONAL TESTS: 

    * Check: \CutIn{P Q}                  = \CutIn{P Q+} 
    * Check: \Intersection{Q \CutIn{P Q}} = \Empty

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
import quex.engine.state_machine.check.same               as same_check
import quex.engine.state_machine.check.identity           as identity
import quex.engine.state_machine.check.superset           as superset
import quex.engine.state_machine.algorithm.beautifier     as beautifier

if "--hwut-info" in sys.argv:
    print "Cut In: Cut P so that it does not contain anything matching Q."
    print "CHOICES: 0, 0b, 1, 2, 3, 4, 5;"
    sys.exit(0)

def clean(SM):
    result = beautifier.do(SM)
    result.clean_up()
    return result

def __core(P, Q):
    return clean(cut.cut_in(P, Q))

    # NOT: complement_begin(cut_begin(P Q) Q) == cut_begin(P Q))
    #      assert identity.do(complement_begin.do(result, cutter), result)

def test(A_txt, B_txt):
    """Performs: \CutIn{P Q} and prints the result!

    """
    print "---------------------------"

    print ("Original = " + A_txt).replace("\n", "\\n").replace("\t", "\\t")
    print ("Cutter   = " + B_txt).replace("\n", "\\n").replace("\t", "\\t")

    A        = regex.do(A_txt, {}).sm
    B        = regex.do(B_txt, {}).sm
    result_0 = __core(A, B)
    print
    print "result = ", result_0.get_string(NormalizeF=True)

    Brepeated = repeat.do(B, min_repetition_n=1)
    result_1  = __core(A, B)

    # \CutIn{P Q} == \CutIn{P Q+}
    assert same_check.do(result_0, result_1)

    # \Intersection{Q \CutIn{P Q}} == \Empty
    assert intersection.do([result_0, B]).is_Empty()

if True:
    test('10',            '0')
    sys.exit()

if "0b" in sys.argv:
    test('0',            '0')
    test('10',            '0')
    test('01',            '0')
    test('101',            '0')
    sys.exit()
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
    # test('abc("123"|("ABC"|"XYZ")+)+"123"("AAA"|"BBB"|"CCC")?xyz', 'abc123ABC123AAAxyz')
    #test('ab("12"|("AB"|"XY")+)+"12"("AA"|"BB"|"CC")?yz', 'ab12AB12AAyz')
    #test('(((a+)b)+c)+', 'abcbc')
    #test('(pri|ri|i)+',  'priri')
    #test('(pri|ri|i)+',  '(((p+)r)+i)+')

