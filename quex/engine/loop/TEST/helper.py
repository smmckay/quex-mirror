import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])
import quex.output.analyzer.indentation_handler      as     indentation_handler
from   quex.input.regular_expression.pattern         import Pattern_Prep
from   quex.input.code.base                          import CodeFragment, SourceRef_VOID
from   quex.input.files.specifier.counter            import LineColumnCount_Default
import quex.engine.loop.skip_character_set           as     character_set_skipper
import quex.engine.loop.skip_range                   as     range_skipper
import quex.engine.loop.skip_nested_range            as     nested_range_skipper
import quex.engine.loop.indentation_counter          as     indentation_counter
from   quex.engine.misc.interval_handling            import NumberSet
from   quex.engine.state_machine.core                import DFA
from   quex.engine.analyzer.door_id_address_label    import get_plain_strings
import quex.engine.analyzer.engine_supply_factory    as     engine
import quex.engine.state_machine.transformation.core as     bc_factory
import quex.output.analyzer.adapt                    as     adapt
from   quex.output.core.TEST.generator_test          import *
from   quex.output.core.TEST.generator_test          import __Setup_init_language_database
from   quex.output.core.variable_db                  import variable_db
import quex.output.counter.run_time                  as     run_time_counter
import quex.output.core.base                         as     generator
from   quex.output.core.base                         import do_state_router

class AuxMode:
    def __init__(self):
        self.incidence_db = {}

# Setup.buffer_element_specification_prepare()
Setup.set_all_character_set_UNIT_TEST()

def run(Executable, TestStr, FilterF=False, NextLetter="X"):
    if FilterF:
        def filter(db, Line):
            if Line.find("column_number_at_end") != -1:
                db["column_n"] = Line.split()[1]
            elif Line.find("next letter:") != -1:
                db["next_letter"] = Line.split()[2]
            elif Line.find("'") == 0:
                db["test_string"] = Line.strip()
        db = {}
    else:
        filter = None
        db     = None

    fh = open("test.txt", "wb")
    fh.write(TestStr)
    fh.close()
    run_this("./%s test.txt" % Executable, db, filter)

    if FilterF:
        test_string = "%s" % db.get("test_string")
        column_n    = "%s" % db.get("column_n")
        next_letter = "%s" % db.get("next_letter")
        print "%s => real: { column_n: %s next_letter: %s; }" \
              % (test_string, column_n, next_letter)
        print "%s => real: { column_n: %s; next_letter: <%s>; }" \
              % (" " * len(test_string), TestStr.find(NextLetter) + 1, NextLetter)

    if REMOVE_FILES:
        os.remove("test.txt")

class MiniAnalyzer:
    def __init__(self):
        self.reload_state = None
        self.engine_type  = engine.FORWARD

FSM = MiniAnalyzer()

def __prepare(Language):
    global dial_db
    end_str  = '    printf("end\\n");\n'
    end_str += "#   define self (*me)\n"
    end_str += "    self.send(&self, QUEX_TKN_TERMINATION);\n"
    end_str += "    return;\n"
    end_str += "#   undef self\n"

    __Setup_init_language_database(Language)
    dial_db = DialDB()
    variable_db.init()

    return end_str

def __require_variables(RequiredRegisterSet):
    variable_db.require("input")  
    variable_db.require("target_state_else_index")  # upon reload failure
    variable_db.require("target_state_index")       # upon reload success
    variable_db.require_array("position", ElementN = 0, Initial = "(void*)0")
    variable_db.require("PositionRegisterN", Initial = "(size_t)0")

    variable_db.require_registers(RequiredRegisterSet)

