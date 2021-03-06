#! /usr/bin/env python

# Switch: Removal of source and executable file
#         'False' --> No removal.
if True: 
    REMOVE_FILES = True; 
else:     
    print "NOTE:> Do not remove files!;"
    REMOVE_FILES = False

# Switch: Verbose debug output: 
#         'False' --> Verbose debug output
if True: # False: # True:
    SHOW_TRANSITIONS_STR  = ""
    SHOW_BUFFER_LOADS_STR = ""
else:
    REMOVE_FILES = False
    print "NOTE:> Print transitions and do not remove files!;"
    SHOW_TRANSITIONS_STR  = "-DQUEX_OPTION_DEBUG_SHOW_EXT "  
    SHOW_BUFFER_LOADS_STR = "-DQUEX_OPTION_DEBUG_SHOW_LOADS_EXT " \
                            "-DQUEX_OPTION_INFORMATIVE_BUFFER_OVERFLOW_MESSAGE_EXT " \
                            "-DQUEX_SETTING_DEBUG_OUTPUT_CHANNEL_EXT=stdout"

# Switch: Turn off some warnings
#         'False' --> show (almost) all compiler warnings
if True:
    IGNORE_WARNING_F = True
else:
    IGNORE_WARNING_F = False

import sys
import os
import subprocess
from StringIO import StringIO
from tempfile import mkstemp
sys.path.insert(0, os.environ["QUEX_PATH"])
#
from   quex.input.code.base                        import SourceRef_VOID
from   quex.input.setup                            import Lexatom
from   quex.input.files.specifier.mode             import ModeDocumentation
from   quex.input.regular_expression.auxiliary     import PatternShorthand
import quex.input.regular_expression.engine        as     regex
from   quex.input.regular_expression.exception     import RegularExpressionException
from   quex.input.code.core                        import CodeTerminal
from   quex.input.files.specifier.counter          import LineColumnCount_Default
import quex.engine.state_machine.transformation.core  as  bc_factory
from   quex.engine.analyzer.door_id_address_label  import DoorID, DialDB
from   quex.engine.analyzer.terminal.core          import Terminal
from   quex.engine.analyzer.terminal.factory       import TerminalFactory
from   quex.engine.misc.string_handling            import blue_print
from   quex.engine.misc.tools                      import all_isinstance
from   quex.engine.mode                            import Mode
from   quex.engine.incidence_db                    import IncidenceDB
import quex.output.core.variable_db                as     variable_db
from   quex.output.core.variable_db                import VariableDB
from   quex.output.languages.core                  import db
import quex.output.core.engine                     as     engine_generator
import quex.output.analyzer.adapt                  as     adapt
import quex.output.analyzer.modes                  as     modes
#
import quex.blackboard as blackboard
from   quex.constants  import E_Compression, \
                              E_IncidenceIDs
from   quex.blackboard import setup as Setup, \
                              Lng

from   copy import deepcopy

# Must be set in any case, because 'TestAnalyzer' is generated with the according pointers
blackboard.required_support_indentation_count_set()


dial_db = DialDB()

choices_list = ["ANSI-C-PlainMemory", "ANSI-C", "ANSI-C-CG", 
                "Cpp", "Cpp_StrangeStream", "Cpp-Template", "Cpp-Template-CG", 
                "Cpp-Path", "Cpp-PathUniform", "Cpp-Path-CG", 
                "Cpp-PathUniform-CG", "ANSI-C-PathTemplate"] 

def hwut_input(Title, Extra="", AddChoices=[], DeleteChoices=[]):
    global choices_list

    choices = choices_list + AddChoices
    for choice in DeleteChoices:
        if choice in choices: 
            del choices[choices.index(choice)]

    choices_str  = "CHOICES: " + repr(choices)[1:-1].replace("'", "") + ";"

    if "--hwut-info" in sys.argv:
        print Title + ";"
        print choices_str
        print "SAME;"
        sys.exit(0)

    if len(sys.argv) < 2:
        print "Choice argument requested. Run --hwut-info"
        sys.exit(0)

    if sys.argv[1] not in choices:
        print "Choice '%s' not acceptable." % sys.argv[1]
        sys.exit(0)

    return sys.argv[1]

