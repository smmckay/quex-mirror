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
import quex.engine.analyzer.core                          as     analyzer_generator
from   quex.engine.analyzer.terminal.core                 import Terminal
from   quex.engine.analyzer.door_id_address_label         import DialDB, DoorID
import quex.engine.analyzer.door_id_address_label         as     dial
import quex.engine.analyzer.engine_supply_factory         as     engine
from   quex.engine.state_machine.core                     import StateMachine  
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
from   quex.output.cpp.counter_for_pattern                import map_SmLineColumnCountInfo_to_code

from   quex.blackboard import setup as Setup, Lng
from   quex.constants  import E_CharacterCountType, \
                              E_R

from   itertools   import chain

class MiniTerminal(object):
    __slots__ = ("__code", "name", "incidence_id")
    def __init__(self, Code, Name, IncidenceId):
        self.__code       = Code
        self.name         = Name
        self.incidence_id = IncidenceId

    def get_code(self, LoopStateMachineId):
        """This function may be overwritten, so that LoopStateMachineId
        is used to determine a 'goto' command.
        """
        return self.__code

class LoopMapEntry:
    def __init__(self, CharacterSet, TheCountAction, CoupleIncidenceId, AppendixSmId, 
                 HasTransitionsF=False):
        self.character_set  = CharacterSet
        self.count_action   = TheCountAction
        self.incidence_id   = CoupleIncidenceId
        self.appendix_sm_id = AppendixSmId
        self.appendix_sm_has_transitions_f = HasTransitionsF

    def __repr__(self):
        return "(%s, %s, %s, %s, %s)" % \
               (self.character_set, self.count_action, self.incidence_id, 
                self.appendix_sm_id, self.appendix_sm_has_transitions_f)

class LoopMap(list):
    def __init__(self, *LoopMapEntryLists):
        for lei_list in LoopMapEntryLists:
            self.extend(
                x for x in lei_list if not x.character_set.is_empty()
            )
        self._assert_consistency()

    def _assert_consistency(self):
        assert not any(lei is None for lei in self)
        assert not any(lei.character_set is None for lei in self)
        assert not any(lei.incidence_id is None for lei in self)

        # Assert: Transition triggers do not intersect! 
        total = NumberSet()
        for lei in self:
            assert not lei.character_set.has_intersection(total)
            total.unite_with(lei.character_set)

