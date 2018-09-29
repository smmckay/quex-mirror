#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.regular_expression.engine as core
import quex.engine.state_machine.algebra.reverse     as     reverse
from quex.blackboard import setup as Setup
Setup.buffer_limit_code = -1
Setup.path_limit_code   = -1

if "--hwut-info" in sys.argv:
    print "Conditional Analysis: pre- and post-conditions"
    sys.exit(0)
    
def test(TestString):
    print "-------------------------------------------------------------------"
    print "expression    = \"" + TestString + "\""
    pattern = core.do(TestString, {}).finalize(None)
    print "pattern\n"
    print pattern.sm
    print "pre-context = ", reverse.do(pattern.sm_pre_context_to_be_reversed)

test('"a"/";"/"b"')

test('(d|e)/(a|z)/c')
test('"123"/"aac"|"bad"/"z"|congo')
# test('"aac"|"bad"|bcad')
# test("you[a-b]|[a-e]|[g-m]you")    
# test("a(a|b)*")
