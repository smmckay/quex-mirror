#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

from   quex.input.code.base              import SourceRef_VOID
import quex.engine.state_machine.construction.setup_post_context as setup_post_context
import quex.engine.state_machine.construction.sequentialize as sequentialize
from   quex.engine.state_machine.TEST_help.some_dfas   import *
import quex.engine.state_machine.algorithm.nfa_to_dfa as nfa_to_dfa
import quex.engine.state_machine.algorithm.hopcroft_minimization as hopcroft

if "--hwut-info" in sys.argv:
    print "DFA Operations: Append Post Condition"
    sys.exit(0)

def test(sm, post_sm):    
    print "EXPRESSION = ", sm
    print "POST CONDITION = ", post_sm
    return_sm = setup_post_context.do(sm, post_sm, False, False, SourceRef_VOID)
    print "APPENDED = ", sm
    sm = nfa_to_dfa.do(sm)
    print "DFA = ", sm
    sm = hopcroft.do(sm)
    print "HOPCROFT = ", sm

if False:
    sm  = DFA()
    si  = sm.init_state_index
    si0 = sm.add_transition(si, ord('u'))
    si1 = sm.add_transition(si0, ord('y'), AcceptanceF=True)
    si2 = sm.add_transition(si0, ord('x'))
    si2 = sm.add_transition(si2, ord('x'), si2, AcceptanceF=True)
    print "#sm:", sm

    smp = DFA()
    si  = smp.init_state_index
    si0 = smp.add_transition(si, ord('x'), si)
    si1 = smp.add_transition(si, ord('y'), AcceptanceF=True)
    print "#sm2:", smp

    # return_sm = setup_post_context.do(sm, smp, False, False, SourceRef_VOID)
    print "#return_sm:", nfa_to_dfa.do(sequentialize.do([sm, smp]))
    sys.exit()

print "-------------------------------------------------------------------------------"
tiny0 = DFA()
tiny0.add_transition(tiny0.init_state_index, ord('a'), AcceptanceF=True)

tiny1 = DFA()
tiny1.add_transition(tiny1.init_state_index, ord(';'), AcceptanceF=True)

test(tiny0, tiny1)    
    
print "-------------------------------------------------------------------------------"
sm = sm1 
post_sm = sm3.clone()

test(sm, post_sm)    
   

