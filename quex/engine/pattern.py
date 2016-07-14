from   quex.engine.state_machine.character_counter import SmLineColumnCountInfo
from   quex.engine.misc.tools import typed


class Pattern:
    """ALL STATE MACHINES ARE GIVEN IN THE CODEC OF 'Setup.buffer_codec'!

    .sm:
            Main state machine to match in forward direction for 
            incoming lexemes.

    .sm_pre_context:

            If not None: state machine in backward direction to match
            against a necessary pre-context. If the pre-context is not
            given, this pattern cannot match.

    .sm_bipd:

            State machine to detect the input position in backward 
            direction. This is necessary to deal with the trailing 
            post context problem.

    .line_column_count_info:
            
            Tells how to determine the change of line and column 
            number upon match of this pattern.
    """
    @typed(LCCI=SmLineColumnCountInfo, PatternString=(str,unicode))
    def __init__(self, IncidenceId, Sm, PreContextSm, BipdSm, LCCI, PatternString, Sr):
        assert IncidenceId == Sm.get_id()
        self.incidence_id           = IncidenceId
        self.sm                     = Sm
        self.sm_pre_context         = PreContextSm
        self.sm_bipd                = BipdSm
        # lcci = line column count information for main state machine
        self.lcci                   = LCCI

        self.__pattern_string       = PatternString
        self.sr                     = Sr

    def pattern_string(self):
        return self.__pattern_string # May be, later generate it on demand

    def has_pre_context(self): 
        return self.sm_pre_context is not None

    def clone(self, NewIncidenceId=None):
        new_sm = self.sm.clone()

        if self.sm_pre_context is not None: new_sm_pre_context = self.sm_pre_context.clone()
        else:                               new_sm_pre_context = None
        if self.sm_bipd is not None: new_sm_bipd = self.sm_bipd.clone()
        else:                        new_sm_bipd = None

        if NewIncidenceId is not None:
            new_sm.set_id(NewIncidenceId)

        return Pattern(new_sm.get_id(), new_sm, new_sm_pre_context, new_sm_bipd,
                       self.lcci, self.__pattern_string, self.sr)
