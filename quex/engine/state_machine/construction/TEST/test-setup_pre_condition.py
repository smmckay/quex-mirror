#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])


import quex.engine.state_machine.construction.setup_pre_context as setup_pre_context 
import quex.engine.state_machine.algebra.reverse                 as reverse
from   quex.engine.state_machine.TEST_help.some_dfas   import *

from   quex.engine.state_machine.TEST_help.some_dfas   import *

if "--hwut-info" in sys.argv:
    print "DFA Operations: Setup Pre-Condition"
    sys.exit(0)

def test(sm, pre_sm):    
    print "EXPRESSION = ", sm
    print "PRE-CONDITION = ", pre_sm
    pre_context_sm         = setup_pre_context.do(sm, pre_sm, False, False)
    inverse_pre_context_sm = reverse.do(pre_context_sm)
    inverse_pre_context_sm.set_id(pre_context_sm.get_id())
    #
    print "with pre-context = ", sm
    print "inverse pre-context = ", inverse_pre_context_sm

print "-------------------------------------------------------------------------------"
tiny0 = DFA()
tiny0.add_transition(tiny0.init_state_index, ord('a'), AcceptanceF=True)
tiny1 = DFA()
tiny1.add_transition(tiny1.init_state_index, ord(';'), AcceptanceF=True)

test(tiny0, tiny1)    
    
print "-------------------------------------------------------------------------------"
test(sm1, sm3)    
   