def create_character_set_skipper_code(Language, TestStr, TriggerSet, QuexBufferSize=1024, InitialSkipF=True, OnePassOnlyF=False, CounterPrintF=True):
    global dial_db

    end_str = __prepare(Language)

    analyzer_list,  \
    terminal_list, \
    loop_map,      \
    required_register_set = character_set_skipper.do("M", LineColumnCount_Default(), 
                                                     TriggerSet, FSM.reload_state,
                                                     dial_db)
    loop_code = generator.do_analyzer_list(analyzer_list)

    variable_db.require_registers(required_register_set)

    loop_code.extend(
        generator.do_terminals(terminal_list, TheAnalyzer=None, dial_db=dial_db)
    )

    if InitialSkipF: marker_char_list = TriggerSet.get_number_list()
    else:            marker_char_list = []

    result = create_customized_analyzer_function(Language, TestStr, loop_code,
                                                 QuexBufferSize, 
                                                 CommentTestStrF = False, 
                                                 ShowPositionF   = False, 
                                                 EndStr          = end_str,
                                                 SkipUntilMarkerSet = marker_char_list, 
                                                 LocalVariableDB = deepcopy(variable_db.get()), 
                                                 ReloadF         = True, 
                                                 OnePassOnlyF    = OnePassOnlyF,
                                                 CounterPrintF   = CounterPrintF)

    result = language_defines + result
    result = result.replace("$$TEST_ANALYZER_DIR$$",    test_analyzer_dir(Language))
    result = result.replace("$$COMPUTED_GOTOS_CHECK$$", computed_gotos_check_str())
    return result

def create_range_skipper_code(Language, TestStr, CloserSequence, QuexBufferSize=1024, 
                              CommentTestStrF=False, ShowPositionF=False, CounterPrintF=True):
    assert QuexBufferSize >= len(CloserSequence) + 2

    end_str        = __prepare(Language)

    sm_close       = DFA.from_sequence(CloserSequence)  
    closer_pattern = Pattern_Prep(sm_close,
                                  PatternString="<skip range closer>",
                                  Sr=SourceRef_VOID)
    door_id_exit   = DoorID.continue_without_on_after_match(dial_db)

    analyzer_list,         \
    terminal_list,         \
    required_register_set, \
    run_time_counter_f     = range_skipper.do("MrUnitTest", 
                                              CaMap         = LineColumnCount_Default(), 
                                              CloserPattern = closer_pattern, 
                                              DoorIdExit    = door_id_exit, 
                                              ReloadState   = FSM.reload_state, 
                                              dial_db       = dial_db)
    loop_code = generator.do_analyzer_list(analyzer_list)
    assert not run_time_counter_f

    __require_variables(required_register_set)
    loop_code.extend(
        generator.do_terminals(terminal_list, TheAnalyzer=None, dial_db=dial_db)
    )

    result = create_customized_analyzer_function(Language, TestStr, loop_code,
                                                 QuexBufferSize, CommentTestStrF, ShowPositionF, end_str,
                                                 SkipUntilMarkerSet = [], 
                                                 LocalVariableDB = deepcopy(variable_db.get()),
                                                 DoorIdOnSkipRangeOpenF=True, 
                                                 CounterPrintF=CounterPrintF) 
    result = language_defines + result
    result = result.replace("$$TEST_ANALYZER_DIR$$",    test_analyzer_dir(Language))
    result = result.replace("$$COMPUTED_GOTOS_CHECK$$", computed_gotos_check_str())
    return result

