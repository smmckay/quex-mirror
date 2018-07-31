"""LOOP STATE MACHINES

A 'loop state machine' has a core state machine that loops on incoming
lexatoms 'i' as long as they fall into the set 'L' which it treats. The
first lexatom that does not fit 'L' causes an exit from the loop, as
shown below. 
                                    
                    .--<-( next i )--. i in L
                 .----.              |
      --------->( Loop )-------------+----------------> Exit
                 '----'                i not in L


The set 'L' may be divided into subsets 'L0', 'L1', etc. that require
loop-actions. Those actions are implemented by means of terminal states.  With
'NL' as the complementary set to 'L', the more general loop is shown below.

             .---------------( next i )-------------.
             |    .------.                          |
         ----+--->|  L0  |------->[ Terminal 0 ]----+
                  +------+                          |
                  |  L1  |------->[ Terminal 1 ]----+
                  +------+                          |
                  |  L2  |------->[ Terminal 2 ]----'
                  +------+
                  |  NL  |------->[ Terminal Exit ]-----------> Exit
                  '------'

_________________________________
MOUNTING PARALLEL STATE MACHINES:

In parallel, matching state machines may be mounted to the loop. The following
assumption is made:

             .-----------------------------------------------.
             | SM's first transition lexatoms are all IN 'L' |
             '-----------------------------------------------'

The characters of the first transition 'La' in 'SM' are plugged into the loop
state machine causing a transit to a '*couple* terminal'. This couple terminal
enters the remaining state machine, the '*appendix* state machine'.

The position of the entry into the appendix is stored in the loop restart
pointer (here 'ir'). If the appendix fails to match, the loop continues
from there.

      .---<-----------( next i )<----------. 
      |                                    | 
      |                                [ i = ir ]
      |   .------.                         |     
    --+-->: ...  :    Couple               | drop-out 
          +------+    Terminal             |          
          |  La  |--->[ ir = i ]--->( Appendix SM )------->[ Terminal SM ]
          +------+                                  match
          : ...  :
          '------'

DEFINITION: 'SML':  Set of state machines where the first lexatom belongs to
                    'L'. Upon drop-out, it LOOPS back.
__________
PROCEDURE:

(1) -- Determine 'L'.
    -- Generate 'Terminal i' for all subsets 'Li' in 'L'.
       Each terminal transits to the loop start.

(2) Group state machines into: 'SMi':  SM's first lexatom in 'L'.

    (Some state machines may be mentioned in both sets)

(3) -- Determine 'pure L', the set of lexatoms in 'L' which do not appear
                           as first lexatoms in parallel state machines.

    -- Determine ('Li', 'TerminalId', 'Pruned SM') for each SM in 'SMi'.
                  'Li' = subset of 'L'. 
                  'TerminalId' indicates the terminal associated with 'Li'.
                  'Pruned SM' = SM with the first lexatom pruned.

(4) Generate the terminals concerned for looping:

    -- Terminals for each 'La' in 'L': Append transition to loop begin.

    -- Terminals for 'SMi'-drop-outs

(4) Setup:

    -- Transitions for each 'La' in 'L' and 'Terminal a' mount a transition:

          .------------------------( next i )----------.
          |   .------.                                 |
          '-->| Loop |-----( La )---->[ Terminal a ]---'
              '------'

    -- Setup 'store input reference' upon entry in all parallel state machines.
"""
from   quex.input.code.core                               import CodeTerminal
import quex.engine.loop.parallel_state_machines           as     parallel_state_machines
from   quex.engine.loop.loop_map                          import MiniTerminal, \
                                                                 LoopMapEntry, \
                                                                 LoopMap, \
                                                                 LoopEventHandlers
import quex.engine.analyzer.core                          as     analyzer_generator
from   quex.engine.analyzer.terminal.core                 import Terminal
from   quex.engine.analyzer.door_id_address_label         import DialDB, DoorID
import quex.engine.analyzer.door_id_address_label         as     dial
import quex.engine.analyzer.engine_supply_factory         as     engine
from   quex.engine.state_machine.core                     import DFA  
import quex.engine.state_machine.construction.combination as     combination
from   quex.engine.state_machine.character_counter        import SmLineColumnCountInfo
import quex.engine.state_machine.index                    as     index
from   quex.engine.operations.operation_list              import Op, \
                                                                 OpList