def __Setup_init_language_database(Language):
    global Setup

    try:
        Setup.language = { 
            "ANSI-C-PlainMemory": "C",
            "ANSI-C-from-file":   "C",
            "ANSI-C":             "C",
            "ANSI-C-CG":          "C",
            "ANSI-C-PathTemplate": "C",
            "Cpp":                "C++", 
            "Cpp_StrangeStream":  "C++", 
            "Cpp-Template":       "C++", 
            "Cpp-Template-CG":    "C++", 
            "Cpp-Path":           "C++", 
            "Cpp-PathUniform":    "C++", 
            "Cpp-Path-CG":        "C++", 
            "Cpp-PathUniform-CG": "C++",
        }[Language]
    except:
        print "Error: missing language specifier: %s" % Language
        sys.exit()

    Setup.language_db = db[Setup.language]()

def do(PatternActionPairList, TestStr, PatternDictionary={}, Language="ANSI-C-PlainMemory", 
       QuexBufferSize=15, # DO NOT CHANGE!
       SecondPatternActionPairList=[], QuexBufferFallbackN=0, ShowBufferLoadsF=False,
       AssertsActionvation_str="-DQUEX_OPTION_ASSERTS",
       Encoding="unicode",
       CodeUnitSize_inByte=1):
    assert type(TestStr) == list or isinstance(TestStr, (str, unicode))

    assert QuexBufferFallbackN >= 0
    __Setup_init_language_database(Language)

    BufferLimitCode = 0
    Setup.buffer_limit_code = BufferLimitCode
    Setup.buffer_setup("", CodeUnitSize_inByte, Encoding)

    CompileOptionStr = ""
    Setup.computed_gotos_f  = False
    FullLanguage     = Language
    if Language.find("StrangeStream") != -1:
        CompileOptionStr += " -DQUEX_OPTION_STRANGE_ISTREAM_IMPLEMENTATION_EXT "

    if Language.find("-CG") != -1:
        Language = Language.replace("-CG", "")
        Setup.computed_gotos_f = True

    if Language == "Cpp-Template":
        Language = "Cpp"
        # Shall template compression be used?
        Setup.compression_type_list = [ E_Compression.TEMPLATE ]
        Setup.compression_template_min_gain = 0

    elif Language == "Cpp-Path":
        Language = "Cpp"
        Setup.compression_type_list = [ E_Compression.PATH ]

    elif Language == "Cpp-PathUniform":
        Language = "Cpp"
        Setup.compression_type_list = [ E_Compression.PATH_UNIFORM ]

    elif Language == "ANSI-C-PathTemplate":
        Language = "ANSI-C"
        Setup.compression_type_list = [ E_Compression.PATH, E_Compression.TEMPLATE ]
        Setup.compression_template_min_gain = 0

    try:
        adapted_dict = {}
        for key, regular_expression in PatternDictionary.items():
            string_stream = StringIO(regular_expression)
            pattern       = regex.do(string_stream, adapted_dict)
            # It is ESSENTIAL that the state machines of defined patterns do not 
            # have origins! Actually, there are not more than patterns waiting
            # to be applied in regular expressions. The regular expressions 
            # can later be origins.

            ## assert not pattern.sm.has_specific_acceptance_id()

            adapted_dict[key] = PatternShorthand(key, pattern.extract_sm())

    except RegularExpressionException, x:
        print "Dictionary Creation:\n" + repr(x)

    if type(TestStr) != list:
        test_str = TestStr
        test_str_list = None
    else:
        test_str      = sorted(TestStr, key=lambda x: len(x))[-1] # longest test string
        test_str_list = TestStr

    if FullLanguage.find("PlainMemory") != -1:
        assert type(test_str) != list
        QuexBufferSize = len(test_str) + 2

    test_program = create_main_function(Language, test_str, QuexBufferSize, 
                                        ComputedGotoF=Setup.computed_gotos_f)

    state_machine_code = create_state_machine_function(PatternActionPairList, 
                                                       adapted_dict, 
                                                       BufferLimitCode)

    if len(SecondPatternActionPairList) != 0:
        dial_db = DialDB()
        CompileOptionStr += "-DQUEX_UNIT_TEST_SECOND_MODE"
        state_machine_code += create_state_machine_function(SecondPatternActionPairList, 
                                                            PatternDictionary, 
                                                            BufferLimitCode,
                                                            SecondModeF=True)

    if ShowBufferLoadsF:
        state_machine_code = "#define QUEX_OPTION_DEBUG_SHOW_LOADS_EXT\n" + \
                             "#define QUEX_OPTION_UNIT_TEST_EXT\n"                   + \
                             state_machine_code

    source_code =   create_common_declarations(Language, QuexBufferSize, 
                                               QuexBufferFallbackN, BufferLimitCode, 
                                               ComputedGotoF=Setup.computed_gotos_f) \
                  + state_machine_code \
                  + test_program

    # Verify, that Templates and Pathwalkers are really generated
    __verify_code_generation(FullLanguage, source_code)

    source_code = "%s%s" % (language_defines, adapt.do(source_code, test_analyzer_dir(Language)))

    source_code = source_code.replace("$$TEST_ANALYZER_DIR$$",
                                      test_analyzer_dir(Language))
    
    source_code = source_code.replace("$$COMPUTED_GOTOS_CHECK$$", computed_gotos_check_str())
    

    compile_and_run(Language, source_code, AssertsActionvation_str, CompileOptionStr, 
                    test_str_list)

