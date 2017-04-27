# (C) Frank-Rene Schaefer
from   quex.input.code.base                                      import SourceRef_VOID, \
                                                                        SourceRef
from   quex.engine.state_machine.core                            import StateMachine
from   quex.engine.state_machine.character_counter               import SmLineColumnCountInfo
import quex.engine.state_machine.construction.setup_post_context as     setup_post_context
import quex.engine.state_machine.construction.setup_pre_context  as     setup_pre_context
import quex.engine.state_machine.algorithm.beautifier            as     beautifier
import quex.engine.state_machine.algebra.reverse                 as     reverse
import quex.engine.misc.error                                    as     error
from   quex.engine.misc.tools                                    import typed

from   quex.engine.pattern import Pattern

from   quex.blackboard  import setup as Setup
import quex.blackboard  as blackboard

class Pattern_Prep(object):
    __slots__ = ("__sr", # Source Reference (filename, line_n)
                 "__sm", 
                 "__post_context_f", 
                 "__post_context_sm",
                 "__pre_context_sm_to_be_inverted", 
                 "__pre_context_begin_of_line_f", 
                 "__post_context_end_of_line_f", 
                 "__pattern_string",
                 "__finalized_self")
    @typed(CoreSM=StateMachine, BeginOfLineF=bool, EndOfLineF=bool, 
           AllowNothingIsNecessaryF=bool, Sr=SourceRef)
    def __init__(self, CoreSM, PreContextSM=None, PostContextSM=None, 
                 BeginOfLineF=False, EndOfLineF=False, Sr=SourceRef_VOID, 
                 PatternString="",
                 AllowNothingIsNecessaryF=False):
        def assert_sm(sm):
            if sm is None: return
            assert isinstance(sm, StateMachine)
            assert sm.is_DFA_compliant()
        assert CoreSM is not None
        assert_sm(CoreSM)
        assert_sm(PreContextSM)
        assert_sm(PostContextSM)

        self.check_initial(CoreSM, 
                           BeginOfLineF, PreContextSM, 
                           EndOfLineF, PostContextSM, 
                           Sr,
                           AllowNothingIsNecessaryF)

        self.__pattern_string = PatternString
        self.__sr             = Sr

        # (*) Setup the whole pattern
        self.__sm                         = CoreSM
        self.__post_context_sm            = PostContextSM
        self.__post_context_end_of_line_f = EndOfLineF

        # -- [optional] pre contexts
        #
        #    Same as for backward input position detection holds for pre-contexts.
        self.__pre_context_sm_to_be_inverted = PreContextSM

        # Detect the trivial pre-context
        self.__pre_context_begin_of_line_f = BeginOfLineF
        
        self.__validate(Sr)
        self.__finalized_self = None

    @property
    def sr(self):             return self.__sr

    @typed(Sr=SourceRef)
    def set_source_reference(self, Sr):
        self.__sr = Sr

    def pattern_string(self): return self.__pattern_string

    def set_pattern_string(self, Value): self.__pattern_string = Value

    def incidence_id(self):   return self.__sm.get_id()

    def set_incidence_id(self, Id):
        self.__sm.set_id(Id)

    @property
    def sm(self):                                  return self.__sm
    @property
    def pre_context_sm_to_be_inverted(self):       return self.__pre_context_sm_to_be_inverted
    @property
    def pre_context_trivial_begin_of_line_f(self): 
        if self.__pre_context_sm_to_be_inverted is not None:
            return False
        return self.__pre_context_begin_of_line_f

    def has_pre_context(self): 
        return    self.__pre_context_begin_of_line_f \
               or self.__pre_context_sm_to_be_inverted is not None
    def has_post_context(self):   
        return    self.__post_context_sm is not None \
               or self.__post_context_end_of_line_f
    def has_pre_or_post_context(self):
        return self.has_pre_context() or self.has_post_context()

    def __validate(self, Sr):
        # (*) It is essential that state machines defined as patterns do not 
        #     have origins.
        if self.__sm.has_origins():
            error.log("Regular expression parsing resulted in state machine with origins.\n" + \
                      "Please, log a defect at the projects website quex.sourceforge.net.\n", Sr)

        # (*) Acceptance states shall not store the input position when they are 'normally'
        #     post-conditioned. Post-conditioning via the backward search is a different 
        #     ball-game.
        acceptance_f = False
        for state in self.__sm.states.values():
            if state.is_acceptance(): 
                acceptance_f = True
            if     state.input_position_store_f() \
               and state.is_acceptance():
                error.log("Pattern with post-context: An irregularity occurred.\n" + \
                          "(end of normal post-contexted core pattern is an acceptance state)\n" 
                          "Please, log a defect at the projects website quex.sourceforge.net.", Sr)

        if acceptance_f == False:
            error.log("Pattern has no acceptance state and can never match.\n" + \
                      "Aborting generation process.", Sr)

        self.assert_consistency()

    def __repr__(self):
        return self.get_string(self)

    def get_string(self, NormalizeF=False, Option="utf8"):
        assert Option in ["utf8", "hex"]

        msg = self.__sm.get_string(NormalizeF, Option)
            
        if self.__pre_context_sm_to_be_inverted is not None:
            msg += "pre-context to be inverted = "
            msg += self.__pre_context_sm_to_be_inverted.get_string(NormalizeF, Option)           

        return msg

    def assert_consistency(self):
        assert self.sm.is_DFA_compliant()
        assert not self.sm.has_orphaned_states()
        if self.pre_context_sm_to_be_inverted is not None:
            assert self.pre_context_sm_to_be_inverted.is_DFA_compliant() 
            assert not self.pre_context_sm_to_be_inverted.has_orphaned_states()

    @staticmethod
    def check_initial(core_sm, 
                      begin_of_line_f, pre_context, 
                      end_of_line_f,   post_context, 
                      Sr, 
                      AllowNothingIsNecessaryF):

        def check(Name, Sm, Sr):
            if Sm is None: 
                return

            elif Sm.has_orphaned_states(): 
                error.log("Orphaned state(s) detected in %spattern (optimization lack).\n" % Name + \
                          "Please, log a defect at the projects website quex.sourceforge.net.\n"    + \
                          "Orphan state(s) = " + repr(Sm.get_orphaned_state_index_list()), 
                          Sr, DontExitF=True)
            elif Sm.is_Empty():
                error.log("Empty %spattern." % Name, Sr)

            elif not AllowNothingIsNecessaryF:
                # 'Nothing is necessary' cannot be accepted. 
                # See the discussion in the module "quex.output.core.engine".
                Pattern_Prep.detect_path_of_nothing_is_necessary(Sm,  Name.strip(),  post_context_f, Sr)

        post_context_f = (post_context is not None)
        for name, sm in [("pre-context ", pre_context), ("", core_sm), ("post-context ", post_context)]:
            check(name, sm, Sr)

    @staticmethod
    def detect_path_of_nothing_is_necessary(sm, Name, PostContextPresentF, fh):
        assert Name in ["", "pre-context", "post-context"]
        if sm is None: 
            return
        elif not sm.get_init_state().is_acceptance(): 
            return
        if len(Name) == 0: name_str = "core pattern"
        else:              name_str = Name

        msg = "The %s contains in a 'nothing is necessary' path in the state machine.\n"   \
              % name_str                                                                     + \
              "This means, that without reading a character the analyzer drops into\n"   + \
              "an acceptance state. "

        msg += { 
            "":
                "The analyzer would then stall.",

            "pre-context":
                "E.g., pattern 'x*/y/' means that zero or more 'x' are a pre-\n"             + \
                "condition for 'y'. If zero appearances of 'x' are enough, then obviously\n" + \
                "there is no pre-context for 'y'! Most likely the author intended 'x+/y/'.",

            "post-context":
                "A post context where nothing is necessary is superfluous.",
        }[Name]

        if Name != "post-context" and PostContextPresentF:
            msg += "\n"                                                          \
                   "Note: A post context does not change anything to that fact." 

        error.log(msg, fh)

    def finalize(self, CaMap):
        """NOTE: The finalization leaves the 'Specifer_Pattern' in a dysfunctional
        state. It is no longer to be used--the generated 'Pattern' object takes
        its place.
        """
        if self.__finalized_self is not None:
            return self.__finalized_self

        # Count information must be determined BEFORE transformation!
        if CaMap is not None:
            lcci = SmLineColumnCountInfo.from_StateMachine(CaMap, self.sm, 
                                                           self.pre_context_trivial_begin_of_line_f, 
                                                           Setup.buffer_codec)
        else: 
            lcci = None

        # (*) Transform all state machines into buffer codec
        #     => may change state machine id 
        #     => backup the original id and restore later
        original_incidence_id = self.incidence_id()

        verdict_f,      \
        sm_main,                       \
        sm_pre_context_to_be_inverted, \
        sm_post_context                = self.__finalize_transform(Setup.buffer_codec)
        if not verdict_f:
            error.warning("Pattern contains elements not found in engine codec '%s'.\n" % Setup.buffer_codec.name \
                          + "(Buffer element size is %s [byte])" % Setup.buffer_lexatom_size_in_byte,
                          self.sr)

        sm_main.set_id(original_incidence_id)

        # (*) Cut the signalling characters from any state machine
        self.__finalize_cut_signal_character_list([sm_main, 
                                                   sm_pre_context_to_be_inverted, 
                                                   sm_post_context])

        # (*) Pre-contexts and BIPD can only be mounted, after the transformation.
        sm_main, sm_bipd = self.__finalize_mount_post_context_sm(sm_main, 
                                                                 sm_post_context,
                                                                 self.__post_context_end_of_line_f)
        sm_pre_context = self.__finalize_mount_pre_context_sm(sm_main, 
                                                              sm_pre_context_to_be_inverted,
                                                              self.__pre_context_begin_of_line_f)

        # Store finalized self
        if self.__pattern_string is not None: pattern_string = self.__pattern_string
        else:                                 pattern_string = ""
        if self.__sr is None: sr = SourceRef_VOID
        else:                 sr = self.__sr

        self.__finalized_self = Pattern(original_incidence_id, 
                                        sm_main, sm_pre_context, sm_bipd,
                                        lcci, 
                                        PatternString = pattern_string, 
                                        Sr            = sr)

        # Set: self = Dysfunctional! (after storing finalized 'self')
        self.__sm                            = None
        self.__pattern_string                = None
        self.__sr                            = None
        self.__post_context_sm               = None
        self.__post_context_end_of_line_f    = None
        self.__post_context_f                = None
        self.__pre_context_sm_to_be_inverted = None
        self.__pre_context_begin_of_line_f   = None

        return self.__finalized_self

    def __finalize_mount_pre_context_sm(self, Sm, SmPreContextToBeInverted, BeginOfLineF):
        if SmPreContextToBeInverted is None and BeginOfLineF == False:
            return None

        return setup_pre_context.do(Sm, SmPreContextToBeInverted, BeginOfLineF)

    def __finalize_mount_post_context_sm(self, Sm, SmPostContext, EndOfLineF):
        # In case of a 'trailing post context' a 'bipd_sm' may be provided
        # to detect the input position after match in backward direction.
        # BIPD = backward input position detection.
        sm,     \
        bipd_sm_to_be_inverted = setup_post_context.do(Sm, SmPostContext, EndOfLineF,
                                                       self.__sr)

        if bipd_sm_to_be_inverted is None: 
            return sm, None

        elif not bipd_sm_to_be_inverted.is_DFA_compliant(): 
            bipd_sm_to_be_inverted = beautifier.do(bipd_sm_to_be_inverted)

        bipd_sm = reverse.do(bipd_sm_to_be_inverted)

        return sm, bipd_sm

    def __finalize_cut_signal_character_list(self, sm_list):
        """Characters can only be cut, if transformation is done and 
        pre- and bipd are mounted.
        """
        def my_error(Name, Pattern):
            error.log("Pattern becomes empty after deleting signal character '%s'." % Name,
                      Pattern.sr)

        for character, name in blackboard.signal_character_list(Setup):
            for sm in sm_list:
                if sm is None: continue
                sm.delete_transitions_on_number(character)
                sm.clean_up()
                if sm.is_Empty(): 
                    my_error(name, self)

    def __finalize_transform(self, TrafoInfo):
        """Transform state machine if necessary."""
        # Make sure that a pattern is never transformed twice
        # Transformation MUST be called before any pre-context or bipd
        # is mounted.

        # IncidenceId == StateMachine's id. 
        # However: Transformation may generate a new state machine.
        # => To maintain incidence id, store the original one and restore it
        #    after transformation. 
        c0, sm                            = Setup.buffer_codec.do_state_machine(self.__sm) 
        c1, pre_context_sm_to_be_inverted = Setup.buffer_codec.do_state_machine(self.__pre_context_sm_to_be_inverted) 
        c2, post_context_sm               = Setup.buffer_codec.do_state_machine(self.__post_context_sm) 
        verdict = c0 and c1 and c2

        # Only if all transformations have been complete, then the transformation
        # can be considered complete.

        return verdict, \
               sm, \
               pre_context_sm_to_be_inverted, \
               post_context_sm

