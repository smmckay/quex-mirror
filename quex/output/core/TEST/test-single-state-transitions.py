#! /usr/bin/env python
# PURPOSE: Test the code generation for number sets. Two outputs are generated:
#
#           (1) stdout: containing value pairs (x,y) where y is 1.8 if x lies
#               inside the number set and 1.0 if x lies outside the number set.
#           (2) 'tmp2': containing the information about the number set under
#               consideration.
#
# NOTE: The file '$QUEX_PATH/development-setup.sh' implements basic helper
#       functions.
#
# The result is best viewed with 'gnuplot'. Call the program redirect the stdout
# to file 'tmp2' and type in gnuplot:
#
#         > plot [][0.8:2] "tmp2" w l, "tmp" w p
################################################################################
import sys
import os
import random
sys.path.insert(0, os.environ["QUEX_PATH"])
                                                   
from   quex.input.setup                              import Lexatom
import quex.engine.analyzer.engine_supply_factory    as     engine
from   quex.engine.misc.interval_handling            import Interval, NumberSet
import quex.output.languages.core                    as     languages
from   quex.output.core.base                         import do_analyzer
from   quex.engine.state_machine.core                import DFA
from   quex.engine.analyzer.door_id_address_label    import DoorID
import quex.engine.analyzer.core                     as     analyzer_generator
from   quex.engine.analyzer.door_id_address_label    import DialDB
from   quex.engine.analyzer.transition_map           import TransitionMap  
import quex.engine.state_machine.transformation.core as     bc_factory
import quex.output.analyzer.adapt                    as     adapt
from   quex.blackboard                               import setup as Setup, \
                                                            E_IncidenceIDs, \
                                                            Lng
from   collections import defaultdict

dial_db = DialDB()

Setup.language_db = languages.db["C++"]()
Setup.buffer_setup("uint32_t", 4, "none")

if "--hwut-info" in sys.argv:
    print "Single DFA_State: Transition Code Generation;"
    print "CHOICES: A, B, C, A-UTF8, B-UTF8, C-UTF8;"
    sys.exit(0)

choice, codec = {
        "A":      ("A", ""),
        "B":      ("B", ""),
        "C":      ("C", ""),
        "A-UTF8": ("A", "UTF8"),
        "B-UTF8": ("B", "UTF8"),
        "C-UTF8": ("C", "UTF8"),
}[sys.argv[1]]

# initialize pseudo random generator: produces always the same numbers.
random.seed(110270)   # must set the seed for randomness, otherwise system time
#                     # is used which is no longer deterministic.

if choice == "A":
    tm0 = TransitionMap.from_iterable([
        (Interval(10,20),    1L), 
        (Interval(195,196),  1L),
        (Interval(51,70),    2L), 
        (Interval(261,280),  2L),
        (Interval(90,100),   3L), 
        (Interval(110,130),  3L),
        (Interval(150,151),  4L), 
        (Interval(151,190),  4L),
        (Interval(190,195),  5L), 
        (Interval(21,30),    5L),
        (Interval(197, 198), 6L), 
        (Interval(200,230),  7L), 
        (Interval(231,240),  7L),
        (Interval(250,260),  8L), 
        (Interval(71,80),    8L), 
    ])

    interval_end = 300

elif choice == "B":
    def make(start):
        size               = int(random.random() * 4) + 1
        target_state_index = long(random.random() * 10)
        return (Interval(start, start + size), target_state_index)

    tm0            = TransitionMap()
    interval_begin = 0
    for i in range(4000):
        tm0.append(make(interval_begin))
        interval_begin = tm0[-1][0].end

    interval_end = interval_begin

elif choice == "C":
    def make(start, size=None):
        if size is None:
            size = int(random.random() * 3) + 1
        target_state_index = long(random.random() * 5)
        return (Interval(start, start + size), target_state_index)

    tm0            = TransitionMap()
    interval_begin = 0
    for i in range(3000):
        if random.random() > 0.75:
            tm0.append(make(interval_begin))
            interval_begin = tm0[-1][0].end
        else:
            for dummy in xrange(0, int(random.random() * 5) + 2):
                tm0.append(make(interval_begin, size=1))
                interval_begin = tm0[-1][0].end + int(random.random() * 2)

    interval_end = interval_begin

