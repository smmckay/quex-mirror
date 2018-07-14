# (C) Frank-Rene Schaefer
#     ABSOLUTELY NO WARRANTY
import quex.engine.state_machine.algorithm.beautifier            as     beautifier
import quex.engine.state_machine.cut.stem_and_branches           as     stem_and_branches
import quex.engine.state_machine.algebra.reverse                 as     reverse
import quex.engine.state_machine.construction.sequentialize      as     sequentialize
from   quex.engine.state_machine.construction.setup_post_context import DFA_Newline
import quex.engine.misc.error                                    as     error
from   quex.constants                                            import E_AcceptanceCondition
from   quex.blackboard                                           import setup as Setup

def do(the_state_machine, pre_context_sm, BeginOfLinePreContextF, BeginOfStreamPreContextF):
    """Sets up a pre-condition to the given state machine. This process
       is entirely different from any concatenation or parallelization
       of state machines. Here, the state machine representing the pre-
       condition is **not** webbed into the original state machine!

       Instead, the following happens:

          -- the pre-condition state machine is inverted, because
             it is to be walked through backwards.
          -- the inverted state machine is marked with the state machine id
             of the_state_machine.        
          -- the original state machine will refer to the inverse
             state machine of the pre-condition.
          -- the initial state origins and the origins of the acceptance
             states are marked as 'pre-conditioned' indicating the id
             of the inverted state machine of the pre-condition.             
    """
    #___________________________________________________________________________________________
    # (*) do some consistency checking   
    # -- state machines with no states are senseless here. 
    assert not the_state_machine.is_Empty() 
    assert pre_context_sm is None or not pre_context_sm.is_Empty()
    # -- trivial pre-conditions should be added last, for simplicity

    #___________________________________________________________________________________________
    if pre_context_sm is None:
        # NOT: 'and ...' !
        if BeginOfLinePreContextF:
            # Set acceptance condition: 'begin of line'.
            for state in the_state_machine.get_acceptance_state_list():
                state.set_acceptance_condition_id(E_AcceptanceCondition.BEGIN_OF_LINE)
        if BeginOfStreamPreContextF:
            # Set acceptance condition: 'begin of stream'.
            for state in the_state_machine.get_acceptance_state_list():
                state.set_acceptance_condition_id(E_AcceptanceCondition.BEGIN_OF_STREAM)
        return None

    # (*) Reverse the state machine of the pre-condition 
    reverse_pre_context = reverse.do(pre_context_sm, EnsureDFA_f=False)
        
    if BeginOfLinePreContextF:
        # Extend the existing pre-context with a preceeding 'begin-of-line'.
        reverse_newline_sm  = reverse.do(DFA_Newline(), EnsureDFA_f=False)
        reverse_pre_context = sequentialize.do([reverse_pre_context, 
                                                reverse_newline_sm])

    # (*) Once an acceptance state is reached no further analysis is necessary.
    stem_and_branches.prune_branches(reverse_pre_context)
    if     Setup.error_on_arbitrary_length_of_pre_context_f \
       and reverse_pre_context.longest_path_to_first_acceptance() is None:
        error.log("Pre-context contains patterns of arbitrary length to first acceptance backwards.")

    # (*) Clean up what has been done by inversion (and optionally 'BeginOfLinePreContextF')
    #     AFTER 'prune_branches' (!)
    reverse_pre_context = beautifier.do(reverse_pre_context)

    # (*) let the state machine refer to it 
    #     [Is this necessary? Is it not enough that the acceptance origins point to it? <fschaef>]
    pre_context_sm_id = reverse_pre_context.get_id()

    # (*) Associate acceptance with pre-context id. 
    for state in the_state_machine.get_acceptance_state_list():
        state.set_acceptance_condition_id(pre_context_sm_id)
    
    return reverse_pre_context

            
