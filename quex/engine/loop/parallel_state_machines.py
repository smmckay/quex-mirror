from   quex.engine.loop.loop_map                          import LoopMapEntry
import quex.engine.analyzer.door_id_address_label         as     dial
import quex.engine.state_machine.construction.combination as     combination
import quex.engine.state_machine.algebra.intersection     as     intersection
from   quex.engine.state_machine.character_counter        import SmLineColumnCountInfo
from   quex.engine.counter                                import CountAction, \
                                                                 CountActionMap
from   quex.engine.misc.tools                             import typed, flatten_list_of_lists
from   quex.engine.misc.interval_handling                 import NumberSet
import quex.engine.misc.error                             as     error

from   quex.blackboard import setup as Setup
from   quex.constants  import E_CharacterCountType, \
                              E_R, \
                              E_IncidenceIDs

@typed(CaMap=CountActionMap)
def do(loop_config, CaMap, SmList):
    """Perform separation:
    
         Parallel state machine  ---->    first transition  
                                       +  appendix state machine

         Appendix Sm-Id --> Original Sm-Id
    
    The 'first transition' is mounted on the loop state machine triggering an
    acceptance that causes a transit to the appendix state machine. 

    RETURNS: list of LoopMapEntry-s 
    """
    # ESSENTIAL: Delimiter state machines shall never match on a common lexeme!
    _assert_no_intersections(SmList)
    assert all(sm.get_id() is not None for sm in SmList)

    loop_map_1,     \
    original_iid_db = split_first_transition(SmList)
    # loop_map_1: list of [0] first transition character set
    #                     [1] appendix sm with first transition removed
    #
    # original_iid_db:    appendix sm id --> original sm id

    appendix_cmd_list_db = loop_config.get_appendix_terminal_cmd_list_db(
                                CaMap, [sm for cs, sm in loop_map_1],
                                original_iid_db)
    # appendix_cmd_list_db: appendix sm id --> CmdList(count action,
    #                                                  goto original terminal)

    loop_map_2 = \
        split_first_character_set_for_distinct_count_actions(CaMap, 
                                                             loop_map_1)
    # loop_map_2: list of [0] character set where all elements
    #                         require same count actions
    #                     [1] count action 
    #                     [2] appendix sm

    # For a 'state transition' it is required that all character sets
    # in the list are disjoint. Thus, any intersection must build its
    # on entry. Thus, some entries might have more than one appendix.
    loop_map_3 = combine_intersecting_character_sets(loop_map_2)
    # loop_map_2: list of [0] character set no character set intersects
    #                         with any other.
    #                     [1] count action 
    #                     [2] list of (appendix sm)

    # A transition can only enter one state machine, so all appendix
    # state machines related to the same character set must be combined.
    loop_map_4,                   \
    combined_appendix_sm_list_raw = combine_appendix_sm_lists(loop_map_3)
    # loop_map_4: list of [0] (disjoint) character set 
    #                     [1] count action for character set
    #                     [2] state machine id of related combined appendix sm
    # combined_appendix_sm_lists: list of all generated (combined) appendix sm-s

    loop_map_5, \
    combined_appendix_sm_list = determine_CmdLists(loop_config, loop_map_4, 
                                                   combined_appendix_sm_list_raw,
                                                   original_iid_db)
    # loop_map_5: list of [0] (disjoint) character set 
    #                     [1] CmdList = (count action, goto terminal/appendix sm),
    # combined_appendix_sm_list: contains only those combined appendix state machines
    #                            that do have transitions

    loop_map_6 = [
        LoopMapEntry(character_set, 
                     IidCoupleTerminal = dial.new_incidence_id(), 
                     Code              = cmd_list) 
        for character_set, cmd_list in loop_map_5
    ]
    # loop_map_6: list of LoopMapEntry-s

    # There must be a command list for any acceptance in the appendix 
    # state machines. 
    all_acceptance_id_set = flatten_list_of_lists(sm.acceptance_id_set() for sm in combined_appendix_sm_list)
    assert all(iid in appendix_cmd_list_db for iid in all_acceptance_id_set)

    return loop_map_6, combined_appendix_sm_list, appendix_cmd_list_db

def _assert_no_intersections(SmList):
    # ESSENTIAL: Delimiter state machines shall never match on a common lexeme!
    if   len(SmList) == 1: return
    intersection_sm = intersection.do(SmList)
    if   intersection_sm.is_Nothing(): return
    elif intersection_sm.is_Empty(): return
    error.log("Skip range or indentation: Delimiter patterns intersect!\n"
              "(This should have been detected earlier during parsing)")

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

    ADAPTS:  Makes the init state's success state the new init state.
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
        