def prepare(tm):
    tm.sort()
    tm.fill_gaps(E_IncidenceIDs.MATCH_FAILURE, 
                 Setup.lexatom.type_range.begin, 
                 Setup.lexatom.type_range.end)

    iid_db = defaultdict(NumberSet)
    for interval, iid in tm:
        iid_db[iid].add_interval(interval)
    iid_map = [ (character_set, iid) for iid, character_set in iid_db.iteritems() ]
    return iid_map

def get_transition_function(iid_map, Codec):
    global dial_db
    if Codec == "UTF8": Setup.buffer_setup("uint8_t", 1,  "utf8")
    else:               Setup.buffer_setup("uint32_t", 4, "unicode")

    Setup.bad_lexatom_detection_f = False
    sm        = DFA.from_IncidenceIdMap(iid_map)
    dummy, sm = Setup.buffer_encoding.do_state_machine(sm,
                                                       BadLexatomDetectionF=Setup.bad_lexatom_detection_f)
    analyzer  = analyzer_generator.do(sm, engine.CHARACTER_COUNTER, dial_db=dial_db)
    tm_txt    = do_analyzer(analyzer)
    tm_txt    = Lng.GET_PLAIN_STRINGS(tm_txt, dial_db=dial_db)
    tm_txt.append("\n")
    #label   = dial_db.get_label_by_door_id(DoorID.incidence(E_IncidenceIDs.MATCH_FAILURE))

    for character_set, iid in iid_map:
        tm_txt.append("%s return (int)%s;\n" % (Lng.LABEL(DoorID.incidence(iid, dial_db)), iid))
    tm_txt.append("%s return (int)-1;\n" % Lng.LABEL(DoorID.drop_out(-1, dial_db)))

    return "".join(tm_txt)