def run_this(Str, filter_result_db=None, FilterFunc=None):
    if True: #try:
        fh_out = open("tmp.out", "w")
        fh_err = open("tmp.err", "w")
        call_list = Str.split()
        subprocess.call(call_list, stdout=fh_out, stderr=fh_err)
        fh_out.close()
        fh_err.close()
        fh_out = open("tmp.out", "r")
        fh_err = open("tmp.err", "r")
        txt = fh_err.read() + fh_out.read()
        # In the current version we forgive unused static functions
        postponed_list = []
        for line in txt.splitlines():
            if    line.find("defined but not used") != -1 \
               or line.find("but never defined") != -1 \
               or line.find("unused variable") != -1 \
               or line.find("At top level") != -1 \
               or line.find("t global scope") != -1 \
               or (     (line.find("warning: unused variable") != -1 )                                           \
                   and ((line.find("path_") != -1 and not line.find("_end")) or line.find("pathwalker_") != -1)) \
               or (line.find("In function") != -1 and line.lower().find("error") == -1):
                    if IGNORE_WARNING_F: 
                        postponed_list.append("## IGNORED: " + line.replace(os.environ["QUEX_PATH"] + "/quex/", ""))
                        continue
            if FilterFunc is None:
                print line
            else:
                FilterFunc(filter_result_db, line)

        if FilterFunc is None:
            for line in postponed_list:
                print line
        else:
            for line in postponed_list:
                FilterFunc(filter_result_db, line)

        os.remove("tmp.out")
        os.remove("tmp.err")
    else: #except:
        print "<<execution failed>>"

def compile_and_run(Language, SourceCode, AssertsActionvation_str="", StrangeStream_str="",
                    TestStrList=None):

    executable_name, filename_tmp = compile(Language, SourceCode, AssertsActionvation_str, 
                                            StrangeStream_str)

    print "## (*) running the test"
    if TestStrList is None:
        run_this("./%s" % executable_name)
    else:
        for test_str in TestStrList:
            print "-----------------------------------------------------------------"
            with open("tmp.txt", "w") as fh:
                fh.write(test_str)
                fh.close()
            run_this("./%s tmp.txt" % executable_name)
    if REMOVE_FILES:
        try:    os.remove(filename_tmp)
        except: pass
        try:    os.remove(executable_name)
        except: pass

