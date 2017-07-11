import quex.engine.misc.error                                    as     error
from   quex.engine.misc.interval_handling                        import NumberSet, Interval_All, Interval
import quex.engine.state_machine.algorithm.nfa_to_dfa            as     nfa_to_dfa
import quex.engine.state_machine.algorithm.hopcroft_minimization as     hopcroft_minimization
import quex.engine.state_machine.index                           as     state_machine_index
from   quex.engine.state_machine.state.core                      import DFA_State
from   quex.engine.misc.tools                                    import typed
from   quex.constants                                            import INTEGER_MAX

from   collections     import defaultdict

class EncodingTrafo:
    """Maintains information about a encoding transformation and functions that
    transform numbers and state machines from the 'pure' encoding to a target
    encoding.

        .name       = Name of the codec.
        .source_set = NumberSet of unicode code points which have a representation 
                      the given codec.
        .drain_set  = NumberSet of available code points in the given codec.
    """
    def __init__(self, Name, SourceSet, DrainSet):
        self.name       = Name
        self.source_set = SourceSet   # 'Unicode input'
        self.drain_set  = DrainSet    # 'Range of all code units'.

        # To be adapted later by 'adapt_source_and_drain_range()'
        self.lexatom_range = Interval_All()

    def do_state_machine(self, sm, BadLexatomDetectionF):
        """Transforms a given state machine from 'Unicode Driven' to another
        character encoding type.
        
        RETURNS: 
           [0] Transformation complete (True->yes, False->not all transformed)
           [1] Transformed state machine. It may be the same as it was 
               before if there was no transformation actually.

        It is ensured that the result of this function is a DFA compliant
        state machine.
        """
        if sm is None: return True, None
        assert sm.is_DFA_compliant()

        all_complete_f = True
        if BadLexatomDetectionF: bad_lexatom_si = state_machine_index.get()
        else:                    bad_lexatom_si = None

        # NOTE: Not 'iteritems()', for some encodings intermediate states are 
        #       generated. Those shall not be subject to transformation.
        for from_si, state in sm.states.items():
            target_map = state.target_map.get_map()

            for to_si, trigger_set in target_map.items():

                complete_f,  \
                new_state_db = self.do_transition(from_tm, from_si, to_si, 
                                                  bad_lexatom_si) 
                # Assume that the 'target_map' has been adapted if changes were
                # necessary.

                if new_state_db is not None:
                    sm.states.update(new_state_db)

                all_complete_f &= complete_f

            # Transition to 'bad lexatom acceptor' on first code unit is best
            # to happen here, after all transitions have been adapted.
            if bad_lexatom_si is not None:
                target_map[bad_lexatom_si] = self._error_range_by_code_unit_db[0]

            # If there were intermediate states being generated, the error
            # error detection must have been implemented right then.

        # Generate the 'bad lexatom accepter'.
        bad_lexatom_state = DFA_State(AcceptanceF=True)
        bad_lexatom_state.mark_acceptance_id(E_IncidenceIDs.BAD_LEXATOM)
        self.states[bad_lexatom_si] = bad_lexatom_state

        for from_si, state in sm.states.items():
            target_map = state.target_map.get_map()
            for trigger_set in target_map.itervalues():
                trigger_set.mask_interval(self.lexatom_range)

        sm.delete_orphaned_states()

        # AFTER: Whatever happend, the transitions in the state machine MUST
        #        lie in the drain_set.
        # sm.assert_range(self.drain_set)
        if not sm.is_DFA_compliant(): 
            sm = nfa_to_dfa.do(sm)
        sm = hopcroft_minimization.do(sm, CreateNewStateMachineF=False)
        return all_complete_f, sm

    def lexatom_n_per_character(self, CharacterSet):
        return 1     # Default behavior (e.g. UTF8 differs here)

    def lexatom_n_per_character_in_state_machine(self, SM):
        return 1     # Default behavior (e.g. UTF8 differs here)

    def variable_character_sizes_f(self): 
        return False # Default behavior (e.g. UTF8 differs here)

    def adapt_source_and_drain_range(self, LexatomByteN):
        """The drain range may be restricted due to the number of bytes given
        per lexatom. If the 'LexatomByteN' is '-1' it is unrestricted which 
        may be useful for unit tests and theoretical investigations.

        DERIVED CLASS MAY HAVE TO WRITE A DEDICATED VERSION OF THIS FUNCTION
        TO MODIFY THE SOURCE RANGE '.source_set'.
        """
        if LexatomByteN == -1:
            self.lexatom_range = Interval_All()
            return 

        assert LexatomByteN >= 1
        lexatom_min_value = self.drain_set.minimum()
        lexatom_max_value = self.drain_set.least_greater_bound() - 1
        if LexatomByteN != -1:
            try:    
                value_n = 256 ** LexatomByteN
            except:
                error.log("Error while trying to compute 256 power the 'lexatom-size' (%i bytes)\n"   \
                          % LexatomByteN + \
                          "Adapt \"--buffer-element-size\" or \"--buffer-element-type\",\n"       + \
                          "or specify '--buffer-element-size-irrelevant' to ignore the issue.")
            lexatom_min_value = 0
            lexatom_max_value = min(lexatom_max_value, value_n - 1)

        lexatom_max_value = min(lexatom_max_value, INTEGER_MAX)

        assert lexatom_max_value > lexatom_min_value

        self.lexatom_range = Interval(lexatom_min_value, 
                                      lexatom_max_value + 1)
        self.drain_set.mask_interval(self.lexatom_range)
        # Source can only be adapted if the codec is known.

    def hopcroft_minimization_always_makes_sense(self): 
        # Default-wise no intermediate states are generated
        # => hopcroft minimization does not make sense.
        return False

class EncodingTrafoUnicode(EncodingTrafo):
    @typed(SourceSet=NumberSet, DrainSet=NumberSet)
    def __init__(self, SourceSet, DrainSet):
        EncodingTrafo.__init__(self, "unicode", SourceSet, DrainSet)

    def do_transition(self, from_target_map, FromSi, ToSi, BadLexatomSi):
        """Translates to transition 'FromSi' --> 'ToSi' inside the state
        machine according to 'Unicode'.

        'BadLexatomSi' is ignored. This argument is only of interest if
        intermediate states are to be generated. This it not the case for this
        type of transformation.

        RETURNS: [0] True if complete, False else.
                 [1] StateDb of newly generated states (always None, here)
        """
        number_set = from_target_map[ToSi]

        if self.drain_set.is_superset(number_set): 
            return True, None
        else:
            # Adapt 'number_set' in 'from_target_map' according to addmissible
            # range.
            number_set.intersect_with(self.drain_set)
            return False, None

    def adapt_source_and_drain_range(self, LexatomByteN):
        EncodingTrafo.adapt_source_and_drain_range(self, LexatomByteN)
        self.source_set.mask_interval(self.lexatom_range)
