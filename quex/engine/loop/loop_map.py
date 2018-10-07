from   quex.input.code.core                        import CodeTerminal
from   quex.engine.state_machine.character_counter import SmLineColumnCountInfo
import quex.engine.state_machine.index             as     index
from   quex.engine.analyzer.terminal.core          import Terminal
from   quex.engine.analyzer.door_id_address_label  import DialDB, DoorID
import quex.engine.analyzer.door_id_address_label  as     dial
from   quex.engine.operations.operation_list       import Op, \
                                                          OpList
from   quex.engine.counter                         import count_operation_db_with_reference, \
                                                          count_operation_db_without_reference
from   quex.engine.misc.interval_handling          import NumberSet
from   quex.engine.misc.tools                      import typed

from   quex.blackboard import setup as Setup, Lng
from   quex.constants  import E_CharacterCountType, \
                              E_R, E_Op

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

    def get_Terminal(self, PreCode, dial_db, LoopStateMachineId):
        assert LoopStateMachineId is not None

        return Terminal(CodeTerminal(PreCode + self.get_code(LoopStateMachineId)), 
                        self.name, self.incidence_id, dial_db=dial_db)

class MiniTerminalCmd(MiniTerminal):
    def __init__(self, IncidenceId, CmdList):
        self.incidence_id = IncidenceId
        self.__cmd_list = CmdList

    def get_code(self, LoopStateMachineId):
        return Lng.COMMAND_LIST(self.__cmd_list)

class LoopMapEntry:
    """
       character set --> * Terminal Iid, that implements the reaction on character set.
                         * Code that is to be implemented in that terminal
                         * (auxiliary: countin action for 'character set')
    """
    def __init__(self, CharacterSet, IidCoupleTerminal, Code=None, CA=None):
        self.character_set       = CharacterSet
        self.iid_couple_terminal = IidCoupleTerminal
        self.code                = Code # NEW
        #
        self.aux_count_action    = CA  # Useful when loop map is used 'outside', so that
        #                              # count action does not have to be determined twice.

    def __repr__(self):
        return "<todo>"

class LoopMap(list):
    def __init__(self, *LoopMapEntryLists):
        for lme_list in LoopMapEntryLists:
            self.extend(x for x in lme_list if not x.character_set.is_empty())
        self._assert_consistency()

    def _assert_consistency(self):
        assert not any(lme is None               for lme in self)
        assert not any(lme.character_set is None for lme in self)
        assert not any((lme.iid_couple_terminal is None) and (lme.code is None) 
                       for lme in self)

        # Assert: Transition triggers do not intersect! 
        total = NumberSet()
        for lme in self:
            assert not lme.character_set.has_intersection(total)
            total.unite_with(lme.character_set)