def compile(Language, SourceCode, AssertsActionvation_str="", StrangeStream_str=""):
    print "## (2) compiling generated engine code and test"    
    we_str = "-Wall -Werror -Wno-error=unused-function -Wno-missing-braces"
    if Language.find("ANSI-C") != -1:
        extension = ".c"
        # The '-Wvariadic-macros' shall remind us that we do not want use variadic macroes.
        # Because, some compilers do not swallow them!
        compiler  = "gcc -ansi -Wvariadic-macros %s" % we_str
    else:
        extension = ".cpp"
        compiler  = "g++ %s" % we_str

    fd, filename_tmp = mkstemp(extension, "tmp-", dir=os.getcwd())

    os.write(fd, SourceCode) 
    os.close(fd)    
    
    os.system("mv -f %s tmp%s" % (filename_tmp, extension)); 
    filename_tmp = "./tmp%s" % extension # DEBUG

    executable_name = "%s.exe" % filename_tmp
    # NOTE: QUEX_OPTION_ASSERTS is defined by AssertsActionvation_str (or not)
    try:    os.remove(executable_name)
    except: pass
    compile_str = compiler                + " " + \
                  StrangeStream_str       + " " + \
                  AssertsActionvation_str + " " + \
                  filename_tmp            + " " + \
                  "-I./. -I../../../code_base/TESTS -I%s " % os.environ["QUEX_PATH"] + \
                  "-o %s "      % executable_name         + \
                  SHOW_TRANSITIONS_STR    + " " + \
                  SHOW_BUFFER_LOADS_STR


    # If computed gotos are involved, then make sure that the option is really active.
    # if compile_str.find("-DQUEX_OPTION_COMPUTED_GOTOS_EXT") != -1:
    #   run_this(compile_str + " -E") # -E --> expand macros
    #   content = open(filename_tmp, "rb").read()
    #   if content.find("QUEX_STATE_ROUTER"):
    #       print "##Error: computed gotos contain state router."
    #       sys.exit()

    print compile_str + "##" # DEBUG
    run_this(compile_str)
    sys.stdout.flush()

    return executable_name, filename_tmp

def create_main_function(Language, TestStr, QuexBufferSize, CommentTestStrF=False, ComputedGotoF=False):
    test_str = TestStr.replace("\"", "\\\"")
    test_str = test_str.replace("\n", "\\n\"\n\"")
    test_str = test_str.replace("\t", "\\t")

    txt = test_program_db[Language]
    txt = txt.replace("$$BUFFER_SIZE$$", repr(QuexBufferSize))
    txt = txt.replace("$$TEST_STRING$$", test_str)

    if CommentTestStrF: txt = txt.replace("$$COMMENT$$", "##")
    else:               txt = txt.replace("$$COMMENT$$", "")

    return txt

def create_common_declarations(Language, QuexBufferSize, 
                               QuexBufferFallbackN=0, BufferLimitCode=0, 
                               IndentationSupportF=False, 
                               ComputedGotoF=False):
    assert QuexBufferFallbackN >= 0

    # Determine the 'fallback' region size in the buffer
    #if QuexBufferFallbackN == -1: 
    #    QuexBufferFallbackN = QuexBufferSize - 3
    #if Language == "ANSI-C-PlainMemory": 
    #    QuexBufferFallbackN = max(0, len(TestStr) - 3) 

    txt  = ""
    txt += "#    define QUEX_SETTING_BUFFER_SIZE_EXT  %s\n" % QuexBufferSize

    # Parameterize the common declarations
    txt += "#define QUEX_OPTION_SUPPORT_BEGIN_OF_LINE_PRE_CONDITION_EXT\n" 
    txt += "#define QUEX_OPTION_UNIT_TEST_EXT\n" 

    txt += test_program_common_declarations.replace("$$BUFFER_FALLBACK_N$$", 
                                                    repr(QuexBufferFallbackN)) 
    txt  = txt.replace("$$BUFFER_SIZE$$", "%s" % QuexBufferSize)
    class Something:
        pass
    mode_1 = Something()
    mode_1.name = "M"
    mode_1.incidence_db = {}
    mode_2 = Something()
    mode_2.name = "M2"
    mode_2.incidence_db = {}
    txt  = txt.replace("$$MODE_DEF_M$$", modes.initialization(mode_1))
    txt  = txt.replace("$$MODE_DEF_M2$$", modes.initialization(mode_2))

    txt = txt.replace("$$BUFFER_LIMIT_CODE$$", repr(BufferLimitCode))

    replace_str = "#define QUEX_OPTION_INDENTATION_TRIGGER_EXT"
    if not IndentationSupportF: replace_str = "/* %s */" % replace_str
    txt = txt.replace("$$QUEX_OPTION_INDENTATION_TRIGGER$$", replace_str)
       
    replace_str = "#define QUEX_OPTION_PLAIN_C_EXT"
    if Language not in ["ANSI-C", "ANSI-C-PlainMemory", "ANSI-C-from-file"]: replace_str = "/* %s */" % replace_str
    txt = txt.replace("$$QUEX_OPTION_PLAIN_C_EXT$$", replace_str)

    return txt

