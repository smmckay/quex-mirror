#! /usr/bin/env python
# PURPOSE: creates a state machine that is the repeated version of the 
#          given one. this means, that the success state is linked to the 
#          start state.
import quex.engine.state_machine.construction.sequentialize as sequentialize

def do(the_state_machine, min_repetition_n = 0, max_repetition_n = -1):
    """ Creates a state machine that represents a repetition of the given 
        'the_state_machine'. Minimum and maximim number of repetitions can be specified.
    """
    assert min_repetition_n <= max_repetition_n or max_repetition_n == -1
    def clone_n(SM, N):
        return [SM.clone() for i in range(N)]

    # (*) if minimum number of repetitions is required, then the initial
    #     repetition is produced by sequentialization.
    initial_state_machine = None
    if min_repetition_n != 0:
        # Concatinate the state machine N times, at the beginning, so that 
        # there are N repetitions at least. Any 'bail out' before the first N
        # repetitions happen from a 'non-acceptance' state => fail. Only, when
        # the first N repetitions happend, the state machines enters into the
        # following 'repetition states'.
        # NOTE: sequentialize clones the given state machines 
        sm_list = clone_n(the_state_machine, min_repetition_n)
        initial_state_machine = sequentialize.do(sm_list)

    if max_repetition_n != -1:
        # if a maximum number of repetitions is given, then the state machine needs 
        # to be repeated 'physically'. No new 'repeated' version of the state machine
        # is computed.
        # NOTE: sequentialize clones the given state machines 
        if initial_state_machine is not None: 
            sm_list = [initial_state_machine]
            sm_list.extend(
                clone_n(the_state_machine, (max_repetition_n - min_repetition_n))
            )
            return sequentialize.do(sm_list, 
                                    LeaveIntermediateAcceptanceStatesF = True)
        else:
            sm_list = clone_n(the_state_machine, max_repetition_n)
            concatenation = sequentialize.do(sm_list,
                                             LeaveIntermediateAcceptanceStatesF = True)
            # Here, zero initial repetitions are required, thus the initial state must be
            # an acceptance state.
            concatenation.states[concatenation.init_state_index].set_acceptance(True)                                      
            return concatenation
    else:
        # (*) clone the state machine
        #     NOTE: kleene_closure() clones the state machine.
        pure_repetition = kleene_closure(the_state_machine)
        if initial_state_machine is not None: 
            sm_list = [initial_state_machine, pure_repetition]
            return sequentialize.do(sm_list,
                                    LeaveIntermediateAcceptanceStatesF = True)
        else:
            return pure_repetition

def kleene_closure(the_state_machine):
    """Creates a state machine that is repeated any number of times 
       (zero is also accepted).
       See: Thomson construction.
    """    
    # (*) clone the machine
    result = the_state_machine.clone()

    # (*) add additional initial state
    prev_init_state_index = result.init_state_index
    result.create_new_init_state() 
    result.states[result.init_state_index].target_map.add_epsilon_target_state(prev_init_state_index)

    # (*) add additional terminal state
    new_terminal_state_index = result.create_new_state()

    # (*) connect all acceptance states via epsilon transition 
    #     *backwards* to old initial state.
    #
    #     NOTE: do not cancel the acceptance state of any acceptance state,
    #           so the next step can enter another target state index.
    result.mount_to_acceptance_states(prev_init_state_index,
                                      CancelStartAcceptanceStateF=False)
    # (*) connect all acceptance states via epsilon transition 
    #     *forwards* to terminal state
    result.mount_to_acceptance_states(new_terminal_state_index,
                                      CancelStartAcceptanceStateF=True)

    # (*) add epsilon transition from new init state to new terminal state
    result.add_epsilon_transition(result.init_state_index, new_terminal_state_index, 
                                  RaiseAcceptanceF=True)    

    return result


