import quex.input.files.specifier.patterns_and_terminals as     patterns_and_terminals
from   quex.input.files.specifier.ppt_list               import PPT_List
from   quex.input.regular_expression.pattern             import Pattern_Prep
from   quex.input.files.mode_option                      import OptionDB
from   quex.input.code.core                              import CodeUser
from   quex.input.code.base                              import SourceRef
                                                                
from   quex.engine.state_machine.character_counter       import SmLineColumnCountInfo
import quex.engine.state_machine.check.superset          as     superset_check
from   quex.engine.analyzer.door_id_address_label        import DialDB
from   quex.engine.analyzer.terminal.factory             import TerminalFactory
import quex.engine.analyzer.engine_supply_factory        as     engine
from   quex.engine.analyzer.state.core                   import ReloadState
from   quex.engine.incidence_db                          import IncidenceDB
from   quex.engine.counter                               import CountActionMap           
from   quex.engine.pattern                               import Pattern           
from   quex.engine.mode                                  import Mode           
import quex.engine.misc.error                            as     error
from   quex.engine.misc.tools                            import typed, all_isinstance

import quex.blackboard as     blackboard
from   quex.blackboard import setup as Setup, \
                              E_IncidenceIDs

from   copy        import deepcopy
from   collections import namedtuple
from   itertools   import islice

ModeDocumentation = namedtuple("ModeDocumentation", ("history_deletion", 
                                                     "history_reprioritization", 
                                                     "entry_mode_name_list",
                                                     "exit_mode_name_list",
                                                     "base_mode_name_sequence"))

#-----------------------------------------------------------------------------------------
# Mode_PrepPrep/Mode Objects:
#
# During parsing 'Mode_PrepPrep' objects are generated. Once parsing is over, 
# the descriptions are translated into 'real' mode objects where code can be generated
# from. All matters of inheritance and pattern resolution are handled in the
# transition from description to real mode.
#-----------------------------------------------------------------------------------------
class Mode_PrepPrep:
    """Mode description delivered directly from the parser.
    ______________________________________________________________________________
    MAIN MEMBERS:

     (1) .pattern_action_pair_list:   [ (Pattern, CodeUser) ]

     Lists all patterns which are directly defined in this mode (not the ones
     from the base mode) together with the user code (class CodeUser) to be
     executed upon the detected match.

     (2) .incidence_db:               incidence_id --> [ CodeFragment ]

     Lists of possible incidences (e.g. 'on_match', 'on_enter', ...) together
     with the code fragment to be executed upon occurence.

     (3) .option_db:                  option name  --> [ OptionSetting ]

     Maps the name of a mode option to a list of OptionSetting according to 
     what has been defined in the mode. Those options describe

        -- [optional] The character counter behavior.
        -- [optional] The indentation handler behavior.
        -- [optional] The 'skip' character behavior.
           ...

     That is, they parameterize code generators of 'helpers'. The option_db
     also contains information about mode transition restriction, inheritance
     behavior, etc.

     (*) .direct_base_mode_name_list:   [ string ]
     
     Lists all modes from where this mode is derived, that is only the direct 
     super modes.
    ______________________________________________________________________________
    OTHER NON_TRIVIAL MEMBERS:

     If the mode is derived from another mode, it may make sense to adapt the 
     priority of patterns and/or delete pattern from the matching hierarchy.

     (*) .reprioritization_info_list: [ PatternRepriorization ] 
       
     (*) .deletion_info_list:         [ PatternDeletion ] 
    ______________________________________________________________________________
    """
    __slots__ = ("name",
                 "sr",
                 "direct_base_mode_name_list",
                 "option_db",
                 "pattern_action_pair_list",
                 "incidence_db",
                 "reprioritization_info_list",
                 "deletion_info_list")

    def __init__(self, Name, SourceReference):
        # Register Mode_PrepPrep at the mode database
        blackboard.mode_prep_prep_db[Name] = self
        self.name  = Name
        self.sr    = SourceReference

        self.direct_base_mode_name_list          = []

        self.pattern_action_pair_list   = []  
        self.option_db                  = OptionDB()    # map: option_name    --> OptionSetting
        self.incidence_db               = IncidenceDB() # map: incidence_name --> CodeFragment

        self.reprioritization_info_list = []  
        self.deletion_info_list         = [] 

    @typed(ThePattern=Pattern_Prep, Action=CodeUser)
    def add_pattern_action_pair(self, ThePattern, TheAction, fh):
        assert ThePattern.check_consistency()

        if ThePattern.pre_context_trivial_begin_of_line_f:
            blackboard.required_support_begin_of_line_set()

        TheAction.set_source_reference(SourceRef.from_FileHandle(fh, self.name))

        self.pattern_action_pair_list.append(PatternActionPair(ThePattern, TheAction))

    def add_match_priority(self, ThePattern, fh):
        """Whenever a pattern in the mode occurs, which is identical to that given
           by 'ThePattern', then the priority is adapted to the pattern index given
           by the current pattern index.
        """
        PatternIdx = ThePattern.incidence_id() 
        self.reprioritization_info_list.append(
            PatternRepriorization(ThePattern, PatternIdx, 
                                  SourceRef.from_FileHandle(fh, self.name))
        )

    def add_match_deletion(self, ThePattern, fh):
        """If one of the base modes contains a pattern which is identical to this
           pattern, it has to be deleted.
        """
        PatternIdx = ThePattern.incidence_id() 
        self.deletion_info_list.append(
            PatternDeletion(ThePattern, PatternIdx, 
                            SourceRef.from_FileHandle(fh, self.name))
        )

    def finalize(self):
        base_mode_name_sequence = blackboard.determine_base_mode_name_sequence([], [])
        # At least the mode itself must be there
        # The mode itself is base_mode_sequence[-1]
        assert len(base_mode_sequence) >= 1 \
               and base_mode_sequence[-1].name == self.name

        # Collect Options
        # (A finalized Mode does not contain an option_db anymore).
        collected_options_db = OptionDB.from_BaseModeSequence(base_mode_sequence)
        inheritable,          \
        exit_mode_name_list,  \
        entry_mode_name_list, \
        loopers,              \
        counter_db            = collected_options_db.finalize()
        ca_map                = counter_db.count_command_map

        collected_incidence_db = IncidenceDB.from_BaseModeSequence(base_mode_sequence)

        if (    E_IncidenceIDs.INDENTATION_DEDENT   in collected_incidence_db \
            and E_IncidenceIDs.INDENTATION_N_DEDENT in collected_incidence_db):
             error.log("After deriving from base mode, mode '%s' contains 'on_dedent'\n" % self.name
                       + "and 'on_n_dedent' handler. Both are mutually exclusive.", self.sr)

        pap_list = [
            PatternActionPair(pap.pattern().finalize(CaMap), pap.action())
            for pap in self.pattern_action_pair_list
        ]
        loopers.finalize(CaMap)

        # At this stage, no information is aggregated from base types.
        return Mode_Prep(self.name, self.sr, base_mode_sequence, 
                         pap_list, loopers,
                         collected_incidence_db, counter_db, 
                         self.deletion_info_list, 
                         self.reprioritization_info_list)

