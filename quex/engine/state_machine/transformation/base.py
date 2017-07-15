from   quex.engine.misc.interval_handling                        import NumberSet 
import quex.engine.state_machine.algorithm.nfa_to_dfa            as     nfa_to_dfa
import quex.engine.state_machine.algorithm.hopcroft_minimization as     hopcroft_minimization
import quex.engine.state_machine.index                           as     state_machine_index
from   quex.engine.state_machine.state.core                      import DFA_State
from   quex.engine.misc.tools                                    import typed
from   quex.constants                                            import E_IncidenceIDs
from   quex.blackboard import setup as Setup

class EncodingTrafo:
    """Maintains information about a encoding transformation and functions that
    transform numbers and state machines from the 'pure' encoding to a target
    encoding.

        .name       = Name of the codec.
        .source_set = NumberSet of unicode code points which have a representation 
                      the given codec.
    """
    @typed(Name=str, SourceSet=NumberSet, DrainSet=NumberSet, ErrorRangeByCodeUnitDb={int:NumberSet})
    def __init__(self, Name, SourceSet, DrainSet, ErrorRangeByCodeUnitDb):
        self.name               = Name
        self.source_set         = SourceSet   # 'Unicode input'

        # For every position in a code unit sequence, there might be a different
        # error range (see UTF8 or UTF16 for example).
        self._error_range_by_code_unit_db = ErrorRangeByCodeUnitDb

    def bad_lexatom_possible(self):
        """If there is any non-empty error range, then a lexatom may occurr
        which is outside the given encoding.
        """
        return any(not error_range.is_empty() 
                   for error_range in self._error_range_by_code_unit_db.itervalues())

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
        assert Setup.lexatom.type_range is not None

        if sm is None: return True, None
        assert sm.is_DFA_compliant()

        all_complete_f = True
        if BadLexatomDetectionF: 
            bad_lexatom_si = state_machine_index.get()
            # Generate the 'bad lexatom accepter'.
            bad_lexatom_state = DFA_State(AcceptanceF=True)
            bad_lexatom_state.mark_acceptance_id(E_IncidenceIDs.BAD_LEXATOM)
            sm.states[bad_lexatom_si] = bad_lexatom_state

        else:                    
            bad_lexatom_si = None

        # NOTE: Not 'iteritems()', for some encodings intermediate states are 
        #       generated. Those shall not be subject to transformation.
        for from_si, state in sm.states.items():
            target_map = state.target_map.get_map()

            for to_si, trigger_set in target_map.items():

                complete_f,  \
                new_state_db = self.do_transition(target_map, from_si, to_si, 
                                                  bad_lexatom_si) 
                # Assume that the 'target_map' has been adapted if changes were
                # necessary.
                if new_state_db is not None:
                    sm.states.update(new_state_db)

                all_complete_f &= complete_f

            # Transition to 'bad lexatom acceptor' on first code unit is best
            # to happen here, after all transitions have been adapted.
            self._add_transition_to_bad_lexatom_detector(target_map, bad_lexatom_si, 0)

            # If there were intermediate states being generated, the error
            # error detection must have been implemented right then.

        sm.delete_transitions_beyond_interval(Setup.lexatom.type_range)

        sm.delete_orphaned_states()

        # AFTER: Whatever happend, the transitions in the state machine MUST
        #        lie in the drain_set.
        if not sm.is_DFA_compliant(): 
            sm = nfa_to_dfa.do(sm)
        sm = hopcroft_minimization.do(sm, CreateNewStateMachineF=False)
        return all_complete_f, sm

    def _add_transition_to_bad_lexatom_detector(self, target_map, BadLexatomSi, CodeUnitIndex):
        if BadLexatomSi is None: return
        error_range = self._error_range_by_code_unit_db[CodeUnitIndex]
        if error_range.is_empty(): return
        target_map[BadLexatomSi] = error_range

    def lexatom_n_per_character(self, CharacterSet):
        return 1     # Default behavior (e.g. UTF8 differs here)

    def lexatom_n_per_character_in_state_machine(self, SM):
        return 1     # Default behavior (e.g. UTF8 differs here)

    def variable_character_sizes_f(self): 
        return False # Default behavior (e.g. UTF8 differs here)

    def adapt_ranges_to_lexatom_type_range(self, LexatomTypeRange):
        raise MustBeImplementedInDerivedClass

    def _adapt_error_ranges_to_lexatom_type_range(self, LexatomTypeRange):
        for error_range in self._error_range_by_code_unit_db.itervalues():
            error_range.mask_interval(LexatomTypeRange)

    def hopcroft_minimization_always_makes_sense(self): 
        # Default-wise no intermediate states are generated
        # => hopcroft minimization does not make sense.
        return False

class EncodingTrafoUnicode(EncodingTrafo):
    @typed(SourceSet=NumberSet, DrainSet=NumberSet)
    def __init__(self, SourceSet, DrainSet):
        # Plain 'Unicode' associates a character with a single code unit, i.e.
        # its 'code point'. 
        # => Only code unit '0' is specified and everything is allowed.
        #    ('everything allowed' is disputable, since certain ranges are
        #     disallowed.)
        error_range_by_code_unit_db = { 0: NumberSet() }
        EncodingTrafo.__init__(self, "unicode", SourceSet, DrainSet, 
                               error_range_by_code_unit_db)

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

        if self.source_set.is_superset(number_set): 
            return True, None
        else:
            # Adapt 'number_set' in 'from_target_map' according to addmissible
            # range.
            number_set.intersect_with(self.source_set)
            return False, None

    def adapt_ranges_to_lexatom_type_range(self, LexatomTypeRange):
        self._adapt_error_ranges_to_lexatom_type_range(LexatomTypeRange)
        self.source_set.mask_interval(LexatomTypeRange)