def create_state_machine_function(PatternActionPairList, PatternDictionary, 
                                  BufferLimitCode, SecondModeF=False):
    global dial_db
    incidence_db = IncidenceDB()

    if not SecondModeF:  sm_name = "M"
    else:                sm_name = "M2"

    Setup.analyzer_class_name = "TestAnalyzer"
    Setup.analyzer_name_safe  = "TestAnalyzer"

    # (*) Initialize address handling
    dial_db = DialDB()     # BEFORE constructor of generator; 
    variable_db.variable_db.init()  # because constructor creates some addresses.
    blackboard.required_support_begin_of_line_set()
    terminal_factory = TerminalFactory(sm_name, incidence_db, dial_db)

    # -- Display Setup: Patterns and the related Actions
    print "(*) Lexical Analyser Patterns:"
    for pair in PatternActionPairList:
        print "%20s --> %s" % (pair[0], pair[1])

    def action(ThePattern, PatternName): 
        txt = []
        if ThePattern.sm_bipd_to_be_reversed is not None:
            terminal_factory.do_bipd_entry_and_return(txt, pattern)

        txt.append("%s\n" % Lng.STORE_LAST_CHARACTER(blackboard.required_support_begin_of_line()))
        txt.append("%s\n" % Lng.LEXEME_TERMINATING_ZERO_SET(True))
        txt.append('printf("%19s  \'%%s\'\\n", Lexeme); fflush(stdout);\n' % PatternName)

        if   "->1" in PatternName: txt.append("me->current_analyzer_function = QUEX_NAME(M_analyzer_function);\n")
        elif "->2" in PatternName: txt.append("me->current_analyzer_function = QUEX_NAME(M2_analyzer_function);\n")

        if   "CONTINUE" in PatternName: txt.append("")
        elif "STOP" in PatternName:     txt.append("QUEX_NAME(MF_error_code_set_if_first)(me, E_Error_UnitTest_Termination); return;\n")
        else:                           txt.append("return;\n")

        txt.append("%s\n" % Lng.GOTO(DoorID.continue_with_on_after_match(dial_db), dial_db))
        ## print "#", txt
        return CodeTerminal(txt)
    
    pattern_action_list = [
        (regex.do(pattern_str, PatternDictionary), action_str)
        for pattern_str, action_str in PatternActionPairList
    ]
    
    ca_map       = LineColumnCount_Default()
    pattern_list = []
    terminal_db  = {}
    for pattern, action_str in pattern_action_list:
        pattern  = pattern.finalize(ca_map)
        name     = Lng.SAFE_STRING(pattern.pattern_string())
        terminal = Terminal(action(pattern, action_str), name, dial_db=dial_db)
        terminal.set_incidence_id(pattern.incidence_id)

        pattern_list.append(pattern)
        terminal_db[pattern.incidence_id] = terminal

    # -- PatternList/TerminalDb
    #    (Terminals can only be generated after the 'mount procedure', because, 
    #     the bipd_sm is generated through mounting.)
    on_failure = CodeTerminal(["QUEX_NAME(MF_error_code_set_if_first)(me, E_Error_UnitTest_Termination); return;\n"])
    terminal_db.update({
        E_IncidenceIDs.MATCH_FAILURE: Terminal(on_failure, "FAILURE", 
                                               E_IncidenceIDs.MATCH_FAILURE,
                                               dial_db=dial_db),
        E_IncidenceIDs.END_OF_STREAM: Terminal(on_failure, "END_OF_STREAM", 
                                               E_IncidenceIDs.END_OF_STREAM,
                                               dial_db=dial_db),
        E_IncidenceIDs.BAD_LEXATOM:   Terminal(on_failure, "BAD_LEXATOM", 
                                               E_IncidenceIDs.BAD_LEXATOM,
                                               dial_db=dial_db),
        E_IncidenceIDs.LOAD_FAILURE:  Terminal(on_failure, "LOAD_FAILURE", 
                                               E_IncidenceIDs.LOAD_FAILURE,
                                               dial_db=dial_db),
    })

    mode = Mode(sm_name, SourceRef_VOID, 
                pattern_list, terminal_db, [], incidence_db,
                RunTimeCounterDb=None, 
                ReloadStateForward=None, 
                RequiredRegisterSet=set(),
                dial_db=dial_db,
                Documentation=ModeDocumentation([],[],[],[],[]))

    print "## (1) code generation"    

    txt = engine_generator.do_with_counter(mode, ["M", "M2"])
    assert all_isinstance(txt, str)

    return "#define  QUEX_OPTION_UNIT_TEST_EXT\n" + "".join(txt)

