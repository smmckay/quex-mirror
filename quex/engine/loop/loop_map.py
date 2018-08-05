from   quex.input.code.core                               import CodeTerminal
from   quex.engine.analyzer.terminal.core                 import Terminal
from   quex.engine.analyzer.door_id_address_label         import DialDB, DoorID
from   quex.engine.operations.operation_list              import Op, \
                                                                 OpList
from   quex.engine.counter                                import count_operation_db_with_reference, \
                                                                 count_operation_db_without_reference
from   quex.engine.misc.interval_handling                 import NumberSet
from   quex.engine.misc.tools                             import typed
from   quex.output.counter.pattern                        import map_SmLineColumnCountInfo_to_code

from   quex.blackboard import setup as Setup, Lng
from   quex.constants  import E_CharacterCountType, \
                              E_R, E_Op

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

class MiniTerminalCmd(MiniTerminal):
    def __init__(self, IncidenceId, CmdList):
        self.incidence_id = IncidenceId
        self.__cmd_list = CmdList

    def get_code(self, LoopStateMachineId):
        return Lng.COMMAND_LIST(self.__cmd_list)

class LoopMapEntry:
    """
         character set <---> (incidence id of couple terminal, 
                              count action for character set,
                              id of appendix DFA (None if none existent),
                              incidence id of terminal of appendix)
    """
    def __init__(self, CharacterSet, TheCountAction, 
                 IidCoupleTerminal, IidAppendixTerminal,
                 AppendixDfaId, Code=None):
        self.character_set         = CharacterSet
        self.count_action          = TheCountAction
        self.iid_couple_terminal   = IidCoupleTerminal
        self.iid_appendix_terminal = IidAppendixTerminal # NEW
        self.appendix_sm_id        = AppendixDfaId

        self.code = Code # NEW

    def __repr__(self):
        return "(%s, %s, %s, %s, %s)" % \
               (self.character_set, self.count_action, 
                self.iid_couple_terminal, 
                self.appendix_sm_id,
                self.appendix_sm_id is not None)

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
    Lazy_DoorIdLoop = ("Marker that identifies a 'GotoDoorId(LoopReentry)'",)
    @typed(LexemeEndCheckF=bool, UserOnLoopExitDoorId=DoorID, dial_db=DialDB, 
           OnReloadFailureDoorId=(None, DoorID))
    def __init__(self, ColumnNPerCodeUnit, LexemeEndCheckF, 
                 EngineType, ReloadStateExtern, UserBeforeEntryOpList, 
                 UserOnLoopExitDoorId, dial_db, OnReloadFailureDoorId, ModeName): 
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
        self.door_id_on_loop_exit_user_code = UserOnLoopExitDoorId

        if UserBeforeEntryOpList is None: UserBeforeEntryOpList = [] 
        self.on_loop_entry      = OpList.concatinate(on_loop_entry, 
                                                     on_loop_reentry_pos, 
                                                     on_loop_entry_count,
                                                     UserBeforeEntryOpList)
        self.on_loop_reentry    = OpList.from_iterable(on_loop_reentry_pos)
        self.on_loop_exit       = OpList.concatinate(on_loop_exit_pos, 
                                                     on_loop_exit_count, 
                                                     [Op.GotoDoorId(self.door_id_on_loop_exit_user_code)])
                                                     
        self.on_before_reload             = OpList.concatinate(on_before_reload_pos, 
                                                               on_before_reload_count)
        self.on_before_reload_in_appendix = OpList.from_iterable(on_before_reload_pos_apx)

        self.on_after_reload              = OpList.concatinate(on_after_reload_pos, 
                                                               on_after_reload_count)
        self.on_after_reload_in_appendix  = OpList.from_iterable(on_after_reload_pos_apx)

        self.__loop_state_machine_id = None

        self.__appendix_dfa_present_f = False

    def appendix_dfa_present_f(self):
        return self.__appendix_dfa_present_f

    def loop_state_machine_id_set(self, SmId):
        assert SmId is not None
        self.__loop_state_machine_id = SmId

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

    def __prepare_positioning_at_loop_begin_and_exit(self):
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

    def _cmd_list_Frame(self, TheCountAction, CmdList, JumpToDoorId):
        if TheCountAction is not None:
            code = TheCountAction.get_OpList(self.column_number_per_code_unit) 
        else:
            code = []
        code.extend(CmdList)
        code.append(Op.GotoDoorId(JumpToDoorId))
        return code

    def cmd_list_CA_GotoAppendixTerminal(self, CA, IidAppendixTerminal): 
        jump_to_door_id = DoorID.incidence(IidAppendixTerminal, self.dial_db)
        return self._cmd_list_Frame(CA, [], jump_to_door_id)
        
    def cmd_list_CA_GotoAppendixDfa(self, CA, AppendixDfaId): 
        # Couple Terminal: transit to appendix state machine.
        # When the appendix drops out, the loop must continue where the
        # appendix has began => Set 'LoopRestartP' to current position.
        self.__appendix_dfa_present_f = True
        cmd_list        = [Op.Assign(E_R.LoopRestartP, E_R.InputP)]
        jump_to_door_id = DoorID.state_machine_entry(AppendixDfaId, self.dial_db)
        return self._cmd_list_Frame(CA, cmd_list, jump_to_door_id)

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
        jump_to_door_id = self.door_id_on_loop_exit_user_code
        return self._cmd_list_Frame(CA, cmd_list, jump_to_door_id)

    @typed(LEI=LoopMapEntry)
    def get_loop_terminal_code(self, LEI, DoorIdLoop, DoorIdLoopExit): 
        """RETURNS: A loop terminal. 

        A terminal: (i)    Counts,
                    (ii)   checks possibly for the lexeme end, and
                    (iii)a either re-enters the loop, or
                    (iii)b transits to an appendix state machine (couple terminal).
        """
        if LEI.code is not None:
            name = "<LOOP TERMINAL %s>" % LEI.iid_couple_terminal
            code = LEI.code

        code = [ self.replace_Lazy_DoorIdLoop(cmd, DoorIdLoop) for cmd in code ]
        return Terminal(CodeTerminal(Lng.COMMAND_LIST(code, self.dial_db)), name, 
                        IncidenceId=LEI.iid_couple_terminal,
                        dial_db=self.dial_db)

    def replace_Lazy_DoorIdLoop(self, cmd, DoorIdLoop):
        GotoDoorIdCmdIdSet = (E_Op.GotoDoorId, E_Op.GotoDoorIdIfInputPNotEqualPointer)
        if   cmd.id == E_Op.GotoDoorId:
            if cmd.content.door_id != self.Lazy_DoorIdLoop: return cmd
            return Op.GotoDoorId(DoorIdLoop)
        elif cmd.id == E_Op.GotoDoorIdIfInputPNotEqualPointer:
            if cmd.content.door_id != self.Lazy_DoorIdLoop: return cmd
            return Op.GotoDoorIdIfInputPNotEqualPointer(DoorIdLoop, cmd.content.pointer)
        else:
            return cmd

    def get_Terminal_from_mini_terminal(self, LCCI, mini_terminal):
        if LCCI is not None:
            run_time_counter_required_f, \
            count_code                   = map_SmLineColumnCountInfo_to_code(LCCI, ModeName=self.mode_name) 
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

