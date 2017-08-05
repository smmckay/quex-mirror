#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.regular_expression.engine as core
from quex.blackboard import setup as Setup
Setup.buffer_limit_code = -1
Setup.path_limit_code   = -1

if "--hwut-info" in sys.argv:
    print "Conditional Analysis: End of Line '$' (with DOS/Windows '\\r\\n')"
    sys.exit(0)

def test(TestString):
    test_core("^" + TestString + "$")

def test_core(TestString):
    print "___________________________________________________________________________"
    print "expression    = \"" + TestString + "\""

    Setup.dos_carriage_return_newline_f = True

    pattern = core.do(TestString, {}).finalize(None)
    if pattern is None: 
        print "pattern syntax error"
    else:
        print "pattern\n", 
        print pattern.sm
        if pattern.sm_pre_context:
            print "pre-context =", pattern.sm_pre_context
            print "begin of line = ", pattern.has_acceptance_condition(E_AcceptanceCondition.BEGIN_OF_LINE)

test('[a-z]+')
# test('[a-z]*')
# test('[a-z]?')
# test("[a-z]?/[a-z]/")
test("[a-b]/[c-z]")
#test('[a-z]{2,5}')
#test('[a-z]{3,}')
#test('[a-z]{4}')
#test('"You"{3}')
#test('"You"*')
#test('"You"+')
#test('"You"?')
#test('a+(b|c)*t')
