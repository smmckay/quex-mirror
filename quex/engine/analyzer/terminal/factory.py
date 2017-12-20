# (C) Frank-Rene Schaefer
from   quex.input.code.core                        import CodeFragment, \
                                                          CodeTerminal
from   quex.engine.pattern                         import Pattern
from   quex.engine.analyzer.terminal.core          import Terminal
from   quex.engine.analyzer.door_id_address_label  import DoorID
from   quex.engine.misc.tools                      import typed

from   quex.output.counter.pattern                 import map_SmLineColumnCountInfo_to_code

import quex.blackboard as blackboard
from   quex.blackboard import Lng
from   quex.constants  import E_IncidenceIDs, \
                              E_TerminalType

def _aux_adorn_nothing(Code):
    return Code

def _aux_adorn_on_skip_range_open(Code):
    return CodeTerminal([
        "%s\n" % Lng.DEFINE_NESTED_RANGE_COUNTER(), 
        Lng.SOURCE_REFERENCED(Code)
    ])

aux_db = {
    E_TerminalType.PLAIN:           (_aux_adorn_nothing, None, False, ""),
    E_TerminalType.MATCH_PATTERN:   (_aux_adorn_nothing, None, False, ""),

    E_TerminalType.MATCH_FAILURE:   (_aux_adorn_nothing, "FAILURE", True, ""),

    E_TerminalType.END_OF_STREAM:   
     (_aux_adorn_nothing, "END_OF_STREAM", False,
      "End of Stream FORCES a return from the lexical analyzer, so that no\n" \
      "tokens can be filled after the termination token.",
     ),
    E_TerminalType.BAD_LEXATOM:     
     (_aux_adorn_nothing, "BAD_LEXATOM", True,
      "Bad lexatom detection FORCES a return from the lexical analyzer, so that no\n" \
      "tokens can be filled after the termination token.",
     ),
    E_TerminalType.LOAD_FAILURE:    
     (_aux_adorn_nothing, "LOAD_FAILURE", True,
      "Load failure FORCES a return from the lexical analyzer, so that no\n" \
      "tokens can be filled after the termination token.",
     ),
    E_TerminalType.SKIP_RANGE_OPEN: 
     (_aux_adorn_on_skip_range_open, "SKIP_RANGE_OPEN", True,
      "End of Stream appeared, while scanning for end of skip-range.",
     ),
}

