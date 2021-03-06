import quex.input.regular_expression.engine                       as     regex
import quex.output.languages.core                                 as     languages
from   quex.engine.misc.interval_handling                         import NumberSet, Interval
from   quex.engine.state_machine.state.single_entry               import SeAccept     
import quex.engine.state_machine.construction.combination         as     combination
import quex.engine.state_machine.algorithm.beautifier             as     beautifier
from   quex.engine.state_machine.core                             import DFA
from   quex.engine.state_machine.state.core                       import DFA_State
import quex.engine.state_machine                                  as     state_machine
from   quex.engine.state_machine.transformation.utf8_state_split  import EncodingTrafoUTF8
import quex.engine.state_machine.TEST_help.many_shapes            as     sms
import quex.engine.state_machine.index                            as     index
from   quex.blackboard import setup as Setup, \
                              E_IncidenceIDs
from   StringIO import StringIO
import sys
from   copy            import copy

Setup.language_db = languages.db["C++"]()

class X:
    def __init__(self, Name):
        sh = StringIO("[:\\P{Script=%s}:]" % Name)
        self.name = Name
        self.charset = regex.snap_set_expression(sh, {})
        self.sm = DFA()
        self.sm.add_transition(self.sm.init_state_index, self.charset, AcceptanceF=True)
        self.id = self.sm.get_id()

    def check(self, SM, TransformFunc):
        """This function throws an exception as soon as one single value
           is not matched according to the expectation.
        """
        print "## [%i] Name = %s" % (self.id, self.name), 
        interval_list  = self.charset.get_intervals(PromiseToTreatWellF=True)
        interval_count = len(interval_list)
        for interval in interval_list:
            for i in range(interval.begin, interval.end):
                lexatom_seq = TransformFunc(i)

                # Apply sequence to state machine
                state = SM.apply_sequence(lexatom_seq)
                if state is None:
                    error(self.sm, SM, lexatom_seq)

                # All acceptance flags must belong to the original state machine
                acceptance_id_list = [
                    cmd.acceptance_id()
                    for cmd in state.single_entry.get_iterable(SeAccept)
                ]
                if acceptance_id_list and self.id not in acceptance_id_list: 
                    print eval("u'\U%08X'" % i) 
                    print "#Seq:  ", ["%02X" % x for x in lexatom_seq]
                    print "#acceptance-ids:", acceptance_id_list
                    error(self.sm, SM, lexatom_seq)

        print " (OK=%i)" % interval_count

def error(SM_orig, SM_trafo, LexatomSeq):
    print 
    print "#sm.orig:  ", SM_orig.get_string(NormalizeF=False, Option="hex")
    print "#sm.result:", SM_trafo.get_string(NormalizeF=False, Option="hex")
    # print "#UCS: { interval: %s; value: %s; }" % (interval.get_string(Option="hex"), i)
    print "#Seq: ", ["0x%02X" % x for x in LexatomSeq]
    assert False

def check_negative(SM, ImpossibleIntervals, TransformFunc):
    """None of the given unicode values shall reach an acceptance state.
    """
    print "Inverse Union Check:",
    for interval in ImpossibleIntervals:
        for i in [interval.begin, (interval.end + interval.begin) / 2, interval.end - 1]:
            lexatom_seq = TransformFunc(i)

            # Apply sequence to state machine
            state = SM.apply_sequence(lexatom_seq)
            if state is None: continue

            # An acceptance state cannot be reached by a unicode value in ImpossibleIntervals
            if any(state.single_entry.get_iterable(SeAccept)):
                error(None, SM, lexatom_seq)

    print " (OK)"

