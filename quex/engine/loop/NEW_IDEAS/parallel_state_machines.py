from   quex.engine.loop.loop_map                          import MiniTerminal, \
                                                                 LoopMapEntry, \
                                                                 LoopMap, \
                                                                 LoopEventHandlers
import quex.engine.analyzer.door_id_address_label         as     dial
import quex.engine.state_machine.construction.combination as     combination
import quex.engine.state_machine.check.identity           as     identity
from   quex.engine.state_machine.character_counter        import SmLineColumnCountInfo
from   quex.engine.counter                                import CountAction, \
                                                                 CountActionMap, \
                                                                 count_operation_db_with_reference, \
                                                                 count_operation_db_without_reference
from   quex.engine.misc.tools                             import typed

from   quex.blackboard import setup as Setup, Lng
from   quex.constants  import E_CharacterCountType, \
                              E_R

@typed(CaMap=CountActionMap)
def do(CaMap, SmList):
    """Perform separation:
    
         Parallel state machine  ---->    first transition  
                                       +  appendix state machine
    
    The 'first transition' is mounted on the loop state machine triggering an
    acceptance that causes a transit to the appendix state machine. 

    RETURNS: list of LoopMapEntry-s 
    """
    def _append_sm_db_get_combined(appendix_sm_db, AppendixSm):
        id_key      = AppendixSm.get_id()
        combined_sm = appendix_sm_db.get(id_key)
        if id_key not in appendix_sm_db: 
            combined_sm = AppendixSm
            appendix_sm_db[id_key] = combined_sm
        return combined_sm

    def _determine_LoopMapEntry(sm_db, CharacterSet, CA, AppendixSm):
        appendix_sm       = _append_sm_db_get_combined(sm_db, AppendixSm)
        has_transitions_f = appendix_sm.get_init_state().has_transitions()

        return LoopMapEntry(CharacterSet, CA, dial.new_incidence_id(),
                            appendix_sm.get_id(), has_transitions_f)

    first_vs_appendix_sm = [ 
        (first_set, appendix_sm)
        for sm in SmList
        for first_set, appendix_sm in _cut_first_transition(sm, CloneStateMachineId=True)
    ]

    appendix_sm_list = [
        sm for dummy, sm in first_vs_appendix_sm
        if sm.get_init_state().has_transitions()
    ]

    for sm in appendix_sm_list:
        sm.mark_state_origins(sm.get_id())

    distinct_count_action_map = _get_distinct_count_action_map(CaMap, first_vs_appendix_sm)
    distinct                  = _get_disjoint_character_set_map(CaMap, distinct_count_action_map)

    appendix_sm_db   = {}
    loop_map         = [
        _determine_LoopMapEntry(appendix_sm_db, character_set, ca, appendix_sm)
        for character_set, ca, appendix_sm in distinct
    ]

    appendix_lcci_db = _get_appendix_lcci_db(CaMap, appendix_sm_list)

    return loop_map, appendix_sm_list, appendix_lcci_db

def _get_appendix_lcci_db(CaMap, AppendixSmList):
    """RETURNS:

              map (appendix state machine id ---> LCCI)

    Where 'LCCI' is the 'line-column counting information related to the
    appendix state machine.
    """
    return dict(
        (appendix_sm.get_id(), SmLineColumnCountInfo.from_DFA(CaMap, appendix_sm, 
                                                             False, Setup.buffer_encoding))
        for appendix_sm in AppendixSmList
        if appendix_sm.get_init_state().has_transitions()
    )