language_defines = """
#ifdef __cplusplus
#    define QUEX_INLINE inline
#else
#    define QUEX_INLINE 
#endif
"""

test_program_common_declarations = """
$$QUEX_OPTION_PLAIN_C_EXT$$
$$QUEX_OPTION_INDENTATION_TRIGGER$$
#define QUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN_DISABLED_EXT
#define QUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT
#define QUEX_SETTING_BUFFER_FALLBACK_N_EXT     ((size_t)$$BUFFER_FALLBACK_N$$)
#define QUEX_SETTING_BUFFER_LIMIT_CODE_EXT         ((TestAnalyzer_lexatom_t)$$BUFFER_LIMIT_CODE$$)
#define QUEX_OPTION_INCLUDE_STACK_DISABLED_EXT

#if 0
#define QUEX_TKN_TERMINATION       0
#define QUEX_TKN_UNINITIALIZED     1
#define QUEX_TKN_INDENT            3
#define QUEX_TKN_DEDENT            4
#define QUEX_TKN_NODENT            5
#endif

#ifdef __cplusplus
#include <cassert>
namespace quex {
typedef int TestAnalyzer_indentation_t;
}
#include "$$TEST_ANALYZER_DIR$$/TestAnalyzer"
#else
#include <assert.h>
typedef int TestAnalyzer_indentation_t;
#include "$$TEST_ANALYZER_DIR$$/TestAnalyzer.h"
#endif
#include "$$TEST_ANALYZER_DIR$$/lib/analyzer/asserts.i"
#include "$$TEST_ANALYZER_DIR$$/lib/analyzer/struct/constructor.i"
#include "$$TEST_ANALYZER_DIR$$/lib/analyzer/struct/reset.i"
#include "$$TEST_ANALYZER_DIR$$/lib/analyzer/member/mode-handling.i"
#include "$$TEST_ANALYZER_DIR$$/lib/buffer/asserts.i"
#include "$$TEST_ANALYZER_DIR$$/lib/token/TokenQueue.i"

#include "$$TEST_ANALYZER_DIR$$/lib/implementations.i"
#include "$$TEST_ANALYZER_DIR$$/lib/implementations-inline.i"

QUEX_NAMESPACE_MAIN_OPEN     
TestAnalyzer_lexatom_t   LexemeNull = (TestAnalyzer_lexatom_t)0;
QUEX_NAMESPACE_MAIN_CLOSE     

#ifndef RETURN
#   define RETURN    return
#endif

TestAnalyzer*        lexer_state;

extern void  QUEX_NAME(M_analyzer_function)(QUEX_TYPE_ANALYZER*);
#ifdef QUEX_UNIT_TEST_SECOND_MODE
extern void  QUEX_NAME(M2_analyzer_function)(QUEX_TYPE_ANALYZER*);
#endif

QUEX_NAMESPACE_MAIN_OPEN
bool QUEX_NAME(M_has_base)(QUEX_NAME(Mode) const* me)       { return false; }                                                                  
bool QUEX_NAME(M_has_entry_from)(QUEX_NAME(Mode) const* me) { return false; }                                                            
bool QUEX_NAME(M_has_exit_to)(QUEX_NAME(Mode) const* me)    { return false; }                                                               
void QUEX_NAME(M_on_buffer_before_change)(void* me)         { return; }                                                                                
void QUEX_NAME(M_on_buffer_overflow)(void* me)              { return; }                                                                                     

$$MODE_DEF_M$$

#ifdef QUEX_UNIT_TEST_SECOND_MODE
bool QUEX_NAME(M2_has_base)(QUEX_NAME(Mode) const* me)       { return false; }                                                                  
bool QUEX_NAME(M2_has_entry_from)(QUEX_NAME(Mode) const* me) { return false; }                                                            
bool QUEX_NAME(M2_has_exit_to)(QUEX_NAME(Mode) const* me)    { return false; }                                                               
void QUEX_NAME(M2_on_buffer_before_change)(void* me)         { return; }                                                                                
void QUEX_NAME(M2_on_buffer_overflow)(void* me)              { return; }                                                                                     

$$MODE_DEF_M2$$
#endif

const QUEX_NAME(Mode) *(QUEX_NAME(mode_db)[256]) = {
   &QUEX_NAME(M)
#  ifdef QUEX_UNIT_TEST_SECOND_MODE
   , 
   &QUEX_NAME(M2)
#  endif
};
QUEX_NAMESPACE_MAIN_CLOSE

static int
run_test(const char* TestString, const char* Comment)
{
    ptrdiff_t  real_buffer_size;
            
    if( strlen(TestString) > 256 ) {
        printf("(*) test string: \\n'%.256s...'%s\\n", TestString, Comment);
    } 
    else {
        printf("(*) test string: \\n'%s'%s\\n", TestString, Comment);
    }
    printf("(*) result:\\n");

    real_buffer_size =   lexer_state->buffer._memory._back 
                       - lexer_state->buffer._memory._front + 1;
    if( real_buffer_size != $$BUFFER_SIZE$$ ) {
        printf("ERROR: buffer_size: { required: $$BUFFER_SIZE$$; real: %i; }\\n",
               (int)real_buffer_size);
        return -1;
    }

    while( lexer_state->error_code == E_Error_None ) {
        lexer_state->current_analyzer_function(lexer_state);
        /* printf("---\\n"); */

        /* Print the token queue */
        while( QUEX_NAME(TokenQueue_is_empty)(&lexer_state->_token_queue) == false ) {        
            switch( QUEX_NAME(TokenQueue_pop)(&lexer_state->_token_queue)->id ) {
            case QUEX_TKN_INDENT:      printf("INDENT\\n"); break;
            case QUEX_TKN_DEDENT:      printf("DEDENT\\n"); break;
            case QUEX_TKN_NODENT:      printf("NODENT\\n"); break;
            case QUEX_TKN_TERMINATION: return 0;
            default:                   printf("Unknown Token ID\\n"); break;
            }
        }
        QUEX_NAME(TokenQueue_reset)(&lexer_state->_token_queue);
    }

    printf("  ''\\n");
    return 0;
}
"""


