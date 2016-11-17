import quex.engine.state_machine.algorithm.nfa_to_dfa as nfa_to_dfa

def do(sm):
    """Acceptable Pattern:

        If the initial state is an acceptance state, remove acceptance.
    """
    if not sm.is_DFA_compliant():
        sm = nfa_to_dfa.do(sm)

    # (i) and (ii): Invert acceptance behavior. _______________________________
    #
    for state_index, state in sm.states.iteritems():
        if state_index == new_acceptance_state_index: continue
        state.set_acceptance(not state_index in original_acceptance_state_index_set)

    # Delete orphan states (which where acceptance state or connected to them)
    for state_index in sm.get_orphaned_state_index_list():
        del sm.states[state_index]

    return sm

