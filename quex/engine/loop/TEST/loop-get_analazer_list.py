# TEST: Generate all FSM-s based on a given LoopMap
#
# This test calls 'analyzer_construction' to generate a list of analyzers
# related to a loop map. 
#
# IMPORTANT:
#
#      -- The loop analyzer implements the loop map correctly. 
#      -- All appendix state machines are translated into analyzers.
#      -- For counting, the counting behavior differs if the number 
#         of code units per character is constant or not.
#
# CHOICES: loop         -- only a loop map exists, no appendix state machines.
#          appendix     -- an appendix state machine exists.
#          appendix-wot -- an appendix state machine exists without transitions..
#          non-constttt -- loop map an appendix exist with non-homogeneous
#                          colum number per lexatom.
#
# UNIMPORTANT:
#
#      -- The structure of the analyzers in the list is unimportant;
#         none of them is modified.
#      -- The loop maps constitution is (almost) unimportant. 
# 
# Variations: Column Number per CodeUnit = const. or not.
#             Number of CodeUnits per Character = const. or not.
#
# Both variations are played through by the 'buffer_encoding' being plain Unicode
# or UTF8, thus the choices: 'Unicode' and 'UTF8'. Additionally, two loop maps
# are presented: One with all the same ratios for 'ColumnN/CodeUnit' for all 
# characters and one with differing ratios.
#
# (C) Frank-Rene Schaefer
#------------------------------------------------------------------------------
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

from   quex.engine.state_machine.core             import DFA  
from   quex.engine.misc.interval_handling         import NumberSet, \
                                                         NumberSet_All
import quex.engine.analyzer.door_id_address_label as     dial
from   quex.engine.analyzer.door_id_address_label import DialDB
import quex.engine.state_machine.transformation.core as  bc_factory
import quex.engine.loop.core                      as     loop
import quex.engine.loop.analyzer_construction     as     analyzer_construction
import quex.engine.analyzer.engine_supply_factory as     engine
from   quex.blackboard                            import setup as Setup
from   quex.constants                             import E_CharacterCountType
import quex.output.languages.core                 as     languages
                                                         

from   operator import attrgetter
from   collections import namedtuple

# Test Loop Map Entry
TestLME = namedtuple("TestLME", ("character_set", "iid_couple_terminal", "appendix_sm_id"))

if "--hwut-info" in sys.argv:
    print "Loop: Get All Analyzers."
    print "CHOICES: loop, appendix, appendix-wot, non-const;"
    sys.exit()

dial_db = DialDB()
Setup.language_db = languages.db["C++"]()
Setup.buffer_setup("none", 1, "utf8") 

def test(LoopMap, ColumnNPerCodeUnit):
    global dial_db

    Setup.buffer_encoding.source_set = NumberSet_All()

    # Generate sample state machines from what the loop map tells.
    appendix_sm_list = _get_appendix_sm_list(LoopMap)

    UserOnLoopExitDoorId  = dial_db.new_door_id()
    events = loop.LoopEvents(ColumnNPerCodeUnit, None, UserOnLoopExitDoorId)
    config = loop.LoopConfig(ColumnNPerCodeUnit    = ColumnNPerCodeUnit,
                                    LexemeEndCheckF       = False, 
                                    EngineType            = engine.FORWARD, 
                                    ReloadStateExtern     = None, 
                                    UserOnLoopExitDoorId  = UserOnLoopExitDoorId,
                                    dial_db               = dial_db, 
                                    OnReloadFailureDoorId = None, 
                                    ModeName              = "M", 
                                    Events                = events) 
    config.iid_loop_after_appendix_drop_out = dial.new_incidence_id()


    loop_sm = DFA.from_IncidenceIdMap(
         (lei.character_set, lei.iid_couple_terminal) for lei in LoopMap
    )

    analyzer_list, \
    door_id_loop   = analyzer_construction.do(loop_sm, appendix_sm_list, config, True) 

    print_this(analyzer_list)

def _get_appendix_sm_list(LoopMap):
    def get_sm(SmId, Trigger):
        sm = DFA.from_IncidenceIdMap([
            (NumberSet.from_range(Trigger, Trigger + 1), SmId)
        ])
        sm.set_id(SmId)
        return sm

    sm_ids = set(lei.appendix_sm_id for lei in LoopMap
                 if lei.appendix_sm_id is not None)
    return [
        get_sm(SmId=appendix_sm_id, Trigger = 0xB612 + i) 
        for i, appendix_sm_id in enumerate(sm_ids)
    ]

def print_drop_out(analyzer):
    done = set()
    for ta in sorted(analyzer.drop_out.entry.itervalues(), key=attrgetter("door_id")):
        if ta.door_id in done: continue
        assert len(ta.command_list) == 1
        cmd = ta.command_list[0]
        print "%s => %s" % (ta.door_id, cmd.content.router_element)
        done.add(ta.door_id)

def print_this(AnalyzerList):
    print "#_[ Print %i analyzer(s) ]______________________________" % len(AnalyzerList)
    print
    for i, analyzer in enumerate(AnalyzerList):
        print "--( %i: init si = %i )-------------------------\n" % (i, analyzer.init_state_index)
        print analyzer
        print_drop_out(analyzer)


NS_A = NumberSet.from_range(0x600, 0x601) # UTF8: D8 80 => 216, 128
NS_B = NumberSet.from_range(0x601, 0x602) # UTF8: D8 81 => 216, 129
NS_C = NumberSet.from_range(0x640, 0x641) # UTF8: D9 80 => 217, 128

appendix_sm_id = 4711L

if "loop" in sys.argv:
    loop_map = loop.LoopMap([
        TestLME(NS_A, dial.new_incidence_id(), None),
    ])
    column_n_per_code_unit = 5
elif "appendix" in sys.argv:
    loop_map = loop.LoopMap([
        TestLME(NS_A, dial.new_incidence_id(), appendix_sm_id), # appendix_sm_id
    ])
    column_n_per_code_unit = 5
elif "appendix-wot" in sys.argv:
    loop_map = loop.LoopMap([
        TestLME(NS_A, dial.new_incidence_id(), None),
    ])
    column_n_per_code_unit = 5
elif "non-const" in sys.argv:
    loop_map = loop.LoopMap([
        TestLME(NS_A, dial.new_incidence_id(), None),
        TestLME(NS_B, dial.new_incidence_id(), appendix_sm_id), # appendix_sm_id
        TestLME(NS_C, dial.new_incidence_id(), None),
    ])
    column_n_per_code_unit = None
else:
    assert False

test(loop_map, column_n_per_code_unit)
