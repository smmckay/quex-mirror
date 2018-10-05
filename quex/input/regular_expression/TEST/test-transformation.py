#! /usr/bin/env python
# vim: set fileencoding=utf8 :
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.regular_expression.engine          as     core
import quex.engine.state_machine.algorithm.beautifier as     beautifier
import quex.engine.state_machine.algebra.reverse     as     reverse
from   quex.blackboard                               import setup as Setup
import quex.output.languages.core                    as     languages

Setup.buffer_limit_code = -1
Setup.path_limit_code   = -1
# Setup.buffer_element_specification_prepare()
Setup.bad_lexatom_detection_f = False
Setup.language_db = languages.db["C++"]()
Setup.buffer_setup("<no-type>", -1, "utf8")

if "--hwut-info" in sys.argv:
    print "Transformations"
    sys.exit(0)
    
def test(TestString):
    print "-------------------------------------------------------------------"
    print "expression    = \"" + TestString + "\""
    pattern = core.do(TestString, {}).finalize(None)

    # During 'finalize()': pattern.transform(Setup.buffer_encoding)
    # During 'finalize()': pattern.mount_post_context_sm()
    # During 'finalize()': pattern.mount_pre_context_sm()
    print "pattern\n" 
    assert pattern.sm.is_DFA_compliant()
    ok_f, sm = Setup.buffer_encoding.do_state_machine(pattern.sm)
    sm = beautifier.do(pattern.sm)
    print sm.get_string(NormalizeF=True, Option="hex") 
    if pattern.sm_pre_context_to_be_reversed:
        assert pattern.sm_pre_context_to_be_reversed.is_DFA_compliant()
        ok_f, sm = Setup.buffer_encoding.do_state_machine(pattern.sm_pre_context_to_be_reversed)
        reversed_sm = reverse.do(sm)
        print "pre-context = ", reversed_sm.get_string(NormalizeF=True, Option="hex") 
    if pattern.sm_bipd_to_be_reversed:
        assert pattern.sm_bipd_to_be_reversed.is_DFA_compliant()
        ok_f, sm = Setup.buffer_encoding.do_state_machine(pattern.sm_bipd_to_be_reversed)
        sm = reverse.do(sm)
        print "post-context backward input position detector = ", sm.get_string(NormalizeF=True, Option="hex") 

test('µ/µ+/µ')
test('[aµ]+/[aµ]')
test('\Intersection{[^a] [\X0000-\U10FFFF]}+/\Intersection{[^a] [\X0000-\U10FFFF]}a')