class LoopEventHandlers:
    """Event handlers in terms of 'List of Operations' (objects of class 'Op'):

        .on_loop_entry:     upon entry into loop
        .on_loop_exit:      upon exit from loop
        .on_loop_reentry:   upon every iteration of loop entry.
        .on_before_reload:             before buffer reload is performed.
        .on_before_reload_in_appendix: as above ... in appendix state machine.
        .on_after_reload:              after buffer reload is performed.
        .on_after_reload_in_appendix:  as above ... in appendix state machine.
    """
    @typed(LexemeEndCheckF=bool, UserOnLoopExitDoorId=DoorID, dial_db=DialDB, 
           OnReloadFailureDoorId=(None, DoorID))
    def __init__(self, ColumnNPerCodeUnit, LexemeEndCheckF, 
                 EngineType, ReloadStateExtern, UserBeforeEntryOpList, 
                 UserOnLoopExitDoorId, AppendixSmExistF, dial_db, OnReloadFailureDoorId): 
        """ColumnNPerCodeUnit is None => no constant relationship between 
                                         column number and code unit.
        """
        self.column_number_per_code_unit = ColumnNPerCodeUnit
        self.lexeme_end_check_f          = LexemeEndCheckF
        self.reload_state_extern         = ReloadStateExtern
        self.engine_type                 = EngineType
        self.dial_db                     = dial_db
        self.door_id_on_reload_failure   = OnReloadFailureDoorId

        # Determine required register set before (required for reload actions)
        self.required_register_set = self.__get_required_register_set(AppendixSmExistF) 

        # Counting Actions upon: loop entry/exit; before/after reload
        #
        on_loop_entry_count,    \
        on_loop_exit_count,     \
        on_before_reload_count, \
        on_after_reload_count   = self.__prepare_count_actions(self.column_number_per_code_unit)

        # Input pointer positioning: loop entry/exit; before/after reload
        #
        on_loop_entry,            \
        on_loop_reentry_pos,      \
        on_loop_exit_pos          = self.__prepare_positioning_at_loop_begin_and_exit()
        on_before_reload_pos,     \
        on_after_reload_pos       = self.__prepare_positioning_before_and_after_reload() 
        on_before_reload_pos_apx, \
        on_after_reload_pos_apx   = self.__prepare_positioning_before_and_after_reload(AppendixSmF=True) 

        # _____________________________________________________________________
        #
        self.Op_goto_on_loop_exit_user_door_id = Op.GotoDoorId(UserOnLoopExitDoorId)

        if UserBeforeEntryOpList is None: UserBeforeEntryOpList = [] 
        self.on_loop_entry      = OpList.concatinate(on_loop_entry, 
                                                     on_loop_reentry_pos, 
                                                     on_loop_entry_count,
                                                     UserBeforeEntryOpList)
        self.on_loop_reentry    = OpList.from_iterable(on_loop_reentry_pos)
        self.on_loop_exit       = OpList.concatinate(on_loop_exit_pos, 
                                                     on_loop_exit_count, 
                                                     [self.Op_goto_on_loop_exit_user_door_id])
                                                     
        self.on_before_reload             = OpList.concatinate(on_before_reload_pos, 
                                                               on_before_reload_count)
        self.on_before_reload_in_appendix = OpList.from_iterable(on_before_reload_pos_apx)

        self.on_after_reload              = OpList.concatinate(on_after_reload_pos, 
                                                              on_after_reload_count)
        self.on_after_reload_in_appendix  = OpList.from_iterable(on_after_reload_pos_apx)

        self.__loop_state_machine_id = None

    def loop_state_machine_id_set(self, SmId):
        assert SmId is not None
        self.__loop_state_machine_id = SmId

    @staticmethod
    def __prepare_count_actions(ColumnNPerCodeUnit):
        # Variable character sizes: store the begin of character in 
        # 'LoopRestartP'. Loop start and character start are the same position.
        if Setup.buffer_codec.variable_character_sizes_f():
            pointer = E_R.LoopRestartP
        else:                                            
            pointer = E_R.InputP

        if ColumnNPerCodeUnit is None: db = count_operation_db_without_reference 
        else:                          db = count_operation_db_with_reference 

        # Count Actions: on loop entry/exit; before/after reload.
        #
        return db[E_CharacterCountType.LOOP_ENTRY](pointer, ColumnNPerCodeUnit), \
               db[E_CharacterCountType.LOOP_EXIT](pointer, ColumnNPerCodeUnit), \
               db[E_CharacterCountType.BEFORE_RELOAD](pointer, ColumnNPerCodeUnit), \
               db[E_CharacterCountType.AFTER_RELOAD](pointer, ColumnNPerCodeUnit)

    def __prepare_positioning_at_loop_begin_and_exit(self):
        """With codecs of dynamic character sizes (UTF8), the pointer to the 
        first letter is stored in 'character_begin_p'. To reset the input 
        pointer 'input_p = character_begin_p' is applied.  
        """
        if Setup.buffer_codec.variable_character_sizes_f():
            # 1 character == variable number of code units
            # => Begin of character must be stored upon entry 
            #    and restored upon exit.
            entry   = [ Op.Assign(E_R.LoopRestartP, E_R.InputP) ]
            reentry = [ Op.Assign(E_R.LoopRestartP, E_R.InputP) ]
            exit    = [ Op.Assign(E_R.InputP, E_R.LoopRestartP) ]
        else:
            # 1 character == 1 code unit
            # => reset to last character: 'input_p = input_p - 1'
            entry   = []
            reentry = []
            exit    = [ Op.Decrement(E_R.InputP) ]

        if self.column_number_per_code_unit is not None:
            entry.append( 
                Op.Assign(E_R.CountReferenceP, E_R.InputP, Condition="COLUMN") 
            )

        return entry, reentry, exit

    def __prepare_positioning_before_and_after_reload(self, AppendixSmF=False):
        """When new content is loaded into the buffer, the positions of the
        pointers must be adapted, so that they point to the same byte as
        before the reload. This function determines the pointer adaptions for 
        all required pointers depending on the 'circumstances'.
        
            AppendixSmF: True  --> generate for appendix state machines
                         False --> generate for main loop
        
        The considered pointers are:

            CountReferenceP --> required for counting with 'delta reference'.
            LoopRestartP    --> Position where to restart loop or 'character':
                                  * if the appendix state machine drops-out.
                                  * if current multi byte character is incomplete.
        
        If the lexeme is not to be maintained, the amount of data to be reloaded
        is maximized by setting the lexeme start pointer to the read pointer.

        ! TODO: The 'Buffer_reload()' function should simply take an array of 
        !       position pointers. Then this function would be (almost) superfluous.

        RETURNS: [0] on_before_reload
                 [1] on_after_reload
        """
        if Setup.buffer_codec.variable_character_sizes_f():
            maintain_loop_restart_p = True
        elif AppendixSmF:
            maintain_loop_restart_p = True
        else:
            maintain_loop_restart_p = False

        # NOTE: The 'CountReferenceP' is not subject to reload, since a 
        #       'delta addition' is done right before reload. After reload,
        #       the pointer is set to the input pointer.

        before = []
        after  = []

        # Before Reload:
        # Just get the 'lexeme_start_p' out of the way, so that anything
        # is filled from 'read_p'.
        before.append(
            Op.Assign(E_R.LexemeStartP, E_R.InputP)
        )

        if maintain_loop_restart_p:
            before.append(
                Op.Assign(E_R.InputPBeforeReload, E_R.InputP)
            )
            before.append(
                Op.PointerAssignMin(E_R.LexemeStartP, E_R.LexemeStartP, E_R.LoopRestartP)
            )

        # After Reload:
        if maintain_loop_restart_p:
            after.append(
                Op.AssignPointerDifference(E_R.PositionDelta, 
                                           E_R.InputP, E_R.InputPBeforeReload),
            )
            after.append(
                Op.PointerAdd(E_R.LoopRestartP, E_R.PositionDelta)
            )

        # Make sure, that the lexeme start pointer makes sense:
        # => begin of input
        after.append(
            Op.Assign(E_R.LexemeStartP, E_R.InputP)
        )

        return before, after

    @typed(LEI=LoopMapEntry)
    def get_loop_terminal_code(self, LEI, DoorIdLoop, DoorIdLoopExit): 
        """RETURNS: A loop terminal. 

        A terminal: (i)    Counts,
                    (ii)   checks possibly for the lexeme end, and
                    (iii)a either re-enters the loop, or
                    (iii)b transits to an appendix state machine (couple terminal).
        """
        IncidenceId    = LEI.incidence_id
        AppendixSmId   = LEI.appendix_sm_id
        TheCountAction = LEI.count_action

        code = []
        if TheCountAction is not None:
            code.extend(TheCountAction.get_OpList(self.column_number_per_code_unit))

        if AppendixSmId is not None: name = "<COUPLE %s>" % IncidenceId
        else:                        name = "<LOOP %s>"   % IncidenceId

        if AppendixSmId is not None:
            #
            # loop map:  lei.character_set --> one of the parallel state machines
            #
            if not LEI.appendix_sm_has_transitions_f:
                # No appendix 
                # => no couple terminal 
                # => goto terminal of parallel state machine.
                code.append(
                    Op.GotoDoorId(DoorID.incidence(AppendixSmId, self.dial_db)) 
                )
            else:
                # Implement: --> couple terminal
                #                (prepare entry into appendix state machine)
                #            --> appendix state machine
                # ASSERT: 
                #  + lexeme end check only required for 'counting' after match. 
                #  + counting does not involve parallel state machines.
                #  => 'parallel state machines' only when 'no lexeme end check'.
                assert not self.lexeme_end_check_f 
                # Couple Terminal: transit to appendix state machine.
                code.extend(
                    self.on_couple_terminal_to_appendix_sm(AppendixSmId)
                )

        elif not self.lexeme_end_check_f: 
            # Loop Terminal: directly re-enter loop.
            code.append(
                Op.GotoDoorId(DoorIdLoop) 
            )
        else:
            # Check Terminal: check against lexeme end before re-entering loop.
            code.append(
                Op.GotoDoorIdIfInputPNotEqualPointer(DoorIdLoop, E_R.LexemeEnd)
            )
            if     self.column_number_per_code_unit is not None \
               and TheCountAction is not None \
               and TheCountAction.cc_type == E_CharacterCountType.COLUMN: 
                # With reference counting, no column counting while looping.
                # => Do it now, before leaving.
                code.append(
                    Op.ColumnCountReferencePDeltaAdd(E_R.InputP, 
                                                     self.column_number_per_code_unit, 
                                                     False)
                )
            code.append(
                self.Op_goto_on_loop_exit_user_door_id 
            )

        return Terminal(CodeTerminal(Lng.COMMAND_LIST(code, self.dial_db)), 
                        name, IncidenceId=IncidenceId,
                        dial_db=self.dial_db)

    def get_Terminal_from_mini_terminal(self, LCCI, mini_terminal):
        if LCCI is not None:
            run_time_counter_required_f, \
            count_code                   = map_SmLineColumnCountInfo_to_code(LCCI) 
            if run_time_counter_required_f:
                # The content to be counted starts where the appendix started.
                # * Begin of counting at 'loop restart pointer'.
                # * Run-time counting can ONLY work, if the lexeme start pointer 
                #   is at position of appendix begin.
                count_code[:0] = Lng.COMMAND(Op.Assign(E_R.LexemeStartP, E_R.LoopRestartP), 
                                             self.dial_db)

            if self.column_number_per_code_unit is not None:
                # If the reference counting is applied, the reference pointer
                # must be set right behind the last counted character.
                count_code.append(
                    Lng.COMMAND(Op.Assign(E_R.CountReferenceP, E_R.InputP, Condition="COLUMN"), self.dial_db)
                )
        else:
            run_time_counter_required_f = False
            count_code = []
        
        assert self.__loop_state_machine_id is not None
        return run_time_counter_required_f, \
               Terminal(CodeTerminal(count_code + mini_terminal.get_code(self.__loop_state_machine_id)), 
                        mini_terminal.name, 
                        mini_terminal.incidence_id, 
                        dial_db=self.dial_db)

    def on_couple_terminal_to_appendix_sm(self, AppendixSmId):
        return [
            # When the appendix drops out, the loop must continue where the
            # appendix has began => Set 'LoopRestartP' to current position.
            Op.Assign(E_R.LoopRestartP, E_R.InputP),
            Op.GotoDoorId(DoorID.state_machine_entry(AppendixSmId, self.dial_db)) 
        ]

    def on_loop_after_appendix_drop_out(self, DoorIdLoop):
        # Upon drop-out, the input position is set to where the apendix 
        # started. Then, the loop is re-entered.
        op_list = []

        if self.column_number_per_code_unit is not None:
            op_list.append(
                Op.Assign(E_R.CountReferenceP, E_R.LoopRestartP, Condition="COLUMN")
            )

        op_list.extend([
            Op.Assign(E_R.InputP, E_R.LoopRestartP),
            Op.GotoDoorId(DoorIdLoop)
        ])

        return op_list
        
    def on_loop_exit_text(self):
        return Lng.COMMAND_LIST(self.on_loop_exit, self.dial_db)

    def __get_required_register_set(self, AppendixSmExistF):
        result = set()
        if self.column_number_per_code_unit is not None:
            result.add((E_R.CountReferenceP, "QUEX_OPTION_COLUMN_NUMBER_COUNTING"))
        if AppendixSmExistF:
            result.add(E_R.LoopRestartP)
        if Setup.buffer_codec.variable_character_sizes_f():
            result.add(E_R.LoopRestartP)
        if     E_R.LoopRestartP in result \
           and self.engine_type.subject_to_reload():
            result.add(E_R.InputPBeforeReload)
            result.add(E_R.PositionDelta)

        return result

