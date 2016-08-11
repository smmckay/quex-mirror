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

=> There is a subset 'La' in 'L' which is associated with a terminal 'Terminal
a'.  If SM fails to match, the first lexatom is still a loop lexatom, and
therefore, the loop CONTINUES after the first lexatom. 

      .---<-----------( next i )<-----------------------------.
      |                                                       |
      |                              [ i = ir ]--------->[ Terminal a ]
      |   .------.                       |     
    --+-->: ...  :                       | drop-out 
          +------+                       |          
          |  La  |--->[ ir = i ]--->( Pruned SM )------->[ Terminal SM ]
          +------+                                match
          : ...  :
          '------'

The position of the first input must be stored in 'ir' so that upon drop-out it
may be restored into 'i'. After the appriate 'Terminal a' is executed, the loop
continues. The 'Pruned SM' is the SM without the transition on the first
lexatom.

___________
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
from   quex.engine.analyzer.terminal.factory              import TerminalFactory
from   quex.engine.analyzer.door_id_address_label         import DialDB, DoorID
import quex.engine.analyzer.door_id_address_label         as     dial
import quex.engine.analyzer.engine_supply_factory         as     engine
from   quex.engine.state_machine.core                     import StateMachine  
import quex.engine.state_machine.construction.combination as     combination
from   quex.engine.state_machine.character_counter        import SmLineColumnCountInfo
import quex.engine.state_machine.index                    as     index
import quex.engine.state_machine.algorithm.beautifier     as     beautifier
from   quex.engine.operations.operation_list              import Op, \
                                                                 OpList
from   quex.engine.counter                                import CountAction, \
                                                                 CountBase, \
                                                                 CountActionMap, \
                                                                 count_operation_db_with_reference, \
                                                                 count_operation_db_without_reference
from   quex.engine.misc.interval_handling                 import NumberSet
from   quex.engine.misc.tools                             import typed, \
                                                                 print_callstack, \
                                                                 flatten_list_of_lists
from   quex.output.cpp.counter_for_pattern                import map_SmLineColumnCountInfo_to_code
from   quex.output.core.variable_db                       import variable_db
import quex.output.core.base                              as     generator

from   quex.blackboard import E_StateIndices, \
                              E_CharacterCountType, \
                              E_R, \
                              setup as Setup, \
                              Lng

from   collections import namedtuple
from   itertools   import chain

MiniTerminal = namedtuple("MiniTerminal", ("code", "name", "incidence_id"))

