import quex.engine.analyzer.core                          as     analyzer_generator
import quex.engine.state_machine.index                    as     index
from   quex.engine.state_machine.core                     import DFA  
from   quex.engine.misc.tools                             import typed

@typed(loop_sm=DFA, AppendixSmList=[DFA])
def do(loop_sm, AppendixSmList, loop_config, CutSignalLexatomsF):
    """An appendix state machine is a parallel state machine that is pruned by
    its first transition. The first transition is absorbed into the 'loop_map'.
    
    RETURNS: list of FSM-s.
    """
    # (transformed state machines have same id)

    # AppendixSm Ids MUST be unique!
    assert len(set([sm.get_id() for sm in AppendixSmList])) == len(AppendixSmList)

    # Core Loop FSM 
    loop_analyzer,         \
    door_id_loop           = _get_analyzer_for_loop(loop_sm, loop_config, 
                                                    CutSignalLexatomsF)

    # Appendix Analyzers 
    appendix_analyzer_list = _get_analyzer_list_for_appendices(AppendixSmList, 
                                                               loop_config, 
                                                               CutSignalLexatomsF) 
    
    analyzer_list          = [ loop_analyzer ] + appendix_analyzer_list

    # FSM Ids MUST be unique (LEAVE THIS ASSERT IN PLACE!)
    assert len(set(a.state_machine_id for a in analyzer_list)) == len(analyzer_list)

    return analyzer_list, door_id_loop

def _get_analyzer_list_for_appendices(AppendixSmList, loop_config, CutSignalLexatomsF): 
    """Parallel state machines are mounted to the loop by cutting the first
    transition and implementing it in the loop. Upon acceptance of the first
    character the according tail (appendix) of the state machine is entered.

    RETURNS: [0] List of appendix state machines in terms of analyzers.
             [1] Appendix terminals.
    """
    # Appendix Sm Drop Out => Restore position of last loop character.
    # (i)  Couple terminal stored input position in 'LoopRestartP'.
    # (ii) Terminal 'LoopAfterAppendixDropOut' restores that position.
    # Accepting on the initial state of an appendix state machine ensures
    # that any drop-out ends in this restore terminal.
    for init_state in (sm.get_init_state() for sm in AppendixSmList):
        if init_state.has_specific_acceptance_id(): continue
        init_state.set_acceptance()
        init_state.set_specific_acceptance_id(loop_config.iid_loop_after_appendix_drop_out)

    # Appendix FSM List
    return [
        analyzer_generator.do(sm, 
                              loop_config.engine_type, 
                              loop_config.reload_state_extern, 
                              OnBeforeReload = loop_config.events.on_before_reload_in_appendix, 
                              OnAfterReload  = loop_config.events.on_after_reload_in_appendix, 
                              dial_db        = loop_config.dial_db,
                              CutF           = CutSignalLexatomsF)
        for sm in AppendixSmList
    ]

@typed(loop_sm=DFA)
def _get_analyzer_for_loop(loop_sm, loop_config, 
                           CutSignalLexatomsF):
    """Construct a state machine that triggers only on one character. Actions
    according the the triggered character are implemented using terminals which
    are entered upon acceptance.

            .------.
       ---->| Loop |
            |      |----> accept A                 (normal loop terminals)
            |      |----> accept B
            |      |----> accept C
            :      :         :
            |      |----> accept CoupleIncidenceA  (couple terminals towards
            |      |----> accept CoupleIncidenceB   appendix state machines)
            |      |----> accept CoupleIncidenceC    
            :______:         :
            | else |----> accept iid_loop_exit
            '------'

    RETURNS: [0] Loop analyzer (prepared state machine)
             [1] DoorID of loop entry
    """

    # Loop FSM
    analyzer = analyzer_generator.do(loop_sm, 
                                     loop_config.engine_type, 
                                     loop_config.reload_state_extern, 
                                     OnBeforeReload = loop_config.events.on_before_reload, 
                                     OnAfterReload  = loop_config.events.on_after_reload,
                                     OnBeforeEntry  = loop_config.events.on_loop_entry, 
                                     dial_db        = loop_config.dial_db,
                                     OnReloadFailureDoorId = loop_config.door_id_on_reload_failure, 
                                     CutF                  = CutSignalLexatomsF)

    # If reload state is generated 
    # => All other analyzers MUST use the same generated reload state.
    if loop_config.reload_state_extern is None:
        loop_config.reload_state_extern = analyzer.reload_state

    # Set the 'Re-Entry' Operations.
    entry       = analyzer.init_state().entry
    tid_reentry = entry.enter_OpList(analyzer.init_state_index, index.get(), 
                                     loop_config.events.on_loop_reentry)
    entry.categorize(analyzer.init_state_index)

    return analyzer, entry.get(tid_reentry).door_id

