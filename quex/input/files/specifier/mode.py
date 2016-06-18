
#-----------------------------------------------------------------------------------------
# Specifier_Mode/Mode Objects:
#
# During parsing 'Specifier_Mode' objects are generated. Once parsing is over, 
# the descriptions are translated into 'real' mode objects where code can be generated
# from. All matters of inheritance and pattern resolution are handled in the
# transition from description to real mode.
#-----------------------------------------------------------------------------------------
class Specifier_Mode:
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

     (*) .derived_from_list:   [ string ]
     
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
                 "derived_from_list",
                 "option_db",
                 "pattern_action_pair_list",
                 "incidence_db",
                 "reprioritization_info_list",
                 "deletion_info_list")

    def __init__(self, Name, SourceReference):
        # Register Specifier_Mode at the mode database
        blackboard.mode_description_db[Name] = self
        self.name  = Name
        self.sr    = SourceReference

        self.derived_from_list          = []

        self.pattern_action_pair_list   = []  
        self.option_db                  = OptionDB()    # map: option_name    --> OptionSetting
        self.incidence_db               = IncidenceDB() # map: incidence_name --> CodeFragment

        self.reprioritization_info_list = []  
        self.deletion_info_list         = [] 

    @typed(ThePattern=Pattern, Action=CodeUser)
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

    def is_abstract(self, PatternList):
        """If the mode has incidences and/or patterns defined it is free to be 
        abstract or not. If neither one is defined, it cannot be implemented and 
        therefore MUST be abstract.
        """
        abstract_f = (self.option_db.value("inheritable") == "only")

        if len(self.incidence_db) != 0 or len(PatternList) != 0:
            return abstract_f

        elif abstract_f == False:
            error.warning("Mode without pattern and event handlers needs to be 'inheritable only'.\n" + \
                          "<inheritable: only> has been set automatically.", self.sr)
            abstract_f = True # Change to 'inheritable: only', i.e. abstract_f == True.

        return abstract_f

    def determine_base_mode_sequence(self, InheritancePath, base_mode_sequence):
        """Determine the sequence of base modes. The type of sequencing determines
           also the pattern precedence. The 'deep first' scheme is chosen here. For
           example a mode hierarchie of

                                       A
                                     /   \ 
                                    B     C
                                   / \   / \
                                  D  E  F   G

           results in a sequence: (A, B, D, E, C, F, G).reverse()

           => That is the mode itself is base_mode_sequence[-1]

           => Patterns and event handlers of 'E' have precedence over
              'C' because they are the childs of a preceding base mode.

           This function detects circular inheritance.

        __dive -- inserted this keyword for the sole purpose to signal 
                  that here is a case of recursion, which may be solved
                  later on by a TreeWalker.
        """
        if self.name in InheritancePath:
            msg = "mode '%s'\n" % InheritancePath[0]
            for mode_name in InheritancePath[InheritancePath.index(self.name) + 1:]:
                msg += "   inherits mode '%s'\n" % mode_name
            msg += "   inherits mode '%s'" % self.name

            error.log("circular inheritance detected:\n" + msg, self.sr)

        base_mode_name_list_reversed = deepcopy(self.derived_from_list)
        #base_mode_name_list_reversed.reverse()
        for name in base_mode_name_list_reversed:
            # -- does mode exist?
            error.verify_word_in_list(name, blackboard.mode_description_db.keys(),
                                      "Mode '%s' inherits mode '%s' which does not exist." % (self.name, name),
                                      self.sr)

            if name in map(lambda m: m.name, base_mode_sequence): continue

            # -- grab the mode description
            mode_descr = blackboard.mode_description_db[name]
            self.determine_base_mode_sequence(InheritancePath + [self.name], 
                                              base_mode_sequence)

        base_mode_sequence.append(self)

        return base_mode_sequence


PatternRepriorization = namedtuple("PatternRepriorization", ("pattern", "new_pattern_index", "sr"))
PatternDeletion       = namedtuple("PatternDeletion",       ("pattern", "pattern_index",     "sr"))

class PatternActionPair(object):
    __slots__ = ("__pattern", "__action")
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

