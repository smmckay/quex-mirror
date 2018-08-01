from   quex.engine.loop.loop_map                          import MiniTerminal, \
                                                                 LoopMapEntry, \
                                                                 LoopMap, \
                                                                 LoopEventHandlers
import quex.engine.analyzer.door_id_address_label         as     dial
import quex.engine.state_machine.construction.combination as     combination
import quex.engine.state_machine.index                    as     index
import quex.engine.state_machine.check.identity           as     identity
import quex.engine.state_machine.algebra.intersection     as     intersection
import quex.engine.state_machine.algebra.union            as     union
from   quex.engine.state_machine.character_counter        import SmLineColumnCountInfo
from   quex.engine.counter                                import CountAction, \
                                                                 CountActionMap, \
                                                                 count_operation_db_with_reference, \
                                                                 count_operation_db_without_reference
from   quex.engine.misc.tools                             import typed
import quex.engine.misc.error                             as     error

from   quex.blackboard import setup as Setup, Lng
from   quex.constants  import E_CharacterCountType, \
                              E_R

from   copy import copy

@typed(CaMap=CountActionMap)
def do(CaMap, SmList):
    """Perform separation:
    
         Parallel state machine  ---->    first transition  
                                       +  appendix state machine
    
    The 'first transition' is mounted on the loop state machine triggering an
    acceptance that causes a transit to the appendix state machine. 

    RETURNS: list of LoopMapEntry-s 
    """
    # ESSENTIAL: Delimiter state machines shall never match on a common lexeme!
    _assert_no_intersections(SmList)

    def get_appendix_lcci_db(AppendixDfaList):
        """The tuples reported by 'iterable()' may contain overlapping character
        sets. That is, their may be multiple parallel state machines that trigger
        on the same characters in a first transition. 
        """
        result = {} # map: appendix state machine id --> LCCI
        for character_set, appendix_sm in first_vs_appendix_sm:
            if not appendix_sm.get_init_state().has_transitions(): continue
            lcci = SmLineColumnCountInfo.from_DFA(CaMap, appendix_sm, False,
                                                  Setup.buffer_encoding)
            result[appendix_sm.get_id()] = lcci
        return result

    def get_LoopMap_and_appendix_sm_list(Distinct):
        # Combine the appendix state machine lists which are related to character
        # sets into a single combined appendix state machine.
        appendix_sm_db   = {}
        loop_map         = [
            _determine_LoopMapEntry(appendix_sm_db, character_set, ca, appendix_sm_list)
            for character_set, ca, appendix_sm_list in distinct
        ]
        appendix_sm_list = [
            appendix_sm for appendix_sm in appendix_sm_db.itervalues()
                        if appendix_sm.get_init_state().has_transitions()
        ]
        return loop_map, appendix_sm_list

    first_vs_appendix_sm = split_first_transition(SmList)
    distinct             = split_distinct_count_actions(CaMap, first_vs_appendix_sm)
    distinct             = combine_intersecting_character_sets(distinct)

    loop_map,        \
    appendix_sm_list = get_LoopMap_and_appendix_sm_list(distinct)

    appendix_lcci_db = get_appendix_lcci_db(first_vs_appendix_sm)

    return loop_map, appendix_sm_list, appendix_lcci_db

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
    for sm in SmList:
        for first_set, appendix_sm in _cut_first_transition(sm, CloneStateMachineId=True):
            # Every appendix DFA gets its own 'id'.
            # HOWEVER: Multiple appendix DFAs might match to same 'acceptance id',
            #          => Such DFAs transit to same terminal upon acceptance.
            ## appendix_sm.set_id(index.get_state_machine_id())
            result.append((first_set, appendix_sm))
    return result

def _assert_no_intersections(SmList):
    # ESSENTIAL: Delimiter state machines shall never match on a common lexeme!
    if   len(SmList) == 1: return
    intersection_sm = intersection.do(SmList)
    if   intersection_sm.is_Nothing(): return
    elif intersection_sm.is_Empty(): return
    error.log("Skip range or indentation: Delimiter patterns intersect!\n"
              "(This should have been detected earlier during parsing)")

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

