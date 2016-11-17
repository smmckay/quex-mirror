"""PURPOSE: Complement of pattern: '\Not{P}'

   => Matches every lexeme that P does not match.

ALGEBRAIC RELATIONS:

    union(complement(P), P)        == All
    intersection(complement(P), P) == Empty
    complement(complement(P))      == P

(C) 2013-2016 Frank-Rene Schaefer
"""
import quex.engine.state_machine.check.special as     special
import quex.engine.state_machine.index         as     index
from   quex.engine.state_machine.state.core    import State
from   quex.engine.misc.interval_handling      import NumberSet_All
from   quex.blackboard                         import setup as Setup
from   copy import deepcopy

def do(SM):
    """RETURNS: A state machines that matches anything which is 
                not matched by SM.

        (1a) Non-Acceptance           --> Acceptance
        (1b) Acceptance               --> Non-Acceptance
        (2a) Transition to Accept-all --> Drop-out
        (2b) Drop-out                 --> Transition to Accept-all

       NOTE: This function produces a finite state automaton which
             is not applicable by itself. It would eat ANYTHING
             from a certain state on.
    """
    assert SM.is_DFA_compliant()

    result = deepcopy(SM) # Not clone, state indices MUST be SAME!

    accept_all_state_index = result.create_new_state(AcceptanceF=True) 
    result.add_transition(accept_all_state_index, NumberSet_All(), 
                          accept_all_state_index)

    # (1a) acceptance state     --> non-acceptance state.
    # (1b) non-acceptance state --> acceptance state.
    for state_index, state in SM.states.iteritems():
        #if state_index == SM.init_state_index: continue
        # deepcopy --> use same state indices in SM and result
        result_state = result.states[state_index]
        result_state.set_acceptance(not state.is_acceptance())

    for state_index, state in SM.states.iteritems():
        result_state = result.states[state_index]

        # (2a) transition to 'Accept-All' state --> drop-out.
        for target_index in (i for i in state.target_map.get_target_state_index_list()
                             if special.is_accept_all_state(SM, i)):
            result_state.target_map.delete_transitions_to_target(target_index)

        # (2b) drop-out                         --> transition to 'Accept-All' state.
        drop_out_trigger_set = state.target_map.get_drop_out_trigger_set_union()
        if not drop_out_trigger_set.is_empty():
            result_state.add_transition(drop_out_trigger_set, accept_all_state_index)

    result.clean_up()

    return result.clone()