def test_on_UCS_sample_sets(Trafo, unicode_to_transformed_sequence):
    script_list = [
        "Arabic", "Armenian", "Balinese", "Bengali", "Bopomofo", "Braille", "Buginese", "Buhid",
        "Canadian_Aboriginal", "Cherokee", "Common",  "Cuneiform",  "Cypriot",  "Deseret",
        "Gothic",  "Greek",  
        "Hanunoo", "Hebrew", "Hiragana", "Inherited", "Kannada", "Han",  
        "Katakana", "Kharoshthi", "Khmer", "Lao", "Latin", "Limbu", "Linear_B", "Malayalam",
        "Mongolian", "Myanmar", "New_Tai_Lue", "Nko", "Osmanya", "Ogham", "Old_Italic", "Old_Persian",
        "Phoenician",  "Shavian",  "Syloti_Nagri", 
        "Syriac", "Tagalog", "Tagbanwa", "Tai_Le", "Tamil", "Telugu", "Thaana", "Thai",
        "Tibetan", "Tifinagh", "Ugaritic", "Yi"
    ]
    sets = [ X(name) for name in script_list ]

    orig = combination.do(map(lambda x: x.sm, sets))
    state_n_before, result = transform(Trafo, orig)

    # print result.get_graphviz_string(Option="hex")

    for set in sets:
        set.check(result, unicode_to_transformed_sequence)
    print "Translated %i groups without abortion on error (OK)" % len(sets)

    union = NumberSet()
    for nset in map(lambda set: set.charset, sets):
        union.unite_with(nset)

    inverse_union = NumberSet(Interval(0, 0x110000))
    inverse_union.subtract(union)
    # print inverse_union.get_string(Option="hex")
    check_negative(result, inverse_union.get_intervals(PromiseToTreatWellF=True), 
                   unicode_to_transformed_sequence)

def transform(Trafo, orig):
    print "# Number of states in state machine:"
    print "#   Unicode:       %i" % len(orig.states)
    state_n_before = len(orig.states)
    verdict_f, result = Trafo.do_state_machine(orig)
    print "#   %s:            %i" % (Trafo.name, len(result.states))
    return state_n_before, result

def test_on_UCS_range(Trafo, Source, Drain, CharacterBackwardTrafo):
    sm     = DFA()
    acc_db = {}
    for x in range(Source.begin, Source.end):
        ti = sm.add_transition(sm.init_state_index, x, AcceptanceF=True)
        acc_id    = len(acc_db)
        sm.states[ti].mark_acceptance_id(acc_id)
        acc_db[x] = acc_id

    if Setup.bad_lexatom_detection_f:
        acc_db[None] = E_IncidenceIDs.BAD_LEXATOM
    else:
        acc_db[None] = None

    state_n_before, result = transform(Trafo, sm)
    # assert state_n_before == len(result.states)

    init_state = result.get_init_state()
    count      = 0
    for y in range(Drain.begin, Drain.end):
        # Translate character into 
        x  = CharacterBackwardTrafo(y)
        # Transit on the translated charater
        ti = init_state.target_map.get_resulting_target_state_index(y)
        # Compare resulting state with the expected state's acceptance
        assert_only_acceptance_id(sm.states, ti, acc_db, x, y)

        count += 1

    print "<terminated: %i transitions ok>" % count

def assert_only_acceptance_id(states, TargetIndex, AcceptanceDb, FromChar, ToChar):
    if TargetIndex is None:
        assert FromChar is None, \
               "(from: %s; to: %s;)" % (FromChar, ToChar)
    else:
        state = states[TargetIndex]
        expected_acceptance_id = AcceptanceDb[FromChar]
        acceptance_id_list = [
            cmd.acceptance_id()
            for cmd in state.single_entry.get_iterable(SeAccept)
        ]
        assert len(acceptance_id_list) == 1, \
               "(from: %s; to: %s;) acceptance_id_list: %s" % (FromChar, ToChar, acceptance_id_list)
        assert acceptance_id_list[0] == expected_acceptance_id, \
                "(from: %s; to: %s;) Expected: %s; Found: %s;" % \
                (FromChar, ToChar, expected_acceptance_id, acceptance_id_list)

def generate_sm_for_boarders(Boarders, Trafo):
    sm = DFA()
    for ucs_char in Boarders:
        target_idx = index.get() 
        sms.line(sm, sm.init_state_index, 
                 (ucs_char, target_idx), (ucs_char, target_idx))
        sm.states[target_idx].set_acceptance()

    Trafo.adapt_ranges_to_lexatom_type_range(Setup.lexatom.type_range)
    verdict_f, result = Trafo.do_state_machine(sm)
    assert verdict_f
    return result

def get_bad_sequences(GoodSequenceList, Bad1st_list, BadOther_list):
    """Take each good sequence and implant a codec error at any possible byte
    position.

    RETURNS: List of bad sequences.
    """
    result = []
    for sequence in GoodSequenceList:
        # Implement a couple of bad sequences based on the good sequence.
        for i, lexatom in enumerate(sequence):
            if i == 0: bad_lexatoms = Bad1st_list
            else:      bad_lexatoms = BadOther_list
            for bad in bad_lexatoms:
                bad_copy    = copy(sequence)
                bad_copy[i] = bad
                result.append(bad_copy)
    return result