@typed(CaMap=CountActionMap, dial_db=DialDB, 
       ReloadF=bool, LexemeEndCheckF=bool, OnLoopExit=list,
       LoopCharacterSet=(None, NumberSet))
def do(CaMap, OnLoopExitDoorId, BeforeEntryOpList=None, LexemeEndCheckF=False, EngineType=None, 
       ReloadStateExtern=None, ParallelSmTerminalPairList=None, dial_db=None,
       LoopCharacterSet=None, OnReloadFailureDoorId=None):
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
             |      |-->[ Terminals C ]-->( ir = i )--[ StateMachine ]-->[ Terminals X ]
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

    event_handler = LoopEventHandlers(CaMap.get_column_number_per_code_unit(), 
                                      LexemeEndCheckF, 
                                      EngineType, ReloadStateExtern, 
                                      UserOnLoopExitDoorId=OnLoopExitDoorId,
                                      UserBeforeEntryOpList=BeforeEntryOpList,
                                      AppendixSmExistF=len(appendix_sm_list) != 0,
                                      dial_db=dial_db,
                                      OnReloadFailureDoorId=OnReloadFailureDoorId) 

    # Loop represented by Analyzer-s and Terminal-s ___________________________
    #
    analyzer_list,      \
    door_id_loop,       \
    appendix_sm_exist_f = _get_analyzer_list(loop_map, event_handler, appendix_sm_list,
                                             iid_loop_after_appendix_drop_out)
    event_handler.loop_state_machine_id_set(analyzer_list[0].state_machine_id)

    if not appendix_sm_exist_f:
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
    clean_loop_map = [lei for lei in loop_map if lei.incidence_id != iid_loop_exit]
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

