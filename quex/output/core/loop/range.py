from   quex.engine.operations.operation_list       import Op
from   quex.engine.analyzer.door_id_address_label  import DoorID, DialDB
import quex.engine.analyzer.door_id_address_label  as     dial
from   quex.engine.counter                         import CountActionMap
import quex.engine.state_machine.index             as     sm_index
from   quex.engine.state_machine.core              import StateMachine
from   quex.engine.misc.tools                      import typed

from   quex.output.core.variable_db                import variable_db
import quex.output.core.loop.core                  as     loop
from   quex.output.core.loop.common                import line_counter_in_loop, \
                                                          get_character_sequence, \
                                                          get_on_skip_range_open, \
                                                          line_column_counter_in_loop
from   quex.blackboard                             import setup as Setup, Lng
from   copy                                        import copy


def do(Data, ReloadState):
    """Functioning see 'get_skipper()'
    """
    CaMap            = Data["ca_map"]
    CloserPattern    = Data["closer_pattern"]
    ModeName         = Data["mode_name"]
    OnSkipRangeOpen  = Data["on_skip_range_open"]
    DoorIdAfter      = Data["door_id_after"]
    dial_db          = Data["dial_db"]

    return get_skipper(ReloadState, CloserPattern, ModeName, OnSkipRangeOpen, 
                       DoorIdAfter, CaMap, dial_db) 

@typed(CaMap=CountActionMap)
def get_skipper(ReloadState, CloserPattern, ModeName, OnSkipRangeOpen, 
                DoorIdAfter, CaMap, dial_db):
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
    psml        = _get_state_machine_vs_terminal_list(CloserPattern, dial_db, 
                                                      DoorIdAfter)
    engine_type = None # Default
    if ReloadState: engine_type = ReloadState.engine_type

    result,               \
    terminal_list,        \
    loop_map,             \
    door_id_beyond,       \
    required_register_set = loop.do(CaMap,
                                    OnLoopExitDoorId  = DoorIdAfter,
                                    LexemeEndCheckF   = False,
                                    LexemeMaintainedF = False,
                                    EngineType        = engine_type,
                                    ReloadStateExtern = ReloadState,
                                    ParallelSmTerminalPairList = psml, 
                                    dial_db           = dial_db) 
    return result, terminal_list, required_register_set

def _get_state_machine_vs_terminal_list(CloserPattern, dial_db, DoorIdAfter): 
    """Additionally to all characters, the loop shall walk along the 'closer'.
    If the closer matches, the range skipping exits. Characters need to be 
    counted properly.

    RETURNS: list(state machine, terminal)

    The list contains only one single element.
    """
    sm            = CloserPattern.sm.clone(StateMachineId=dial.new_incidence_id())
    code          = [ Lng.GOTO(DoorIdAfter, dial_db) ]
    mini_terminal = loop.MiniTerminal(code, "<SKIP RANGE TERMINATED>", sm.get_id())
    return [ (sm, mini_terminal) ]