from   quex.engine.counter                                import CountAction, \
                                                                 CountActionMap, \
                                                                 count_operation_db_with_reference, \
                                                                 count_operation_db_without_reference
from   quex.engine.misc.interval_handling                 import NumberSet
from   quex.engine.misc.tools                             import typed
import quex.engine.misc.error                             as     error
from   quex.output.counter.pattern                        import map_SmLineColumnCountInfo_to_code

from   quex.blackboard import setup as Setup, Lng
from   quex.constants  import E_CharacterCountType, \
                              E_R

from   itertools   import chain

@typed(CaMap=CountActionMap, dial_db=DialDB, 
       ReloadF=bool, LexemeEndCheckF=bool, OnLoopExit=list,
       LoopCharacterSet=(None, NumberSet))
def do(CaMap, LoopCharacterSet=None, ParallelSmTerminalPairList=None, 
       OnLoopExitDoorId=None, BeforeEntryOpList=None, LexemeEndCheckF=False, EngineType=None, 
       ReloadStateExtern=None, dial_db=None,
       OnReloadFailureDoorId=None, ModeName=None):
    """Generates a structure that 'loops' quickly over incoming characters.

                                                             Loop continues           
        .---------( ++i )-----+--------<-------------------. at AFTER position of 
        |    .------.         |                            | the first lexatom 'ir'.
        '--->|      |         |                            |  
             | pure |-->[ Terminals A ]                    |  
             |  L   |-->[ Terminals B ]                    |
             |      |-->[ Terminals C ]                    |
             +------+                                      | 
             |      |                                  ( i = ir )  
             | LaF  |-->[ Terminals A ]-->-.               | drop-out     
             |      |-->[ Terminals B ]-->. \              | 
             |      |-->[ Terminals C ]-->( ir = i )--[ DFA ]-->[ Terminals X ]
             |      |                                               \
             +------+                                                '-->[ Terminals Y ]
             | Else |----> Exit
             '------'
    
    The terminals may contain a 'lexeme end check', that ensures that the
    borders of a lexeme are not exceeded.  The loop therefore ends:

        (i)   when a character appears, that is not a loop character.
        (ii)  one of the appendix state machine exits.
        (iii) [Optional] if the lexeme end is reached.
        
    At the end of the iteration, the input pointer points to (the begin of) the
    first lexatom behind what is treated.

            [i][i][i]..................[i][i][X][.... 
                                             |
                                          input_p
            
    During the 'loop' possible line/column count commands may be applied. 

    RETURNS: [0] Generated code for related analyzers
             [1] List of terminals to be implemented by caller
             [2] LoopMap (to be plugged into state machine's init state)
             [3] Required register set
    """
    if EngineType is None:
        EngineType = engine.FORWARD

    parallel_terminal_list, \
    parallel_sm_list        = _sm_terminal_pair_list_extract(ParallelSmTerminalPairList)

    iid_loop_exit                    = dial.new_incidence_id()
    iid_loop_after_appendix_drop_out = dial.new_incidence_id() 

    # LoopMap: Associate characters with the reactions on their occurrence ____
    #
    loop_map,         \
    appendix_sm_list, \
    appendix_lcci_db  = _get_loop_map(CaMap, parallel_sm_list, iid_loop_exit, 
                                      dial_db, LoopCharacterSet)
    # Loop DFA
    loop_sm = DFA.from_IncidenceIdMap(
         (lei.character_set, lei.iid_couple_terminal) for lei in loop_map
    )

    event_handler = LoopEventHandlers(CaMap.get_column_number_per_code_unit(), 
                                      LexemeEndCheckF, 
                                      EngineType, ReloadStateExtern, 
                                      UserOnLoopExitDoorId  = OnLoopExitDoorId,
                                      UserBeforeEntryOpList = BeforeEntryOpList,
                                      AppendixSmExistF      = len(appendix_sm_list) != 0,
                                      dial_db               = dial_db,
                                      OnReloadFailureDoorId = OnReloadFailureDoorId, 
                                      ModeName              = ModeName) 

    # Loop represented by FSM-s and Terminal-s ___________________________
    #
    loop_sm          = _encoding_transform(loop_sm)
    appendix_sm_list = [ _encoding_transform(sm) for sm in appendix_sm_list ]

    analyzer_list,   \
    door_id_loop     = _get_analyzer_list(loop_sm, appendix_sm_list, event_handler, 
                                          iid_loop_after_appendix_drop_out)
    event_handler.loop_state_machine_id_set(analyzer_list[0].state_machine_id)

    if not any(lei.appendix_sm_has_transitions_f for lei in loop_map):
        iid_loop_after_appendix_drop_out = None

    terminal_list, \
    run_time_counter_required_f = _get_terminal_list(loop_map, 
                                                     event_handler, 
                                                     appendix_lcci_db, 
                                                     parallel_terminal_list,
                                                     door_id_loop,
                                                     iid_loop_exit, 
                                                     iid_loop_after_appendix_drop_out)

    # Clean the loop map from the 'exit transition'.
    clean_loop_map = [lei for lei in loop_map if lei.iid_couple_terminal != iid_loop_exit]
    return analyzer_list, \
           terminal_list, \
           clean_loop_map, \
           door_id_loop, \
           event_handler.required_register_set , \
           run_time_counter_required_f