def split_first_transition(SmList):
    """Perform separation:
    
          state machine  ---->    first transition  
                               +  appendix state machine
    
    for each state machine.

    RETURNS: list of(character set, appendix state machine)

    Character sets MAY INTERSECT, and MAY REQUIRE NON-UNIFORM count actions.
    """
    result = []
    appendix_sm_to_iid_original_db = {}
    for original_sm in SmList:
        iid_original = original_sm.get_id()
        for first_set, appendix_sm in _cut_first_transition(original_sm, CloneStateMachineId=False):
            # Every appendix DFA gets its own 'id'.
            # HOWEVER: Multiple appendix DFAs might match to same 'acceptance id',
            #          => Such DFAs transit to same terminal upon acceptance.
            appendix_sm.mark_state_origins()
            result.append((first_set, appendix_sm))
            assert appendix_sm.get_id() not in appendix_sm_to_iid_original_db
            appendix_sm_to_iid_original_db[appendix_sm.get_id()] = iid_original

    for character_set, appendix_sm in result:
        init_state = appendix_sm.get_init_state()
        if init_state.input_position_store_f():
            error.log("skip/skip_range/indentation/counter implementation.\n"
                      "Inadmissible post context after first character.\n"
                      "(This should have been detected during the parsing process)")

    return result, appendix_sm_to_iid_original_db

def combine_intersecting_character_sets(first_vs_appendix_sm):
    result = []   # list of [0] Character Set
    #                       [1] Count Action related to [0]
    #                       [2] List of appendix state machines related [0]
    # All character sets [0] in the distinct list are NON-OVERLAPPING.
    for character_set, ca, appendix_sm in first_vs_appendix_sm:
        remainder = character_set
        for prev_character_set, prev_ca, prev_appendix_sm_list in result:
            intersection = character_set.intersection(prev_character_set)
            if intersection.is_empty(): 
                continue
            elif intersection.is_equal(prev_character_set):
                prev_appendix_sm_list.append(appendix_sm)
            else:
                prev_character_set.subtract(intersection)
                result.append(
                    (intersection, ca, prev_appendix_sm_list + [appendix_sm])
                )
            remainder.subtract(intersection)
            if remainder.is_empty(): break

        if not remainder.is_empty():
            result.append(
                (remainder, ca, [appendix_sm])
            )
    return result

def combine_appendix_sm_lists(FirstVsAppendixSmList):
    def combine(appendix_sm_db, SmList):
        id_key      = tuple(sorted([sm.get_id() for sm in SmList]))
        combined_sm = appendix_sm_db.get(id_key)
        if combined_sm is None:
            if len(SmList) == 1:
                combined_sm = SmList[0]
            else:
                combined_sm = combination.do(SmList, AlllowInitStateAcceptF=True)
            appendix_sm_db[id_key] = combined_sm
        return combined_sm

    appendix_sm_db = {}
    first_vs_count_action_and_appendix_sm = [
        (character_set, ca, combine(appendix_sm_db, appendix_sm_list))
        for character_set, ca, appendix_sm_list in FirstVsAppendixSmList
    ]
    appendix_sm_list = [
        appendix_sm for appendix_sm in appendix_sm_db.itervalues()
                    if appendix_sm.get_init_state().has_transitions()
    ]
    return first_vs_count_action_and_appendix_sm, appendix_sm_list

def split_first_character_set_for_distinct_count_actions(CaMap, FirstVsAppendixSmList):
    """Each entry in 'FirstVsAppendixSmList' is split up into subsets 
    where the character set has the same count action.

    RETURNS: [0] list of [0] Character Set
                         [1] CountAction related to that character set.
                         [2] Appendix state machine related to that character set.

    The iterable reports character sets for which their is a distinct count
    action and appendix state machine.

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
        for trigger_set, appendix_sm in FirstVsAppendixSmList
            for character_set, ca in CaMap.iterable_in_sub_set(trigger_set)
    ]

def determine_CmdLists(loop_config, LoopMap4, combined_appendix_sm_list, OriginalIidDb):
    result = []
    dispensables = set()
    for character_set, ca, combined_appendix_sm in LoopMap4:
        cmd_list,         \
        appendix_exists_f = loop_config.get_couple_terminal_cmd_list(ca, combined_appendix_sm, 
                                                                     OriginalIidDb)

        result.append((character_set, cmd_list))
        if not appendix_exists_f:
            dispensables.add(combined_appendix_sm.get_id())

    new_combined_appendix_sm_list = [
        sm for sm in combined_appendix_sm_list if sm.get_id() not in dispensables
    ]
    return result, new_combined_appendix_sm_list

