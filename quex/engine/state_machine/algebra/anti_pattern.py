import quex.engine.state_machine.algorithm.nfa_to_dfa         as nfa_to_dfa

def do(sm):
    """Anti Pattern: 
            -- drop-out                  => transition to acceptance state.
            -- transition to acceptances => drop-out
    """
    if not sm.is_DFA_compliant():
        sm = nfa_to_dfa.do(sm)

    original_acceptance_state_index_set = set(sm.get_acceptance_state_index_list())
    acceptance_state_index              = sm.create_new_state(AcceptanceF=True)

    for state_index, state in sm.states.iteritems():
        if state_index == acceptance_state_index: continue

        # Transform DropOuts --> Transition to Acceptance
        drop_out_trigger_set = state.target_map.get_drop_out_trigger_set_union()
        state.add_transition(drop_out_trigger_set, acceptance_state_index)

        # Transform Transitions to Acceptance --> DropOut
        for target_index in original_acceptance_state_index_set:
            state.target_map.delete_transitions_to_target(target_index)

    # Remove acceptance from any previous acceptance state.
    for state_index in original_acceptance_state_index_set:
        sm.states[state_index].set_acceptance(False)

    # Delete orphan states (which where acceptance state or connected to them)
    for state_index in sm.get_orphaned_state_index_list():
        del sm.states[state_index]

    return sm