main_template = """
/* From '.begin' the target map targets to '.target' until the next '.begin' is
 * reached.                                                                   */
#define QUEX_OPTION_WCHAR_T_DISABLED_EXT
/* Prevent analyzer specific definition of '__quex_assert_no_passage' 
 * in 'lib/asserts'.                                                          */
#define __quex_assert_no_passage()     assert(false)
#include "ut/lib/quex/compatibility/stdint.h"
#include "ut/lib/quex/debug_print"

#include "../../../code_base/TESTS/minimum-definitions.h"
#include <stdio.h>
#define QUEX_OPTION_PLAIN_C_EXT

typedef struct {
    struct {
        TestAnalyzer_lexatom_t*  _read_p;
        TestAnalyzer_lexatom_t*  _lexeme_start_p;
    } buffer;
} MiniAnalyzer;

int transition(TestAnalyzer_lexatom_t* buffer);

typedef struct { 
    uint32_t begin; 
    int      target; 
} entry_t;

#include "ut/lib/lexeme/converter-from-utf8"
#include "ut/lib/lexeme/converter-from-utf8.i"
#include "ut/lib/lexeme/converter-from-unicode"
#include "ut/lib/lexeme/converter-from-unicode.i"

int
main(int argc, char** argv) {
    const entry_t db[]      = {
$$ENTRY_LIST$$
    };
    const entry_t*       db_last  = &db[sizeof(db)/sizeof(entry_t)] - 1;
    const entry_t*       iterator = &db[0];

    int                  output          = -1;
    int                  output_expected = -1;
    uint32_t             unicode_input;
    TestAnalyzer_lexatom_t buffer[8];
    
    printf("No output is good output!\\n");
    for(iterator=&db[0]; iterator != db_last; ++iterator) {
        output_expected = iterator->target;
        for(unicode_input = iterator->begin; unicode_input != iterator[1].begin ; ++unicode_input) {
            $$PREPARE_INPUT$$

            output = transition(&buffer[0]);

            if( output != output_expected ) {
                printf("unicode_input: 0x%06X; output: %i; expected: %i;   ERROR\\n",
                       (int)unicode_input, (int)output, (int)output_expected);
                return 0;
            }
        }
    }
    printf("Intervals:  %i\\n", (int)(iterator - &db[0]));
    printf("Characters: %i\\n", (int)unicode_input);
    printf("Oll Korrekt\\n");
    return 0;
}

int 
transition(TestAnalyzer_lexatom_t* buffer)
{
    MiniAnalyzer            self;
    MiniAnalyzer*           me = &self;
    TestAnalyzer_lexatom_t  input = 0;

    me->buffer._read_p = buffer;

$$TRANSITION$$

    if( 0 ) {
        goto $$ON_BAD_LEXATOM$$; /* Avoid unreferenced label */
        goto $$ON_BAD_LEXATOM$$;    /* Avoid unreferenced label */
        goto $$DROP_OUT_MINUS_1$$;
    }
    return 0;

$$ON_BAD_LEXATOM$$:
    return -1;
}

"""
def get_main_function(tm0, TranstionTxt, Codec):
    def indent(Txt, N):
        return (" " * N) + (Txt.replace("\n", "\n" + (" " * N)))

    input_preperation = get_read_preparation(codec)

    entry_list = [ 
        (0 if interval.begin < 0 else interval.begin, target) 
        for interval, target in tm0 
    ]
    entry_list.append((tm0[-1][0].begin, -1))
    entry_list.append((0x1FFFF, -1))
    expected_array = [ 
        "        { 0x%06X, %s },\n" % (begin, target) 
        for begin, target in entry_list 
    ]

    txt = main_template.replace("$$ENTRY_LIST$$",     "".join(expected_array))
    txt = txt.replace("$$TRANSITION$$",               indent(TranstionTxt, 4))
    txt = txt.replace("$$PREPARE_INPUT$$",            input_preperation)

    door_id = DoorID.incidence(E_IncidenceIDs.BAD_LEXATOM, dial_db)
    txt = txt.replace("$$ON_BAD_LEXATOM$$", Lng.LABEL_STR(door_id, dial_db))
    txt = txt.replace("$$DROP_OUT_MINUS_1$$", Lng.LABEL_STR(DoorID.drop_out(-1, dial_db)))

    txt = txt.replace("MATCH_FAILURE", "((int)-1)")
    return txt

def get_read_preparation(Codec):
    if Codec == "UTF8":
        txt = [
            "{\n"
            "    TestAnalyzer_lexatom_t*  buffer_p    = &buffer[0];\n"
            "    const uint32_t*          u32_input_p = &unicode_input;\n"
            "    TestAnalyzer_unicode_to_utf8_character(&u32_input_p, &buffer_p);\n"
            "}\n"
        ]
    else:
        txt = [
            "buffer[0] = unicode_input;\n"
        ]
    return "".join("        %s" % line for line in txt)

iid_map        = prepare(tm0)
transition_txt = get_transition_function(iid_map, codec)
txt            = get_main_function(tm0, transition_txt, codec)

Lng.REPLACE_INDENT(txt)

fh = open("test.c", "wb")
fh.write("".join(adapt.do(txt, "ut")))
fh.close()
try:    os.remove("./test")
except: pass

if codec == "UTF8": qtc_str = "-DQUEX_TYPE_LEXATOM_EXT=uint8_t"
else:               qtc_str = "-DQUEX_TYPE_LEXATOM_EXT=uint32_t"

os.system("gcc -Wall -Werror -I. -I../../../code_base -DQUEX_OPTION_ASSERTS -DQUEX_INLINE=static %s -o test test.c -ggdb -std=c89" % qtc_str)
os.system("./test")

if True:
    try:    os.remove("./test.c")
    except: pass
    try:    os.remove("./test")
    except: pass
else:
    print "re-install 'remove files'"