def create_nested_range_skipper_code(Language, TestStr, OpenerSequence, CloserSequence, 
                                     QuexBufferSize=1024, CommentTestStrF=False, ShowPositionF=False):
    assert QuexBufferSize >= len(CloserSequence) + 2

    end_str = __prepare(Language)

    sm_close = DFA.from_sequence(CloserSequence)  
    sm_open  = DFA.from_sequence(OpenerSequence)  
    ca_map   = LineColumnCount_Default()

    closer_pattern = Pattern_Prep(sm_close, 
                             PatternString="<skip range closer>",
                             Sr=SourceRef_VOID)
    opener_pattern = Pattern_Prep(sm_open, 
                             PatternString="<skip range opener>",
                             Sr=SourceRef_VOID)
    door_id_exit   = DoorID.continue_without_on_after_match(dial_db)

    analyzer_list,         \
    terminal_list,         \
    required_register_set, \
    run_time_counter_f     = nested_range_skipper.do("MrUnitTest", ca_map, 
                                                     OpenerPattern = opener_pattern,
                                                     CloserPattern = closer_pattern, 
                                                     DoorIdExit    = door_id_exit, 
                                                     ReloadState   = FSM.reload_state, 
                                                     dial_db       = dial_db)
    loop_code = generator.do_analyzer_list(analyzer_list)
    assert not run_time_counter_f
    __require_variables(required_register_set)
    loop_code.extend(
        generator.do_terminals(terminal_list, TheAnalyzer=None, dial_db=dial_db)
    )

    code = []
    if run_time_counter_f:
        counter_code = run_time_counter.get(ca_map, "M")
        code.extend(counter_code)                       

    code.extend(
        loop_code
    )

    result = create_customized_analyzer_function(Language, TestStr, 
                                                 loop_code,
                                                 QuexBufferSize=QuexBufferSize, 
                                                 CommentTestStrF=CommentTestStrF, 
                                                 ShowPositionF=ShowPositionF, 
                                                 EndStr=end_str,
                                                 SkipUntilMarkerSet=[], 
                                                 LocalVariableDB=deepcopy(variable_db.get()), 
                                                 DoorIdOnSkipRangeOpenF=True, 
                                                 CounterPrintF="short") 
    result = language_defines + result
    result = result.replace("$$TEST_ANALYZER_DIR$$",    test_analyzer_dir(Language))
    result = result.replace("$$COMPUTED_GOTOS_CHECK$$", computed_gotos_check_str())
    return result

def create_indentation_handler_code(Language, TestStr, ISetup, BufferSize):
                                
    end_str = __prepare(Language)
                                
    class MiniIncidenceDb(dict) :
        def __init__(self):
            self[E_IncidenceIDs.INDENTATION_BAD] = ""
        def default_indentation_handler_f(self):
            return True
    mini_incidence_db = MiniIncidenceDb()

    ca_map = LineColumnCount_Default()
    
    counter_code   = run_time_counter.get(ca_map, "M")

    code = [] # [ "%s\n" % Lng.LABEL(DoorID.incidence(E_IncidenceIDs.INDENTATION_HANDLER, dial_db)) ]

    variable_db.init()
    analyzer_list,         \
    terminal_list,         \
    required_register_set, \
    run_time_counter_f     = indentation_counter.do("M", ca_map, ISetup, 
                                                    mini_incidence_db, FSM.reload_state, 
                                                    dial_db)
    loop_code = generator.do_analyzer_list(analyzer_list)

    loop_code.extend(
        generator.do_terminals(terminal_list, TheAnalyzer=None, dial_db=dial_db)
    )

    if not run_time_counter_f:
        counter_code = None

    code.extend(
        loop_code
    )

    __require_variables(required_register_set)
    main_txt = create_customized_analyzer_function(Language, TestStr, 
                                                   code, 
                                                   QuexBufferSize=BufferSize, 
                                                   CommentTestStrF="", ShowPositionF=True, 
                                                   EndStr=end_str, 
                                                   SkipUntilMarkerSet="behind newline",
                                                   LocalVariableDB=deepcopy(variable_db.get()), 
                                                   IndentationSupportF=True,
                                                   ReloadF=True, 
                                                   CounterPrintF=False,
                                                   BeforeCode=counter_code)

    on_indentation_txt = indentation_handler.do(AuxMode(), ["M", "M2"]).replace("$on_indentation", "QUEX_NAME(M_on_indentation)")

    Setup.analyzer_class_name = "TestAnalyzer"
    Setup.analyzer_name_safe = "TestAnalyzer"
    result = adapt.do(main_txt + on_indentation_txt, test_analyzer_dir(Language))
    result = language_defines + result
    result = result.replace("$$TEST_ANALYZER_DIR$$",    test_analyzer_dir(Language))
    result = result.replace("$$COMPUTED_GOTOS_CHECK$$", computed_gotos_check_str())
    return result
    

