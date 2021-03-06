import quex.engine.analyzer.mega_state.path_walker.core  as     paths 
from   quex.engine.analyzer.door_id_address_label        import DialDB
import quex.engine.analyzer.mega_state.path_walker.find  as     find
import quex.engine.analyzer.engine_supply_factory        as     engine
from   quex.engine.analyzer.core                         import FSM
from   quex.constants                                    import E_Compression, \
                                                                E_StateIndices

def find_core(sm, SelectF=False):
    print sm.get_graphviz_string(NormalizeF=False)
    print
    analyzer = FSM.from_DFA(sm, engine.FORWARD, dial_db=DialDB())
    for state in analyzer.state_db.itervalues():
        state.entry.categorize(state.index)
    analyzer.drop_out.entry.categorize(E_StateIndices.DROP_OUT)

    for state in analyzer.state_db.itervalues():
        assert state.transition_map is not None
        state.transition_map = state.transition_map.relate_to_DoorIDs(analyzer, state.index)

    AvailableStateIndexSet = set(analyzer.state_db.keys())
    CompressionType        = E_Compression.PATH
    result = find.do(analyzer, 
                     CompressionType=CompressionType, 
                     AvailableStateIndexSet=AvailableStateIndexSet)

    print "## A character path does (not yet) produce a common door in the global drop-out"
    print "## (this happens in '.finalize()' of the MegaState."
    if SelectF:
        result = paths.select(result)
        paths.path_list_assert_consistency(result, analyzer, AvailableStateIndexSet, CompressionType)

    return result

