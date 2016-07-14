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
from   quex.engine.analyzer.terminal.core           import Terminal
from   quex.engine.analyzer.door_id_address_label   import DoorID, \
                                                           DialDB
import quex.engine.analyzer.door_id_address_label   as     dial
import quex.output.core.skipper.character_set       as     skip_character_set
import quex.output.core.skipper.range               as     skip_range
import quex.output.core.skipper.nested_range        as     skip_nested_range
import quex.output.core.skipper.indentation_counter as     indentation_counter
from   quex.input.code.core                         import CodeTerminal
from   quex.engine.misc.tools import typed

from   quex.blackboard import standard_incidence_db_is_immutable, \
                                     E_IncidenceIDs


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

class PPT(namedtuple("PPT_tuple", ("priority", "pattern", "code_fragment"))):
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

    @staticmethod
    def for_character_set_skipper(Priority, CharacterSet, Sr):
        """Generate a PPT for a character set skipper. That is, 
            -- A PatternPriority based on a given MHI and the specified incidence id.
            -- A Pattern to be webbed into the lexical analyzer state machine.
            -- A Terminal implementing the character set skipper.
        """
        pattern  = Pattern_Prep.from_character_set(CharacterSet, IncidenceId)
        pattern.set_pattern_string("<skip>")
        pattern.set_source_reference(Sr)
        pattern  = pattern.finalize()

        # Terminal for 'IncidenceId' is already coded in the character skipper
        return PPT(Priority, pattern, None)

    @staticmethod
    @typed(dial_db=DialDB)
    def for_range_skipper(terminal_factory, CaMap, NestedF, Priority, data, ReloadState):
        """Generate a PPT for a range skipper.
        """
        # -- terminal and code generator
        pattern = deepcopy(data["opener_pattern"])
        pattern.set_incidence_id(dial.new_incidence_id())
        pattern.set_pattern_string("<skip_range>")
        pattern = pattern.finalize(CaMap)

        if NestedF:
            name_prefix = "SKIP NESTED RANGE: "
            code, \
            required_register_set = skip_nested_range.do(data, ReloadState)
        else:
            name_prefix = "SKIP RANGE: "
            code, \
            required_register_set = skip_range.do(data, ReloadState)

        terminal = terminal_factory.do_plain(CodeTerminal(code), pattern, name_prefix, 
                                             RequiredRegisterSet=required_register_set)
        return PPT(Priority, pattern, terminal)

    @staticmethod
    def for_indentation_handler_newline(MHI, data, ISetup, CounterDb, ReloadState):
        """Generate a PPT for newline, that is:

            -- its PatternPriority.
            -- the Pattern object.
            -- the Terminal object.

        The terminal object contains a generator which generates the INDENTATION
        COUNTER.
        """
        sm = ISetup.sm_newline.get()

        pattern = Pattern_Prep(sm, 
                               Sr = ISetup.sm_newline.sr)
                                
        pattern.set_incidence_id(E_IncidenceIDs.INDENTATION_HANDLER)

        code, \
        required_register_set = indentation_counter.do(data, ReloadState)

        terminal = terminal_factory.do_plain(CodeTerminal(code), 
                                             "INDENTATION COUNTER NEWLINE: ", 
                                             pattern, lcci,
                                             RequiredRegisterSet=required_register_set)

        return PPT(PatternPriority(MHI, 0), pattern, terminal)

    @staticmethod
    def for_indentation_handler_suppressed_newline(MHI, SmSuppressedNewline):
        """Generate a PPT for suppressed newline, that is:

            -- its PatternPriority.
            -- the Pattern object.
            -- the Terminal object.

        The terminal simply jumpts to the re-entry of the lexical analyzer.
        """
        assert SmSuppressedNewline is not None

        pattern  = Pattern_Prep(SmSuppressedNewline) 
        code     = CodeTerminal([Lng.GOTO(DoorID.global_reentry())])
        terminal = terminal_factory.do_plain(code, pattern, lcci,
                                             "INDENTATION COUNTER SUPPRESSED_NEWLINE: ")
        return PPT(PatternPriority(MHI, 1), pattern, terminal)


