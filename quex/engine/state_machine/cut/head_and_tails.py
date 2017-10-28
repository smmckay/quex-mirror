"""PURPOSE: Head and Tails

This module prunes DFAs with respect to the set of 'front acceptance states'.
A front acceptance state is an acceptance state which can be reached without
stepping over any other acceptance state.

Head: Is the graph of the state machine starting from the initial state until
      a front acceptance state is reached. The acceptance state is overtaken,
      but none of its transitions.

Tail: Is the complete reachable graph of a state machine starting from a 
      front acceptance state.
      
A DFA has, obviously, only one head but potentially more than one tail. 
"""
from   quex.engine.state_machine.core         import DFA
from   quex.engine.state_machine.state.core   import DFA_State
import quex.engine.state_machine.index        as     state_index

def head(Dfa):
    """Generates a DFA containing a copy of the 'Dfa's graph starting
    from the initial state until the first front acceptance state is reached.

    RETURN: DFA containing the 'head' of 'Dfa'.
    """
    overtake_set, \
    front_set     = __find_front_acceptance_states(Dfa)

    correspondance_db = {
        si: state_index.get() for si in overtake_set
    }
    result = DFA(InitStateIndex = correspondance_db[Dfa.init_state_index])
    for si in overtake_set:
        if si not in front_set:
            result_state = Dfa.states[si].clone(correspondance_db)
        else:
            result_state = DFA_State()
            result_state.set_acceptance()
        result.states[correspondance_db[si]] = result_state

    return result

def tails(Dfa):
    """Generates for each front acceptance state a copy of the complete
    graph which can be reached inside 'Dfa' starting from it.

    RETURNS: List of DFAs containing a tail for each found acceptance states.
    """
    dummy,    \
    front_set = __find_front_acceptance_states(Dfa)

    return [ __clone_tail(Dfa, si) for si in front_set ]

def __clone_tail(Dfa, StartSi):
    """Starts walking from state 'Si' in Dfa and clones all states which it reaches
    into the result DFA.

    RETURNS: DFA that contains the graph of state machine transitions starting 
             from state 'Si'.
    """
    result            = DFA(AcceptanceF=Dfa.states[StartSi].is_acceptance())
    correspondance_db = { StartSi: result.init_state_index }
    work_list         = [ (StartSi, result.init_state_index) ]
    done_set          = set([StartSi])

    while work_list:
        si, result_si = work_list.pop()
        state         = Dfa.states[si]
        for target_si, trigger_set in state.target_map.get_map().iteritems():
            result_target_si = correspondance_db.get(target_si)
            if result_target_si is None: 
                result_target_si = state_index.get()
                correspondance_db[target_si] = result_target_si

            if target_si not in done_set: 
                work_list.append((target_si, result_target_si))
                done_set.add(target_si)

            result.add_transition(result_si, trigger_set, result_target_si, 
                                  AcceptanceF = state.is_acceptance())

    return result

def __find_front_acceptance_states(Dfa):
    """Finds the first acceptance states which can be reached in the given DFA
    without stepping over another acceptance states.

    RETURNS: [0] List of state indices reached until an acceptance state is hit.
             [1] indices of 'front' acceptance states.
    """
    front_set   = set()
    work_list   = [ (Dfa.init_state_index, Dfa.get_init_state()) ]

    reached_set = set([Dfa.init_state_index])
    if Dfa.get_init_state().is_acceptance(): 
        front_set.add(Dfa.init_state_index)

    while work_list:
        si, state = work_list.pop()
        for target_si in state.target_map.get_map().iterkeys():
            if target_si in reached_set: continue
            reached_set.add(target_si)

            target_state = Dfa.states[target_si]
            if target_state.is_acceptance():
                front_set.add(target_si)
            else:
                work_list.append((target_si, target_state))

    return reached_set, front_set

