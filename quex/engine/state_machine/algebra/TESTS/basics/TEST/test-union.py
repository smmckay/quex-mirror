#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.regular_expression.engine           as regex
import quex.engine.state_machine.algebra.union        as union
import quex.engine.state_machine.algebra.intersection as intersection
import quex.engine.state_machine.check.identity       as identity

if "--hwut-info" in sys.argv:
    print "Union"
    print "CHOICES: Sequences, SequenceAndOptional, SequenceAndLoop, Loops;"
    sys.exit(0)
    
def test(A_str, B_str):
    print ("A = " + A_str).replace("\n", "\\n").replace("\t", "\\t")
    print ("B = " + B_str).replace("\n", "\\n").replace("\t", "\\t")
    print "---------------------------"

    A = regex.do(A_str, {}).sm
    B = regex.do(B_str, {}).sm

    x = union.do([A, B])
    y = union.do([B, A])
    assert identity.do(x, y)

    print "union = ", x
    print

if "Sequences" in sys.argv:
    test('abc', 'abc')          # same
    test('abc', 'def')          # different
    test('Xbc', 'abc')          # partly same I
    test('aXc', 'abc')          # partly same II
    test('abX', 'abc')          # partly same III

elif "SequenceAndOptional" in sys.argv:
    test('ab(c?)', 'abc')       # same
    test('ab(c?)', 'def')       # different
    test('Xb(c?)', 'abc')       # partly same I
    test('aX(c?)', 'abc')       # partly same II
    test('ab(X?)', 'abc')       # partly same III

    test('(a?)b(c?)', 'abc')    # same
    test('(a?)b(c?)', 'def')    # different
    test('(X?)b(c?)', 'abc')    # partly same I
    test('(a?)X(c?)', 'abc')    # partly same II
    test('(a?)b(X?)', 'abc')    # partly same III

elif "SequenceAndLoop" in sys.argv:
    test('(abc)+', 'abc')       # same
    test('(abc)+', 'def')       # different
    test('(Xbc)+', 'abc')       # partly same I
    test('(aXc)+', 'abc')       # partly same II
    test('(abX)+', 'abc')       # partly same III

    test('ab(c*)', 'abc')       # same
    test('ab(c*)', 'def')       # different
    test('Xb(c*)', 'abc')       # partly same I
    test('aX(c*)', 'abc')       # partly same II
    test('ab(X*)', 'abc')       # partly same III

    test('(a*)b(c*)', 'abc')    # same
    test('(a*)b(c*)', 'def')    # different
    test('(X*)b(c*)', 'abc')    # partly same I
    test('(a*)X(c*)', 'abc')    # partly same II
    test('(a*)b(X*)', 'abc')    # partly same III

if "Loops" in sys.argv:
    test('(abc)+', '(abc)+')    # same
    test('(abc)+', '(def)+')    # different
    test('(Xbc)+', '(abc)+')    # partly same I
    test('(aXc)+', '(abc)+')    # partly same II
    test('(abX)+', '(abc)+')    # partly same III


