import quex.engine.loop.core                      as     loop
import quex.engine.analyzer.engine_supply_factory   as     engine

def do(CaMap, DoorIdLoopExit, dial_db, LexemeEndCheckF=False):
    """Implement loop based on an 'action map'. The 'CaMap' maps from
    character sets to actions to be accomplished.

    RETURNS: [0] analyzer_list
             [1] terminal_list
             [2] required_register_set
    """

    analyzer_list,         \
    terminal_list,         \
    loop_map,              \
    door_id_loop,          \
    required_register_set, \
    run_time_counter_f     = loop.do(CaMap, 
                                     OnLoopExitDoorId = DoorIdLoopExit,
                                     LexemeEndCheckF  = LexemeEndCheckF,
                                     EngineType       = engine.CHARACTER_COUNTER, 
                                     dial_db          = dial_db)
    assert not run_time_counter_f

    return analyzer_list, terminal_list, required_register_set
