from   quex.engine.analyzer.door_id_address_label  import __nice, dial_db
import quex.engine.analyzer.engine_supply_factory  as     engine
from   quex.engine.operations.operation_list       import Op
from   quex.engine.analyzer.door_id_address_label  import DoorID
import quex.output.core.loop                       as     loop
from   quex.engine.counter                         import CountBase
import quex.engine.state_machine.index             as     sm_index
from   quex.engine.state_machine.core              import StateMachine
from   quex.engine.misc.tools                      import typed

from   quex.output.core.variable_db                import variable_db
from   quex.output.core.skipper.common             import line_counter_in_loop, \
                                                          get_character_sequence, \
                                                          get_on_skip_range_open, \
                                                          line_column_counter_in_loop
import quex.output.cpp.counter                     as     counter
from   quex.blackboard                             import setup as Setup, Lng
from   copy                                        import copy


def do(Data, TheAnalyzer):
    """Functioning see 'get_skipper()'
    """
    CounterDb       = Data["counter_db"]
    CloserSequence  = Data["closer_sequence"]
    CloserPattern   = Data["closer_pattern"]
    ModeName        = Data["mode_name"]
    OnSkipRangeOpen = Data["on_skip_range_open"]
    DoorIdAfter     = Data["door_id_after"]

    return get_skipper(TheAnalyzer, CloserSequence, CloserPattern, ModeName, OnSkipRangeOpen, DoorIdAfter, CounterDb) 

@typed(CounterDb=CountBase)
def get_skipper(TheAnalyzer, CloserSequence, CloserPattern, ModeName, OnSkipRangeOpen, DoorIdAfter, CounterDb):
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
    psml             = _get_state_machine_vs_terminal_list(CloserSequence, 
                                                           CounterDb)
    result,          \
    door_id_beyond   = loop.do(CounterDb,
                               OnLoopExitDoorId  = DoorID.continue_without_on_after_match(),
                               LexemeEndCheckF   = False,
                               LexemeMaintainedF = False,
                               EngineType        = engine.FORWARD,
                               ReloadStateExtern = TheAnalyzer.reload_state,
                               ParallelSmTerminalPairList = psml) 
    return result

def _get_state_machine_vs_terminal_list(CloserSequence, CounterDb): 
    """Additionally to all characters, the loop shall walk along the 'closer'.
    If the closer matches, the range skipping exits. Characters need to be 
    counted properly.

    RETURNS: list(state machine, terminal)

    The list contains only one single element.
    """
    sm = StateMachine.from_sequence(CloserSequence)
    sm.set_id(dial_db.new_incidence_id())

    code          = [ Lng.GOTO(DoorID.continue_without_on_after_match()) ]
    mini_terminal = loop.MiniTerminal(code, "<SKIP RANGE TERMINATED>", sm.get_id())
    return [ (sm, mini_terminal) ]