def test_good_and_bad_sequences(sm, good_sequences, bad_sequence_list):
    print
    print "Good Sequences: ________________________________________________________"
    print
    for sequence in good_sequences:
        state = sm.apply_sequence(sequence, StopAtBadLexatomF=True)
        print_sequence_result(state, sequence)
           
    print
    print "Bad Sequences: _________________________________________________________"
    print
    for sequence in bad_sequence_list:
        state = sm.apply_sequence(sequence, StopAtBadLexatomF=True)
        print_sequence_result(state, sequence)

def sequence_string(Sequence):
    return "".join("%02X." % x for x in Sequence)[:-1]

def result_string(state):
    if state is None:
        return "None"
    elif state.has_acceptance_id(E_IncidenceIDs.BAD_LEXATOM):
        return "Bad Lexatom"
    elif state.is_acceptance():
        return "Accept"
    else:
        return "No Accept"

def print_sequence_result(state, sequence):
    print "%s: %s" % (result_string(state), sequence_string(sequence))

def test_plug_sequence(ByteSequenceDB):
    L = len(ByteSequenceDB[0])

    for seq in ByteSequenceDB:
        assert len(seq) == L
        for x in seq:
            assert isinstance(x, Interval)

    first_different_byte_index = -1
    for i in range(L):
        x0 = ByteSequenceDB[0][i]
        for seq in ByteSequenceDB[1:]:
            if not seq[i].is_equal(x0): 
                first_different_byte_index = i
                break
        if first_different_byte_index != -1: 
            break
    if first_different_byte_index == -1:
        first_different_byte_index = 0

    print "# Best To be Displayed by:"
    print "#"
    print "#  > " + sys.argv[0] + " " + sys.argv[1] + " | dot -Tsvg -o tmp.svg"
    print "#"
    print "# -------------------------"
    print "# Byte Sequences:     "
    i = -1
    for seq in ByteSequenceDB:
        i += 1
        print "# (%i) " % i,
        for x in seq:
            print "    " + x.get_string(Option="hex"), 
        print
    print "#    L    = %i" % L
    print "#    DIdx = %i" % first_different_byte_index

    sm = DFA()
    end_index = state_machine.index.get()
    sm.states[end_index] = DFA_State()

    Setup.buffer_setup("", 1, "utf8")

    if Setup.bad_lexatom_detection_f: bad_lexatom_si = index.get()
    else:                             bad_lexatom_si = None

    trafo = Setup.buffer_encoding

    new_first_tm,    \
    new_state_db = trafo.plug_interval_sequences(sm.init_state_index, end_index, 
                                                 ByteSequenceDB,
                                                 BadLexatomSi=bad_lexatom_si)

    if bad_lexatom_si is not None:
        new_first_tm[bad_lexatom_si] = trafo._error_range_by_code_unit_db[0]

    # Generate the 'bad lexatom accepter'.
    bad_lexatom_state = DFA_State(AcceptanceF=True)
    bad_lexatom_state.mark_acceptance_id(E_IncidenceIDs.BAD_LEXATOM)
    sm.states[bad_lexatom_si] = bad_lexatom_state

    first_tm = sm.get_init_state().target_map.get_map() 
    if end_index in first_tm: del first_tm[end_index]
    first_tm.update(new_first_tm)

    sm.states.update(new_state_db)

    sm = beautifier.do(sm)
    if len(sm.get_orphaned_state_index_list()) != 0:
        print "Error: Orphaned States Detected!"

    # Double check, that there are no 'circles'
    predecessor_db = sm.get_predecessor_db()
    assert not any(si in predecessor_db[si] for si in sm.states)

    show_graphviz(sm)

def show_graphviz(sm):
    gv_str = sm.get_graphviz_string(Option="hex")
    for line in gv_str.splitlines():
        if line.startswith("digraph state_machine_"):
            line = line.replace("digraph state_machine_", "digraph ((state_machine_")
            line = line.replace(" {", ")) {")
        if "->" not in line or "label" not in line: print line; continue
        fields = line.split()
        if len(fields) < 3: 
            print line; continue;
        if len(fields) > 3:
            remainder = reduce(lambda x,y: "%s %s" % (x, y), fields[3:])
        else:
            remainder = ""
        print "((%s)) -> ((%s)) %s" % (fields[0], fields[2], remainder)