def _get_distinct_count_action_map(CaMap, first_vs_appendix_sm):
    """Associates first transitions with related appendix state machines.

    INPUT:  [character_set_0 | appendix_sm_0]
            [character_set_1 | appendix_sm_1]
            ...
            [character_set_2 | appendix_sm_N]

    Character sets of first transition are split according to the required
    count actions.

    OUTPUT: [character_set_0 | count_action_A | appendix_sm_0]
            [character_set_0 | count_action_B | appendix_sm_0]
            [character_set_1 | count_action_B | appendix_sm_1]
            [character_set_1 | count_action_A | appendix_sm_1]
            [character_set_1 | count_action_C | appendix_sm_1]
            ...

    RETURNS: list of(character_set, count action, appendix_sm_list)
             associates 'character_set' with: * count action
                                              * appendix_sm_list
    """
    def prepare_count_action(CA):
        if CA.cc_type == E_CharacterCountType.COLUMN:
            if Setup.buffer_encoding.variable_character_sizes_f(): pointer = E_R.LoopRestartP
            else:                                                  pointer = E_R.InputP
            return CountAction(E_CharacterCountType.COLUMN_BEFORE_APPENDIX_SM,
                             pointer, CA.sr, ExtraValue=CA.value)
        else:
            return CA

    return [
        (character_set, prepare_count_action(ca), appendix_sm)
        for trigger_set, appendix_sm in first_vs_appendix_sm
        for character_set, ca in CaMap.iterable_in_sub_set(trigger_set)
    ]

def _get_disjoint_character_set_map(WorkList):
    # pseudo target maps:
    pseudo_target_map_list = [
        dict((i, entry[0])) for i, entry in WorkList # entry[0] = character_set
    ]
    get_intersection_line_up(pseudo_target_map_list)


def _determine_LoopMapEntry(unique_appendix_sm_set, CharacterSet, CA, AppendixSmList):
    # IMPORTANT: In this case the 'appendix_sm.get_id()' IS NOT DISTINCT
    #            => It may not be used as a key!
    new_appendix_sm = combination.do(AppendixSmList, AlllowInitStateAcceptF=True)
    appendix_sm     = unique_appendix_sm_set.add_if_new(new_appendix_sm)
    # 'appendix_sm' might be a state machine that is equivalent to 'new_appendix_sm'

    has_transitions_f = appendix_sm.get_init_state().has_transitions()
    if not has_transitions_f:
        # There is NO appendix after the first transition.
        # => directly goto to terminal of the matched state machine.
        appendix_sm_id = min(sm.get_id() for sm in AppendixSmList)
    else:
        appendix_sm_id = appendix_sm.get_id()

    if CA.cc_type == E_CharacterCountType.COLUMN:
        if Setup.buffer_encoding.variable_character_sizes_f(): pointer = E_R.LoopRestartP
        else:                                                  pointer = E_R.InputP
        ca = CountAction(E_CharacterCountType.COLUMN_BEFORE_APPENDIX_SM,
                         pointer, CA.sr, ExtraValue=CA.value)
    else:
        ca = CA

    return LoopMapEntry(CharacterSet, ca, dial.new_incidence_id(),
                        appendix_sm_id, has_transitions_f)

def _cut_first_transition(sm, CloneStateMachineId=False):
    """Cuts the first transition and leaves the remaining states in place. 
    This solution is general(!) and it covers the case that there are 
    transitions to the init state!
    
    EXAMPLE:
        
        .-- z -->(( 1 ))          z with: (( 1c ))
      .'                   ---\
    ( 0 )--- a -->( 2 )    ---/   a with: ( 2c )-- b ->( 0c )-- z -->(( 1c ))
      \             /                       \           / 
       '-<-- b ----'                         '-<- a ---'

    where '0c', '1c', and '2c' are the cloned states of '0', '1', and '2'.

    RETURNS: list of pairs: (trigger set, pruned state machine)
             
    trigger set = NumberSet that triggers on the initial state to
                  the remaining state machine.

    pruned state machine = pruned cloned version of this state machine
                           consisting of states that come behind the 
                           state which is reached by 'trigger set'.

    ADAPTS:  Makes the init state's successor state the new init state.
    """
    successor_db = sm.get_successor_db()

    if CloneStateMachineId: cloned_sm_id = sm.get_id()
    else:                   cloned_sm_id = None

    return [
        (trigger_set, sm.clone_subset(target_si, 
                                      list(successor_db[target_si]) + [target_si],
                                      cloned_sm_id))
        for target_si, trigger_set in sm.iterable_init_state_transitions()
    ]