class Mode_Prep:
    focus = ("<skip>", "<skip_range>", "<skip_nested_range>", "<indentation newline>")

    def __init__(self, Name, Sr, BaseModeSequence, PapList, Loopers, IncidenceDb, CounterDb,
                 DeletionInfoList, RepriorizationInfoList):
        self.name                    = Name
        self.sr                      = Sr
        self.base_mode_name_sequence = [m.name for m in BaseModeSequence]

        # PapList = list with 'finalized' Pattern objects
        # BUT: Only local patterns!
        #      Patterns from base modes are collected later in 
        #      'ppt_list.collect_match_pattern()'.
        self.pattern_action_pair_list = PapList
        # Loopers = Containing all 'looping' objects for skipping and 
        #           indentation handling. (patterns are finalized)
        self.loopers      = Loopers

        # OptionsDb, IncidenceDb, and CounterDb contain aggregated content
        # from base modes.
        self.incidence_db = IncidenceDb
        self.counter_db   = CounterDb

        self.deletion_info_list         = DeletionInfoList
        self.reprioritization_info_list = RepriorizationInfoList

        self.entry_mode_name_list = EntryModeNameList # This mode can be entered from those.
        self.exit_mode_name_list  = ExitModeNameList  # This mode can exit to those.

    def second_init(self, ModePrepDb):
        """When all Mode_Prep-s are defined, the patterns can be collected from
        the base modes.
        """
        self.dial_db              = DialDB()
        self.base_mode_sequence   = [ ModePrepDb[name] for name in self.base_mode_name_sequence ]

        self.pattern_list, \
        self.terminal_db, \
        self.run_time_counter_required_f, \
        self.reload_state_forward         = self.__setup_matching_configuration(ModePrepDb)

        self.implemented_f = self.__determine_implemented_f()

    def __setup_matching_configuration(self, ModePrepDb):
        """Collect all pattern-action pairs and 'loopers' and align it in a list
        of 'priority-pattern-terminal' objects, i.e. a 'ppt_list'. That list associates
        each pattern with a priority and a terminal containing an action to be executed
        upon match. 

        RETURNS: [0] List of all patterns to be matched, each pattern has a unique
                     'incidence_id'
                 [1] TerminalDb: incidence_id--> Terminal object
                 [2] Flag indicating if run-time character counting is required.
                 [3] ReloadState in forward direction.

        It is necessary to generate the reload state in forward direction, because, the
        loopers implement state machines which are subject to reload. The same reload 
        state later used by the general matching state machine.
        """
        # PPT from pattern-action pairs
        #
        ppt_list = PPT_List(TerminalFactory(self.name, self.incidence_db, self.dial_db))
        ppt_list.collect_match_pattern(ModePrepDb, self.base_mode_sequence)

        # PPT and Extra Terminals from skippers, and indentation handlers
        #
        reload_state_forward = ReloadState(EngineType=engine.FORWARD, 
                                           dial_db=self.dial_db)
        ppt_list.collect_loopers(self.loopers, self.counter_db, 
                                 reload_state_forward)

        self.doc_history_deletion,        \
        self.doc_history_reprioritization = \
                       ppt_list.delete_and_reprioritize(self.base_mode_sequence)

        return ppt_list.finalize_pattern_list(), \
               ppt_list.finalize_terminal_db(self.incidence_db), \
               ppt_list.finalize_run_time_counter_required_f(), \
               reload_state_forward

    def finalize(self, ModePrepDb):
        assert self.implemented_f

        def filter_implemented(L):
            return [m for m in L if ModePrepDb[m].implemented_f]

        self.doc = ModeDocumentation(self.doc_history_deletion,
                                     self.doc_history_reprioritization,
                                     filter_implemented(self.entry_mode_name_list),
                                     filter_implemented(self.exit_mode_name_list),
                                     filter_implemented(self.base_mode_name_sequence))

        if not self.run_time_counter_required_f:
            run_time_counter_db = None
        else:
            run_time_counter_db = self.counter_db.count_command_map

        return Mode(self.name, self.sr, 
                    self.pattern_list, self.terminal_db, self.incidence_db,
                    RunTimeCounterDb   = run_time_counter_db,
                    ReloadStateForward = self.reload_state_forward,
                    Documentation      = self.doc, 
                    dial_db            = self.dial_db)

    def __determine_implemented_f(self):
        """If the mode has incidences and/or patterns defined it is free to be 
        abstract or not. If neither one is defined, it cannot be implemented and 
        therefore MUST be abstract.
        """
        abstract_f = (self.options_db.value("inheritable") == "only")

        if self.incidence_db or self.pattern_list:
            return abstract_f

        elif not abstract_f:
            error.warning("Mode without pattern and event handlers needs to be 'inheritable only'.\n" + \
                          "<inheritable: only> has been set automatically.", self.sr)
            abstract_f = True # Change to 'inheritable: only', i.e. abstract_f == True.

        return abstract_f

    def check_consistency(self):
        # (*) Modes that are inherited must allow to be inherited
        #     __base_mode_sequence[-1] == the mode itself.
        for base_mode in self.base_mode_sequence[:-1]:
            if base_mode.option_db.value("inheritable") == "no":
                error.log("mode '%s' inherits mode '%s' which is not inheritable." % \
                          (self.name, base_mode.name), self.sr)

    def unique_pattern_pair_iterable(self):
        """Iterates over pairs of patterns:

            (high precedence pattern, low precedence pattern)

           where 'pattern_i' as precedence over 'pattern_k'
        """
        for i, high in enumerate(self.pattern_list):
            for low in islice(self.pattern_list, i+1, None):
                yield high, low

    def check_special_incidence_outrun(self, ErrorCode):
        for high, low in self.unique_pattern_pair_iterable():
            if     high.pattern_string() not in Mode_Prep.focus \
               and low.pattern_string()  not in Mode_Prep.focus: continue
            
            elif not outrun_checker.do(high.sm, low.sm):                  
                continue
            error.log_consistency_issue(high, low, ExitF=True, 
                            ThisComment  = "has lower priority but",
                            ThatComment  = "may outrun",
                            SuppressCode = ErrorCode)
                                 
    def check_higher_priority_matches_subset(self, ErrorCode):
        """Checks whether a higher prioritized pattern matches a common subset
           of the ReferenceSM. For special patterns of skipper, etc. this would
           be highly confusing.
        """
        global special_pattern_list
        for high, low in self.unique_pattern_pair_iterable():
            if     high.pattern_string() not in Mode_Prep.focus \
               and low.pattern_string() not in Mode_Prep.focus: continue

            if not superset_check.do(high.sm, low.sm):             
                continue

            error.log_consistency_issue(high, low, ExitF=True, 
                            ThisComment  = "has higher priority and",
                            ThatComment  = "matches a subset of",
                            SuppressCode = ErrorCode)

    def check_dominated_pattern(self, ErrorCode):
        for high, low in self.unique_pattern_pair_iterable():
            # 'low' comes after 'high' => 'i' has precedence
            # Check for domination.
            if superset_check.do(high, low):
                error.log_consistency_issue(high, low, 
                                ThisComment  = "matches a superset of what is matched by",
                                EndComment   = "The former has precedence and the latter can never match.",
                                ExitF        = True, 
                                SuppressCode = ErrorCode)

    def check_match_same(self, ErrorCode):
        """Special patterns shall never match on some common lexemes."""
        for high, low in self.unique_pattern_pair_iterable():
            if     high.pattern_string() not in Mode_Prep.focus \
               and low.pattern_string() not in Mode_Prep.focus: continue

            # A superset of B, or B superset of A => there are common matches.
            if not same_check.do(high.sm, low.sm): continue

            # The 'match what remains' is exempted from check.
            if high.pattern_string() == "." or low.pattern_string() == ".":
                continue

            error.log_consistency_issue(high, low, 
                            ThisComment  = "matches on some common lexemes as",
                            ThatComment  = "",
                            ExitF        = True,
                            SuppressCode = ErrorCode)

    def check_low_priority_outruns_high_priority_pattern(self):
        """Warn when low priority patterns may outrun high priority patterns.
        Assume that the pattern list is sorted by priority!
        """
        for high, low in self.unique_pattern_pair_iterable():
            if outrun_checker.do(high.sm, low.sm):
                error.log_consistency_issue(low, high, ExitF=False, ThisComment="may outrun")

