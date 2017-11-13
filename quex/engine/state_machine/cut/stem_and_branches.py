"""PURPOSE: Stem and Branches

This module prunes DFAs with respect to the set of 'front acceptance states'.
A front acceptance state is an acceptance state which can be reached without
stepping over any other acceptance state.

Stem: Is the graph of the state machine starting from the initial state until
      a front acceptance state is reached. The acceptance state is overtaken,
      but none of its transitions.

Branch: All graphs from one acceptance state until another acceptance state
      is reached.
      
A DFA has, obviously, only one head but potentially more than one tail. 
"""
from   quex.engine.state_machine.core         import DFA
from   quex.engine.state_machine.state.core   import DFA_State
import quex.engine.state_machine.index        as     state_index

def stem(Dfa):
    """Generates a DFA containing a copy of the 'Dfa's graph starting
    from the initial state until the first front acceptance state is reached.

    RETURN: DFA containing the 'head' of 'Dfa'.
    """
    return __clone_until_acceptance(Dfa, Dfa.init_state_index)

_unit_test_deactivate_branch_pruning_f = False
def prune_branches(Dfa):
    """Modifies the specified 'dfa' so that all branches are removed from it.
    """
    global _unit_test_deactivate_branch_pruning_f
    if _unit_test_deactivate_branch_pruning_f: return

    work_set  = set([Dfa.init_state_index])
    done_set  = set([Dfa.init_state_index])
    while work_set:
        si    = work_set.pop()
        state = Dfa.states[si]

        if state.is_acceptance():
            state.target_map.clear()
        else:
            target_si_iterable = state.target_map.get_target_state_index_list()
            work_set.update(
                target_si for target_si in target_si_iterable 
                          if target_si not in done_set
            )
            done_set.update(target_si_iterable)

    for si in Dfa.states.keys(): # not 'iterkeys()'
        if si not in done_set: Dfa.states.pop(si, None)

def branches(Dfa):
    """Generates for each front acceptance state a copy of the complete
    graph which can be reached inside 'Dfa' starting from it until the next
    acceptance state.

    RETURNS: List of DFAs containing a tail for each found acceptance states.
    """
    return [
        Dfa.clone_subset(acceptance_si, 
                         Dfa.get_successors(acceptance_si))
        for acceptance_si in Dfa.get_acceptance_state_index_list()
    ]

def partials(Dfa):
    """
    """
    predecessor_db = Dfa.get_predecessor_db()
    return [
        Dfa.clone_subset(acceptance_si, 
                         predecessor_db[acceptance_si] + [acceptance_si])
        for acceptance_si in Dfa.get_acceptance_state_index_list()
    ]

def __clone_until_acceptance(Dfa, StartSi):
    """Make a new DFA from the graph between the given 'StartSi' to the 
    until an acceptance state is reached. Walks from a given 'StartSi'
    along all paths until an acceptance state is reached.

    RETURNS: DFA containing the graph.
    """
    correspondance_db = {
        si: state_index.get() for si in Dfa.states
    }
    result = DFA(InitStateIndex = correspondance_db[StartSi],
                 AcceptanceF    = Dfa.states[StartSi].is_acceptance())

    work_set = set([ StartSi ])
    done_set = set([StartSi])
    while work_set:
        si    = work_set.pop()
        state = Dfa.states[si]

        if si == Dfa.init_state_index:
            result_state       = result.get_init_state()
            target_si_iterable = state.target_map.get_target_state_index_list()
        elif not state.is_acceptance():
            result_state       = state.clone(correspondance_db)
            target_si_iterable = state.target_map.get_target_state_index_list()
        else:
            result_state       = DFA_State()
            result_state.set_acceptance()
            target_si_iterable = []

        work_set.update(
            target_si 
            for target_si in target_si_iterable if target_si not in done_set
        )
        result.states[correspondance_db[si]] = result_state

    return result