class PPT_List(list):
    def __init__(self, terminal_factory):
        self.__extra_terminal_list = [] 
        self.terminal_factory      = terminal_factory

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
        for i, info in enumerate([
                (self._prepare_skip_character_set,  Loopers.skip),
                (self._prepare_skip_range,          Loopers.skip_range),
                (self._prepare_skip_nested_range,   Loopers.skip_nested_range), 
                (self._prepare_indentation_counter, Loopers.indentation_handler)]):
            func, looper = info
            if looper is None: continue
            # Mode hierarchie index = before all: -4 to -1
            # => skippers and indentation handlers have precendence over all others.
            mode_hierarchy_index = -4 + i
            terminals, ppts = func(mode_hierarchy_index, looper, CounterDb, 
                                   ReloadState = ReloadState)
            self.__extra_terminal_list.extend(terminals)
            self.extend(ppts)

    def delete_and_reprioritize(self, BaseModeSequence):
        """Performs the deletion and repriorization according the DELETE and PRIORITY-MARK
        commands in the mode. This may change the order and the incidence ids of the 
        mode's patterns. Thus, the ppt_list needs to be resorted and new incidence_id-s
        need to be assigned.
        """
        # -- Delete and reprioritize
        history_deletion         = self._pattern_deletion(BaseModeSequence) 
        history_reprioritization = self._pattern_reprioritization(BaseModeSequence) 

        # -- Re-sort and re-assign new incidence id which reflect the new order. 
        self.sort(key=attrgetter("priority"))
        for i, ppt in enumerate(list(self)): 
            priority, pattern, terminal = ppt
            if standard_incidence_db_is_immutable(pattern.incidence_id):
                continue
            # Generate a new, cloned pattern. So that other related modes are not effected.
            new_incidence_id = dial.new_incidence_id() # new id > any older id.
            new_pattern      = pattern.clone(new_incidence_id)
            if terminal is not None: new_terminal = terminal.clone(new_incidence_id)
            else:                    new_terminal = None

            new_ppt = PPT(priority, new_pattern, new_terminal)
            self[i] = new_ppt

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
        for mode_hierarchy_index, mode_descr in enumerate(BaseModeSequence):
            for info in mode_descr.reprioritization_info_list:
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
        return [ p for prio, p, t in self ]

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

        # Consistency check
        # (i) Incidence Ids are either integers or 'E_IncidenceIDs'
        assert all((   isinstance(t.incidence_id(), (int, long)) 
                    or t.incidence_id() in E_IncidenceIDs)
                   for t in terminal_list)
        # (ii) Every incidence id appears only once.
        assert    len(set(t.incidence_id() for t in terminal_list)) \
               == len(terminal_list)

        return dict((t.incidence_id(), t) for t in terminal_list)

    def finalize_run_time_counter_required_f(self):
        if self.terminal_factory.run_time_counter_required_f:
            return True
        return any(p.lcci.run_time_counter_required_f for prio, p, t in self)

    def _prepare_skip_character_set(self, MHI, Loopers, CounterDb, ReloadState):
        """MHI = Mode hierarchie index."""
        SkipSetupList = Loopers.skip
        if SkipSetupList is None or len(SkipSetupList) == 0:
            return [], []

        iterable           = SkipSetupList.__iter__()
        pattern, total_set = iterable.next()
        pattern_str        = pattern.pattern_string()
        source_reference   = pattern.sr
        # Multiple skippers from different modes are combined into one pattern.
        # This means, that we cannot say exactly where a 'skip' was defined 
        # if it intersects with another pattern.
        for ipattern, icharacter_set in iterable:
            total_set.unite_with(icharacter_set)
            pattern_str += "|" + ipattern.pattern_string()

        # The column/line number count actions for the characters in the 
        # total_set may differ. Thus, derive a separate set of characters
        # for each same count action, i.e.
        #
        #          map:  count action --> subset of total_set
        # 
        # When the first character is matched, then its terminal 'TERMINAL_x*'
        # is entered, i.e the count action for the first character is performed
        # before the skipping starts. This will look like this:
        #
        #     TERMINAL_x0:
        #                 count action '0';
        #                 goto __SKIP;
        #     TERMINAL_x1:
        #                 count action '1';
        #                 goto __SKIP;
        #        ...

        # An optional codec transformation is done later. The state machines
        # are entered as pure Unicode state machines.
        # It is not necessary to store the count action along with the state
        # machine.  This is done in "action_preparation.do()" for each
        # terminal.

        data = { 
            "counter_db":    CounterDb, 
            "character_set": total_set,
        }
        # The terminal is not related to a pattern, because it is entered
        # from the sub_terminals. Each sub_terminal relates to a sub character
        # set.
        code, \
        loop_map, \
        required_register_set = skip_character_set.do(data, ReloadState)

        # Counting actions are added to the terminal automatically by the
        # terminal_factory. The only thing that remains for each sub-terminal:
        # 'goto skipper'.
        new_ppt_list = [
            PPT.for_character_set_skipper(PatternPriority(MHI, lei.incidence_id), 
                                          lei.character_set, 
                                          source_reference)
            for lei in loop_map
        ]

        terminal = Terminal(CodeTerminal(code), "<skip>", E_IncidenceIDs.SKIP, 
                            RequiredRegisterSet=required_register_set) 

        return [ terminal ], new_ppt_list

    def _prepare_skip_range(self, MHI, Loopers, CounterDb, ReloadState):
        """MHI = Mode hierarchie index.
        
        RETURNS: new ppt_list to be added to the existing one.
        """

        SrSetup = Loopers.skip_range
        if SrSetup is None or len(SrSetup) == 0: return [], []

        return [], [
            PPT.for_range_skipper(self.terminal_factory, CounterDb.count_command_map, False, 
                                  PatternPriority(MHI, i), 
                                  self._range_skipper_data(data, CounterDb, OptionsDb), 
                                  ReloadState)
            for i, data in enumerate(SrSetup)
        ]

    def _prepare_skip_nested_range(self, MHI, Loopers, CounterDb, ReloadState):

        SrSetup = Loopers.skip_nested_range
        if SrSetup is None or len(SrSetup) == 0: return [], []

        return [], [
            PPT.for_range_skipper(terminal_factory, True, 
                                  PatternPriority(MHI, i), 
                                  self._range_skipper_data(data, CounterDb, OptionsDb), 
                                  ReloadState)
            for i, data in enumerate(SrSetup)
        ]

    def _range_skipper_data(self, data, CounterDb, OptionsDb):
        dial_db     = self.terminal_factory.dial_db
        IncidenceDb = self.terminal_factory.incidence_db
        # -- door_id_after: Where to go after the closing character sequence matched:
        #     + Normally: To the begin of the analyzer. Start again.
        #     + End(Sequence) == newline of indentation counter.
        #       => goto indentation counter.
        if self._match_indentation_counter_newline_pattern(OptionsDb.value("indentation"), 
                                                           data["closer_sequence"]):
            door_id_after = DoorID.incidence(E_IncidenceIDs.INDENTATION_HANDLER, dial_db)
        else:
            door_id_after = DoorID.continue_without_on_after_match(dial_db)

        # -- data for code generation
        my_data = deepcopy(data)
        my_data["mode_name"]          = self.terminal_factory.mode_name
        my_data["on_skip_range_open"] = IncidenceDb[E_IncidenceIDs.SKIP_RANGE_OPEN]
        my_data["door_id_after"]      = door_id_after
        my_data["counter_db"]         = CounterDb
        my_data["dial_db"]            = dial_db
        return my_data

    def _match_indentation_counter_newline_pattern(self, IndentationSetup, Sequence):
        if IndentationSetup is None: return False
        sm_newline = IndentationSetup.sm_newline.get()
        if sm_newline is None: return False
        return sm_newline.match_sequence(Sequence)

    def _prepare_indentation_counter(self, MHI, Loopers, CounterDb, ReloadState):
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

        data = { 
            "counter_db":                    CounterDb,
            "indentation_setup":             ISetup,
            "incidence_db":                  IncidenceDb,
            "default_indentation_handler_f": IncidenceDb.default_indentation_handler_f(),
            "mode_name":                     ModeName,
            "sm_suppressed_newline":         ISetup.pattern_suppressed_newline,
        }

        ppt_list = [
            # 'newline' triggers --> indentation counter
            PPT.for_indentation_handler_newline(MHI, data, ISetup, CounterDb, ReloadState)
        ]

        if sm_suppressed_newline is not None:
            ppt_list.append(
                # 'newline-suppressor' followed by 'newline' is ignored (skipped)
                PPT.for_indentation_handler_suppressed_newline(MHI, 
                                                               sm_suppressed_newline)
            )

        return [], ppt_list

def check_indentation_setup(isetup):
    """None of the elements 'comment', 'newline', 'newline_suppressor' should 
       not match some subsets of each other. Otherwise, the behavior would be 
       too confusing.
    """
    sm_newline            = isetup.sm_newline.get()
    sm_newline_suppressor = isetup.sm_newline_suppressor.get()
    sm_comment            = isetup.sm_comment.get()
    candidates            = (sm_newline, sm_newline_suppressor, sm_comment)

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