PatternRepriorization = namedtuple("PatternRepriorization", ("pattern", "new_pattern_index", "sr"))
PatternDeletion       = namedtuple("PatternDeletion",       ("pattern", "pattern_index",     "sr"))


class PatternActionPair(object):
    __slots__ = ("__pattern", "__action")
    @typed(ThePattern=(Pattern_Prep, Pattern))
    def __init__(self, ThePattern, TheAction):
        self.__pattern = ThePattern
        self.__action  = TheAction

    @property
    def line_n(self):    return self.action().sr.line_n
    @property
    def file_name(self): return self.action().sr.file_name

    def pattern(self):   return self.__pattern

    def action(self):    return self.__action

    def __repr__(self):         
        txt  = ""
        if self.pattern() not in E_IncidenceIDs:
            txt += "self.pattern_string = %s\n" % repr(self.pattern().pattern_string())
        txt += "self.pattern        = %s\n" % repr(self.pattern()).replace("\n", "\n      ")
        txt += "self.action         = %s\n" % self.action().get_text()
        if hasattr(self.action(), "sr"):
            txt += "self.file_name  = %s\n" % repr(self.action().sr.file_name) 
            txt += "self.line_n     = %s\n" % repr(self.action().sr.line_n) 
        txt += "self.incidence_id = %s\n" % repr(self.pattern().incidence_id()) 
        return txt