class TerminalFactory:
    """Factory for Terminal-s
    ___________________________________________________________________________

    A TerminalStateFactory generates Terminal-s by its '.do()' member function.
    Terminal-s are created dependent on the E_TerminalTypes indicator.  The
    whole process is initiated in its constructor.

    Additionally, the factory keeps track of the necessity to count lexemes
    and the necessity of a default counter for line and column number.
    ___________________________________________________________________________
    """
    def __init__(self, ModeName, IncidenceDb, dial_db): 
        """Sets up the terminal factory, i.e. specifies all members required
        in the process of Terminal construction. 
        """
        self.run_time_counter_required_f = False
        self.mode_name    = ModeName
        self.incidence_db = IncidenceDb
        self.dial_db      = dial_db

        if blackboard.required_support_indentation_count(): 
            self.txt_indentation_handler_call = Lng.INDENTATION_HANDLER_CALL(ModeName) 
        else:
            self.txt_indentation_handler_call = ""

        self.txt_store_last_character = Lng.STORE_LAST_CHARACTER(blackboard.required_support_begin_of_line())

        self.on_match       = IncidenceDb.get_CodeTerminal(E_IncidenceIDs.MATCH)
        self.on_after_match = IncidenceDb.get_CodeTerminal(E_IncidenceIDs.AFTER_MATCH)

    @typed(Code=CodeFragment)
    def do(self, TerminalType, Code, ThePattern=None):
        """Construct a Terminal object based on the given TerminalType and 
        parameterize it with 'IncidenceId' and 'Code'.
        """
        global aux_db

        if ThePattern is not None:
            assert ThePattern.count_info() is not None

        if TerminalType in (E_TerminalType.END_OF_STREAM, 
                            E_TerminalType.BAD_LEXATOM, 
                            E_TerminalType.LOAD_FAILURE,
                            E_TerminalType.SKIP_RANGE_OPEN):

            adorn, name, raise_error_f, comment_txt = aux_db[TerminalType]
            if raise_error_f:
                Code.insert_front(Lng.RAISE_ERROR_FLAG_BY_TERMINAL_TYPE(TerminalType))

            return self.__terminate_analysis_step(adorn(Code), name, comment_txt)
        else:
            return {
                E_TerminalType.PLAIN:           self.do_plain,
                E_TerminalType.MATCH_PATTERN:   self.do_match_pattern,
                # Error handlers:
                E_TerminalType.MATCH_FAILURE:   self.do_match_failure,
            }[TerminalType](Code, ThePattern)

    @typed(ThePattern=Pattern)
    def do_match_pattern(self, Code, ThePattern):
        """A pattern has matched."""

        lexeme_begin_f,     \
        terminating_zero_f, \
        adorned_code        = self.__adorn_user_code(Code, MatchF=True)

        # IMPORTANT: Terminals can be entered by any kind of 'GOTO'. In order to
        #            be on the safe side, BIPD should be started from within the
        #            terminal itself. Otherwise, it may be missed due to some 
        #            coding negligence.
        text = []
        if ThePattern.sm_bipd is not None:
            self.do_bipd_entry_and_return(text, ThePattern)

        text.extend([
            self.__counter_code(ThePattern.lcci),
            #
            adorned_code,
            #
            Lng.RETURN # 'RETURN' since mode change may have occurred
        ])
        t = self.__terminal(text, Code, 
                            ThePattern.pattern_string(),
                            IncidenceId            = ThePattern.incidence_id,
                            LexemeBeginF           = lexeme_begin_f,
                            LexemeTerminatingZeroF = terminating_zero_f)
        assert t.incidence_id() == ThePattern.incidence_id
        return t

    def do_match_failure(self, Code, ThePattern):
        """No pattern in the mode has matched. Line and column numbers are 
        still counted. But, no 'on_match' or 'on_after_match' action is 
        executed.
        """
        lexeme_begin_f,     \
        terminating_zero_f, \
        adorned_code        = self.__adorn_user_code(Code, MatchF=False)

        text = [ 
            #Lng.IF_END_OF_FILE(),
            #    self.__counter_code(None),
            #    Lng.GOTO(DoorID.continue_without_on_after_match()),
            #Lng.IF_INPUT_P_EQUAL_LEXEME_START_P(FirstF=False),
            #    Lng.INPUT_P_INCREMENT(),
            #Lng.END_IF(),
            self.__counter_code(None),
            #
            adorned_code,
            #
            Lng.PURE_RETURN # 'RETURN' since mode change may have occurred
        ]
        return self.__terminal(text, Code, "FAILURE")

    def do_plain(self, Code, ThePattern, NamePrefix="", RequiredRegisterSet=None):
        """Plain source code text as generated by quex."""

        text = []
        text.extend(self.__counter_code(ThePattern.lcci))
        text.extend(Code.get_code())

        if ThePattern is None: name = "<no name>"
        else:                  name = ThePattern.pattern_string() 
        name = "%s%s" % (NamePrefix, name)

        return self.__terminal(text, Code, name, 
                               IncidenceId         = ThePattern.incidence_id, 
                               RequiredRegisterSet = RequiredRegisterSet)

    def __lexeme_flags(self, Code):
        lexeme_begin_f     =    self.on_match.requires_lexeme_begin_f(Lng)      \
                             or Code.requires_lexeme_begin_f(Lng)               \
                             or self.on_after_match.requires_lexeme_begin_f(Lng) 
        terminating_zero_f =    self.on_match.requires_lexeme_terminating_zero_f(Lng)       \
                             or Code.requires_lexeme_terminating_zero_f(Lng)                \
                             or self.on_after_match.requires_lexeme_terminating_zero_f (Lng)
        return lexeme_begin_f, terminating_zero_f

    def do_bipd_entry_and_return(self, txt, ThePattern):
        """(This is a very seldom case) After the pattern has matched, one needs 
        to determine the end of the lexeme by 'backward input position detection' 
        (bipd). Thus,

              TERMINAL 
                   '----------.
                       (goto) '---------> BIPD DFA
                                               ...
                                          (determine _read_p)
                                               |
                      (label) .----------------'
                   .----------'
                   |
              The actions on 
              pattern match.
        """
        door_id_entry  = DoorID.state_machine_entry(ThePattern.sm_bipd.get_id(), self.dial_db)
        door_id_return = DoorID.bipd_return(ThePattern.incidence_id, self.dial_db)
        txt.append("    %s\n%s\n" 
           % (Lng.GOTO(door_id_entry, self.dial_db),   # Enter BIPD
              Lng.LABEL(door_id_return)) # Return from BIPD
        )

    def __counter_code(self, LCCI):
        """Get the text of the source code required for 'counting'. This information
        has been stored along with the pattern before any transformation happened.
        No database or anything is required as this point.
        """
        run_time_counter_f, \
        text               = map_SmLineColumnCountInfo_to_code(LCCI)

        self.run_time_counter_required_f |= run_time_counter_f
        return "".join(Lng.REPLACE_INDENT(text))

    def __adorn_user_code(self, Code, MatchF):
        """Adorns user code with:
           -- storage of last character, if required for 'begin of line'
              pre-context.
           -- storage of the terminating zero, if the lexeme is required
              as a zero-terminated string.
           -- add the 'on_match' event handler in front, if match is relevant.
           -- adding source reference information.
        """
        code_user = Lng.SOURCE_REFERENCED(Code)

        lexeme_begin_f,    \
        terminating_zero_f = self.__lexeme_flags(Code)

        txt_terminating_zero = Lng.LEXEME_TERMINATING_ZERO_SET(terminating_zero_f)

        if MatchF: txt_on_match = Lng.SOURCE_REFERENCED(self.on_match)
        else:      txt_on_match = ""

        result = "".join([
            self.txt_store_last_character,
            txt_terminating_zero,
            txt_on_match,
            "{\n",
            code_user,
            "\n}\n",
        ])

        return lexeme_begin_f, terminating_zero_f, result

    def __terminate_analysis_step(self, Code, Name, Comment):
        lexeme_begin_f,     \
        terminating_zero_f, \
        adorned_code        = self.__adorn_user_code(Code, MatchF=True)
        
        # No indentation handler => Empty string.
        text = [ 
            Lng.DEFAULT_COUNTER_CALL(),
            self.txt_indentation_handler_call,
            #
            adorned_code,
            #
            Lng.ML_COMMENT(Comment),
            Lng.PURE_RETURN # RETURN without on after match
            #__________________________________________________________________
            #
            # NOT: The following might include that something is sent after 
            #      the TERMINATION token. Also, the above code has *NOTHING'*
            #      to do with pattern match actions. It handles events.
            #
            # Lng.GOTO(DoorID.return_with_on_after_match(self.dial_db), self.dial_db)
            #
            #__________________________________________________________________
        ]
        return self.__terminal(text, Code, Name)

    def __terminal(self, Text, Code, Name,
                   IncidenceId=None,
                   LexemeTerminatingZeroF=False, LexemeBeginF=False,
                   RequiredRegisterSet=None):

        code = CodeTerminal(Text, SourceReference = Code.sr, 
                            PureCode = Code.get_pure_code())

        return Terminal(code, Name, 
                        IncidenceId                   = IncidenceId,
                        RequireLexemeTerminatingZeroF = LexemeTerminatingZeroF,
                        RequiresLexemeBeginF          = LexemeBeginF,
                        RequiredRegisterSet           = RequiredRegisterSet, 
                        dial_db                       = self.dial_db)

