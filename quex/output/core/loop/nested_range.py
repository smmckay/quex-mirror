from   quex.input.code.core                         import CodeTerminal
import quex.output.core.loop.core                   as     loop
from   quex.engine.counter                          import CountActionMap
from   quex.engine.operations.operation_list        import Op, OpList
import quex.engine.analyzer.door_id_address_label   as     dial
from   quex.engine.analyzer.terminal.core           import Terminal
from   quex.engine.misc.tools                       import typed
from   quex.blackboard                              import Lng, E_R

def do(Data, ReloadState):

    CaMap           = Data["ca_map"]
    OpenerPattern   = Data["opener_pattern"]
    CloserPattern   = Data["closer_pattern"]
    OnSkipRangeOpen = Data["on_skip_range_open"]
    DoorIdExit      = Data["door_id_exit"]
    dial_db         = Data["dial_db"]

    return get_skipper(ReloadState, OpenerPattern, CloserPattern, OnSkipRangeOpen, 
                       DoorIdExit, CaMap, dial_db) 

@typed(CaMap=CountActionMap)
def get_skipper(ReloadState, OpenerPattern, CloserPattern, 
                OnSkipRangeOpen, DoorIdExit, CaMap, dial_db):
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
    psml, \
    iid_aux_reentry = _get_state_machine_vs_terminal_list(CloserPattern, OpenerPattern,
                                                          DoorIdExit, dial_db)
    engine_type = None # Default
    if ReloadState: engine_type = ReloadState.engine_type

    # The first opening pattern must have matched --> counter = 1
    entry_op_list = OpList(Op.AssignConstant(E_R.Counter, 1))

    analyzer_list,         \
    terminal_list,         \
    loop_map,              \
    door_id_loop,          \
    required_register_set, \
    run_time_counter_f     = loop.do(CaMap,
                                     BeforeEntryOpList          = entry_op_list,
                                     OnLoopExitDoorId           = DoorIdExit,
                                     EngineType                 = engine_type,
                                     ReloadStateExtern          = ReloadState,
                                     ParallelSmTerminalPairList = psml,
                                     dial_db                    = dial_db) 

    reentry_op_list = [
        Op.GotoDoorId(door_id_loop)
    ]
    terminal_list.append(
        Terminal(CodeTerminal(Lng.COMMAND_LIST(reentry_op_list, dial_db)),
                 Name        = "<SKIP NESTED RANGE REENTRY>",
                 IncidenceId = iid_aux_reentry, 
                 dial_db     = dial_db)
    )

    required_register_set.add(E_R.Counter)
    return analyzer_list, \
           terminal_list, \
           required_register_set, \
           run_time_counter_f

def _get_state_machine_vs_terminal_list(CloserPattern, OpenerPattern, DoorIdExit,
                                        dial_db): 
    """Additionally to all characters, the loop shall walk along the 'closer'.
    If the closer matches, the range skipping exits. Characters need to be 
    counted properly.

    RETURNS: [0] list(state machine, terminal)
             [1] incidence id of auxiliary terminal that goto-s to the
                 loop entry.

    The auxiliary terminal is necessary since the DoorID of the loop entry
    cannot be known beforehand.
    """
    # DoorID of loop entry cannot be known beforehand.
    # => generate an intermediate door_id from where the loop is entered.
    iid_aux_reentry     = dial.new_incidence_id()
    door_id_aux_reentry = dial.DoorID.incidence(iid_aux_reentry, dial_db)

    # Opener Pattern Reaction
    opener_op_list = [
        Op.Increment(E_R.Counter),
        Op.GotoDoorId(door_id_aux_reentry)
    ]

    # Closer Pattern Reaction
    closer_op_list = [
        Op.Decrement(E_R.Counter),
        Op.GotoDoorIdIfCounterEqualZero(DoorIdExit),
        Op.GotoDoorId(door_id_aux_reentry)
    ]

    def sm_terminal_pair(Pattern, Name, OpList, dial_db):
        sm       = Pattern.sm.clone(StateMachineId=dial.new_incidence_id())
        terminal = loop.MiniTerminal(Lng.COMMAND_LIST(OpList, dial_db), 
                                     Name, sm.get_id())
        return sm, terminal

    smt_list = [ 
        sm_terminal_pair(OpenerPattern, "<SKIP NESTED RANGE OPENER>",
                         opener_op_list, dial_db),
        sm_terminal_pair(CloserPattern, "<SKIP NESTED RANGE CLOSER>",
                         closer_op_list, dial_db)
    ]

    return smt_list, iid_aux_reentry

