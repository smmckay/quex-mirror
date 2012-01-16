"""TODO:

    NOTE: Acceptance Pruning of 'Pre-Contexts', 'Non-Ambigous Post Context'
          and 'Backward Input Position Detectors' happens with the original
          state machines: Module 'state_machine/acceptance_pruning.py'

    (*) Post-pone acceptance storage and position storage as much as 
        possible. This decreases the probability that a transition
        sequence ever hits such places.

    (2) If the state is the terminal of a post-context pattern
        without further transitions, then the input position
        is set to the end of the core pattern. Thus, it does
        not need to be incremented.

    (11) If all successor acceptance states depend on 
         a certain pre-context flag being raised, then
         the first state on that path can drop-out 
         on the condition that the pre-context is not met.

    (12) When a terminal is reached where the paths took 
         care of the pre-context checks, then there is no
         need to check it again in the terminal.

    (16) If no successor acceptance state 'cares' about the lexeme and
         a 'dont-care' acceptance state has been passed, then then reload
         can set the lexeme_start_p to the current input position and 
         reload the buffer from start.

    (17) All non-acceptance states that immediately follow a 'skipper
         state' must cause 'skip-failure' on drop-out.

"""
from   quex.blackboard import E_EngineTypes, E_AcceptanceIDs
from   itertools       import imap

def do(analyzer):

    # (*) Use information about position storage registers that can be shared.
    #     Replace old register values with new ones.
    for state in analyzer.state_db.itervalues():
        # transition_id_to_door_id_db = state.entry.finish(analyzer.position_register_map))
        # analyzer.transition_id_to_entry_id_db.update(
        #    (transition_id, EntryID(state.index, door_id)) \
        #    for transition_id, door_id in transition_id_to_door_id_db.iteritems()
        # )
        state.entry.finish(analyzer.position_register_map)
        state.drop_out.finish(analyzer.position_register_map)

    return analyzer


