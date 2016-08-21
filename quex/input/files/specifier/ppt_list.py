"""PPT List: A list of tuples that associate:

     (i)   the PRIORITY of a pattern in the match process.
     (ii)  the PATTERN, and
     (iii) a   TERMINAL to be executed upon match.

The complete matching process of the analyzer in forward direction is described
in this file by a list off PPT objects. This includes PPT entries for skippers
and incidence handlers. Based on the PPT list optional pattern deletion and
repriorization is implemented. Finaly, a mode's pattern list and terminal
database is extracted.
"""
from   quex.input.code.core                         import CodeTerminal, \
                                                           SourceRef_VOID
from   quex.input.regular_expression.pattern        import Pattern_Prep
from   quex.engine.counter                          import CountActionMap, \
                                                           IndentationCount
from   quex.engine.pattern                          import Pattern
import quex.engine.state_machine.check.tail         as     tail
from   quex.engine.operations.operation_list        import Op
from   quex.engine.analyzer.terminal.core           import Terminal
from   quex.engine.analyzer.door_id_address_label   import DoorID, \
                                                           DialDB
import quex.engine.analyzer.door_id_address_label   as     dial
import quex.engine.misc.error_check                 as     error_check
from   quex.engine.misc.tools import typed
import quex.output.core.loop.character_set          as     skip_character_set
import quex.output.core.loop.range                  as     skip_range
import quex.output.core.loop.nested_range           as     skip_nested_range
import quex.output.core.loop.indentation_counter    as     indentation_counter

from   quex.blackboard import E_IncidenceIDs, \
                              Lng


from   collections  import namedtuple
from   operator     import attrgetter
from   copy         import deepcopy

class PatternPriority(object):
    """Description of a pattern's priority.
    ___________________________________________________________________________
    PatternPriority-s are possibly adapted according the re-priorization 
    or other 'mode-related' mechanics. Thus, they cannot be named tuples.
    ___________________________________________________________________________
    """
    __slots__ = ("mode_hierarchy_index", "pattern_index")
    def __init__(self, MHI, PatternIdx):
        self.mode_hierarchy_index = MHI
        self.pattern_index        = PatternIdx

    def __cmp__(self, Other):
        if   self.mode_hierarchy_index > Other.mode_hierarchy_index: return 1
        elif self.mode_hierarchy_index < Other.mode_hierarchy_index: return -1
        elif self.pattern_index > Other.pattern_index:               return 1
        elif self.pattern_index < Other.pattern_index:               return -1
        else:                                                        return 0

class PPT(namedtuple("PPT_tuple", ("priority", "pattern", "terminal"))):
    """PPT -- (Priority, Pattern, Terminal) 
    ______________________________________________________________________________

    Collects information about a pattern, its priority, and the terminal 
    to be executed when it triggers. Objects of this class are intermediate
    they are not visible outside class 'Mode'.
    ______________________________________________________________________________
    """
    @typed(ThePatternPriority=PatternPriority, TheTerminal=(Terminal, None))
    def __new__(self, ThePatternPriority, ThePattern, TheTerminal):
        return super(PPT, self).__new__(self, ThePatternPriority, ThePattern, TheTerminal)

