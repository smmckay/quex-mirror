"""State-Split Transformation
-----------------------------
(C) Frank-Rene Schaefer

The 'State-Split' is a procedure transforms a state machine that triggers on
some 'pure' values (e.g. Unicode Characters) into a state machine that triggers
on the code unit sequences (e.g. UTF8 Code Units) that correspond to the
original values. For example, a state transition on a Unicode Character
'0x1329D' as shown below,

        [ A ]--->( 0x1329D )---->[ B ]

is translated into a sequence of UTF16 transitions with a new intermediate
state 'i' as follows.

        [ A ]--( 0xD80C )-->[ i ]-->( 0xDE9E )-->[ B ]

This is so, since the character 0x1329D in Unicode is represented as the
sequence 0xD80C, 0xDE9E. The present algorithm exploits the fact that
translations of adjacent character result in sequences of adjacent intervals.

 .----------------------------------------------------------------------------.
 | This procedure is to be used for encodings of dynamic size, i.e. where the |
 | number of code units to represent a 'pure' value changes depending on the  |
 | value itself (e.g. UTF8, UTF16).                                           |
 '----------------------------------------------------------------------------'

PRINCIPLE:

A state transition is described by a 'trigger set' and a target state.  If an
input occurs that belongs to the 'trigger set' the state machine transits into
the specific target state. Trigger sets are composed of one ore more intervals
of adjacent values. If the encoding has some type of continuity, it can be
assumed that an interval in the pure values can be represented by a sequence of
intervals in the transformed state machine. This is, indeed true for the
encodings UTF8 and UTF16.

The algorithm below considers intervals of pure values and translates them
into interval sequences. All interval sequences of a triggger set that 
triggers to a target state are then combined into a set of state transitions.

A unicode transition from state A to state B:

         [ A ]-->(x0, x1)-->[ B ]

is translated into a chain of utf8-byte sequence transitions that might look
like this

     [ A ]-->(b0)-->[ 1 ]-->(c0,c1)-->[ B ] 
         \                             /
          `->(d1)-->[ 2 ]---(e0,e1)---' 

That means that intermediate states may be introduced to reflect the different
byte sequences that represent the original interval.

IDEAS:
    
In a simple approach one would translate each element of a interval into an
utf8-byte sequence and generate state transitions between A and B.  Such an
approach, however, produces a huge computational overhead and charges the later
Hopcroft Minimization with a huge state machine.

To avoid such an hughe computational effort, the Hopcroft Minimzation can be
prepared on the basis of transition intervals. 
    
(A) Backwards: In somewhat greater intervals, the following might occur:


                 .-->(d1)-->[ 1 ]---(A3,BF)---. 
                /                              \
               /  ,->(d1)-->[ 2 ]---(80,BF)--.  \
              /  /                            \  \
             [ A ]-->(b0)-->[ 3 ]-->(80,BF)-->[ B ] 
                 \                             /
                  `->(d1)-->[ 4 ]---(80,81)---' 

That means, that for states 2 and 3 the last transition is on [80, BF]
to state B. Thus, the intermediate states 2 and 3 are equivalent. Both
can be replaced by a single state. 

(B) Forwards: The first couple of bytes in the correspondent utf8 sequences
    might be the same. Then, no branch is required until the first differing
    byte.

PROCESS:

(1) The original interval translated into a list of interval sequence
    that represent the values in the target encoding.

(2) The interval sequences are plugged in between the state A and B
    of the state machine.
"""
from   quex.engine.state_machine.core                import DFA
import quex.engine.state_machine.transformation.base as     base
from   quex.engine.misc.interval_handling            import NumberSet

from   quex.engine.misc.tools import flatten_list_of_lists

class EncodingTrafoBySplit(base.EncodingTrafo):
    """Transformation that takes a lexatom and produces a lexatom sequence.
    """
    def __init__(self, Name, CodeUnitRange):
        base.EncodingTrafo.__init__(self, Name, NumberSet.from_range(0, 0x110000),
                                    CodeUnitRange)

    def do_transition(self, sm, FromSi, from_target_map, ToSi):
        """Translates to transition 'FromSi' --> 'ToSi' inside the state
        machine according to the specific coding (see derived class, i.e.
        UTF8 or UTF16).

        If setup, the transition to 'BAD_LEXATOM' is added for invalid
        values of code units. 

        RETURNS: [0] True if complete, False else.
                 [1] True if transition needs to be removed from map.
        """
        number_set = from_target_map[ToSi]

        # 'FromSi' is a state that handles code unit '0'.
        self._code_unit_to_state_list_db[0].add(FromSi)
        print "#add0:", FromSi

        # Check whether a modification is necessary
        if number_set.least_greater_bound() <= self.UnchangedRange: 
            # 'UnchangedRange' => No change to numerical values.
            return True, False

        # Cut out any forbidden range. Assume, that is has been checked
        # before, or is tolerated to be omitted.
        self.prune(number_set)
        if number_set.is_empty():
            return False, True

        transformed_interval_sequence_list = self.do_NumberSet(number_set)

        # Second, enter the new transitions.
        self._plug_interval_sequences(sm, FromSi, ToSi, 
                                      transformed_interval_sequence_list)
        return True, False

    def do_NumberSet(self, NSet):
        """RETURNS: List of interval sequences that implement the number set.
        """
        return flatten_list_of_lists(
            self.get_interval_sequences(interval)
            for interval in NSet.get_intervals(PromiseToTreatWellF=True)
        )

    def variable_character_sizes_f(self):
        return True

    def lexatom_n_per_character_in_state_machine(self, SM):
        lexatom_n = None
        for state in SM.states.itervalues():
            for number_set in state.target_map.get_map().itervalues():
                candidate_lexatom_n = self.lexatom_n_per_character(number_set)
                if   candidate_lexatom_n is None:      return None
                elif lexatom_n is None:                lexatom_n = candidate_lexatom_n
                elif lexatom_n != candidate_lexatom_n: return None
        return lexatom_n

    def hopcroft_minimization_always_makes_sense(self): 
        return True

    def _plug_interval_sequences(self, sm, BeginIndex, EndIndex, 
                                 IntervalSequenceList):
        sub_sm,      \
        new_end_si,  \
        code_unit_db = DFA.from_interval_sequences(IntervalSequenceList)
        # The init state index is not supposed to be mentioned
        # It is to be replaced by 'BeginIndex' once the 'sub_sm' is mounted.
        assert 0 not in code_unit_db

        for code_unit, state_index_set in code_unit_db.iteritems():
            print "#xx - code_unit_db[%i] = %s" % (code_unit, repr(state_index_set))
            self._code_unit_to_state_list_db[code_unit].update(state_index_set)
        code_unit_db[0].add(BeginIndex)
        print "#code_unit_db[%i] = %i" % (0, BeginIndex)
        

        # Mount the states inside the state machine
        sm.mount_absorbed_states_between(BeginIndex, EndIndex, 
                                         sub_sm.states, sub_sm.init_state_index, 
                                         new_end_si)