def create_customized_analyzer_function(Language, TestStr, EngineSourceCode, 
                                        QuexBufferSize, CommentTestStrF, ShowPositionF, 
                                        EndStr, SkipUntilMarkerSet,
                                        LocalVariableDB, IndentationSupportF=False, 
                                        ReloadF=False, OnePassOnlyF=False, 
                                        DoorIdOnSkipRangeOpenF=False, 
                                        CounterPrintF=True,
                                        BeforeCode=None):

    txt  = create_common_declarations(Language, QuexBufferSize,
                                      IndentationSupportF = IndentationSupportF, 
                                      QuexBufferFallbackN = 0)

    if BeforeCode is not None:
        txt += BeforeCode

    state_router_txt = do_state_router(dial_db)
    EngineSourceCode.extend(state_router_txt)
    txt += my_own_mr_unit_test_function(EngineSourceCode, EndStr, LocalVariableDB, 
                                        ReloadF, OnePassOnlyF, DoorIdOnSkipRangeOpenF, 
                                        CounterPrintF)

    if SkipUntilMarkerSet == "behind newline":
        txt += skip_behind_newline()
    elif SkipUntilMarkerSet:
        txt += skip_irrelevant_character_function(SkipUntilMarkerSet)
    else:
        txt += "static bool skip_irrelevant_characters(QUEX_TYPE_ANALYZER* me) { return true; }\n"

    txt += show_next_character_function(ShowPositionF)

    txt += create_main_function(Language, TestStr, QuexBufferSize, CommentTestStrF)

    txt = txt.replace(Lng._SOURCE_REFERENCE_END(), "")

    Setup.analyzer_class_name = "TestAnalyzer"
    Setup.analyzer_name_safe = "TestAnalyzer"
    return adapt.do(txt, test_analyzer_dir(Language))

def my_own_mr_unit_test_function(SourceCode, EndStr, 
                                 LocalVariableDB={}, ReloadF=False, 
                                 OnePassOnlyF=True, DoorIdOnSkipRangeOpenF=False, 
                                 CounterPrintF=True):
    
    if type(SourceCode) == list:
        plain_code = "".join(Lng.GET_PLAIN_STRINGS(SourceCode, dial_db))

    label_failure      = Lng.LABEL_STR(DoorID.incidence(E_IncidenceIDs.MATCH_FAILURE, dial_db))
    label_bad_lexatom  = Lng.LABEL_STR(DoorID.incidence(E_IncidenceIDs.BAD_LEXATOM, dial_db))
    label_load_failure = Lng.LABEL_STR(DoorID.incidence(E_IncidenceIDs.LOAD_FAILURE, dial_db))
    # label_overflow     = Lng.LABEL_STR(DoorID.incidence(E_IncidenceIDs.OVERFLOW, dial_db))
    label_eos          = Lng.LABEL_STR(DoorID.incidence(E_IncidenceIDs.END_OF_STREAM, dial_db))
    label_reentry      = Lng.LABEL_STR(DoorID.global_reentry(dial_db))
    label_reentry2     = Lng.LABEL_STR(DoorID.continue_without_on_after_match(dial_db))

    if DoorIdOnSkipRangeOpenF:
        label_sro = Lng.LABEL_STR(DoorID.incidence(E_IncidenceIDs.SKIP_RANGE_OPEN, dial_db))
    else:
        label_sro = Lng.LABEL_STR(dial_db.new_door_id())

    if CounterPrintF == "short":
        counter_print_str = 'printf("column_number_at_end(real): %i;\\n", (int)self.counter._column_number_at_end);\n'
    elif CounterPrintF:
        counter_print_str = "%s(&self.counter);" % Lng.NAME_IN_NAMESPACE_MAIN("Counter_print_this")
    else:
        counter_print_str = ""


    return blue_print(customized_unit_test_function_txt,
                      [
                       ("$$LOCAL_VARIABLES$$",        Lng.VARIABLE_DEFINITIONS(VariableDB(LocalVariableDB))),
                       ("$$SOURCE_CODE$$",            plain_code),
                       ("$$COUNTER_PRINT$$",          counter_print_str),
                       ("$$TERMINAL_END_OF_STREAM$$", label_eos),
                       ("$$TERMINAL_FAILURE$$",       label_failure),
                       ("$$ON_BAD_LEXATOM$$",         label_bad_lexatom),
                       ("$$ON_LOAD_FAILURE$$",        label_load_failure),
                       # ("$$NO_MORE_SPACE$$",          label_overflow),
                       ("$$REENTRY$$",                label_reentry),
                       ("$$LEXEME_MACRO_SETUP$$",     Lng.DEFINE_LEXEME_VARIABLES()),
                       ("$$LEXEME_MACRO_CLEAN_UP$$",  Lng.UNDEFINE_LEXEME_VARIABLES()),
                       ("$$REENTRY2$$",               label_reentry2),
                       ("$$SKIP_RANGE_OPEN$$",        label_sro),
                       ("$$ONE_PASS_ONLY$$",          "true" if OnePassOnlyF else "false"),
                       ("$$QUEX_LABEL_STATE_ROUTER$$", Lng.LABEL_STR(DoorID.global_state_router(dial_db))),
                       ("$$END_STR$$",                EndStr)])

