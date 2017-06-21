#! /usr/bin/env python
import quex.engine.misc.error                           as     error
from   quex.engine.state_machine.core                   import DFA
from   quex.engine.state_machine.state.single_entry     import SeAccept
import quex.engine.state_machine.construction.sequentialize          as     sequentialize
import quex.engine.state_machine.algorithm.beautifier   as     beautifier
import quex.engine.state_machine.construction.ambiguous_post_context as     ambiguous_post_context

from   quex.constants  import E_AcceptanceCondition
from   quex.blackboard import setup as Setup

def do(the_state_machine, post_context_sm, EndOfLinePostContextF, EndOfStreamPostContextF, 
       SourceReference):
    acceptance_id = the_state_machine.get_id()
    result, bipd_sm = _do(the_state_machine, post_context_sm, 
                          EndOfLinePostContextF, EndOfStreamPostContextF, 
                          SourceReference)

    # Make sure that the resulting state machine has the same state machine index
    # as 'the_state_machine'. This is important, since otherwise the precedence get
    # confused.
    result.set_id(acceptance_id)
    return result, bipd_sm

def _do(the_state_machine, post_context_sm, EndOfLinePostContextF, EndOfStreamPostContextF, 
        SourceReference):
    """Appends a post context to the given state machine and changes 
       state infos as required. 

       NOTE: 

           In case that:    post_context_sm is not None 
                         or EndOfLinePostContextF  

           The function appends something to the state machine and
           it is therefore required to pass 'NFA to DFA'--better
           also Hopcroft Minimization.
       
       ________________________________________________________________________
       This process is very similar to sequentialization. 
       There is a major difference, though:
       
       Given a state machine (e.g. a pattern) X with a post context Y, 
       a match is only valid if X is followed by Y. Let Xn be an acceptance
       state of X and Ym an acceptance state of Y: 

              ---(Xn-1)---->(Xn)---->(Y0)----> ... ---->((Ym))
                            store                       acceptance
                            input
                            position
       
       That is, it holds:

          -- The next input position is stored the position of Xn, even though
             it is 'officially' not an acceptance state.

          -- Ym will be an acceptance state, but it will not store 
             the input position!       

       The analysis of the next pattern will start at the position where
       X stopped, even though Ym is required to state acceptance.    
       
    """
    __entry_asserts(the_state_machine, post_context_sm)

    if post_context_sm is None:
        if EndOfLinePostContextF: 
            # Mount 'newline' to existing post context
            post_context_sm = sequentialize.do([the_state_machine, 
                                                DFA_Newline()]) 
        if EndOfStreamPostContextF:
            # Set acceptance condition: 'end of stream'.
            for state in the_state_machine.get_acceptance_state_list():
                state.set_pre_context_id(E_AcceptanceCondition.END_OF_STREAM)

        return the_state_machine, None

    # A post context with an initial state that is acceptance is not really a
    # 'context' since it accepts anything. The state machine remains un-post context.
    if post_context_sm.get_init_state().is_acceptance():
        error.warning("Post context accepts anything--replaced by no post context.",
                      SourceReference)
        return the_state_machine, None
    
    # (*) Two ways of handling post-contexts:
    #
    #     -- Seldom Exception: 
    #        Pseudo-Ambiguous Post Conditions (x+/x) -- detecting the end of the 
    #        core pattern after the end of the post context
    #        has been reached.
    #
    if ambiguous_post_context.detect_forward(the_state_machine, post_context_sm):
        if ambiguous_post_context.detect_backward(the_state_machine, post_context_sm):
            # -- for post contexts that are forward and backward ambiguous
            #    a philosophical cut is necessary.
            error.warning("Post context requires philosophical cut--handle with care!\n"
                      "Proposal: Isolate pattern and ensure results are as expected!", 
                      SourceReference) 
            post_context_sm = ambiguous_post_context.philosophical_cut(the_state_machine, post_context_sm)
        
        # NOTE: May be, the_state_machine does contain now an epsilon transition. See
        #       comment at entry of this function.
        bipd_sm_to_be_inverted = ambiguous_post_context.mount(the_state_machine, post_context_sm)
        the_state_machine      = beautifier.do(the_state_machine)
        return the_state_machine, bipd_sm_to_be_inverted

    # -- The 'normal' way: storing the input position at the end of the core
    #    pattern.
    #
    # (*) Need to clone the state machines, i.e. provide their internal
    #     states with new ids, but the 'behavior' remains. This allows
    #     state machines to appear twice, or being used in 'larger'
    #     conglomerates.
    post_clone = post_context_sm.clone() 

    # -- Once an acceptance state is reached no further analysis is necessary.
    ## NO: acceptance_pruning.do(post_clone)
    ## BECAUSE: it may have to compete with a pseudo-ambiguous post context

    # (*) collect all transitions from both state machines into a single one
    #
    #     NOTE: The start index is unique. Therefore, one can assume that each
    #           clone_list '.states' dictionary has different keys. One can simply
    #           take over all transitions of a start index into the result without
    #           considering interferences (see below)
    #
    orig_acceptance_state_id_list = the_state_machine.get_acceptance_state_index_list()

    # -- mount on every acceptance state the initial state of the following state
    #    machine via epsilon transition
    the_state_machine.mount_to_acceptance_states(post_clone.init_state_index, 
                                                 CancelStartAcceptanceStateF=True)
    for start_state_index, state in post_clone.states.iteritems():        
        the_state_machine.states[start_state_index] = state # states are already cloned

    # -- raise at each old acceptance state the 'store input position flag'
    # -- set the post context flag for all acceptance states
    for state_idx in orig_acceptance_state_id_list:
        state = the_state_machine.states[state_idx]
        state.set_read_position_store_f(True)
    
    # -- no acceptance state shall store the input position
    # -- set the post context flag for all acceptance states
    for state in the_state_machine.get_acceptance_state_list():
        state.set_read_position_store_f(False)
        state.set_read_position_restore_f(True)

    # No input position backward search required
    return beautifier.do(the_state_machine), None

