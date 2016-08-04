from   quex.input.code.core                         import CodeTerminal
from   quex.output.core.variable_db                 import variable_db
import quex.output.core.loop.core                   as     loop
from   quex.output.core.loop.common                 import get_character_sequence, \
                                                           get_on_skip_range_open, \
                                                           line_column_counter_in_loop
from   quex.engine.counter                          import CountActionMap
import quex.engine.analyzer.engine_supply_factory   as     engine
from   quex.engine.operations.operation_list        import Op
import quex.engine.state_machine.index              as     sm_index
from   quex.engine.state_machine.core               import StateMachine
from   quex.engine.misc.interval_handling           import NumberSet_All
import quex.engine.analyzer.door_id_address_label   as     dial
from   quex.engine.analyzer.terminal.core           import Terminal
from   quex.engine.misc.string_handling             import blue_print
from   quex.engine.misc.tools                       import typed
from   quex.blackboard                              import Lng, E_R

def do(Data, ReloadState):

    CaMap           = Data["ca_map"]
    OpenerPattern   = Data["opener_pattern"]
    CloserPattern   = Data["closer_pattern"]
    OnSkipRangeOpen = Data["on_skip_range_open"]
    DoorIdAfter     = Data["door_id_after"]
    dial_db         = Data["dial_db"]

    return get_skipper(ReloadState, OpenerPattern, CloserPattern, OnSkipRangeOpen, 
                       DoorIdAfter, CaMap, dial_db) 

@typed(CaMap=CountActionMap)
def get_skipper(ReloadState, OpenerPattern, CloserPattern, 
                OnSkipRangeOpen, DoorIdAfter, CaMap, dial_db):
    """
                                    .---<---+----------<------+------------------.
                                    |       |                 |                  |
                                    |       | not             | open_n += 1      |  
                                  .------.  | Closer[0]       |                  |
       -------------------------->| Loop +--'                 |                  |
                                  |      |                    | yes              | 
                                  |      |                    |                  |
                                  |      |          .-------------.              |
                                  |      +----->----| Opener[1-N] |              |
                                  |      |          |      ?      |              |
                                  |      |          '-------------'              |
                                  |      |                                       | open_n > 0
                                  |      |          .-------------.              | 
                                  |      +----->----| Closer[1-N] |--------------+------> RESTART
                                  |      |          |      ?      | open_n -= 1    else
                                  |      |          '-------------'             
                                  |      |                             
                                  |  BLC +-->-.  
                              .->-|      |     \                 Reload State 
            .-DoorID(S, 1)--./    '------'      \            .------------------.
         .--| after_reload  |                    \          .---------------.   |
         |  '---------------'                     '---------| before_reload |   |
         |                                                  '---------------'   |
         '---------------------------------------------------|                  |
                                                     success '------------------'     
                                                                     | failure      
                                                                     |            
                                                              .---------------.       
                                                              | SkipRangeOpen |       
                                                              '---------------'                                                                   

    """
    psml        = _get_state_machine_vs_terminal_list(CloserPattern, 
                                                      OpenerPattern,
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
                                    ReloadStateExtern          = ReloadState,
                                    ParallelSmTerminalPairList = psml,
                                    dial_db                    = dial_db) 

    result[0:0] = "%s = 0;\n" % Lng.REGISTER_NAME(E_R.Counter)
    required_register_set.add(E_R.Counter)
    return result, terminal_list, required_register_set 

def _get_state_machine_vs_terminal_list(CloserPattern, OpenerPattern, DoorIdAfter): 
    """Additionally to all characters, the loop shall walk along the 'closer'.
    If the closer matches, the range skipping exits. Characters need to be 
    counted properly.

    RETURNS: list(state machine, terminal)

    The list contains only one single element.
    """
    # Opener Pattern Reaction
    opener_op_list = [
        Op.Increment(E_R.Counter)  
    ]
    # 'Goto loop entry' is added later (loop id unknown, yet).

    # Closer Pattern Reaction
    closer_op_list = [
        Op.Decrement(E_R.Counter),
        Op.GotoDoorIdIfCounterEqualZero(DoorIdAfter)
    ]
    # 'Goto loop entry' is added later (loop id unknown, yet).

    return [ 
        _get_state_machine_and_terminal(OpenerPattern, 
                                        "<SKIP NESTED RANGE OPENER>",
                                        opener_op_list),
        _get_state_machine_and_terminal(CloserPattern, 
                                        "<SKIP NESTED RANGE OPENER>",
                                        closer_op_list)
    ]

def _get_state_machine_and_terminal(Pattern, Name, OpList, dial_db):
    """Create state machine that detects the 'Pattern', names the terminal
    with 'Name', and implements the 'CmdList' in the terminal.

    RETURNS: (state machine, terminal)
    """
    sm = Pattern.sm.clone(StateMachineId=dial.new_incidence_id())
    terminal = loop.MiniTerminal(Lng.COMMAND_LIST(OpList), Name, sm.get_id())
    terminal.set_requires_goto_loop_entry_f()  # --> Goto Loop Entry

    return sm, terminal
