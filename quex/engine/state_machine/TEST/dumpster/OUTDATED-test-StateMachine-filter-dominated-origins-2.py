#! /usr/bin/env python
import sys
from random import random
import os
sys.path.insert(0, os.environ["QUEX_PATH"])


from quex.engine.state_machine.index import get_state_machine_by_id, \
                                            state_machine_ranking_db_register
from quex.engine.state_machine.core        import DFA
from quex.engine.state_machine.state.core  import DFA_State, \
                                                  StateOriginInfo

if "--hwut-info" in sys.argv:
    print "Ranking of DFAs: Filter Dominated Origins - Part 2"
    sys.exit(0)

def add_origin(StateMachineIdx, StoreInputPositionF,
               PostConditionedAcceptanceF=False, PreConditionedStateMachineID=-1L):              

    sm = get_state_machine_by_id(StateMachineIdx)
     
    si.add_origin(StateOriginInfo(long(StateMachineIdx), long(sm.init_state_index), 
                                  StoreInputPositionF, 
                                  PostConditionedAcceptanceF, 
                                  PreConditionedStateMachineID))

def add_priority(A, B):
    print "priority: %s > %s" % (repr(A), repr(B))    
    state_machine_ranking_db_register(A, B)

def print_this(Title):    
    print "---------------------------------------------------------------------"
    print "(*) " + Title    
    print

    for cmd in si.single_entry:
        acceptance_mark = " "
        if cmd.is_acceptance(): acceptance_mark = "*"
        print acceptance_mark + repr(cmd)

    print "---------------------------------------------------------------------"

#----------------------------------------------------------------------------------------    
# (*) setup the state machine origins    
#
# -- the function 'filter dominated origins searches for the original acceptance
#    in the state machine => need to create to dummy state machines
DFA(InitStateIndex=0L, AcceptanceF=True)
DFA(InitStateIndex=1L, AcceptanceF=True)
DFA(InitStateIndex=2L, AcceptanceF=True)
DFA(InitStateIndex=3L, AcceptanceF=True)
DFA(InitStateIndex=4L, AcceptanceF=True)
DFA(InitStateIndex=5L, AcceptanceF=True)
DFA(InitStateIndex=6L, AcceptanceF=True)
DFA(InitStateIndex=100L, AcceptanceF=False)
DFA(InitStateIndex=101L, AcceptanceF=False)
DFA(InitStateIndex=102L, AcceptanceF=False)
DFA(InitStateIndex=103L, AcceptanceF=False)
DFA(InitStateIndex=104L, AcceptanceF=False)
DFA(InitStateIndex=105L, AcceptanceF=False)
DFA(InitStateIndex=106L, AcceptanceF=False)
    
# (*) add priviledges
# add_priority(4L, 0L)   
# add_priority(6L, 3L)   

# (1) only acceptance and non-acceptance states    
si = DFA_State()    
add_origin(1, True)    
add_origin(4, True)    
add_origin(0, True)    
add_origin(5, True)    
add_origin(6, True)    
add_origin(3, True)    
add_origin(2, True)    
add_origin(7, False)    
add_origin(8, False)    
add_origin(9, False)    
add_origin(10, False)    
add_origin(11, False)    
add_origin(12, False)    
add_origin(13, False)    

print_this("Only Acceptance/Non-Acceptance - Before")
si.single_entry.filter_dominated()
print_this("Only Acceptance/Non-Acceptance - After")

# (2) acceptance and pre-conditioned states
si = DFA_State()    
add_origin(1, True, PreConditionedStateMachineID=1L)    
add_origin(4, True)    
add_origin(0, True, PreConditionedStateMachineID=1L)    
add_origin(5, True)    
add_origin(6, True, PreConditionedStateMachineID=1L)    
add_origin(3, True, PreConditionedStateMachineID=1L)    
add_origin(2, True, PreConditionedStateMachineID=1L)    
add_origin(7, False)    
add_origin(8, False)    
add_origin(9, False)    
add_origin(10, False)    
add_origin(11, False)    
add_origin(12, False)    
add_origin(13, False)    

    

print_this("Acceptance and Pre-Conditioned Acceptance - Before")
si.single_entry.filter_dominated()
print_this("Acceptance and Pre-Conditioned Acceptance - After")

# (3) acceptance and post-conditioned states
si = DFA_State()    
add_origin(1, True, PostConditionedAcceptanceF=1L)    
add_origin(4, True)    
add_origin(0, True, PostConditionedAcceptanceF=1L)    
add_origin(5, True)    
add_origin(6, True, PostConditionedAcceptanceF=1L)    
add_origin(3, True, PostConditionedAcceptanceF=1L)    
add_origin(2, True, PostConditionedAcceptanceF=1L)    
add_origin(7, False)    
add_origin(8, StoreInputPositionF=True, PostConditionedAcceptanceF=1L)    
add_origin(9, False)    
add_origin(10, False)    
add_origin(11, True, PostConditionedAcceptanceF=1L)    
add_origin(12, True, PostConditionedAcceptanceF=1L)    
add_origin(13, True, PostConditionedAcceptanceF=1L)    

print_this("Acceptance and Post-Conditioned Acceptance - Before")
si.single_entry.filter_dominated()
print_this("Acceptance and Post-Conditioned Acceptance - After")

