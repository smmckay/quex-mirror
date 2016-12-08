# (C) 2005-2011 Frank-Rene Schaefer
# ABSOLUTELY NO WARRANTY
###############################################################################
from   quex.engine.state_machine.core          import StateMachine
from   quex.engine.state_machine.state.core    import State
import quex.engine.state_machine.algorithm.nfa_to_dfa as nfa_to_dfa
import quex.engine.state_machine.index         as index
from   quex.engine.misc.tools import typed

@typed(StateMachineList=[StateMachine])
def do(StateMachineList, CommonTerminalStateF=True, CloneF=True):
    """Connect state machines paralell.

       CommonTerminalStateF tells whether the state machines shall trigger 
                            to a common terminal. This may help nfa-to-dfa
                            or hopcroft minimization for ISOLATED patterns.

                            A state machine that consists of the COMBINATION
                            of patterns MUST set this flag to 'False'.

       CloneF               Controls if state machine list is cloned or not.
                            If the single state machines are no longer required after
                            construction, the CloneF can be set to False.

                            If Cloning is disabled the state machines themselves
                            will be altered--which brings some advantage in speed.
    """
    assert len(StateMachineList) != 0
              
    def consider(sm):
        return not sm.is_Empty() and sm.get_init_state().has_transitions()
    # filter out empty state machines from the consideration          
    state_machine_list       = [ sm for sm in StateMachineList if consider(sm) ]
    empty_state_machine_list = [ sm for sm in StateMachineList if not consider(sm) ]

    if len(state_machine_list) < 2:
        if len(state_machine_list) < 1: result = StateMachine()
        elif CloneF:                    result = state_machine_list[0].clone()
        else:                           result = state_machine_list[0]

        return __consider_empty_state_machines(result, empty_state_machine_list)

    # (*) need to clone the state machines, i.e. provide their internal
    #     states with new ids, but the 'behavior' remains. This allows
    #     state machines to appear twice, or being used in 'larger'
    #     conglomerates.
    clone_list = state_machine_list

    # (*) collect all transitions from both state machines into a single one
    #     (clone to ensure unique identifiers of states)
    new_init_state = State() 
    result         = StateMachine(InitState=new_init_state)

    for clone in clone_list:
        result.states.update(clone.states)
        new_init_state.target_map.add_epsilon_target_state(clone.init_state_index)

    # ADDES THIS:
    result = nfa_to_dfa.do(result)
    #if CommonTerminalStateF:
    #    result.mount_to_acceptance_states(new_terminal_state_index,
    #                                      CancelStartAcceptanceStateF=False)

    return __consider_empty_state_machines(result, empty_state_machine_list)

def __consider_empty_state_machines(sm, EmptyStateMachineList):
    """An empty state machine basically means that its init state is going to 
       be merge into the init state of the resulting state machine. 

       If there is an empty state machine with an acceptance, then this is 
       reflected in the origins. Thus, the result's init state becomes an
       acceptance state for that pattern. 
       
       => There is no particular need for an epsilon transition to the common
          new terminal index.
    """
    single_entry = sm.get_init_state().single_entry
    for esm in EmptyStateMachineList:
        single_entry.merge(esm.get_init_state().single_entry)

    return sm