class Loopers:
    """Loopers -- loops that are integrated into the pattern state machine.
    """
    def __init__(self, Skip, SkipRange, SkipNestedRange, IndentationHandler):
        self.skip                = Skip
        self.skip_range          = SkipRange
        self.skip_nested_range   = SkipNestedRange
        self.indentation_handler = IndentationHandler

    def finalize(self, CaMap):
        self.skip = [
            (pattern.finalize(CaMap), total_set)
            for pattern, total_set in self.skip
        ]

        def finalize_skip_range_data(data, CaMap):
            data["opener_pattern"] = data["opener_pattern"].finalize(CaMap)

        self.skip_range = [
            finalize_skip_range_data(data)
            for data in self.skip_range
        ]

        def finalize_skip_nested_range_data(data, CaMap):
            data["opener_pattern"] = data["opener_pattern"].finalize(CaMap)
            data["closer_pattern"] = data["closer_pattern"].finalize(CaMap)

        self.skip_nested_range = [
            finalize_skip_nested_range_data(data)
            for data in self.skip_nested_range
        ]

        self.indentation_handler.pattern_newline.finalize(CaMap)
        self.indentation_handler.pattern_newline_supressor.finalize(CaMap)
        self.indentation_handler.pattern_newline_comment.finalize(CaMap)
        self.indentation_handler.pattern_whitespace.finalize(CaMap)