class PPT_List(list):
    def __init__(self, terminal_factory):
        self.__extra_terminal_list = [] 
        self.terminal_factory      = terminal_factory
        self.required_register_set = set()

    def collect_match_pattern(self, ModePrepDb, BaseModeSequence):
        """Collect patterns of all inherited modes. Patterns are like virtual functions
        in C++ or other object oriented programming languages. Also, the patterns of the
        uppest mode has the highest priority, i.e. comes first.
        """
        def pap_iterator(ModePrepDb, BaseModeSequence):
            for mode_hierarchy_index, mode_prep in enumerate(BaseModeSequence):
                for pap in mode_prep.pattern_action_pair_list:
                    yield mode_hierarchy_index, pap.pattern(), pap.action()

        self.extend(
            PPT(PatternPriority(mhi, pattern.incidence_id), 
                pattern, 
                self.terminal_factory.do_match_pattern(code, pattern))
            for mhi, pattern, code in pap_iterator(ModePrepDb, BaseModeSequence)
        )

    def collect_loopers(self, Loopers, CounterDb, ReloadState):
        """Collect patterns and terminals which are required to implement
        skippers and indentation counters.
        """
        CaMap        = CounterDb.count_command_map
        new_ppt_list = []
        for i, func in enumerate([self._prepare_skip_character_set, 
                                  self._prepare_skip_range,         
                                  self._prepare_skip_nested_range,  
                                  self._prepare_indentation_counter]):
            # Mode hierarchie index = before all: -4 to -1
            # => skippers and indentation handlers have precendence over all others.
            mode_hierarchy_index = -4 + i
            pl, tl = func(mode_hierarchy_index, Loopers, CaMap, ReloadState)

            new_ppt_list.extend(pl)
            self.__extra_terminal_list.extend(tl)

        # IMPORTANT: Terminals generated from 'loopers' are NOT to change their
        #            incidence_id. They are already 'gotoed' and cannot change!
        #            They cannot be subject to reprioritization!
        #
        # => All of them are sorted BEFORE any other matching, i.e. with 
        # 
        #                      'mode_hierarchy_index < 0'.
        #
        assert all(priority.mode_hierarchy_index < 0 
                   for priority, dummy, dummy in new_ppt_list)
        new_ppt_list.sort(key=attrgetter("priority"))
        self[:0] = new_ppt_list

    def delete_and_reprioritize(self, BaseModeSequence):
        """Performs the deletion and repriorization according the DELETE and PRIORITY-MARK
        commands in the mode. This may change the order and the incidence ids of the 
        mode's patterns. Thus, the ppt_list needs to be resorted and new incidence_id-s
        need to be assigned.

        RETURNS: [0] history of deletions
                 [1] history of reprioritizations
        """
        #________________
        assert all(p.incidence_id == t.incidence_id() for dummy, p, t in self)
        self._assert_incidence_id_consistency([p.incidence_id for dummy, p, t in self])
        #________________

        if not self: return [], []

        # Delete and reprioritize
        history_deletion         = self._pattern_deletion(BaseModeSequence) 
        history_reprioritization = self._pattern_reprioritization(BaseModeSequence) 

        # Make sure that the incidence-id of each pattern fits the position
        # in the priorization sequence. That is, early entries in the list MUST
        # have a lower incidence id thant later entries.
        prev_incidence_id = self[0].pattern.incidence_id - 1
        self.sort(key=attrgetter("priority"))
        for i, ppt in enumerate(list(self)): 
            priority, pattern, terminal = ppt
            if pattern.incidence_id <= prev_incidence_id:
                # IMPORTANT: Any match with 'mode_hierarchy_index < 0' stems
                #            from generated code! Terminals that relate to such
                #            code are NOT supposed to change their incidence_id!
                assert priority.mode_hierarchy_index >= 0

                # Generate a new, cloned pattern. So that other related modes are not effected.
                new_incidence_id = dial.new_incidence_id() # new id > any older id.
                new_pattern      = pattern.clone_with_new_incidence_id(new_incidence_id)
                if terminal is not None: new_terminal = terminal.clone(new_incidence_id)
                else:                    new_terminal = None
                new_ppt = PPT(priority, new_pattern, new_terminal)
                self[i] = new_ppt

            prev_incidence_id = pattern.incidence_id

        #________________
        assert all(p.incidence_id == t.incidence_id() for dummy, p, t in self)
        self._assert_incidence_id_consistency([p.incidence_id for dummy, p, t in self])
        #________________

        return history_deletion, history_reprioritization

    def _pattern_reprioritization(self, BaseModeSequence):
        """Repriority patterns. The 'reprioritization_info_list' consists of a list of

                     (pattern, new_pattern_index, source_reference)

           If a pattern defined in this mode matches 'pattern' it needs to receive the
           new pattern index and there changes its preceedence.
        """
        def repriorize(MHI, Info, self, ModeName, history):
            done_f = False
            for ppt in self:
                priority, pattern, terminal = ppt
                if   priority.mode_hierarchy_index > MHI:                      continue
                elif priority.pattern_index        >= Info.new_pattern_index:  continue
                elif not identity_checker.do(pattern, Info.pattern):           continue

                done_f = True
                history.append([ModeName, 
                                pattern.pattern_string(), pattern.sr.mode_name,
                                pattern.incidence_id(), Info.new_pattern_index])
                priority.mode_hierarchy_index = MHI
                priority.pattern_index        = Info.new_pattern_index

            if not done_f and Info.sr.mode_name == ModeName:
                error.warning("PRIORITY mark does not have any effect.", 
                              Info.sr)

        history = []
        mode_name = BaseModeSequence[-1].name
        for mode_hierarchy_index, mode in enumerate(BaseModeSequence):
            for info in mode.reprioritization_info_list:
                repriorize(mode_hierarchy_index, info, self, mode_name, history)

        return history

    def _pattern_deletion(self, BaseModeSequence):
        """Delete all patterns that match entries in 'deletion_info_list'.
        """
        def delete(MHI, Info, self, ModeName, history):
            size = len(self)
            for i in range(size-1, -1, -1):
                priority, pattern, terminal = self[i]
                if   priority.mode_hierarchy_index > MHI:          continue
                elif priority.pattern_index >= Info.pattern_index: continue
                elif not superset_check.do(Info.pattern, pattern): continue
                del self[i]
                history.append([ModeName, pattern.pattern_string(), pattern.sr.mode_name])

            if size == len(self) and Info.sr.mode_name == ModeName:
                error.warning("DELETION mark does not have any effect.", Info.sr)

        history = []
        mode_name = BaseModeSequence[-1].name
        for mode_hierarchy_index, mode_prep in enumerate(BaseModeSequence):
            for info in mode_prep.deletion_info_list:
                delete(mode_hierarchy_index, info, self, mode_name, history)

        return history

    def finalize_pattern_list(self): 
        pattern_list = [ p for prio, p, t in self ]
        self._assert_incidence_id_consistency(
            [p.incidence_id for p in pattern_list]
        )
        return pattern_list

    def finalize_terminal_db(self, IncidenceDb):
        """This function MUST be called after 'finalize_pattern_list()'!
        """
        terminal_list = [
            terminal for priority, pattern, terminal in self
                     if terminal is not None
        ]

        # Some incidences have their own terminal
        # THEIR INCIDENCE ID REMAINS FIXED!
        terminal_list.extend(
            IncidenceDb.extract_terminal_db(self.terminal_factory, 
                                            ReloadRequiredF=True).itervalues()
        )

        terminal_list.extend(self.__extra_terminal_list)

        self._assert_incidence_id_consistency(
            [t.incidence_id() for t in terminal_list]
        )

        return dict((t.incidence_id(), t) for t in terminal_list)

    @staticmethod
    def _assert_incidence_id_consistency(IncidenceIdList):
        """Basic constraints on incidence ids.
        """
        # (i) Incidence Ids are either integers or 'E_IncidenceIDs'
        assert all((   isinstance(incidence_id, (int, long)) 
                    or incidence_id in E_IncidenceIDs)
                   for incidence_id in IncidenceIdList)
        # (ii) Every incidence id appears only once.
        assert len(set(IncidenceIdList)) == len(IncidenceIdList)

    def finalize_run_time_counter_required_f(self):
        if self.terminal_factory.run_time_counter_required_f:
            return True
        return any(p.lcci.run_time_counter_required_f 
                   for prio, p, t in self
                   if p.lcci is not None)

    def _prepare_indentation_counter(self, MHI, Loopers, CaMap, ReloadState):
        """Prepare indentation counter. An indentation counter is implemented by 
        the following:

        'newline' pattern --> triggers as soon as an UNSUPPRESSED newline occurs. 
                          --> entry to the INDENTATION COUNTER.

        'suppressed newline' --> INDENTATION COUNTER is NOT triggered.
         
        The supressed newline pattern is longer (and has precedence) over the
        newline pattern. With the suppressed newline it is possible to write
        lines which overstep the newline (see backslahs in Python, for example).

        RETURNS: List of:
                 [0] newline PPT and
                 [1] optionally the PPT of the newline suppressor.

        The primary pattern action pair list is to be the head of all pattern
        action pairs.

        MHI = Mode hierarchie index defining the priority of the current mode.
        """
        ISetup = Loopers.indentation_handler
        if ISetup is None: return [], []

        check_indentation_setup(ISetup)

        incidence_db = self.terminal_factory.incidence_db
        data = { 
            "ca_map":                        CaMap,
            "indentation_setup":             ISetup,
            "incidence_db":                  incidence_db,
            "mode_name":                     self.terminal_factory.mode_name,
            "dial_db":                       self.terminal_factory.dial_db,
        }

        code,                  \
        new_terminal_list,     \
        required_register_set, \
        run_time_counter_f     = indentation_counter.do(data, ReloadState)
        self.terminal_factory.run_time_counter_required_f = run_time_counter_f

        self.required_register_set.update(required_register_set)

        # 'newline' triggers --> indentation counter
        pattern  = ISetup.pattern_newline.clone_with_new_incidence_id(E_IncidenceIDs.INDENTATION_HANDLER)
        terminal = terminal_factory.do_plain(CodeTerminal(code), 
                                             "INDENTATION COUNTER NEWLINE: ", 
                                             pattern, lcci,
                                             RequiredRegisterSet=required_register_set)
        new_ppt_list = [
            PPT(PatternPriority(MHI, 0), pattern, terminal)
        ]

        if sm_suppressed_newline is not None:
            # 'newline-suppressor' causes following 'newline' to be ignored.
            # => next line not subject to new indentation counting.
            pattern = Pattern_Prep(SmSuppressedNewline) 
            code    = CodeTerminal([Lng.GOTO(DoorID.global_reentry())])
            new_ppt_list.append(
                PPT(PatternPriority(MHI, 1), 
                    Pattern_Prep(sm_suppressed_newline),
                    terminal_factory.do_plain(code, pattern, lcci,
                                              "INDENTATION COUNTER SUPPRESSED_NEWLINE: "))
            )

        return new_ppt_list, new_terminal_list

    def _prepare_skip_character_set(self, MHI, Loopers, CaMap, ReloadState):
        """MHI = Mode hierarchie index."""
        if Loopers.skip is None: return [], []

        skipped_character_set, \
        pattern_str,           \
        aux_source_reference   = Loopers.combined_skip()

        data = { 
            "ca_map":        CaMap,
            "character_set": skipped_character_set,
            "dial_db":       self.terminal_factory.dial_db
        }

        code,                 \
        new_terminal_list,    \
        loop_map,             \
        required_register_set = skip_character_set.do(data, ReloadState)
        self.required_register_set.update(required_register_set)

        extra_terminal_list = [ 
            Terminal(CodeTerminal(code), "<skip>", E_IncidenceIDs.SKIP, 
                     RequiredRegisterSet=required_register_set, 
                     dial_db=self.terminal_factory.dial_db) 
        ]
        extra_terminal_list.extend(
            t for t in new_terminal_list
        )

        # Any skipped character must enter the skipper entry.
        goto_code = [ Op.GotoDoorId(DoorID.incidence(E_IncidenceIDs.SKIP, 
                                                     self.terminal_factory.dial_db)) ] 
        new_ppt_list = []
        for lei in loop_map:
            new_incidence_id = dial.new_incidence_id()
            pattern    = Pattern.from_character_set(lei.character_set, 
                                                    new_incidence_id, 
                                                    Sr=SourceRef_VOID)
            # There is no reference pointer => Add directly
            count_code = lei.count_action.get_OpList(None)
            code       = Lng.COMMAND_LIST(count_code + goto_code, 
                                          self.terminal_factory.dial_db)
            terminal   = Terminal(CodeTerminal(code), "ENTER SKIP:", 
                                  new_incidence_id, 
                                  dial_db=self.terminal_factory.dial_db) 

            new_ppt_list.append(
                PPT(PatternPriority(MHI, new_incidence_id), pattern, terminal)
            )

        return new_ppt_list, extra_terminal_list

    def _prepare_skip_range(self, MHI, Loopers, CaMap, ReloadState):
        """MHI = Mode hierarchie index.
        
        RETURNS: new ppt_list to be added to the existing one.
        """
        if not Loopers.skip_range: return [], []

        extra_terminal_list = []
        new_ppt_list        = []
        for i, data in enumerate(Loopers.skip_range):
            data = self._range_skipper_data(data, CaMap, Loopers.indentation_handler)

            code,                  \
            new_terminal_list,     \
            required_register_set, \
            run_time_counter_f     = skip_range.do(data, ReloadState)
            self.terminal_factory.run_time_counter_required_f = run_time_counter_f

            self.required_register_set.update(required_register_set)

            extra_terminal_list.extend(new_terminal_list)

            terminal = self.terminal_factory.do_plain(CodeTerminal(code), 
                                             data["opener_pattern"], "SKIP RANGE: ", 
                                             RequiredRegisterSet=required_register_set)
            new_ppt_list.append(
                PPT(PatternPriority(MHI, i), data["opener_pattern"], terminal)

            )

        return new_ppt_list, extra_terminal_list

    def _prepare_skip_nested_range(self, MHI, Loopers, CaMap, ReloadState):
        if not Loopers.skip_nested_range: return [], []

        extra_terminal_list = []
        new_ppt_list        = []
        for i, data in enumerate(Loopers.skip_nested_range):
            data = self._range_skipper_data(data, CaMap, Loopers.indentation_handler)

            code,                  \
            new_terminal_list,     \
            required_register_set, \
            run_time_counter_f     = skip_nested_range.do(data, ReloadState)
            self.terminal_factory.run_time_counter_required_f = run_time_counter_f

            self.required_register_set.update(required_register_set)

            extra_terminal_list.extend(new_terminal_list)

            terminal = self.terminal_factory.do_plain(CodeTerminal(code), 
                                             data["opener_pattern"], "SKIP NESTED RANGE: ", 
                                             RequiredRegisterSet=required_register_set)
            new_ppt_list.append(
                PPT(PatternPriority(MHI, i), data["opener_pattern"], terminal)
            )

        return new_ppt_list, extra_terminal_list

    @typed(CaMap=CountActionMap, IndentationHandler=(None, IndentationCount))
    def _range_skipper_data(self, data, CaMap, IndentationHandler):
        dial_db     = self.terminal_factory.dial_db
        IncidenceDb = self.terminal_factory.incidence_db
        # -- door_id_exit: Where to go after the closing character sequence matched:
        #     + Normally: To the begin of the analyzer. Start again.
        #     + End(Sequence) == newline of indentation counter.
        #       => goto indentation counter.
        if self._match_indentation_counter_newline_pattern(IndentationHandler,
                                                           data["closer_pattern"]):
            door_id_exit = DoorID.incidence(E_IncidenceIDs.INDENTATION_HANDLER, dial_db)
        else:
            door_id_exit = DoorID.continue_without_on_after_match(dial_db)

        # -- data for code generation
        my_data = deepcopy(data)
        my_data["mode_name"]          = self.terminal_factory.mode_name
        my_data["on_skip_range_open"] = IncidenceDb[E_IncidenceIDs.SKIP_RANGE_OPEN]
        my_data["door_id_exit"]       = door_id_exit
        my_data["ca_map"]             = CaMap
        my_data["dial_db"]            = dial_db
        return my_data

    def _match_indentation_counter_newline_pattern(self, indentation_handler, CloserPattern):
        if indentation_handler is None: return False
        indentation_sm_newline = indentation_handler.sm_newline.get()
        if indentation_sm_newline is None: return False

        only_common_f, \
        common_f       = tail.do(indentation_sm_newline, CloserPattern.sm)

        error_check.tail(only_common_f, common_f, 
                        "indentation handler's newline", indentation_sm_newline.sr, 
                        "range skipper", CloserPattern.sm.sr)

        return only_common_f


def check_indentation_setup(isetup):
    """None of the elements 'comment', 'newline', 'newline_suppressor' should 
       not match some subsets of each other. Otherwise, the behavior would be 
       too confusing.
    """
    candidates = [
        isetup.get_sm_newline(),
        isetup.get_sm_suppressed_newline(),
        isetup.get_sm_comment()
    ]
    candidates = tuple(x for x in candidates if x is not None)

    def mutually_subset(Sm1, Sm2):
        if   Sm1 is None or Sm2 is None:                           return False
        elif superset_check.do(Sm1, Sm2): return True
        elif superset_check.do(Sm2, Sm1): return True
        return False

    for i, candidate1 in enumerate(candidates):
        if candidate1 is None: continue
        for candidate2 in candidates[i+1:]:
            if candidate2 is None: continue
            elif not mutually_subset(candidate1, candidate2): continue
            error.log_consistency_issue(candidate1, candidate2,
                                        ThisComment="matches on some common lexemes as",
                                        ThatComment="") 