test_program_db = { 
    "ANSI-C-PlainMemory": """
    #include <stdlib.h>

    int main(int argc, char** argv)
    {
        TestAnalyzer_lexatom_t  TestString[] = "\\0$$TEST_STRING$$\\0";
        const size_t       MemorySize   = strlen((const char*)&TestString[1]) + 2;
        TestAnalyzer  object;

        $$COMPUTED_GOTOS_CHECK$$;
        lexer_state = &object;
        QUEX_NAME(from_memory)(lexer_state, 
                               TestString, MemorySize, &TestString[MemorySize - 1]); 
        /**/
        return run_test((const char*)&TestString[1], "$$COMMENT$$");
    }\n""",

    "ANSI-C": """
    #include <stdio.h>
    #if 0
    #include "$$TEST_ANALYZER_DIR$$/lib/buffer/lexatoms/LexatomLoader_Plain"
    #endif

    int main(int argc, char** argv)
    {
        char*  test_string = "$$TEST_STRING$$";
        char   buffer[65536*16];
        FILE*  fh;
        int    n;
        TestAnalyzer      object;
        QUEX_NAME(ByteLoader)* byte_loader;

        lexer_state = &object;
    
        if( argc > 1 ) {
            fh = fopen(argv[1], "rb");
            n  = fread(&buffer[0], 1, sizeof(buffer), fh); 
    #       if 0
            printf("%s: %i\\n", argv[1], n);
    #       endif
            test_string    = &buffer[0];
            test_string[n] = '\\0';
        } else {
            fh = tmpfile();
            /* Write test string into temporary file */
            fwrite(test_string, strlen(test_string), 1, fh);
        }
        fseek(fh, 0, SEEK_SET); /* start reading from the beginning */

        $$COMPUTED_GOTOS_CHECK$$;
        byte_loader = QUEX_NAME(ByteLoader_FILE_new)(fh, true);
        QUEX_NAME(from_ByteLoader)(lexer_state, byte_loader, NULL);
        /**/
        (void)run_test(test_string, "$$COMMENT$$");

        fclose(fh); /* this deletes the temporary file (see description of 'tmpfile()') */
        return 0;
    }\n""",

    "Cpp": """
    #include <cstring>
    #include <sstream>
    #include "$$TEST_ANALYZER_DIR$$/lib/buffer/lexatoms/LexatomLoader_Plain"

    int main(int argc, char** argv)
    {
        using namespace std;

        istringstream*          istr = new istringstream("$$TEST_STRING$$");
        QUEX_NAME(ByteLoader)*  byte_loader = QUEX_NAME(ByteLoader_stream_new)(istr);

        $$COMPUTED_GOTOS_CHECK$$;
        lexer_state = TestAnalyzer::from_ByteLoader(byte_loader, NULL);

        return run_test("$$TEST_STRING$$", "$$COMMENT$$");
    }\n""",

    "Cpp_StrangeStream": """
    #include <cstring>
    #include <sstream>
    #include "$$TEST_ANALYZER_DIR$$/lib/buffer/lexatoms/LexatomLoader_Plain"
    #include "$$TEST_ANALYZER_DIR$$/lib/quex/StrangeStream"


    int main(int argc, char** argv)
    {
        using namespace std;

        istringstream                  istr("$$TEST_STRING$$");
        StrangeStream<istringstream>*  strange_stream = new StrangeStream<istringstream>(&istr);
        QUEX_NAME(ByteLoader)*         byte_loader = QUEX_NAME(ByteLoader_stream_new)(strange_stream);

        $$COMPUTED_GOTOS_CHECK$$;
        lexer_state = TestAnalyzer::from_ByteLoader(byte_loader, 0x0);
        return run_test("$$TEST_STRING$$", "$$COMMENT$$");
    }\n""",

    "ANSI-C-from-file": """
    #include <stdio.h>
    #include <stdlib.h>

    int main(int argc, char** argv)
    {
        char              test_string[65536];
        FILE*             fh = fopen(argv[1], "rb");
        TestAnalyzer object;

        lexer_state = &object;

        (void)fread(test_string, 1, 65536, fh);
        fseek(fh, 0, SEEK_SET); /* start reading from the beginning */

        $$COMPUTED_GOTOS_CHECK$$;
        QUEX_NAME(ByteLoader)* byte_loader = QUEX_NAME(ByteLoader_FILE_new)(fh, true);
        QUEX_NAME(from_ByteLoader)(lexer_state, byte_loader, NULL); 

        (void)run_test(test_string, "$$COMMENT$$");

        fclose(fh); 
        return 0;
    }\n""",
}

