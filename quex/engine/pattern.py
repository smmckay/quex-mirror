from   quex.input.code.base                        import SourceRef
from   quex.engine.state_machine.core              import DFA
from   quex.engine.state_machine.character_counter import SmLineColumnCountInfo
from   quex.engine.misc.tools                      import typed
from   quex.constants                              import E_AcceptanceCondition

class Pattern:
    """ALL STATE MACHINES ARE GIVEN IN THE CODEC OF 'Setup.buffer_encoding'!

    .sm:
            Main state machine to match in forward direction for 
            incoming lexemes.

    .sm_pre_context:

            If not None: state machine in backward direction to match
            against a necessary pre-context. If the pre-context is not
            given, this pattern cannot match.

    .sm_bipd_to_be_reversed:

            DFA to detect the input position in backward 
            direction. This is necessary to deal with the trailing 
            post context problem.

    .line_column_count_info:
            
            Tells how to determine the change of line and column 
            number upon match of this pattern.
    """
    @typed(LCCI=(None, SmLineColumnCountInfo), PatternString=(str,unicode), Sr=SourceRef)
    def __init__(self, IncidenceId, Sm, PreContextSm, BipdSmTobeReversed, LCCI, PatternString, Sr):
        assert IncidenceId == Sm.get_id()
        self.incidence_id           = IncidenceId
        self.sm                     = Sm
        self.sm_pre_context         = PreContextSm
        self.sm_bipd_to_be_reversed = BipdSmTobeReversed
        # lcci = line column count information for main state machine
        self.lcci                   = LCCI
        self.sr                     = Sr
        self.__pattern_string       = PatternString

    @staticmethod
    def from_character_set(CharacterSet, StateMachineId, Sr, LCCI=None, PatternString="<character set>"):
        return Pattern(StateMachineId, 
                       DFA.from_character_set(CharacterSet, StateMachineId), 
                       PreContextSm       = None,
                       BipdSmTobeReversed = None, 
                       LCCI          = LCCI,
                       PatternString = PatternString,
                       Sr            = Sr)

    def pattern_string(self):
        return self.__pattern_string # May be, later generate it on demand

    def has_pre_context(self): 
        return    self.sm_pre_context is not None \
               or self.sm.has_acceptance_condition(E_AcceptanceCondition.BEGIN_OF_LINE) \
               or self.sm.has_acceptance_condition(E_AcceptanceCondition.BEGIN_OF_STREAM)

    def clone_with_new_incidence_id(self, NewIncidenceId=None, PatternString=None):
        """Nothing needs to be done, except the main pattern must be associated
        with the NewIncidenceId.

        The state machines in this pattern, therefore, might be referenced in 
        other patterns. It is assumed, though, that they do not change.
        """
        # Once, the incidence id is taken out of the state machine, the main
        # state machine may not have to be cloned either.
        new_sm = self.sm.clone(StateMachineId=NewIncidenceId)
        if PatternString is None: pattern_string = self.__pattern_string
        else:                     pattern_string = PatternString
        return Pattern(new_sm.get_id(), new_sm, self.sm_pre_context, 
                       self.sm_bipd_to_be_reversed,
                       self.lcci, pattern_string, self.sr)
