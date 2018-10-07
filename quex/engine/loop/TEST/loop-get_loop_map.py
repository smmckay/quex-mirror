# TEST: Generation of Loop Map
#
# A 'loop map' associates characters with what has to happen when they occurr.
#
# This test investigates the generation of the state machines only under three
# circumstances expressed as CHOICES:
#
#   Plain:       no parallel state machines.
#   AppendixNoI: a loop with parallel state machines that 
#                do NOT INTERSECT on the first transition.
#   AppendixI:   a loop with parallel state machines that 
#                do INTERSECT.
#   Split:       a state machine's first transition is split
#                into multipl, because it is related to different
#                count actions.
#
# (C) Frank-Rene Schaefer
#------------------------------------------------------------------------------
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

from   quex.engine.counter                        import CountAction, \
                                                         CountActionMap
from   quex.engine.state_machine.core             import DFA  
from   quex.engine.misc.interval_handling         import NumberSet, \
                                                         NumberSet_All
import quex.engine.analyzer.door_id_address_label as     dial
from   quex.engine.analyzer.door_id_address_label import DialDB
import quex.engine.loop.core                      as     loop
from   quex.constants                             import E_CharacterCountType, E_Op
from   quex.blackboard                            import setup as Setup

NS_A = NumberSet.from_range(ord('A'), ord('A') + 1)
NS_B = NumberSet.from_range(ord('B'), ord('B') + 1)
NS_C = NumberSet.from_range(ord('C'), ord('C') + 1)
NS_D = NumberSet.from_range(ord('D'), ord('D') + 1)

dial_db = DialDB()

if "--hwut-info" in sys.argv:
    print "Loop: Get Loop Map."
    print "CHOICES: Plain, AppendixNoI, AppendixI, Split;"

def test(NsCaList, SM_list=[]):
    global dial_db
    Setup.buffer_encoding.source_set = NumberSet_All()
    ca_map        = CountActionMap.from_list(NsCaList)
    iid_loop_exit = dial.new_incidence_id()

    for sm in SM_list:
        sm.mark_state_origins()

    class Pseudo(loop.LoopConfig):
        def __init__(self, TheDialDb):
            self.dial_db                     = TheDialDb
            self.column_number_per_code_unit = None
            self.lexeme_end_check_f          = False
            self.mode_name                   = "TestMode"

    loop_map,         \
    appendix_sm_list, \
    lcci_db           = loop._get_loop_map(Pseudo(dial_db), 
                                           ca_map, 
                                           SM_list, 
                                           iid_loop_exit, 
                                           NumberSet_All())

    print
    print
    print
    general_checks(loop_map, appendix_sm_list)
    print_this(loop_map, appendix_sm_list)

def general_checks(loop_map, appendix_sm_list):

    print "#_[ Checks ]__________________________________________________"
    print
    print "character sets do not intersect",
    all_set = NumberSet()
    for lei in loop_map:
        assert lei.character_set is not None
        assert not lei.character_set.has_intersection(all_set)
        all_set.unite_with(lei.character_set)
    print "[ok]"

    print "count actions do not appear more than once",
    count_action_couple_set = set()
    count_action_plain_set  = set()
    appendix_sm_id_set      = set()
    print "[ok]"

    ## if "Split" in sys.argv or "Plain" in sys.argv:
    ##     list_id_set = set(sm.get_id() for sm in appendix_sm_list)
    ##     assert appendix_sm_id_set == list_id_set
    ##     print "appendix sm-ids are the same in loop map and sm list: [ok]"
    print "exit character set exits: [%s]" % any(lei.aux_count_action is None for lei in loop_map)

    print

def print_this(loop_map, appendix_sm_list):
    print "#_[ Print ]___________________________________________________"
    print
    for lei in sorted(loop_map, key=lambda x: x.character_set.minimum()):
        print lei.character_set.get_string(Option="hex"), "((%s))" % lei.iid_couple_terminal, lei.code[0],
        if lei.code[0].id == E_Op.GotoDoorId is None: print; continue
        print "<appendix: %s>" % repr(lei.code[-1].content.door_id)

    if not appendix_sm_list: return

    print
    print "#_[ Appendix DFAs ]________________________________"
    print
    for sm in sorted(appendix_sm_list, key=lambda sm: sm.get_id()):
        print "IncidenceId: %s" % sm.get_id()
        print sm
        print