@typed(loop_map=LoopMap)
def _get_analyzer_list(loop_map, EventHandler, AppendixSmList, 
                       IidLoopAfterAppendixDropOut): 
    """An appendix state machine is a parallel state machine that is pruned by
    its first transition. The first transition is absorbed into the 'loop_map'.
    
    RETURNS: list of Analyzer-s.
    """
    # AppendixSm Ids MUST be unique!
    assert len(set([sm.get_id() for sm in AppendixSmList])) == len(AppendixSmList)

    # Core Loop Analyzer 
    loop_analyzer,         \
    door_id_loop           = _get_analyzer_for_loop(loop_map, EventHandler)

    # Appendix Analyzers 
    appendix_analyzer_list = _get_analyzer_list_for_appendices(loop_map, EventHandler, 
                                                               AppendixSmList,
                                                               IidLoopAfterAppendixDropOut) 
    
    analyzer_list          = [ loop_analyzer ] + appendix_analyzer_list

    # Analyzer Ids MUST be unique (LEAVE THIS ASSERT IN PLACE!)
    assert len(set(a.state_machine_id for a in analyzer_list)) == len(analyzer_list)

    return analyzer_list, \
           door_id_loop, \
           any(lei.appendix_sm_has_transitions_f for lei in loop_map)

def _get_terminal_list(loop_map, EventHandler, 
                       appendix_lcci_db, ParallelMiniTerminalList, 
                       DoorIdLoop,
                       IidLoopExit, IidLoopAfterAppendixDropOut):
    """RETURNS: list of all Terminal-s.
    """
    loop_terminal_list     = _get_terminal_list_for_loop(loop_map, EventHandler,
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
       .incidence_id:  Incidence Id of terminal that is triggered by character set.
                       -- incidence id of count action terminal, or
                       -- incidence id of couple terminal.
       .appendix_sm:   Appendix state machine
                       -- combined appendix state machines, or
                       -- None, indicating that there is none.
    """
    L = CaMap.union_of_all()

    # 'couple_list': Transitions to 'couple terminals' 
    #                => connect to appendix state machines
    couple_list,      \
    appendix_sm_list, \
    appendix_lcci_db  = _get_LoopMapEntry_list_parallel_state_machines(CaMap, 
                                                                       SmList, 
                                                                       dial_db)

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
    universal_set = Setup.buffer_codec.source_set
    L_exit        = L_loop.get_complement(universal_set)
    if not L_exit.is_empty():
        exit_list = [ LoopMapEntry(L_exit, None, IidLoopExit, None) ]
    else:
        exit_list = []

    result = LoopMap(couple_list, plain_list, exit_list)

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

@typed(CaMap=CountActionMap)
def _get_LoopMapEntry_list_parallel_state_machines(CaMap, SmList, dial_db):
    """Perform separation:
    
         Parallel state machine  ---->    first transition  
                                       +  appendix state machine
    
    The 'first transition' is mounted on the loop state machine triggering an
    acceptance that causes a transit to the appendix state machine. 

    RETURNS: list of LoopMapEntry-s 
    """
    def iterable(FirstVsAppendixSmList):
        """YIELDS: [0] Character Set
                   [1] CountAction related to that character set.
                   [2] Appendix state machine related to that character set.

        The iterable reports character sets for which their is a distinct count
        action and appendix state machine.
        """
        for trigger_set, appendix_sm in FirstVsAppendixSmList:
            # id of 'appendix_sm' == id of original parallel state machine!
            for character_set, ca in CaMap.iterable_in_sub_set(trigger_set):
                yield character_set, ca, appendix_sm

    def unique(SmList):
        """RETURNS: list of state machines, where no state machine appears
                    more than once.
        """
        result   = []
        done_set = set()
        for sm in SmList:
            if sm.get_id() in done_set: continue
            done_set.add(sm.get_id())
            result.append(sm)
        return result

    def append_sm_db_get_combined(appendix_sm_db, SmList):
        sm_ulist    = unique(SmList)
        id_key      = tuple(sorted([sm.get_id() for sm in sm_ulist]))
        combined_sm = appendix_sm_db.get(id_key)
        if combined_sm is None:
            if len(sm_ulist) == 1:
                combined_sm = sm_ulist[0]
                combined_sm.mark_state_origins()
            else:
                # TODO: May be, this is never required!
                combined_sm = combination.do(sm_ulist, 
                                             AlllowInitStateAcceptF=True)
            appendix_sm_db[id_key] = combined_sm
        return combined_sm

    def get_appendix_lcci_db(first_vs_appendix_sm):
        """The tuples reported by 'iterable()' may contain overlapping character
            sets. That is, their may be multiple parallel state machines that trigger
            on the same characters in a first transition. 
        """
        result = {} # map: appendix state machine id --> LCCI
        for character_set, appendix_sm in first_vs_appendix_sm:
            if not appendix_sm.get_init_state().has_transitions(): continue
            lcci = SmLineColumnCountInfo.from_StateMachine(CaMap, appendix_sm, 
                                                           False,
                                                           Setup.buffer_codec)
            result[appendix_sm.get_id()] = lcci
        return result

    def get_distinct_map(first_vs_appendix_sm):
        result = []   # list of [0] Character Set
        #                       [1] Count Action related to [0]
        #                       [2] List of appendix state machines related [0]
        # All character sets [0] in the distinct list are NON-OVERLAPPING.
        for character_set, ca, appendix_sm in iterable(first_vs_appendix_sm):
            remainder = character_set
            for prev_character_set, prev_ca, prev_appendix_sm_list in result:
                intersection = character_set.intersection(prev_character_set)
                if intersection.is_empty(): 
                    continue
                elif intersection.is_equal(prev_character_set):
                    prev_appendix_sm_list.append(appendix_sm)
                else:
                    prev_character_set.subtract(intersection)
                    result.append(
                        (intersection, ca, prev_appendix_sm_list + [appendix_sm])
                    )
                remainder.subtract(intersection)
                if remainder.is_empty(): break

            if not remainder.is_empty():
                result.append(
                    (remainder, ca, [appendix_sm])
                )
        return result

    def _determine_LoopMapEntry(sm_db, CharacterSet, CA, AppendixSmList):
        appendix_sm       = append_sm_db_get_combined(sm_db, AppendixSmList)
        has_transitions_f = appendix_sm.get_init_state().has_transitions()
        if not has_transitions_f:
            # There is NO appendix after the first transition.
            # => directly goto to terminal of the matched state machine.
            appendix_sm_id = min(sm.get_id() for sm in AppendixSmList)
        else:
            appendix_sm_id = appendix_sm.get_id()

        if CA.cc_type == E_CharacterCountType.COLUMN:
            if Setup.buffer_codec.variable_character_sizes_f(): pointer = E_R.LoopRestartP
            else:                                               pointer = E_R.InputP
            ca = CountAction(E_CharacterCountType.COLUMN_BEFORE_APPENDIX_SM,
                             pointer, CA.sr)
        else:
            ca = CA

        return LoopMapEntry(CharacterSet, ca, dial.new_incidence_id(),
                            appendix_sm_id, has_transitions_f)

    def get_LoopMap_and_appendix_sm_list(Distinct):
        # Combine the appendix state machine lists which are related to character
        # sets into a single combined appendix state machine.
        appendix_sm_db   = {}
        loop_map         = [
            _determine_LoopMapEntry(appendix_sm_db, character_set, ca, appendix_sm_list)
            for character_set, ca, appendix_sm_list in distinct
        ]
        appendix_sm_list = [
            appendix_sm for appendix_sm in appendix_sm_db.itervalues()
                        if appendix_sm.get_init_state().has_transitions()
        ]
        return loop_map, appendix_sm_list

    first_vs_appendix_sm = [ 
        (first_set, appendix_sm)
        for sm in SmList
        for first_set, appendix_sm in _cut_first_transition(sm, CloneStateMachineId=True)
    ]

    appendix_lcci_db = get_appendix_lcci_db(first_vs_appendix_sm)
    distinct         = get_distinct_map(first_vs_appendix_sm)
    loop_map,        \
    appendix_sm_list = get_LoopMap_and_appendix_sm_list(distinct)

    return loop_map, appendix_sm_list, appendix_lcci_db

@typed(loop_map=LoopMap)
def _get_analyzer_for_loop(loop_map, EventHandler):
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
    # Loop StateMachine
    sm = StateMachine.from_IncidenceIdMap(
         (lei.character_set, lei.incidence_id) for lei in loop_map
    )

    # Code Transformation
    verdict_f, sm = Setup.buffer_codec.do_state_machine(sm)

    # Loop Analyzer
    analyzer = analyzer_generator.do(sm, 
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
        if   lei.incidence_id in done:        continue
        elif lei.incidence_id == IidLoopExit: continue
        done.add(lei.incidence_id)
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

@typed(loop_map=LoopMap)
def _get_analyzer_list_for_appendices(loop_map, EventHandler, AppendixSmList, 
                                      IidLoopAfterAppendixDropOut): 
    """Parallel state machines are mounted to the loop by cutting the first
    transition and implementing it in the loop. Upon acceptance of the first
    character the according tail (appendix) of the state machine is entered.

    RETURNS: [0] List of appendix state machines in terms of analyzers.
             [1] Appendix terminals.
    """
    # Codec Transformation
    def transform(sm):
        verdict_f, \
        sm_transformed = Setup.buffer_codec.do_state_machine(sm) 
        if not verdict_f:
            error.log("Deep error: loop (skip range, skip nested range, indentation, ...)\n"
                      "contained character not suited for given character encoding.")
        return sm_transformed

    appendix_sm_list = [
        transform(sm) for sm in AppendixSmList
                      if sm.get_init_state().has_transitions()
    ]

    # Appendix Sm Drop Out => Restore position of last loop character.
    # (i)  Couple terminal stored input position in 'LoopRestartP'.
    # (ii) Terminal 'LoopAfterAppendixDropOut' restores that position.
    # Accepting on the initial state of an appendix state machine ensures
    # that any drop-out ends in this restore terminal.
    for init_state in (sm.get_init_state() for sm in appendix_sm_list):
        if init_state.has_specific_acceptance_id(): continue
        init_state.set_acceptance()
        init_state.set_specific_acceptance_id(IidLoopAfterAppendixDropOut)

    # Appendix Analyzer List
    return [
        analyzer_generator.do(sm, 
                              EventHandler.engine_type, 
                              EventHandler.reload_state_extern, 
                              OnBeforeReload = EventHandler.on_before_reload_in_appendix, 
                              OnAfterReload  = EventHandler.on_after_reload_in_appendix, 
                              dial_db        = EventHandler.dial_db)
        for sm in appendix_sm_list
    ]


def _cut_first_transition(sm, CloneStateMachineId=False):
    """Cuts the first transition and leaves the remaining states in place. 
    This solution is general(!) and it covers the case that there are 
    transitions to the init state!
    
    EXAMPLE:
        
        .-- z -->(( 1 ))          z with: (( 1c ))
      .'                   ---\
    ( 0 )--- a -->( 2 )    ---/   a with: ( 2c )-- b ->( 0c )-- z -->(( 1c ))
      \             /                       \           / 
       '-<-- b ----'                         '-<- a ---'

    where '0c', '1c', and '2c' are the cloned states of '0', '1', and '2'.

    RETURNS: list of pairs: (trigger set, pruned state machine)
             
    trigger set = NumberSet that triggers on the initial state to
                  the remaining state machine.

    pruned state machine = pruned cloned version of this state machine
                           consisting of states that come behind the 
                           state which is reached by 'trigger set'.

    ADAPTS:  Makes the init state's success state the new init state.
    """
    successor_db = sm.get_successor_db()

    if CloneStateMachineId: cloned_sm_id = sm.get_id()
    else:                   cloned_sm_id = None

    return [
        (trigger_set, sm.clone_from_state_subset(target_si, 
                                                   list(successor_db[target_si]) + [target_si],
                                                   cloned_sm_id))
        for target_si, trigger_set in sm.iterable_init_state_transitions()
    ]
        