def _sm_terminal_pair_list_extract(ParallelSmTerminalPairList):
    if ParallelSmTerminalPairList is None:
        ParallelSmTerminalPairList = []
    _sm_terminal_pair_list_assert(ParallelSmTerminalPairList)

    parallel_terminal_list = []
    parallel_sm_list       = []
    for sm, terminal in ParallelSmTerminalPairList:
        parallel_terminal_list.append(terminal)
        parallel_sm_list.append(sm)

    assert all(isinstance(t, MiniTerminal) for t in parallel_terminal_list)
    return parallel_terminal_list, parallel_sm_list

def _sm_terminal_pair_list_assert(SmTerminalList):
    for sm, terminal in SmTerminalList:
        assert isinstance(terminal, MiniTerminal)
        assert sm.get_id() == terminal.incidence_id

@typed(loop_sm=DFA, AppendixSmList=[DFA])
def _get_analyzer_list(loop_sm, AppendixSmList, EventHandler,
                       IidLoopAfterAppendixDropOut): 
    """An appendix state machine is a parallel state machine that is pruned by
    its first transition. The first transition is absorbed into the 'loop_map'.
    
    RETURNS: list of FSM-s.
    """
    # AppendixSm Ids MUST be unique!
    assert len(set([sm.get_id() for sm in AppendixSmList])) == len(AppendixSmList)

    # Core Loop FSM 
    loop_analyzer,         \
    door_id_loop           = _get_analyzer_for_loop(loop_sm, EventHandler)

    # Appendix Analyzers 
    appendix_analyzer_list = _get_analyzer_list_for_appendices(AppendixSmList, 
                                                               EventHandler, 
                                                               IidLoopAfterAppendixDropOut) 
    
    analyzer_list          = [ loop_analyzer ] + appendix_analyzer_list

    # FSM Ids MUST be unique (LEAVE THIS ASSERT IN PLACE!)
    assert len(set(a.state_machine_id for a in analyzer_list)) == len(analyzer_list)

    return analyzer_list, door_id_loop

def _get_terminal_list(loop_map, EventHandler, 
                       appendix_lcci_db, ParallelMiniTerminalList, 
                       DoorIdLoop,
                       IidLoopExit, IidLoopAfterAppendixDropOut):
    """RETURNS: list of all Terminal-s.
    """
    loop_terminal_list = _get_terminal_list_for_loop(loop_map, EventHandler,
                                                     IidLoopAfterAppendixDropOut, 
                                                     DoorIdLoop, IidLoopExit) 

    run_time_counter_required_f, \
    parallel_terminal_list       = _get_terminal_list_for_appendices(EventHandler, 
                                                                     appendix_lcci_db,
                                                                     ParallelMiniTerminalList)

    return loop_terminal_list + parallel_terminal_list, \
           run_time_counter_required_f