class LoopEvents:
    """Event handlers in terms of 'List of Operations' (objects of class 'Op'):

        .on_loop_entry:     upon entry into loop
        .on_loop_exit:      upon exit from loop
        .on_loop_reentry:   upon every iteration of loop entry.
        .on_before_reload:             before buffer reload is performed.
        .on_before_reload_in_appendix: as above ... in appendix state machine.
        .on_after_reload:              after buffer reload is performed.
        .on_after_reload_in_appendix:  as above ... in appendix state machine.
    """
    def __init__(self, ColumnNPerCodeUnit, UserBeforeEntryOpList, UserOnLoopExitDoorId):
        # Counting Actions upon: loop entry/exit; before/after reload
        #
        on_loop_entry_count,    \
        on_loop_exit_count,     \
        on_before_reload_count, \
        on_after_reload_count   = self.__prepare_count_actions(ColumnNPerCodeUnit)

        # Input pointer positioning: loop entry/exit; before/after reload
        #
        on_loop_entry,            \
        on_loop_reentry_pos,      \
        on_loop_exit_pos          = self.__prepare_positioning_at_loop_begin_and_exit(ColumnNPerCodeUnit)
        
        on_before_reload_pos,     \
        on_after_reload_pos       = self.__prepare_positioning_before_and_after_reload() 
        on_before_reload_pos_apx, \
        on_after_reload_pos_apx   = self.__prepare_positioning_before_and_after_reload(AppendixSmF=True) 

        # _____________________________________________________________________
        #
        if UserBeforeEntryOpList is None: UserBeforeEntryOpList = [] 
        self.on_loop_entry      = OpList.concatinate(on_loop_entry, 
                                                     on_loop_reentry_pos, 
                                                     on_loop_entry_count,
                                                     UserBeforeEntryOpList)
        self.on_loop_reentry    = OpList.from_iterable(on_loop_reentry_pos)
        self.on_loop_exit       = OpList.concatinate(on_loop_exit_pos, 
                                                     on_loop_exit_count, 
                                                     [ Op.GotoDoorId(UserOnLoopExitDoorId) ])
                                                     
        self.on_before_reload             = OpList.concatinate(on_before_reload_pos, 
                                                               on_before_reload_count)
        self.on_before_reload_in_appendix = OpList.from_iterable(on_before_reload_pos_apx)

        self.on_after_reload              = OpList.concatinate(on_after_reload_pos, 
                                                               on_after_reload_count)
        self.on_after_reload_in_appendix  = OpList.from_iterable(on_after_reload_pos_apx)

    def on_loop_after_appendix_drop_out(self, DoorIdLoop, ColumnNPerCodeUnit):
        # Upon drop-out, the input position is set to where the apendix 
        # started. Then, the loop is re-entered.
        op_list = []

        if ColumnNPerCodeUnit is not None:
            op_list.append(
                Op.Assign(E_R.CountReferenceP, E_R.LoopRestartP, Condition="COLUMN")
            )

        op_list.extend([
            Op.Assign(E_R.InputP, E_R.LoopRestartP),
            Op.GotoDoorId(DoorIdLoop)
        ])

        return op_list
        
    def on_loop_exit_text(self, dial_db):
        return Lng.COMMAND_LIST(self.on_loop_exit, dial_db)

    @staticmethod
    def __prepare_count_actions(ColumnNPerCodeUnit):
        # Variable character sizes: store the begin of character in 
        # 'LoopRestartP'. Loop start and character start are the same position.
        if Setup.buffer_encoding.variable_character_sizes_f():
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

    @staticmethod
    def __prepare_positioning_at_loop_begin_and_exit(ColumnNPerCodeUnit):
        """With encodings of dynamic character sizes (UTF8), the pointer to the 
        first letter is stored in 'character_begin_p'. To reset the input 
        pointer 'input_p = character_begin_p' is applied.  
        """
        if Setup.buffer_encoding.variable_character_sizes_f():
            # 1 character == variable number of code units
            # => Begin of character must be stored upon entry 
            #    and restored upon exit.
            entry   = [ Op.Assign(E_R.LoopRestartP, E_R.InputP)       ]
            reentry = [ Op.Assign(E_R.LoopRestartP, E_R.InputP)       ]
            exit    = [ Op.Assign(E_R.InputP,       E_R.LoopRestartP) ]
        else:
            # 1 character == 1 code unit
            # => reset to last character: 'input_p = input_p - 1'
            entry   = []
            reentry = []
            exit    = [ Op.Decrement(E_R.InputP) ]

        if ColumnNPerCodeUnit is not None:
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
        if Setup.buffer_encoding.variable_character_sizes_f(): maintain_loop_restart_p = True
        elif AppendixSmF:                                      maintain_loop_restart_p = True
        else:                                                  maintain_loop_restart_p = False

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
            before.extend([
                Op.Assign(E_R.InputPBeforeReload, E_R.InputP),
                Op.PointerAssignMin(E_R.LexemeStartP, E_R.LexemeStartP, E_R.LoopRestartP)
            ])

        # After Reload:
        if maintain_loop_restart_p:
            after.extend([
                Op.AssignPointerDifference(E_R.PositionDelta, E_R.InputP, E_R.InputPBeforeReload),
                Op.PointerAdd(E_R.LoopRestartP, E_R.PositionDelta)
            ])

        # Make sure, that the lexeme start pointer makes sense:
        # => begin of input
        after.append(
            Op.Assign(E_R.LexemeStartP, E_R.InputP)
        )

        return before, after

