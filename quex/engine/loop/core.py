"""LOOP STATE MACHINES

A 'loop state machine' has a core state machine that loops on incoming
lexatoms 'i' as long as they fall into the set 'L' which it treats. The
first lexatom that does NOT fit 'L' causes an exit from the loop, as
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

Additionally, matching state machines may be mounted to the loop. The following
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
import quex.engine.loop.parallel_state_machines           as     parallel_state_machines
import quex.engine.loop.analyzer_construction             as     analyzer_construction
import quex.engine.loop.terminal_construction             as     terminal_construction
from   quex.engine.loop.loop_map                          import MiniTerminal, \
                                                                 LoopMapEntry, \
                                                                 LoopMap, \
                                                                 LoopConfig, LoopEvents
from   quex.engine.analyzer.door_id_address_label         import DialDB
import quex.engine.analyzer.door_id_address_label         as     dial
import quex.engine.analyzer.engine_supply_factory         as     engine
from   quex.engine.state_machine.core                     import DFA  
from   quex.engine.counter                                import CountActionMap
from   quex.engine.misc.interval_handling                 import NumberSet
from   quex.engine.misc.tools                             import typed
import quex.engine.misc.error                             as     error

from   quex.blackboard import setup as Setup
from   quex.constants  import E_IncidenceIDs

@typed(CaMap=CountActionMap, dial_db=DialDB, 
       ReloadF=bool, LexemeEndCheckF=bool, OnLoopExit=list,
       LoopCharacterSet=(None, NumberSet))
def do(CaMap, LoopCharacterSet=None, ParallelSmTerminalPairList=None, 
       OnLoopExitDoorId=None, BeforeEntryOpList=None, LexemeEndCheckF=False, EngineType=None, 
       ReloadStateExtern=None, dial_db=None,
       OnReloadFailureDoorId=None, ModeName=None, CutSignalLexatomsF=True):
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

    loop_events = LoopEvents(CaMap.get_column_number_per_code_unit(),
                             BeforeEntryOpList, 
                             OnLoopExitDoorId)

    loop_config = LoopConfig(CaMap.get_column_number_per_code_unit(), 
                             LexemeEndCheckF, 
                             EngineType, ReloadStateExtern, 
                             UserOnLoopExitDoorId  = OnLoopExitDoorId,
                             dial_db               = dial_db,
                             OnReloadFailureDoorId = OnReloadFailureDoorId, 
                             ModeName              = ModeName,
                             Events                = loop_events) 

    parallel_terminal_list, \
    parallel_sm_list        = _sm_terminal_pair_list_extract(ParallelSmTerminalPairList)

    # LoopMap: Associate characters with the reactions on their occurrence _____
    #
    loop_map,                  \
    combined_appendix_sm_list, \
    appendix_cmd_list_db       = _get_loop_map(loop_config, CaMap, parallel_sm_list, 
                                               loop_config.iid_loop_exit, LoopCharacterSet)

    # Loop DFA
    loop_sm = DFA.from_IncidenceIdMap(
        ((lei.character_set, lei.iid_couple_terminal) for lei in loop_map),
        DfaId=loop_config.loop_state_machine_id 
    )

    # Loop represented by FSM-s and Terminal-s ________________________________
    analyzer_list, \
    door_id_loop   = analyzer_construction.do(loop_sm, 
                                              combined_appendix_sm_list, 
                                              loop_config, 
                                              CutSignalLexatomsF) 

    if not loop_config.appendix_dfa_present_f():
        loop_config.iid_loop_after_appendix_drop_out = None

    terminal_list = terminal_construction.do(loop_map, loop_config, 
                                             appendix_cmd_list_db, 
                                             parallel_terminal_list,
                                             door_id_loop)

    # Clean the loop map from the 'exit transition'.
    clean_loop_map = [lei for lei in loop_map if lei.iid_couple_terminal != loop_config.iid_loop_exit]
    return analyzer_list, \
           terminal_list, \
           clean_loop_map, \
           door_id_loop, \
           loop_config.get_required_register_set(len(combined_appendix_sm_list) != 0), \
           loop_config.run_time_counter_required_f()

def _sm_terminal_pair_list_extract(ParallelSmTerminalPairList):
    """Terminals and state machines are linked by the 'incidence id'.
    """
    if ParallelSmTerminalPairList is None:
        ParallelSmTerminalPairList = []
    _sm_terminal_pair_list_assert(ParallelSmTerminalPairList)

    parallel_terminal_list = []
    parallel_sm_list       = []
    for sm, terminal in ParallelSmTerminalPairList:
        parallel_terminal_list.append(terminal)
        parallel_sm_list.append(sm)
        sm.mark_state_origins()

    assert all(isinstance(t, MiniTerminal) for t in parallel_terminal_list)
    return parallel_terminal_list, parallel_sm_list

def _sm_terminal_pair_list_assert(SmTerminalList):
    for sm, terminal in SmTerminalList:
        assert isinstance(terminal, MiniTerminal)
        assert sm.get_id() == terminal.incidence_id

@typed(CaMap=CountActionMap, L_subset=(None, NumberSet))
def _get_loop_map(loop_config, CaMap, SmList, IidLoopExit, L_subset):
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
    assert all(_state_machine_tagged_with_matching_incidence_ids(sm) for sm in SmList)
    # State machines are not to be transformed at this point in time
    assert all(not _exists_bad_lexatom_detector_state(sm) for sm in SmList)

    CaMap.prune(Setup.buffer_encoding.source_set)
    L = CaMap.union_of_all()

    L_couple = NumberSet.from_union_of_iterable(
        sm.get_beginning_character_set() for sm in SmList
    )

    # 'plain_list': Transitions to 'normal terminals' 
    #               => perform count action and loop.
    L_plain = L.difference(L_couple)
    if L_subset is not None: L_plain.intersect_with(L_subset)
    L_loop  = L_plain.union(L_couple)
    L_exit  = L_loop.get_complement(Setup.buffer_encoding.source_set)

    plain_list = _get_LoopMapEntry_list_plain(loop_config, CaMap, L_plain)

    exit_list = []
    if not L_exit.is_empty():
        exit_list.append(
            LoopMapEntry(L_exit, IidLoopExit, 
                         Code = loop_config.cmd_list_CA_GotoTerminal(None, IidLoopExit)) 
        )

    # 'couple_list': Transitions to 'couple terminals' 
    #                => connect to appendix state machines
    couple_list,               \
    combined_appendix_sm_list, \
    appendix_cmd_list_db       = parallel_state_machines.do(loop_config, CaMap, SmList)

    assert L_couple.is_equal(NumberSet.from_union_of_iterable( lei.character_set for lei in couple_list))

    result = LoopMap(couple_list, # --> jump to appendix sm-s
                     plain_list,  # --> iterate to loop start
                     exit_list)   # --> exit loop

    return result, combined_appendix_sm_list, appendix_cmd_list_db

@typed(CaMap=CountActionMap)
def _get_LoopMapEntry_list_plain(loop_config, CaMap, L_pure):
    """RETURNS: list of LoopMapEntry-s.

    The list defines the loop behavior for characters which are not transits
    to appendix state machines. The LoopMapEntry-s are setup as below:

         [0] Character set to trigger to a terminal.
         [1] CountAction.
         [2] IncidenceId of the CountAction.
         [3] 'None' indicating: no appendix sm, no 'goto couple state'.
    """
    assert L_pure is not None

    return [
        LoopMapEntry(character_set, 
                     dial.new_incidence_id(), 
                     Code = loop_config.cmd_list_CA_GotoLoopEntry(ca),
                     CA   = ca)
        for character_set, ca in CaMap.iterable_in_sub_set(L_pure)
    ]

def _state_machine_tagged_with_matching_incidence_ids(Sm):
    # All state machines must match the with the incidence id of the state machine id.
    # The acceptance id is used as terminal id later.
    pure_acceptance_id_set = Sm.acceptance_id_set()
    pure_acceptance_id_set.discard(E_IncidenceIDs.MATCH_FAILURE)
    return pure_acceptance_id_set == set([Sm.get_id()]) 

def _exists_bad_lexatom_detector_state(Sm):
    return any(s.is_bad_lexatom_detector() for s in Sm.states.itervalues())

