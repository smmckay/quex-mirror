from   quex.input.code.base                               import SourceRef
from   quex.engine.pattern                                import Pattern           
from   quex.engine.misc.tools                             import typed, all_isinstance
import quex.engine.state_machine.construction.combination as     combination

import quex.blackboard as     blackboard
from   quex.blackboard import setup as Setup

from   copy        import deepcopy
from   collections import namedtuple
from   itertools   import islice

class Mode:
    """Finalized 'Mode' as it results from combination of base modes.
    ____________________________________________________________________________

    Modes are developpe in three steps:

        (i)   Parsing                                     --> Mode_PrepPrep
        (ii)  Inheritance Handling of all Mode_PrepPrep-s --> Mode_Prep
        (iii) Finalization of Mode_Prep                   --> Mode

    ____________________________________________________________________________
    """
    __mode_id_counter = -1

    @typed(Name=(str,unicode), Sr=SourceRef)
    def __init__(self, Name, Sr, 
                 PatternList, TerminalDb, IncidenceDb,
                 RunTimeCounterDb, 
                 ReloadStateForward, dial_db, 
                 Documentation):
        """Information about a lexical analyzer mode:
        
           Name:        Name of the mode.
           Sr:          SourceReference

        Data to generate the lexical analyzer function:

           PatternList: List of finalized Pattern objects
                        (identifier by 'incidence_id')
           TerminalDb:  Database that connects match patterns to 'actions'.
                        maps: 'incidence_id' --> 'Terminal'
           IncidenceDb: Determines actions to be performed upon general incidences.
                        (Mode entry, exit, ...)

        Data to generate auxiliary helper function:

           RunTimeCounterDb: If not 'None' contains information to generate a 
                             run-time character counter.

        Data passed on from previous code generation stages. That code
        generation relied on object that are supposed to be common with later
        code generation.
            
           ReloadStateForward: The reload state in forward direction.
           dial_db:            Related DoorID-s to Addresses for state machine 
                               generation and keeps tracked of 'gotoed' 
                               addresses.

        Documentation: Contains information about entry, exit, and base mode names.
        """
        self.name    = Name
        self.sr      = Sr
        self.mode_id = Mode.__mode_id_counter 
        Mode.__mode_id_counter += 1

        self.pattern_list = PatternList
        self.terminal_db  = TerminalDb
        self.incidence_db = IncidenceDb

        self.run_time_counter_db  = RunTimeCounterDb # None, if not counter required.

        self.reload_state_forward = ReloadStateForward
        self.dial_db              = dial_db

        self.documentation = Documentation

        # (*) Core SM, Pre-Context SM, ...
        #     ... and sometimes backward input position SMs.
        self.sm,                    \
        self.pre_context_sm,        \
        self.bipd_sm_db,            \
        self.pre_context_sm_id_list = self.__prepare(PatternList)

    def __prepare(self, PatternList):
        # -- setup of state machine lists and id lists
        core_sm_list,                 \
        pre_context_sm_list,          \
        incidence_id_and_bipd_sm_list = self.__prepare_sm_lists(PatternList)

        # (*) Create (combined) state machines
        #     Backward input position detection (bipd) remains separate engines.
        return combination.do(core_sm_list),                  \
               combination.do(pre_context_sm_list,            \
                              FilterDominatedOriginsF=False), \
               dict((incidence_id, sm) for incidence_id, sm in incidence_id_and_bipd_sm_list), \
               [ sm.get_id() for sm in pre_context_sm_list ]

    def __prepare_sm_lists(self, PatternList):
        # -- Core state machines of patterns
        sm_list = [ pattern.sm for pattern in PatternList ]

        # -- Pre-Contexts
        pre_context_sm_list = [    
            pattern.sm_pre_context for pattern in PatternList 
            if pattern.sm_pre_context is not None 
        ]

        # -- Backward input position detection (BIPD)
        bipd_sm_list = [
            (pattern.incidence_id(), pattern.sm_bipd) for pattern in PatternList 
            if pattern.sm_bipd is not None 
        ]
        return sm_list, pre_context_sm_list, bipd_sm_list

    def entry_mode_name_list(self):
        return self.documentation.entry_mode_name_list

    def exit_mode_name_list(self):
        return self.documentation.exit_mode_name_list

    def implemented_base_mode_name_sequence(self):
        """RETURNS: List of names of base modes which are actually implemented.
        """
        assert self.documentation.base_mode_name_sequence[-1] == self.name
        return self.documentation.base_mode_name_sequence

    def get_documentation(self):
        L = max(map(lambda mode: len(mode.name), self.__base_mode_sequence))
        txt  = ["\nMODE: %s\n\n" % self.name]

        if len(self.__base_mode_sequence) != 1:
            txt.append("    BASE MODE SEQUENCE:\n")
            base_mode_name_list = map(lambda mode: mode.name, self.__base_mode_sequence[:-1])
            base_mode_name_list.reverse()
            txt.extend(
                "      %s\n" % name 
                for name in base_mode_name_list
            )
            txt.append("\n")

        if len(self.documentation.history_deletion) != 0:
            txt.append("    DELETION ACTIONS:\n")
            txt.extend(
                "      %s:  %s%s  (from mode %s)\n" % \
                (entry[0], " " * (L - len(self.name)), entry[1], entry[2])
                for entry in self.documentation.history_deletion
            )
            txt.append("\n")

        if len(self.documentation.history_reprioritization) != 0:
            txt.append("    PRIORITY-MARK ACTIONS:\n")
            self.documentation.history_reprioritization.sort(lambda x, y: cmp(x[4], y[4]))
            txt.extend(
                "      %s: %s%s  (from mode %s)  (%i) --> (%i)\n" % \
                (entry[0], " " * (L - len(self.name)), entry[1], entry[2], entry[3], entry[4])
                for entry in self.documentation.history_reprioritization
            )
            txt.append("\n")

        assert all_isinstance(self.__pattern_list, Pattern)
        if len(self.__pattern_list) != 0:
            txt.append("    PATTERN LIST:\n")
            txt.extend(
                "      (%3i) %s: %s%s\n" % \
                (x.incidence_id(), x.sr.mode_name, " " * (L - len(x.sr.mode_name)), x.pattern_string())
                for x in self.__pattern_list
            )
            txt.append("\n")

        return "".join(txt)