def test_analyzer_dir(Language):
    if Language.find("Cpp") != -1: result = "test_cpp"
    else:                          result = "test_c"
    if Setup.computed_gotos_f: result += "_cg"
    return result

def computed_gotos_check_str():
    if Setup.computed_gotos_f:   
        return "{ TestAnalyzer_goto_label_t fails_if_not_computed_goto_labels = (void*)0; (void)fails_if_not_computed_goto_labels; }"
    else:
        return "{ long fails_if_computed_goto_labels = (TestAnalyzer_goto_label_t)0; (void)fails_if_computed_goto_labels; }" 

def __verify_code_generation(FullLanguage, SourceCode):
    def check_occurence(String, Code):
        count_n = 0
        for line in Code.splitlines():
            if line.find(String) != -1:
               count_n += 1
               if count_n == 2: return True
        return False

    if FullLanguage.find("Path") != -1:
        # Check whether paths have been defined
        if check_occurence("path_base", SourceCode)  == False:
            print "ERROR: Option '%s' requires paths to be generated. None is." % FullLanguage
            sys.exit()
        else:
            print "##verified path:", FullLanguage

    elif FullLanguage.find("Template") != -1:
        # Check whether paths have been defined
        if check_occurence("template_", SourceCode) == False: 
            print "ERROR: Option '%s' requires templates to be generated. None is." % FullLanguage
            sys.exit()
        else:
            print "##verified template:", FullLanguage


