#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])


from   quex.input.code.base              import SourceRef_VOID
import quex.engine.state_machine.construction.setup_post_context as setup_post_context
import quex.engine.state_machine.construction.setup_pre_context  as setup_pre_context 
import quex.engine.state_machine.algebra.reverse                 as reverse
# import quex.engine.state_machine.construction.setup_border_conditions as setup_border_conditions 
import quex.engine.state_machine.algorithm.beautifier as beautifier
import quex.engine.state_machine.check.identity      as identity_checker

from   quex.engine.state_machine.TEST_help.some_dfas   import *
from   quex.blackboard import setup as Setup


Setup.dos_carriage_return_newline_f = False
Setup.set_all_character_set_UNIT_TEST()


if "--hwut-info" in sys.argv:
    print "DFA Operations: Append Post Condition"
    sys.exit(0)


def test(Idx, sm_pre, sm, sm_post, BOL_F, EOL_F):    
    ## if Idx != 5: return
    result = sm.clone()
    print "##-- %i -----------------------------------------------------------------------" % Idx

    if sm_pre is not None: print " -- pre-condition  = True"
    else:                  print " -- pre-condition  = False"
        
    if sm_post is not None: print " -- post-condition = True"
    else:                   print " -- post-condition = False"
    print " -- begin of line  = ", BOL_F
    print " -- end of line    = ", EOL_F

    ipsb_sm                = setup_post_context.do(result, sm_post, EOL_F, False, SourceRef_VOID)
    pre_context_sm         = setup_pre_context.do(result, sm_pre, BOL_F, False)
    if pre_context_sm is None:
        inverse_pre_context_sm = None
    else:
        inverse_pre_context_sm = reverse.do(pre_context_sm)
        inverse_pre_context_sm.set_id(pre_context_sm.get_id())
    #
    # print "EXPRESSION = ", result
    # print "POST CONDITION = ", post_sm
    # print "APPENDED = ", result
    result = beautifier.do(result)
    #
    #
    print
    print "result sm.id     = ", result.get_id()
    if inverse_pre_context_sm is not None:
        print "result pre sm.id = ", inverse_pre_context_sm.get_id()

    begin_of_line_f = None
    for state in result.get_acceptance_state_list():
        BOF = state.single_entry.has_pre_context_begin_of_line()
        if begin_of_line_f is None: begin_of_line_f = BOF
        else:                       assert begin_of_line_f == BOF

    print "result = ", result
    if inverse_pre_context_sm is not None:
        print "inverse_pre_context_sm = ", inverse_pre_context_sm
    print "trivially pre-conditioned = ", begin_of_line_f

    ## if Idx == 1: sys.exit(-1)

tiny0 = DFA()
tiny0.add_transition(tiny0.init_state_index, ord('0'), AcceptanceF=True)
tiny1 = DFA()
tiny1.add_transition(tiny1.init_state_index, ord('1'), AcceptanceF=True)
tiny2 = DFA()
tiny2.add_transition(tiny2.init_state_index, ord('2'), AcceptanceF=True)

backup0 = deepcopy(tiny0)
backup1 = deepcopy(tiny1)
backup2 = deepcopy(tiny2)

i = -1
for flag_k in range(0, 4):

    for flag_i in range(0, 4):
        i += 1
        bof_f = flag_i & 2 == 2
        eof_f = flag_i & 1 == 1

        # Clone for this event
        sm_pre  = None
        sm_post = None
        if flag_k & 2 == 2: sm_pre  = tiny0.clone() # None
        if flag_k & 1 == 1: sm_post = tiny2.clone()
        sm = tiny1.clone()

        # Double check on 'cloner'
        assert identity_checker.do(sm, backup1)
        assert sm_pre  is None or identity_checker.do(sm_pre, backup0)
        assert sm_post is None or identity_checker.do(sm_post, backup2)

        test(i, sm_pre, sm, sm_post, bof_f,  eof_f)    
    
   

