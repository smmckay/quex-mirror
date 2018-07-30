from   quex.engine.loop.loop_map                          import MiniTerminal, \
                                                                 LoopMapEntry, \
                                                                 LoopMap, \
                                                                 LoopEventHandlers
import quex.engine.analyzer.door_id_address_label         as     dial
import quex.engine.state_machine.construction.combination as     combination
import quex.engine.state_machine.index                    as     index
import quex.engine.state_machine.check.identity           as     identity
import quex.engine.state_machine.algebra.intersection     as     intersection
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
def do(CaMap, SmList, dial_db):
    """Perform separation:
    
         Parallel state machine  ---->    first transition  
                                       +  appendix state machine
    
    The 'first transition' is mounted on the loop state machine triggering an
    acceptance that causes a transit to the appendix state machine. 

    RETURNS: list of LoopMapEntry-s 
    """
    def iterable(FirstVsAppendixSmList):
        """YIELDS: [0] Character Set
                   [1] CountAction related to that character set.
                   [2] Appendix state machine related to that character set.

        The iterable reports character sets for which their is a distinct count
        action and appendix state machine.
        """
        for trigger_set, appendix_sm in FirstVsAppendixSmList:
            # id of 'appendix_sm' == id of original parallel state machine!
            for character_set, ca in CaMap.iterable_in_sub_set(trigger_set):
                yield character_set, ca, appendix_sm

    def unique(SmList):
        """RETURNS: list of state machines, where no state machine appears
                    more than once.
        """
        result   = []
        done_set = set()
        for sm in SmList:
            if sm.get_id() in done_set: continue
            done_set.add(sm.get_id())
            result.append(sm)
        return result

    def append_sm_db_get_combined(appendix_sm_db, SmList):
        sm_ulist    = unique(SmList)
        id_key      = tuple(sorted([sm.get_id() for sm in sm_ulist]))
        combined_sm = appendix_sm_db.get(id_key)
        if combined_sm is None:
            if len(sm_ulist) == 1:
                combined_sm = sm_ulist[0]
                combined_sm.mark_state_origins()
            else:
                # TODO: May be, this is never required!
                combined_sm = combination.do(sm_ulist, 
                                             AlllowInitStateAcceptF=True)
            appendix_sm_db[id_key] = combined_sm
        return combined_sm

    def get_appendix_lcci_db(first_vs_appendix_sm):
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

    def get_distinct_map(first_vs_appendix_sm):
        result = []   # list of [0] Character Set
        #                       [1] Count Action related to [0]
        #                       [2] List of appendix state machines related [0]
        # All character sets [0] in the distinct list are NON-OVERLAPPING.
        for character_set, ca, appendix_sm in iterable(first_vs_appendix_sm):
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

    def _determine_LoopMapEntry(sm_db, CharacterSet, CA, AppendixSmList):
        appendix_sm       = append_sm_db_get_combined(sm_db, AppendixSmList)
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

    first_vs_appendix_sm = [ 
        (first_set, appendix_sm)
        for sm in SmList
        for first_set, appendix_sm in _cut_first_transition(sm, CloneStateMachineId=True)
    ]

    appendix_lcci_db = get_appendix_lcci_db(first_vs_appendix_sm)
    distinct         = get_distinct_map(first_vs_appendix_sm)
    loop_map,        \
    appendix_sm_list = get_LoopMap_and_appendix_sm_list(distinct)

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
        