def skip_irrelevant_character_function(SkipUntilMarkerSet):
    ml_txt = ""
    if len(SkipUntilMarkerSet) != 0:
        for character in SkipUntilMarkerSet:
            ml_txt += "        if( input == %i ) break;\n" % character
    else:
        ml_txt += "    break;\n"

    return skip_irrelevant_characters_function_txt.replace("$$MARKER_LIST$$", ml_txt).replace("$$FOUND$$", "")

def skip_behind_newline():
    ml_txt  = "if     ( found_f ) break;"
    ml_txt += "else if( input == '\\n' ) found_f = true;\n"

    return skip_irrelevant_characters_function_txt.replace("$$MARKER_LIST$$", ml_txt).replace("$$FOUND$$", "bool found_f = false;")

def show_next_character_function(ShowPositionF):
    if ShowPositionF: show_position_str = "1"
    else:             show_position_str = "0"

    return show_next_character_function_txt.replace("$$SHOW_POSITION$$", show_position_str)

customized_unit_test_function_txt = """
static bool show_next_character(QUEX_TYPE_ANALYZER* me);
static bool skip_irrelevant_characters(QUEX_TYPE_ANALYZER* me);

#include "$$TEST_ANALYZER_DIR$$/lib/implementations.i"
#include "$$TEST_ANALYZER_DIR$$/lib/implementations-inline.i"

void
QUEX_NAME(M_analyzer_function)(QUEX_TYPE_ANALYZER* me)
{
#   define  engine (me)
#   define  self   (*me)
#   define QUEX_LABEL_STATE_ROUTER $$QUEX_LABEL_STATE_ROUTER$$ 
$$LOCAL_VARIABLES$$
$$LEXEME_MACRO_SETUP$$
ENTRY:
    if( skip_irrelevant_characters(me) == false ) {
        goto $$TERMINAL_END_OF_STREAM$$;
    }
    /* QUEX_NAME(Counter_reset)(&me->counter); */
    me->counter._column_number_at_end = 1;
    count_reference_p = me->buffer._read_p;

/*__BEGIN_________________________________________________________________________________*/
$$SOURCE_CODE$$
/*__END___________________________________________________________________________________*/

$$REENTRY$$:
$$REENTRY2$$:
    /* Originally, the reentry preparation does not increment or do anything to _read_p
     * Here, we use the chance to print the position where the skipper ended.
     * If we are at the border and there is still stuff to load, then load it so we can
     * see what the next character is coming in.                                          */
    $$COUNTER_PRINT$$ 
    if( ! show_next_character(me) || $$ONE_PASS_ONLY$$ ) goto $$TERMINAL_END_OF_STREAM$$; 
    goto ENTRY;

$$TERMINAL_FAILURE$$:
$$ON_BAD_LEXATOM$$:
$$ON_LOAD_FAILURE$$:
$$TERMINAL_END_OF_STREAM$$:
$$SKIP_RANGE_OPEN$$: /* <skip range open> */
$$END_STR$$
#undef engine

    if( 0 ) {
        /* Avoid undefined label warnings: */
        goto $$TERMINAL_FAILURE$$;
        goto $$ON_BAD_LEXATOM$$;
        goto $$ON_LOAD_FAILURE$$;
        goto $$TERMINAL_END_OF_STREAM$$;
        goto $$SKIP_RANGE_OPEN$$;
        goto $$REENTRY$$;
        goto $$REENTRY2$$;
$$<not-computed-gotos>-------------
        goto QUEX_LABEL_STATE_ROUTER;
$$-----------------------------
        /* Avoid unused variable error */
        (void)target_state_else_index;
        (void)target_state_index;
    }
$$LEXEME_MACRO_CLEAN_UP$$
}
"""

