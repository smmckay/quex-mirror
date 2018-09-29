#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.engine.state_machine.cut.stem_and_branches as     stem_and_branches
import quex.engine.state_machine.algebra.reverse     as     reverse
import quex.input.regular_expression.engine            as     core
from   quex.blackboard                                 import setup as Setup
from   quex.constants     import E_AcceptanceCondition
Setup.buffer_limit_code = 0
Setup.path_limit_code   = 0
Setup.dos_carriage_return_newline_f = False

if "--hwut-info" in sys.argv:
    print "Conditional Analysis: Begin of Line '^', End of Line '$'"
    sys.exit(0)

stem_and_branches._unit_test_deactivate_branch_pruning_f = True

def test(TestString):
    test_core("^" + TestString + "$")
    if TestString[-1] != "/": test_core("^" + TestString + "/")
    else:                     test_core("^" + TestString)

def test_core(TestString):
    print "___________________________________________________________________________"
    print "expression    = \"" + TestString + "\""
    pattern = core.do(TestString, {}, AllowNothingIsNecessaryF=True).finalize(None)
    if pattern is None: 
        print "pattern syntax error"
    else:
        print "pattern\n", 
        print pattern.sm
        if pattern.sm_pre_context_to_be_reversed:
            reversed_sm = reverse.do(pattern.sm_pre_context_to_be_reversed)
            print "pre-context = ", reversed_sm
        print "begin of line = ", pattern.sm.has_acceptance_condition(E_AcceptanceCondition.BEGIN_OF_LINE)

test('[a-z]+')
test('[a-z]*')
test('[a-z]?')
test("[a-z]?/[a-z]/")
#test('[a-z]{2,5}')
#test('[a-z]{3,}')
#test('[a-z]{4}')
#test('"You"{3}')
#test('"You"*')
#test('"You"+')
#test('"You"?')
#test('a+(b|c)*t')