def NEW_combine_intersecting_character_sets(FirstVsAppendixSmList):
    """First character sets of appendix state machines may intersect.
    Combine the DFAs of the intersection characters sets.

    IMPORTANT: The acceptance ids of the matching state machines remain
               intact!

    RETURNS: list (character set, appendix_sm)

    where the character sets in the list are disjoint.
    """
    # It is conceivable, that character sets of the first transition overlap.
    # => combine those appendices.
    result    = copy(FirstVsAppendixSmList)
    work_list = copy(FirstVsAppendixSmList)
    while work_list:
        new_intersections = []
        for i, entry_i in enumerate(work_list):
            character_set_i, dfa_i = entry_i
            for k, entry_k in enumerate(work_list[i+1:], start=i+1):
                character_set_k, dfa_k = entry_k
                if not character_set_k.has_intersection(character_set_i): continue
                common = character_set_k.intersection(character_set_i)
                new_intersections.append((common, union.do([dfa_i, dfa_k])))
                # Union: check that acceptance ids remain intact!
                character_set_k.subtract(common)
                character_set_i.subtract(common)
        result.extend(new_intersections)
        # If a character set intersects with 'N+1' others, it must at
        # least appear in the set of 'N' intersections.
        # => Consider only 'new_intersections'.
        work_list = new_intersections

    result = [ 
        entry for entry in result if not entry[0].is_empty() 
    ]

    return result

def split_distinct_count_actions(CaMap, FirstVsAppendixSmList):
    """Each entry in 'FirstVsAppendixSmList' is split up into subsets 
    where the character set has the same count action.

    RETURNS: list of [0] Character Set
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

def append_sm_db_get_combined(appendix_sm_db, SmList):
    id_key      = tuple(sorted([sm.get_id() for sm in SmList]))
    combined_sm = appendix_sm_db.get(id_key)
    if combined_sm is None:
        if len(SmList) == 1:
            combined_sm = SmList[0]
            combined_sm.mark_state_origins()
        else:
            combined_sm = combination.do(SmList, AlllowInitStateAcceptF=True)
        appendix_sm_db[id_key] = combined_sm
    return combined_sm

def _determine_LoopMapEntry(sm_db, CharacterSet, CA, AppendixSmList):
    appendix_sm       = append_sm_db_get_combined(sm_db, AppendixSmList)
    has_transitions_f = appendix_sm.get_init_state().has_transitions()
    if not has_transitions_f:
        # There is NO appendix after the first transition.
        # => directly goto to terminal of the matched state machine.
        iid_appendix_terminal = appendix_sm.get_id()
        appendix_sm_id        = None
    else:
        iid_appendix_terminal = appendix_sm.get_id()
        appendix_sm_id        = appendix_sm.get_id()

    return LoopMapEntry(CharacterSet, CA, 
                        IidCoupleTerminal   = dial.new_incidence_id(), 
                        IidAppendixTerminal = iid_appendix_terminal, 
                        AppendixDfaId       = appendix_sm_id) 

def NEW_get_LoopMap_and_appendix_sm_list(Distinct):
    def _get_LoopMapEntry(dfa_list, CharacterSet, CA, AppendixSm):
        if not AppendixSm.get_init_state().has_transitions():
            # NO appendix after the first transition.
            # Not 'None' => directly goto to appendix related terminal
            acceptance_id_list    = AppendixSm.get_acceptance_id_list()
            # Upon entry to the 'loop_map' generator it is ensured that no two
            # DFAs match a common lexeme. => A DFA that matches a single 
            # character set cannot consist of two combined DFAs.
            assert len(acceptance_id_list) == 1
            iid_appendix_terminal = acceptance_id_list[0]
            appendix_dfa_id       = None
        else:
            # 'None' => Do not go directly to appendix terminal
            iid_appendix_terminal = None 
            appendix_dfa_id       = AppendixSm.get_id()
            dfa_list.append(AppendixSm)

        return LoopMapEntry(CharacterSet, CA, 
                            IidCoupleTerminal   = dial.new_incidence_id(),
                            IidAppendixTerminal = iid_appendix_terminal, 
                            AppendixDfaId       = appendix_dfa_id,
                            HasTransitionsF     = AppendixSm.get_init_state().has_transitions())

    appendix_dfa_list = []
    loop_map = [
        _get_LoopMapEntry(appendix_dfa_list, character_set, ca, appendix_sm)
        for character_set, ca, appendix_sm in Distinct
    ]

    return loop_map, appendix_dfa_list

def NEW_cut_first_transition(sm):
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

    return [
        (trigger_set, sm.clone_subset(target_si, 
                                      list(successor_db[target_si]) + [target_si]))
        for target_si, trigger_set in sm.iterable_init_state_transitions()
    ]
        