show_next_character_function_txt = """
static bool
show_next_character(QUEX_TYPE_ANALYZER* me) 
{
    QUEX_NAME(Buffer)* buffer = &me->buffer;

    if( me->buffer._read_p == me->buffer.input.end_p ) {
        buffer->_lexeme_start_p = buffer->_read_p;
        if( QUEX_NAME(Buffer_is_end_of_stream)(buffer) ) {
            return false;
        }
        QUEX_NAME(Buffer_load_forward)(buffer, (TestAnalyzer_lexatom_t**)0x0, 0);
    }
    if( me->buffer._read_p != me->buffer.input.end_p ) {
        if( ((*buffer->_read_p) & 0x80) == 0 ) 
            printf("next letter: <%c>", (int)(buffer->_read_p[0]));
        else
            printf("next letter: <0x%02X>", (int)(buffer->_read_p[0]));

#       if $$SHOW_POSITION$$
        printf(" column_n: %i", (int)me->counter._column_number_at_end);
#       endif
        printf("\\n");
    }
    return true;
}
"""

skip_irrelevant_characters_function_txt = """

static bool
skip_irrelevant_characters(QUEX_TYPE_ANALYZER* me)
{
    TestAnalyzer_lexatom_t   input;
    (void)input;
    $$FOUND$$

    while(1 + 1 == 2) { 
        input = *(me->buffer._read_p);
$$MARKER_LIST$$
        if( me->buffer._read_p == me->buffer.input.end_p ) {
            me->buffer._lexeme_start_p = me->buffer._read_p;
            if( QUEX_NAME(Buffer_is_end_of_stream)(&me->buffer) ) {
                return false;
            }
            QUEX_NAME(Buffer_load_forward)(&me->buffer, (TestAnalyzer_lexatom_t**)0x0, 0);
            assert(me->buffer._read_p >= me->buffer._memory._front);
            assert(me->buffer._read_p <= me->buffer._memory._back);

            if( me->buffer._read_p == me->buffer._memory._back ) {
                return false;
            }
        }
        else {
            ++(me->buffer._read_p);
        }
        assert(me->buffer._read_p >= me->buffer._memory._front);
        assert(me->buffer._read_p <= me->buffer._memory._back);
    }
    return true;
}
"""

def get_Pattern_Prep(SM):
    return Pattern_Prep(SM, Sr=SourceRef_VOID)

