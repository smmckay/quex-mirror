#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.regular_expression.engine as     core
from   quex.blackboard                      import setup as Setup
import quex.engine.state_machine.algebra.reverse     as     reverse
Setup.buffer_limit_code = -1
Setup.path_limit_code   = -1

if "--hwut-info" in sys.argv:
    print "Conditional Analysis: pre conditions"
    print "HAPPY: pre=[0-9]+;"
    sys.exit(0)
    
def test(TestString):
    print "-------------------------------------------------------------------"
    print "expression    = \"" + TestString + "\""
    pattern = core.do(TestString, {}).finalize(None)
    # pattern.mount_pre_context_sm()
    print "pattern\n"
    print pattern.sm
    print "pre-context =", reverse.do(pattern.sm_pre_context_to_be_reversed)

test('"a"/";"/')
test('(a|z)/c/')
test('"aac"|"bad"/"z"|congo/')
# test('"aac"|"bad"|bcad')
# test("you[a-b]|[a-e]|[g-m]you")    
# test("a(a|b)*")