class LoopConfig:
    Lazy_DoorIdLoop = ("Marker that identifies a 'GotoDoorId(LoopReentry)'",)
    @typed(LexemeEndCheckF=bool, UserOnLoopExitDoorId=DoorID, dial_db=DialDB, 
           OnReloadFailureDoorId=(None, DoorID))
    def __init__(self, ColumnNPerCodeUnit, LexemeEndCheckF, 
                 EngineType, ReloadStateExtern, 
                 UserOnLoopExitDoorId, dial_db, OnReloadFailureDoorId, ModeName, Events): 
        """ColumnNPerCodeUnit is None => no constant relationship between 
                                         column number and code unit.
        """
        self.mode_name                   = ModeName
        self.column_number_per_code_unit = ColumnNPerCodeUnit
        self.lexeme_end_check_f          = LexemeEndCheckF
        self.reload_state_extern         = ReloadStateExtern
        self.engine_type                 = EngineType
        self.dial_db                     = dial_db
        self.door_id_on_reload_failure   = OnReloadFailureDoorId
        self.door_id_on_loop_exit_user_code = UserOnLoopExitDoorId
        self.events                      = Events

        self.loop_state_machine_id    = None
        self.__appendix_dfa_present_f = False

        self.loop_state_machine_id            = index.get_state_machine_id()
        self.iid_loop_exit                    = dial.new_incidence_id()
        self.iid_loop_after_appendix_drop_out = dial.new_incidence_id() 

        self.__run_time_counter_required_f = False


    def appendix_dfa_present_f(self):
        return self.__appendix_dfa_present_f

    def run_time_counter_required_f(self):
        return self.__run_time_counter_required_f

    def get_count_code(self, LCCI):
        if LCCI is None: return []

        run_time_counter_required_f, \
        cmd_list                     = SmLineColumnCountInfo.get_OpList(LCCI, ModeName=self.mode_name)

        if run_time_counter_required_f:
            self.__run_time_counter_required_f = True
            # The content to be counted starts where the appendix started.
            # * Begin of counting at 'loop restart pointer'.
            # * Run-time counting can ONLY work, if the lexeme start pointer 
            #   is at position of appendix begin.
            cmd_list[:0] = [ Op.Assign(E_R.LexemeStartP, E_R.LoopRestartP) ]

        if self.column_number_per_code_unit is not None:
            # If the reference counting is applied, the reference pointer
            # must be set right behind the last counted character.
            cmd_list.append(
                Op.Assign(E_R.CountReferenceP, E_R.InputP, Condition="COLUMN")
            )

        return cmd_list

    def __replace_Lazy_DoorIdLoop(self, cmd, DoorIdLoop):
        if   cmd.id == E_Op.GotoDoorId:
            if cmd.content.door_id != self.Lazy_DoorIdLoop: return cmd
            return Op.GotoDoorId(DoorIdLoop)
        elif cmd.id == E_Op.GotoDoorIdIfInputPNotEqualPointer:
            if cmd.content.door_id != self.Lazy_DoorIdLoop: return cmd
            return Op.GotoDoorIdIfInputPNotEqualPointer(DoorIdLoop, cmd.content.pointer)
        else:
            return cmd

    def replace_Lazy_DoorIdLoop(self, CmdList, DoorIdLoop):
        return [ 
            self.__replace_Lazy_DoorIdLoop(cmd, DoorIdLoop) for cmd in CmdList 
        ]

    def CodeTerminal_without_Lazy_DoorIdLoop(self, CmdList, DoorIdLoop):
        return CodeTerminal(
            Lng.COMMAND_LIST(self.replace_Lazy_DoorIdLoop(CmdList, DoorIdLoop), 
                             self.dial_db)
        )

    def get_required_register_set(self, AppendixSmExistF):
        result = set()
        if self.column_number_per_code_unit is not None:
            result.add((E_R.CountReferenceP, "count-column"))
        if AppendixSmExistF:
            result.add(E_R.LoopRestartP)
        if Setup.buffer_encoding.variable_character_sizes_f():
            result.add(E_R.LoopRestartP)
        if     E_R.LoopRestartP in result \
           and self.engine_type.subject_to_reload():
            result.add(E_R.InputPBeforeReload)
            result.add(E_R.PositionDelta)

        return result

    def cmd_list_CA_GotoTerminal(self, CA, IidTerminal): 
        target_door_id = DoorID.incidence(IidTerminal, self.dial_db)
        return self._cmd_list_Frame(CA, [], target_door_id)
        
    def cmd_list_CA_GotoAppendixDfa(self, CA, AppendixDfaId): 
        # Couple Terminal: transit to appendix state machine.
        # When the appendix drops out, the loop must continue where the
        # appendix has began => Set 'LoopRestartP' to current position.
        self.__appendix_dfa_present_f = True
        cmd_list        = [ 
            Op.Assign(E_R.LoopRestartP, E_R.InputP),
            Op.Assign(E_R.LexemeStartP, E_R.InputP)
        ]
        target_door_id = DoorID.state_machine_entry(AppendixDfaId, self.dial_db)
        return self._cmd_list_Frame(CA, cmd_list, target_door_id)

    def cmd_list_CA_GotoLoopEntry(self, CA): 
        if not self.lexeme_end_check_f: 
            return self._cmd_list_Frame(CA, [], self.Lazy_DoorIdLoop)
        else:
            return self._cmd_list_CA_LexemeEndCheck_GotoLoopEntry(CA) 

    def _cmd_list_CA_LexemeEndCheck_GotoLoopEntry(self, CA): 
        # Check Terminal: check against lexeme end before re-entering loop.
        cmd_list = [
            Op.GotoDoorIdIfInputPNotEqualPointer(self.Lazy_DoorIdLoop, E_R.LexemeEnd)
        ]
        if     self.column_number_per_code_unit is not None \
           and CA is not None and CA.cc_type == E_CharacterCountType.COLUMN: 
            # With reference counting, no column counting while looping.
            # => Do it now, before leaving.
            cmd_list.append(
                Op.ColumnCountReferencePDeltaAdd(E_R.InputP, self.column_number_per_code_unit, 
                                                 False)
            )
        target_door_id = self.door_id_on_loop_exit_user_code
        return self._cmd_list_Frame(CA, cmd_list, target_door_id)

    def _cmd_list_Frame(self, TheCountAction, CmdList, DoorIdTarget):
        cmd_list = []
        if TheCountAction is not None:
            cmd_list.extend(TheCountAction.get_OpList(self.column_number_per_code_unit))
        cmd_list.extend(CmdList)
        cmd_list.append(Op.GotoDoorId(DoorIdTarget))
        return cmd_list

    def get_appendix_terminal_cmd_list_db(self, CaMap, AppendixSmList, OriginalIidDb):
        def prepare(AppendixSm, OriginalIidDb):
            lcci     = SmLineColumnCountInfo.from_DFA(CaMap, AppendixSm, False, Setup.buffer_encoding)
            cmd_list = self.get_count_code(lcci)
            target_door_id = DoorID.incidence(OriginalIidDb[AppendixSm.get_id()], self.dial_db)
            cmd_list.append(Op.GotoDoorId(target_door_id))
            return (AppendixSm.get_id(), cmd_list)

        # This includes cmd_list-s for zero transition appendix sm, in case they
        # are combined with others that go further.
        return dict(prepare(sm, OriginalIidDb) for sm in AppendixSmList)

    def get_couple_terminal_cmd_list(self, CA, CombinedAppendixSm, OriginalIidDb):
        """CA:                 Count action for the character set of the loop 
                               entry.
           CombinedAppendixSm: (combined) appendix sm where to jump upon 
                               triggering of the character set.
           OriginalIidDb:      Appendix sm id --> original iid of the state machine
                                                  where it came from.

        RETURNS: [0] CmdList -- for loop count action and transition to appendix
                                state machine or entry into according terminal.
                 [1] True, if there is a transition to an appendix state machine
                     False, if not
                 
        """
        transition_to_appendix_f = CombinedAppendixSm.get_init_state().has_transitions()
        acceptance_id_set        = CombinedAppendixSm.acceptance_id_set()
        combined_appendix_sm_id  = CombinedAppendixSm.get_id()

        cmd_list = []
        if CA is not None:
            cmd_list.extend(CA.get_OpList(self.column_number_per_code_unit))

        if not transition_to_appendix_f:
            # NO appendix after first transition => jump to appendix terminal.
            assert len(acceptance_id_set) == 1
            iid_original   = OriginalIidDb[acceptance_id_set.pop()]
            target_door_id = DoorID.incidence(iid_original, self.dial_db)
            transition_to_appendix_f = False
        else:
            # appendix after first transition. => jump to appendix state machine.
            self.__appendix_dfa_present_f = True
            cmd_list.extend([
                Op.Assign(E_R.LoopRestartP, E_R.InputP),
                Op.Assign(E_R.LexemeStartP, E_R.InputP)
            ])
            target_door_id = DoorID.state_machine_entry(combined_appendix_sm_id,
                                                        self.dial_db)
        cmd_list.append(Op.GotoDoorId(target_door_id))
        return cmd_list, transition_to_appendix_f

