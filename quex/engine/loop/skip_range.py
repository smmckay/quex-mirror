import quex.engine.analyzer.door_id_address_label  as     dial
from   quex.engine.counter                         import CountActionMap
from   quex.engine.misc.tools                      import typed
import quex.engine.loop.core                       as     loop
from   quex.blackboard                             import Lng, E_IncidenceIDs


@typed(CaMap=CountActionMap)
def do(ModeName, CaMap, CloserPattern, DoorIdExit, ReloadState, dial_db):
    """
                                        .---<---+----------<------+
                                        |       |                 |        
                                        |       | not             |       
                                      .------.  | Closer[0]       |       
       ------------------------------>| Loop +--'                 |       
                                      |      |                    | no    
                                      |      |                    |       
                                      |      |          .-------------.          
                                      |      +----->----| Closer[1-N] |------------> RESTART
                                      |      |          |      ?      |   yes           
                                      |      |          '-------------'             
                                      |      |                             
                                      |  BLC +-->-.  
                                  .->-|      |     \                 Reload State 
                .-DoorID(S, 1)--./    '------'      \             .-----------------.
           .----| after_reload  |                    \          .---------------.   |
           |    '---------------'                     '---------| before_reload |   |
           |                                                    '---------------'   |
           '-----------------------------------------------------|                  |
                                                         success '------------------'     
                                                                         | failure      
                                                                         |            
                                                                  .---------------.       
                                                                  | SkipRangeOpen |       
                                                                  '---------------'                                                                   

    """
    psml = _get_state_machine_vs_terminal_list(CloserPattern, dial_db, 
                                               DoorIdExit)

    if ReloadState: engine_type = ReloadState.engine_type
    else:           engine_type = None

    door_id_on_reload_failure = dial.DoorID.incidence(E_IncidenceIDs.SKIP_RANGE_OPEN,
                                                      dial_db)

    analyzer_list,         \
    terminal_list,         \
    loop_map,              \
    door_id_loop,          \
    required_register_set, \
    run_time_counter_f     = loop.do(CaMap,
                                     OnLoopExitDoorId           = DoorIdExit,
                                     EngineType                 = engine_type,
                                     ReloadStateExtern          = ReloadState,
                                     ParallelSmTerminalPairList = psml, 
                                     dial_db                    = dial_db,
                                     OnReloadFailureDoorId      = door_id_on_reload_failure,
                                     ModeName                   = ModeName) 

    return analyzer_list, terminal_list, \
           required_register_set,        \
           run_time_counter_f

def _get_state_machine_vs_terminal_list(CloserPattern, dial_db, DoorIdExit): 
    """Additionally to all characters, the loop shall walk along the 'closer'.
    If the closer matches, the range skipping exits. Characters need to be 
    counted properly.

    RETURNS: list(state machine, terminal)

    The list contains only one single element.
    """
    sm            = CloserPattern.get_cloned_sm(StateMachineId=dial.new_incidence_id())
    code          = [ Lng.GOTO(DoorIdExit, dial_db) ]
    mini_terminal = loop.MiniTerminal(code, "<SKIP RANGE TERMINATED>", sm.get_id())
    return [ (sm, mini_terminal) ]



