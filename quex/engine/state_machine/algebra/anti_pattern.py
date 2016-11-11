import quex.engine.state_machine.algorithm.nfa_to_dfa         as nfa_to_dfa

def do(sm):
    """Anti Pattern: 
            -- drop-out                  => transition to acceptance state.
            -- transition to acceptances => drop-out
    """
    if not sm.is_DFA_compliant():
        sm = nfa_to_dfa.do(sm)

    original_acceptance_state_index_list = sm.get_acceptance_state_index_list()
    acceptance_state_index               = sm.create_new_state(AcceptanceF=True)

    for state_index, state in sm.states.iteritems():
        if state_index == acceptance_state_index: continue

        # Transform DropOuts --> Transition to Acceptance
        drop_out_trigger_set = state.target_map.get_drop_out_trigger_set_union()
        state.add_transition(drop_out_trigger_set, acceptance_state_index)

        # Transform Transitions to Acceptance --> DropOut
        transition_map = state.target_map.get_map()
        for target_index in original_acceptance_state_index_list:
            if transition_map.has_key(target_index):
                state.target_map.delete_transitions_to_target(target_index)

    # All original target states are deleted
    for target_index in original_acceptance_state_index_list:
        del sm.states[target_index]

    return sm