class LoopMapEntry:
    def __init__(self, CharacterSet, TheCountAction, CoupleIncidenceId, AppendixSmId, 
                 HasTransitionsF=False):
        self.character_set  = CharacterSet
        self.count_action   = TheCountAction
        self.incidence_id   = CoupleIncidenceId
        self.appendix_sm_id = AppendixSmId
        self.appendix_sm_has_transitions_f = HasTransitionsF

    def add_appendix_sm(self, SM):
        if any(sm.get_id() == SM.get_id() for sm in self.appendix_sm_list):
            return
        self.appendix_sm_list.append(SM)

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
        .on_before_reload:  before buffer reload is performed.
        .on_after_reload:   after buffer reload is performed.
        .on_loop_reentry:   upon every iteration of loop entry.
    """
    @typed(LexemeEndCheckF=bool, MaintainLexemeF=bool, UserOnLoopExitDoorId=DoorID, dial_db=DialDB)
    def __init__(self, ColumnNPerCodeUnit, LexemeEndCheckF, MaintainLexemeF, 
                 EngineType, ReloadStateExtern, UserBeforeEntryOpList, 
                 UserOnLoopExitDoorId, AppendixSmExistF, dial_db): 
        """ColumnNPerCodeUnit is None => no constant relationship between 
                                         column number and code unit.
        """
        self.column_number_per_code_unit = ColumnNPerCodeUnit
        self.lexeme_end_check_f          = LexemeEndCheckF
        self.reload_state_extern         = ReloadStateExtern
        self.engine_type                 = EngineType
        self.dial_db                     = dial_db

        # Determine required register set before (required for reload actions)
        self.required_register_set = self.__get_required_register_set(AppendixSmExistF, 
                                                                      MaintainLexemeF)

        # Counting Actions upon: loop entry/exit; before/after reload
        #
        on_loop_entry_count,    \
        on_loop_exit_count,     \
        on_before_reload_count, \
        on_after_reload_count   = self.__prepare_count_actions(self.column_number_per_code_unit)

        # Input pointer positioning: loop entry/exit; before/after reload
        #
        on_loop_entry,        \
        on_loop_reentry_pos,  \
        on_loop_exit_pos      = self.__prepare_positioning_at_loop_begin_and_exit()
        on_before_reload_pos, \
        on_after_reload_pos   = self.__prepare_positioning_before_and_after_reload(MaintainLexemeF) 

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
                                                     
        self.on_before_reload   = OpList.concatinate(on_before_reload_pos, 
                                                     on_before_reload_count)
        self.on_after_reload    = OpList.concatinate(on_after_reload_pos, 
                                                     on_after_reload_count)

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
                Op.Assign(E_R.CountReferenceP, E_R.InputP ) 
            )

        return entry, reentry, exit

    def __prepare_positioning_before_and_after_reload(self, MaintainLexemeF):
        """The 'lexeme_start_p' restricts the amount of data which is loaded 
        into the buffer upon reload--if the lexeme needs to be maintained. If 
        the lexeme does not need to be maintained, then the whole buffer can 
        be refilled.
        
        For this, the 'lexeme_start_p' is set to the input pointer. 
        
        EXCEPTION: Variable character sizes. There, the 'lexeme_start_p' is used
        to mark the begin of the current letter. However, letters are short, so 
        the drawback is tiny.

        RETURNS: [0] on_before_reload
                 [1] on_after_reload
        """
        before = []
        after  = []

        # Besides the current 'read_p', the buffer reload must maintain the
        # following pointers. I.e. after reload their position must lie INSIDE
        # the buffer.
        # 
        # CountReferenceP --> required for character counting
        #                     (only if column_number_per_code_unit is specified)
        # LoopRestartP    --> Position where to restart loop:
        #                       * if the appendix state machine drops-out.
        #                       * if current multi byte character is incomplete.
        # LexemeStartP    --> Position where the current lexeme begins
        #                     (only if explicitly required by 'MaintainLexemeF')
        #
        # The (current) reload function only maintains the 'read_p' and 
        # 'lexeme_start_p'. Trick:
        #      BEFORE: 
        #              read_p_before_reload         = read_p
        #              lexeme_start_before_reload_p = LexemeStartP
        #              lexeme_start_p   = min(LoopRestartP, 
        #                                     CountReferenceP,
        #                                     LexemeStartP)
        #      AFTER:  
        #              position_delta   = read_p - read_p_before_reload
        #              LoopRestartP    -= position_delta
        #              CountReferenceP -= position_delta
        #              LexemeStartP     = lexeme_start_backup_p - position_delta
        #
        # Once, the reload function can handle this, the aforementioned may be
        # simplified significantly (TODO).

        # Flag indicating whether there are other pointers beyond 'lexeme_start_p'
        # which need to be maintained.
        maintain_count_ref_p    = E_R.CountReferenceP in self.required_register_set 
        maintain_loop_restart_p = E_R.LoopRestartP in self.required_register_set

        # Before Reload:
        pointer_list = []
        if MaintainLexemeF:         pointer_list.append(E_R.LexemeStartP)    # MUST BE FIRST!
        if maintain_count_ref_p:    pointer_list.append(E_R.CountReferenceP)
        if maintain_loop_restart_p: pointer_list.append(E_R.LoopRestartP)

        if maintain_count_ref_p or maintain_loop_restart_p:
            if MaintainLexemeF:
                before.append(
                    Op.Assign(E_R.LexemeStartBeforeReload, E_R.LexemeStartP),
                )
            before.append(
                Op.Assign(E_R.InputPBeforeReload, E_R.InputP),
            )
            for i, pointer in pointer_list[1:]:
                # Avoid Nonsense: lexeme_p = min(lexeme_p, lexeme_p) 
                if E_R.LexemeStartP == pointer: 
                    continue
                elif i == 0:
                    op = Op.Assign(E_R.LexemeStartP, pointer)
                else:
                    op = Op.PointerAssignMin(E_R.LexemeStartP, E_R.LexemeStartP, pointer)
                before.append(op)

        if not MaintainLexemeF:
            # Just get the 'lexeme_start_p' out of the way, so that anything
            # is filled from 'read_p'.
            before.append(
                Op.Assign(E_R.LexemeStartP, E_R.InputP)
            )

        # After Reload:
        if maintain_count_ref_p or maintain_loop_restart_p:
            if MaintainLexemeF:
                before.append(
                    Op.Assign(E_R.LexemeStartP, E_R.LexemeStartBeforeReload),
                )
            after.extend([
                Op.AssignPointerDifference(E_R.PositionDelta, 
                                           E_R.InputP, E_R.InputPBeforeReload),
            ])
            for p in pointer_list:
                after.append(
                    Op.PointerAdd(p, E_R.PositionDelta)
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
        else:                        name = "<LOOP %s>" % IncidenceId

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

    def get_Terminal_from_mini_terminal(self, CaMap, appendix_sm, mini_terminal):
        if appendix_sm is not None:
            lcci = SmLineColumnCountInfo.from_StateMachine(CaMap, appendix_sm, 
                                                           False,
                                                           Setup.buffer_codec)
            run_time_counter_required_f, \
            count_code                   = map_SmLineColumnCountInfo_to_code(lcci) 

            if self.column_number_per_code_unit is not None:
                # If the reference counting is applied, the reference pointer
                # must be set right behind the last counted character.
                count_code.append(
                    Lng.COMMAND(Op.Assign(E_R.CountReferenceP, E_R.InputP), self.dial_db)
                )
        else:
            run_time_counter_required_f = False
            count_code = []
        
        return run_time_counter_required_f, \
               Terminal(CodeTerminal(count_code + mini_terminal.code), 
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
        return [
            # Upon drop-out, the input position is set to where the apendix 
            # started. Then, the loop is re-entered.
            Op.Assign(E_R.InputP, E_R.LoopRestartP),
            Op.GotoDoorId(DoorIdLoop)
        ]

    def on_loop_exit_text(self):
        return Lng.COMMAND_LIST(self.on_loop_exit, self.dial_db)

    def __get_required_register_set(self, AppendixSmExistF, MaintainLexemeF):
        result = set()
        if self.column_number_per_code_unit is not None:
            result.add((E_R.CountReferenceP, "QUEX_OPTION_COLUMN_NUMBER_COUNTING"))
        if AppendixSmExistF:
            result.add(E_R.LoopRestartP)
        if Setup.buffer_codec.variable_character_sizes_f():
            result.add(E_R.LoopRestartP)
        if    E_R.CountReferenceP in result \
           or E_R.LoopRestartP in result:
            result.add(E_R.InputPBeforeReload)
            result.add(E_R.PositionDelta)
            if MaintainLexemeF:
                result.add(E_R.LexemeStartBeforeReload)

        return result

@typed(CaMap=CountActionMap, dial_db=DialDB, 
       ReloadF=bool, LexemeEndCheckF=bool, OnLoopExit=list,
       LoopCharacterSet=(None, NumberSet))
def do(CaMap, OnLoopExitDoorId, BeforeEntryOpList=None, LexemeEndCheckF=False, EngineType=None, 
       ReloadStateExtern=None, LexemeMaintainedF=False,
       ParallelSmTerminalPairList=None, dial_db=None,
       LoopCharacterSet=None):
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
    parallel_sm_list        = _extract_state_machines_and_terminals(ParallelSmTerminalPairList)
    assert all(isinstance(t, MiniTerminal) for t in parallel_terminal_list)

    iid_loop_exit                    = dial.new_incidence_id()
    iid_loop_after_appendix_drop_out = dial.new_incidence_id() 

    event_handler = LoopEventHandlers(CaMap.get_column_number_per_code_unit(), 
                                      LexemeEndCheckF, LexemeMaintainedF, 
                                      EngineType, ReloadStateExtern, 
                                      UserOnLoopExitDoorId=OnLoopExitDoorId,
                                      UserBeforeEntryOpList=BeforeEntryOpList,
                                      AppendixSmExistF=len(parallel_terminal_list) != 0,
                                      dial_db=dial_db) 

    # LoopMap: Associate characters with the reactions on their occurrence ____
    #
    loop_map,        \
    appendix_sm_list = _get_loop_map(CaMap, parallel_sm_list, iid_loop_exit, 
                                     dial_db, LoopCharacterSet)

    # Loop represented by Analyzer-s and Terminal-s ___________________________
    #
    analyzer_list,      \
    door_id_loop,       \
    appendix_sm_exist_f = _get_analyzer_list(loop_map, event_handler, appendix_sm_list,
                                             iid_loop_after_appendix_drop_out)

    if not appendix_sm_exist_f:
        iid_loop_after_appendix_drop_out = None

    terminal_list = _get_terminal_list(loop_map, event_handler, 
                                       CaMap, appendix_sm_list, parallel_terminal_list,
                                       door_id_loop,
                                       iid_loop_exit, 
                                       iid_loop_after_appendix_drop_out)

    # Generate Code ___________________________________________________________
    #
    txt = _get_source_code(analyzer_list)
    
    # Clean the loop map from the 'exit transition'.
    clean_loop_map = [lei for lei in loop_map if lei.incidence_id != iid_loop_exit]
    return txt, \
           terminal_list, \
           clean_loop_map, \
           door_id_loop, \
           event_handler.required_register_set

def _extract_state_machines_and_terminals(ParallelSmTerminalPairList):
    if ParallelSmTerminalPairList is None:
        ParallelSmTerminalPairList = []
    parallel_terminal_list = []
    parallel_sm_list       = []
    for sm, terminal in ParallelSmTerminalPairList:
        parallel_terminal_list.append(terminal)
        parallel_sm_list.append(sm)
    return parallel_terminal_list, parallel_sm_list

@typed(loop_map=LoopMap)
def _get_analyzer_list(loop_map, EventHandler, AppendixSmList, 
                       IidLoopAfterAppendixDropOut): 
    """An appendix state machine is a parallel state machine that is pruned by
    its first transition. The first transition is absorbed into the 'loop_map'.
    
    RETURNS: list of Analyzer-s.
    """
    # Core Loop Analyzer 
    loop_analyzer, \
    door_id_loop   = _get_loop_analyzer(loop_map, EventHandler)

    # Appendix Analyzers 
    appendix_analyzer_list = _get_appendix_analyzers(loop_map, EventHandler, 
                                                     AppendixSmList,
                                                     IidLoopAfterAppendixDropOut) 
    
    analyzer_list = [ loop_analyzer ] + appendix_analyzer_list

    # Analyzer Ids MUST be unique (LEAVE THIS ASSERT IN PLACE!)
    assert len(set(a.state_machine_id for a in analyzer_list)) == len(analyzer_list)

    return analyzer_list, \
           door_id_loop, \
           any(lei.appendix_sm_has_transitions_f for lei in loop_map)

def _get_terminal_list(loop_map, EventHandler, 
                       CounterDb, AppendixSmList, ParallelMiniTerminalList, 
                       DoorIdLoop,
                       IidLoopExit, IidLoopAfterAppendixDropOut):
    """RETURNS: list of all Terminal-s.
    """
    loop_terminal_list     = _get_loop_terminal_list(loop_map, EventHandler,
                                                     IidLoopAfterAppendixDropOut, 
                                                     DoorIdLoop, IidLoopExit) 

    default_counter_f, \
    parallel_terminal_list = _get_parallel_terminal_list(EventHandler, 
                                                         CounterDb, AppendixSmList, 
                                                         ParallelMiniTerminalList)

    return loop_terminal_list + parallel_terminal_list 

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
    couple_list,     \
    appendix_sm_list = _get_LoopMapEntry_list_parallel_state_machines(CaMap, 
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

    return result, appendix_sm_list

@typed(TheCountBase=CountActionMap)
def _get_LoopMapEntry_list_plain(TheCountBase, L_pure):
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
        for character_set, ca in TheCountBase.iterable_in_sub_set(L_pure)
    ]

@typed(TheCountBase=CountActionMap)
def _get_LoopMapEntry_list_parallel_state_machines(TheCountBase, SmList, dial_db):
    """Perform separation:
    
         Parallel state machine  ---->    first transition  
                                       +  appendix state machine
    
    The 'first transition' is mounted on the loop state machine triggering an
    acceptance that causes a transit to the appendix state machine. 

    RETURNS: list of LoopMapEntry-s 
    """
    def iterable(SmList):
        """YIELDS: [0] Character Set
                   [1] CountAction related to that character set.
                   [2] Appendix state machine related to that character set.

        The iterable reports character sets for which their is a distinct count
        action and appendix state machine.
        """
        for sm in SmList:
            for trigger_set, appendix_sm in sm.cut_first_transition(CloneStateMachineId=True):
                # id of 'appendix_sm' == id of original parallel state machine!
                for character_set, ca in TheCountBase.iterable_in_sub_set(trigger_set):
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

    # The tuples reported by 'iterable()' may contain overlapping character
    # sets. That is, their may be multiple parallel state machines that trigger
    # on the same characters in a first transition. 
    #
    distinct = [] # list of [0] Character Set
    #                       [1] Count Action related to [0]
    #                       [2] List of appendix state machines related [0]
    # All character sets [0] in the distinct list are NON-OVERLAPPING.
    for character_set, ca, appendix_sm in iterable(SmList):
        remainder = character_set
        for prev_character_set, prev_ca, prev_appendix_sm_list in distinct:
            intersection = character_set.intersection(prev_character_set)
            if intersection.is_empty(): 
                continue
            elif intersection.is_equal(prev_character_set):
                prev_appendix_sm_list.append(appendix_sm)
            else:
                prev_character_set.subtract(intersection)
                distinct.append(
                    (intersection, ca, prev_appendix_sm_list + [appendix_sm])
                )
            remainder.subtract(intersection)
            if remainder.is_empty(): break

        if not remainder.is_empty():
            distinct.append(
                (remainder, ca, [appendix_sm])
            )

    def _determine_LoopMapEntry(sm_db, CharacterSet, CA, AppendixSmList):
        appendix_sm       = append_sm_db_get_combined(sm_db, appendix_sm_list)
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

@typed(loop_map=LoopMap)
def _get_loop_analyzer(loop_map, EventHandler):
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
    verdict_f, sm = Setup.buffer_codec.do_state_machine(sm, beautifier)

    # Loop Analyzer
    analyzer = analyzer_generator.do(sm, 
                                     EventHandler.engine_type, 
                                     EventHandler.reload_state_extern, 
                                     OnBeforeReload = EventHandler.on_before_reload, 
                                     OnAfterReload  = EventHandler.on_after_reload,
                                     OnBeforeEntry  = EventHandler.on_loop_entry, 
                                     dial_db        = EventHandler.dial_db)

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
def _get_loop_terminal_list(loop_map, EventHandler, IidLoopAfterAppendixDropOut, 
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
    result = [
        EventHandler.get_loop_terminal_code(lei, DoorIdLoop, door_id_loop_exit) 
        for lei in loop_map
        if lei.incidence_id != IidLoopExit
    ]

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
def _get_parallel_terminal_list(EventHandler, CaMap, 
                                AppendixSmList, ParallelMiniTerminalList):
    """RETURNS: [0] true, default counter is required.
                    false, else.
                [1] list of terminals of the appendix state machines.
    """
    def get_appendix_sm(AppendixSmList, IncidenceId):
        for appendix_sm in AppendixSmList:
            if appendix_sm.get_id() == IncidenceId: 
                return appendix_sm
        return None

    def iterable(AppendixSmList, ParallelMiniTerminalList):
        for mini_terminal in ParallelMiniTerminalList:
            appendix_sm = get_appendix_sm(AppendixSmList, mini_terminal.incidence_id)
            yield appendix_sm, mini_terminal

    run_time_counter_required_f = False
    terminal_list = []
    for appendix_sm, mini_terminal in iterable(AppendixSmList, ParallelMiniTerminalList):
        rtcr_f, \
        terminal = EventHandler.get_Terminal_from_mini_terminal(CaMap, appendix_sm, 
                                                                mini_terminal) 
        terminal_list.append(terminal)
        run_time_counter_required_f |= rtcr_f

    return run_time_counter_required_f, terminal_list

@typed(loop_map=LoopMap)
def _get_appendix_analyzers(loop_map, EventHandler, AppendixSmList, 
                            IidLoopAfterAppendixDropOut): 
    """Parallel state machines are mounted to the loop by cutting the first
    transition and implementing it in the loop. Upon acceptance of the first
    character the according tail (appendix) of the state machine is entered.

    RETURNS: [0] List of appendix state machines in terms of analyzers.
             [1] Appendix terminals.
    """
    # Codec Transformation
    appendix_sm_list = []
    for sm in AppendixSmList:
        if not sm.get_init_state().has_transitions(): continue
        verdict_f, sm = Setup.buffer_codec.do_state_machine(sm, beautifier) 
        appendix_sm_list.append(sm)

    # Appendix Sm Drop Out => Restore position of last loop character.
    # (i)  Couple terminal stored input position in 'LoopRestartP'.
    # (ii) Terminal 'LoopAfterAppendixDropOut' restores that position.
    # Accepting on the initial state of an appendix state machine ensures
    # that any drop-out ends in this restore terminal.
    for init_state in (sm.get_init_state() for sm in appendix_sm_list):
        init_state.set_acceptance()
        init_state.mark_acceptance_id(IidLoopAfterAppendixDropOut)

    # Appendix Analyzer List
    return [
        analyzer_generator.do(sm, 
                              EventHandler.engine_type, 
                              EventHandler.reload_state_extern, 
                              OnBeforeReload = EventHandler.on_before_reload, 
                              OnAfterReload  = EventHandler.on_after_reload, 
                              dial_db        = EventHandler.dial_db)
        for sm in appendix_sm_list
    ]

def _prepare_entry_and_reentry(analyzer, OnLoopEntry, OnLoopReEntry):
    """Prepare the entry and re-entry doors into the initial state
    of the loop-implementing initial state.

                   .----------.
                   | on_entry |
                   '----------'
                        |         .------------.
                        |<--------| on_reentry |<-----.
                        |         '------------'      |
                .----------------.                    |
                |                +-----> Terminal ----+----> Exit
                |      ...       |
                |                +-----> Terminal - - 
                '----------------'

    RETURNS: DoorID of the re-entry door which is used to iterate in the loop.
    """
    # Entry into state machine
    entry            = analyzer.init_state().entry
    init_state_index = analyzer.init_state_index
        
    # OnEntry
    entry.append_OpList(init_state_index, E_StateIndices.BEFORE_ENTRY,
                        OnLoopEntry)

    # OnReEntry

def _get_source_code(analyzer_list):
    """RETURNS: String containing source code for the 'loop'. 

       -- The source code for the (looping) state machine.
       -- The terminals which contain counting actions.

    Also, it requests variable definitions as they are required.
    """
    # Analyzer Ids MUST be unique (LEAVE THIS ASSERT IN PLACE!)
    assert len(set(a.state_machine_id for a in analyzer_list)) == len(analyzer_list)

    loop_analyzer = analyzer_list[0]

    txt = flatten_list_of_lists(
        generator.do_analyzer(analyzer) for analyzer in analyzer_list
    )
    if loop_analyzer.engine_type.subject_to_reload():
        txt.extend(
            generator.do_reload_procedure(loop_analyzer)
        )

    return txt