@typed(CaMap=CountActionMap, L_subset=(None, NumberSet))
def _get_loop_map(CaMap, SmList, IidLoopExit, dial_db, L_subset):
    """A loop map tells about the behavior of the core loop. It tells what
    needs to happen as a consequence to an incoming character. Two options:

    L_subset = NumberSet containing characters that are actually part of 
               the loop. 'None' => all characters of 'CaMap' are considered.

        -- Return to loop (normal case)
        -- Enter the tail (appendix) of a parallel state machine.

    RETURNS: List of LoopMapEntry-s. 

    A LoopMapEntry consists of:

       .character_set: Character set that triggers.
       .count_action:  Count action related to the character set.
                       == None, if the character set causes 'loop exit'.
       .iid_couple_terminal:  Incidence Id of terminal that is triggered by character set.
                       -- incidence id of count action terminal, or
                       -- incidence id of couple terminal.
       .appendix_sm:   Appendix state machine
                       -- combined appendix state machines, or
                       -- None, indicating that there is none.
    """
    CaMap.prune(Setup.buffer_encoding.source_set)
    L = CaMap.union_of_all()

    # 'couple_list': Transitions to 'couple terminals' 
    #                => connect to appendix state machines
    couple_list,      \
    appendix_sm_list, \
    appendix_lcci_db  = parallel_state_machines.do(CaMap, SmList, dial_db)

    L_couple = NumberSet.from_union_of_iterable(
        lei.character_set for lei in couple_list
    )

    # 'plain_list': Transitions to 'normal terminals' 
    #               => perform count action and loop.
    L_plain    = L.difference(L_couple)
    if L_subset is not None: L_plain.intersect_with(L_subset)
    plain_list = _get_LoopMapEntry_list_plain(CaMap, L_plain)

    # 'L_exit': Transition to exit
    #           => remaining characters cause exit.
    L_loop = NumberSet.from_union_of_iterable(
        x.character_set for x in chain(couple_list, plain_list)
    )
    L_exit = L_loop.get_complement(Setup.buffer_encoding.source_set)
    if not L_exit.is_empty():
        exit_list = [ LoopMapEntry(L_exit, None, IidLoopExit, None) ]
    else:
        exit_list = []

    result = LoopMap(couple_list, # --> jump to appendix sm-s
                     plain_list,  # --> iterate to loop start
                     exit_list)   # --> exit loop

    return result, appendix_sm_list, appendix_lcci_db

@typed(CaMap=CountActionMap)
def _get_LoopMapEntry_list_plain(CaMap, L_pure):
    """RETURNS: list of LoopMapEntry-s.

    The list defines the loop behavior for characters which are not transits
    to appendix state machines. The LoopMapEntry-s are setup as below:

         [0] Character set to trigger to a terminal.
         [1] CountAction.
         [2] IncidenceId of the CountAction.
         [3] 'None' indicating: no appendix sm, no 'goto couple state'.
    """
    assert L_pure is not None
    CountAction.incidence_id_db.clear()
    return [
        LoopMapEntry(character_set, ca, CountAction.incidence_id_db_get(ca), None)
        for character_set, ca in CaMap.iterable_in_sub_set(L_pure)
    ]

@typed(loop_sm=DFA)
def _get_analyzer_for_loop(loop_sm, EventHandler):
    """Construct a state machine that triggers only on one character. Actions
    according the the triggered character are implemented using terminals which
    are entered upon acceptance.

            .------.
       ---->| Loop |
            |      |----> accept A                 (normal loop terminals)
            |      |----> accept B
            |      |----> accept C
            :      :         :
            |      |----> accept CoupleIncidenceA  (couple terminals towards
            |      |----> accept CoupleIncidenceB   appendix state machines)
            |      |----> accept CoupleIncidenceC    
            :______:         :
            | else |----> accept iid_loop_exit
            '------'

    RETURNS: [0] Loop analyzer (prepared state machine)
             [1] DoorID of loop entry
    """

    # Loop FSM
    analyzer = analyzer_generator.do(loop_sm, 
                                     EventHandler.engine_type, 
                                     EventHandler.reload_state_extern, 
                                     OnBeforeReload = EventHandler.on_before_reload, 
                                     OnAfterReload  = EventHandler.on_after_reload,
                                     OnBeforeEntry  = EventHandler.on_loop_entry, 
                                     dial_db        = EventHandler.dial_db,
                                     OnReloadFailureDoorId = EventHandler.door_id_on_reload_failure)

    # If reload state is generated 
    # => All other analyzers MUST use the same generated reload state.
    if EventHandler.reload_state_extern is None:
        EventHandler.reload_state_extern = analyzer.reload_state

    # Set the 'Re-Entry' Operations.
    entry       = analyzer.init_state().entry
    tid_reentry = entry.enter_OpList(analyzer.init_state_index, index.get(), 
                                     EventHandler.on_loop_reentry)
    entry.categorize(analyzer.init_state_index)

    return analyzer, entry.get(tid_reentry).door_id

