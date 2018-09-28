from   quex.input.code.base                               import SourceRef
from   quex.engine.misc.tools                             import typed
import quex.engine.state_machine.construction.combination as     combination

class BasicMode:
    """Very basic information about a 'Mode'. Basically, only use the 
    'PatternList' to determine related state machines.
    """
    def __init__(self, Name, PatternList):
        self.name = Name

        self.sm,                        \
        self.pre_context_sm,            \
        self.bipd_sm_to_be_reversed_db, \
        self.pre_context_sm_id_list     = self.__prepare(PatternList)

    def longest_pre_context(self):
        if not self.pre_context_sm: return 0
        return self.pre_context_sm.longest_path_to_first_acceptance()

    def __prepare(self, PatternList):
        # -- setup of state machine lists and id lists
        core_sm_list,                 \
        pre_context_sm_list,          \
        incidence_id_and_bipd_sm_to_be_reversed_list = self.__prepare_sm_lists(PatternList)

        # (*) Create (combined) state machines
        #     Backward input position detection (bipd) remains separate engines.
        return combination.do(core_sm_list),                  \
               combination.do(pre_context_sm_list,            \
                              FilterDominatedOriginsF=False), \
               dict((incidence_id, sm) for incidence_id, sm in incidence_id_and_bipd_sm_to_be_reversed_list), \
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
        bipd_sm_to_be_reversed_list = [
            (pattern.incidence_id, pattern.sm_bipd_to_be_reversed) for pattern in PatternList 
            if pattern.sm_bipd_to_be_reversed is not None 
        ]
        return sm_list, pre_context_sm_list, bipd_sm_to_be_reversed_list

class Mode(BasicMode):
    """Finalized 'Mode' as it results from combination of base modes.
    ____________________________________________________________________________

    Modes are developpe in three steps:

        (i)   Parsing                                     --> Mode_PrepPrep
        (ii)  Inheritance Handling of all Mode_PrepPrep-s --> Mode_Prep
        (iii) Finalization of Mode_Prep                   --> Mode

    ____________________________________________________________________________
    """
    __mode_id_counter = 0

    @typed(Name=(str,unicode), Sr=SourceRef)
    def __init__(self, Name, Sr, 
                 PatternList, TerminalDb, ExtraAnalyzerList, IncidenceDb,
                 RunTimeCounterDb, ReloadStateForward, RequiredRegisterSet,
                 dial_db, Documentation):
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
        assert all(p.incidence_id in TerminalDb for p in PatternList)
        self.name    = Name
        self.sr      = Sr
        self.mode_id = Mode.__mode_id_counter  # Used for mode sorting, nothing else.
        Mode.__mode_id_counter += 1

        self.terminal_db         = TerminalDb
        self.extra_analyzer_list = ExtraAnalyzerList
        self.incidence_db        = IncidenceDb

        self.run_time_counter_db  = RunTimeCounterDb # None, if not counter required.

        self.reload_state_forward  = ReloadStateForward
        self.required_register_set = RequiredRegisterSet
        self.dial_db               = dial_db

        self.documentation = Documentation
        self.documentation.absorb_pattern_list(PatternList)

        BasicMode.__init__(self, Name, PatternList)

    def entry_mode_name_list(self):
        return self.documentation.entry_mode_name_list

    def exit_mode_name_list(self):
        return self.documentation.exit_mode_name_list

    def implemented_base_mode_name_sequence(self):
        """RETURNS: List of names of base modes which are actually implemented.
        """
        assert self.documentation.base_mode_name_sequence[-1] == self.name
        return self.documentation.base_mode_name_sequence