def get_sm_list(FSM0, FSM1, FSM2):
    # SPECIALITIES: -- sm0 and sm1 have an intersection between their second 
    #                  transition.
    #               -- sm1 transits further upon acceptance.
    #               -- sm2 has only one transition.
    # Generate DFA that does not have any intersection with 
    # the loop transitions.
    sm0 = DFA()
    si = sm0.add_transition(sm0.init_state_index, FSM0)
    si = sm0.add_transition(si, NS_A, AcceptanceF=True)
    sm0.states[si].mark_acceptance_id(dial.new_incidence_id())

    sm1 = DFA()
    si0 = sm1.add_transition(sm1.init_state_index, FSM1)
    si  = sm1.add_transition(si0, NS_A, AcceptanceF=True)
    iid1 = dial.new_incidence_id()
    sm1.states[si].mark_acceptance_id(iid1)
    si  = sm1.add_transition(si, NS_B, si0)
    sm1.states[si].mark_acceptance_id(iid1)

    sm2 = DFA()
    si = sm2.add_transition(sm2.init_state_index, FSM2, AcceptanceF=True)
    sm2.states[si].mark_acceptance_id(dial.new_incidence_id())

    return [sm0, sm1, sm2]

def get_ca_list(L0, L1):
    ns_0         = NumberSet.from_range(L0, L1)
    return [
        (ns_0,         CountAction(E_CharacterCountType.COLUMN, 0)),
        # (ns_remainder, None),
        # (ns_remainder, CountAction(E_CharacterCountType.COLUMN, 4711)),
    ]

if "Plain" in sys.argv:
    # No parallel state machines
    test([
        (NumberSet.from_range(0,    0x10), CountAction(E_CharacterCountType.COLUMN, 0)),
        (NumberSet.from_range(0x20, 0x30), CountAction(E_CharacterCountType.LINE,   1)),
        (NumberSet.from_range(0x40, 0x50), CountAction(E_CharacterCountType.GRID,   2)),
        (NumberSet.from_range(0x60, 0x70), CountAction(E_CharacterCountType.COLUMN, 3)),
    ])

elif "AppendixNoI" in sys.argv:
    # Three state machines (no one intersects):
    # 
    # First Trans. sm0:         0x10-0x1F
    # First Trans. sm1:                   0x20-0x2F
    # First Trans. sm2:                             0x30-0x3F
    #
    ca_list = get_ca_list(0x10, 0x40)
    sm_list = get_sm_list(NumberSet.from_range(0x10, 0x20), 
                          NumberSet.from_range(0x20, 0x30), 
                          NumberSet.from_range(0x30, 0x40))

    for sm in sm_list:
        test(ca_list, [sm])
    test(ca_list, sm_list)

elif "AppendixI" in sys.argv:
    # Three state machines (no one intersects):
    # 
    # First Trans. sm0:         0x10 -               0x3F
    # First Trans. sm1:                0x20 -              0x4F
    # First Trans. sm2:                       0x30 -            0x5F
    #                           |  1  | 1&2  |   1&2&3   | 2&3 | 3  |  
    #
    ca_list = get_ca_list(0x10, 0x60)
    sm_list = get_sm_list(NumberSet.from_range(0x10, 0x40), 
                          NumberSet.from_range(0x20, 0x50), 
                          NumberSet.from_range(0x30, 0x60))

    # Test for each 'sm' in 'sm_list' is superfluous. 
    # It is done in 'AppendixNoI'.
    test(ca_list, sm_list)

elif "Split" in sys.argv:
    # A first transition of a state machine is separated into two, because
    # it is covered by more than one different count action.
    NS1 = NumberSet.from_range(0x10, 0x20)
    NS2 = NumberSet.from_range(0x20, 0x30)
    NS3 = NumberSet.from_range(0x30, 0x40)
    NS4 = NumberSet.from_range(0x40, 0x50)
    ca_list = [
        (NS1, CountAction(E_CharacterCountType.COLUMN, 1)),
        (NS2, CountAction(E_CharacterCountType.COLUMN, 2)),
        (NS3, CountAction(E_CharacterCountType.COLUMN, 3)),
        (NS4, CountAction(E_CharacterCountType.COLUMN, 4)),
    ]

    sm  = DFA()
    si  = sm.init_state_index
    iid = dial.new_incidence_id()
    ti0 = sm.add_transition(si, NumberSet.from_range(0x1A, 0x4B))
    ac0 = sm.add_transition(ti0, NS_A, AcceptanceF=True)

    test(ca_list, [sm])