def DFA_Newline():
    """Creates a state machine matching newline according to what has been 
    specified in the setup (Setup.dos_carriage_return_newline_f). 

    That is, if is DOS newline then the state machine represents '\r\n' and
    if it is unix only, then it represents '\n'. If both is required they 
    are implemented in parallel.

    RETURNS: DFA
    """
    UnixF = True
    DosF  = Setup.dos_carriage_return_newline_f

    NL = ord('\n')  # (pure) newline, i.e. line feed
    CR = ord('\r')  # carriage return

    sm = DFA()
    if UnixF:
        sm.add_transition(sm.init_state_index, NL, AcceptanceF=True)
    if DosF:
        idx = sm.add_transition(sm.init_state_index, CR, AcceptanceF=False)
        sm.add_transition(idx, NL, AcceptanceF=True)

    return beautifier.do(sm)

def __entry_asserts(the_state_machine, post_context_sm):
    # DFAs with no states are senseless here. 
    assert not the_state_machine.is_Empty(), \
           "empty state machine can have no post context."
    assert post_context_sm is None or not post_context_sm.is_Empty(), \
           "empty state machine cannot be a post-context."

    # DFAs involved with post condition building are part of a pattern, 
    # but not configured out of multiple patterns. Thus there should be no origins.
    assert the_state_machine.has_origins() == False
    assert post_context_sm is None or not post_context_sm.has_origins()

    for state in the_state_machine.get_acceptance_state_list():
        for cmd in state.single_entry.get_iterable(SeAccept): 
            assert cmd.acceptance_condition_id() == E_AcceptanceCondition.NONE, \
                   "Post Contexts MUST be mounted BEFORE pre-contexts."