@typed(loop_map=LoopMap)
def _get_terminal_list_for_loop(loop_map, EventHandler, IidLoopAfterAppendixDropOut, 
                                DoorIdLoop, IidLoopExit):
    """RETURNS: List of terminals of the loop state:

        (i)   Counting terminals: Count and return to loop entry.
        (ii)  Couple terminals:   Count and goto appendix state machine.
        (iii) Exit terminal:      Exit loop.

    The '<LOOP>' terminal serves as an address for the appendix state machines.
    If they fail, they can accept its incidence id and re-enter the loop from
    there.
    """
    door_id_loop_exit = DoorID.incidence(IidLoopExit, EventHandler.dial_db)

    # Terminal: Normal Loop Characters
    # (LOOP EXIT terminal is generated later, see below).
    result = []
    done   = set()
    for lei in loop_map:
        if   lei.iid_couple_terminal in done:        continue
        elif lei.iid_couple_terminal == IidLoopExit: continue
        done.add(lei.iid_couple_terminal)
        result.append(
            EventHandler.get_loop_terminal_code(lei, DoorIdLoop, 
                                                door_id_loop_exit) 
        )

    # Terminal: Re-enter Loop
    if IidLoopAfterAppendixDropOut is not None:
        txt = Lng.COMMAND_LIST(EventHandler.on_loop_after_appendix_drop_out(DoorIdLoop),
                               EventHandler.dial_db)
        result.append(
            Terminal(CodeTerminal(txt),
                     "<LOOP>", IidLoopAfterAppendixDropOut,
                     dial_db=EventHandler.dial_db)
        )

    # Terminal: Exit Loop
    result.append(
        Terminal(CodeTerminal(EventHandler.on_loop_exit_text()), 
                 "<LOOP EXIT>", IidLoopExit,
                 dial_db=EventHandler.dial_db)
    )

    return result

@typed(ParallelMiniTerminalList=[MiniTerminal])
def _get_terminal_list_for_appendices(EventHandler, appendix_lcci_db, 
                                      ParallelMiniTerminalList):
    """RETURNS: [0] true, default counter is required.
                    false, else.
                [1] list of terminals of the appendix state machines.
    """
    run_time_counter_required_f = False
    terminal_list = []
    for mini_terminal in ParallelMiniTerminalList:
        # lcci may be 'None' due to the appendix_sm being empty.
        lcci     = appendix_lcci_db.get(mini_terminal.incidence_id)
        rtcr_f, \
        terminal = EventHandler.get_Terminal_from_mini_terminal(lcci, 
                                                                mini_terminal) 
        terminal_list.append(terminal)
        run_time_counter_required_f |= rtcr_f

    return run_time_counter_required_f, terminal_list

def _get_analyzer_list_for_appendices(AppendixSmList, EventHandler, 
                                      IidLoopAfterAppendixDropOut): 
    """Parallel state machines are mounted to the loop by cutting the first
    transition and implementing it in the loop. Upon acceptance of the first
    character the according tail (appendix) of the state machine is entered.

    RETURNS: [0] List of appendix state machines in terms of analyzers.
             [1] Appendix terminals.
    """
    # Appendix Sm Drop Out => Restore position of last loop character.
    # (i)  Couple terminal stored input position in 'LoopRestartP'.
    # (ii) Terminal 'LoopAfterAppendixDropOut' restores that position.
    # Accepting on the initial state of an appendix state machine ensures
    # that any drop-out ends in this restore terminal.
    for init_state in (sm.get_init_state() for sm in AppendixSmList):
        if init_state.has_specific_acceptance_id(): continue
        init_state.set_acceptance()
        init_state.set_specific_acceptance_id(IidLoopAfterAppendixDropOut)

    # Appendix FSM List
    return [
        analyzer_generator.do(sm, 
                              EventHandler.engine_type, 
                              EventHandler.reload_state_extern, 
                              OnBeforeReload = EventHandler.on_before_reload_in_appendix, 
                              OnAfterReload  = EventHandler.on_after_reload_in_appendix, 
                              dial_db        = EventHandler.dial_db)
        for sm in AppendixSmList
    ]


def _encoding_transform(sm):
    """Transform the given state machines into the buffer's encoding.
    """
    verdict_f, \
    sm_transformed = Setup.buffer_encoding.do_state_machine(sm, 
                                                            BadLexatomDetectionF=Setup.bad_lexatom_detection_f)
    if not verdict_f:
        error.log("Deep error: loop (skip range, skip nested range, indentation, ...)\n"
                  "contained character not suited for given character encoding.")
    return sm_transformed



