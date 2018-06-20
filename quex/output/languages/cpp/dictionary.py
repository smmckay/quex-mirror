from   quex.input.code.base                              import CodeFragment
from   quex.engine.analyzer.state.core                   import Processor
from   quex.engine.operations.content_terminal_router    import RouterContentElement
from   quex.engine.operations.operation_list             import E_R
from   quex.engine.analyzer.mega_state.template.state    import TemplateState
from   quex.engine.analyzer.mega_state.path_walker.state import PathWalkerState
from   quex.engine.analyzer.door_id_address_label        import DoorID, \
                                                                DialDB, \
                                                                get_plain_strings
from   quex.engine.misc.string_handling                  import blue_print, \
                                                                pretty_code
from   quex.engine.misc.file_operations                  import open_file_or_die, \
                                                                get_file_content_or_die, \
                                                                write_safely_and_close
import quex.engine.misc.error                            as     error
from   quex.engine.misc.tools                            import typed, \
                                                                print_callstack, \
                                                                do_and_delete_if, \
                                                                none_isinstance, \
                                                                flatten_list_of_lists
import quex.output.languages.cpp.templates               as     templates

from   quex.DEFINITIONS  import QUEX_PATH
import quex.token_db     as     token_db
import quex.condition    as     condition
import quex.blackboard   as     blackboard
from   quex.blackboard   import setup as Setup, \
                                standard_incidence_db_get_incidence_id
from   quex.constants    import E_Files, \
                                E_StateIndices,  \
                                E_IncidenceIDs, \
                                E_TransitionN,   \
                                E_AcceptanceCondition, \
                                E_Op
from   itertools import islice, izip
from   math      import log
import re
import os

class Language(dict):
    #------------------------------------------------------------------------------
    # Define Regular Expressions
    #------------------------------------------------------------------------------
    Match_Lexeme              = re.compile("\\bLexeme\\b", re.UNICODE)
    Match_LexemeBegin         = re.compile("\\bLexemeBegin\\b", re.UNICODE)
    Match_string              = re.compile("\\bstring\\b", re.UNICODE) 
    Match_vector              = re.compile("\\bvector\\b", re.UNICODE) 
    Match_map                 = re.compile("\\bmap\\b", re.UNICODE)
    Match_include             = re.compile(r"#[ \t]*include[ \t]*[\"<]([^\">]+)[\">]")
    Match_Lexeme              = re.compile("\\bLexeme\\b", re.UNICODE)
    Match_QUEX_NAME_lexeme    = re.compile("\\bQUEX_NAME\\(lexeme_", re.UNICODE)
    Match_QUEX_NAME           = re.compile(r"\bQUEX_NAME\(([A-Z_a-z0-9]+)\)")
    Match_QUEX_GNAME          = re.compile(r"\bQUEX_GNAME\(([A-Z_a-z0-9]+)\)")
    Match_QUEX_NAME_TOKEN     = re.compile(r"\bQUEX_NAME_TOKEN\(([A-Z_a-z0-9]+)\)")
    Match_QUEX_GNAME_TOKEN    = re.compile(r"\bQUEX_GNAME_TOKEN\(([A-Z_a-z0-9]+)\)")
    Match_QUEX_NAME_LIB       = re.compile(r"\bQUEX_NAME_LIB\(([A-Z_a-z0-9]+)\)")
    Match_QUEX_GNAME_LIB      = re.compile(r"\bQUEX_GNAME_LIB\(([A-Z_a-z0-9]+)\)")
    Match_QUEX_SETTING        = re.compile(r"\bQUEX_SETTING_([A-Z_0-9]+)\b")
    Match_QUEX_OPTION         = re.compile(r"\bQUEX_OPTION_([A-Z_0-9]+)\b")
    # Note: When the first two are replaced, the last cannot match anymore.
    Match_QUEX_INCLUDE_GUARD_TOKEN = re.compile(r"\bQUEX_INCLUDE_GUARD__TOKEN__([a-zA-Z_0-9]+)\b")
    Match_QUEX_INCLUDE_GUARD_QUEX  = re.compile(r"\bQUEX_INCLUDE_GUARD__QUEX__([a-zA-Z_0-9]+)\b")
    Match_QUEX_INCLUDE_GUARD       = re.compile(r"\bQUEX_INCLUDE_GUARD__([a-zA-Z_0-9]+)\b")

    CommentDelimiterList      = [["//", "\n"], ["/*", "*/"]]
    
    CODE_BASE                 = "quex/code_base/"
    LEXEME_CONVERTER_DIR      = "lib/lexeme_converter"
                              
    INLINE                    = "inline"
    RETURN                    = "RETURN;"
    PURE_RETURN               = "return;"
    UNREACHABLE               = "__quex_assert_no_passage();"
    ELSE                      = "else {"
    ELSE_FOLLOWS              = "} else {"
    ELSE_SIMPLE               = "else"
    END_IF                    = "}"
    FALSE                     = "false"
    TRUE                      = "true"
    OR                        = "||"
    AND                       = "&&"

    PATH_ITERATOR_INCREMENT   = "++(path_iterator);"
    VIRTUAL_DESTRUCTOR_PREFIX = "virtual "

    STANDARD_TYPE_DB          = {
        1: "uint8_t", 2: "uint16_t", 4: "uint32_t", 8: "uint64_t",
    }

    all_extension_db = {
        "": { 
              E_Files.SOURCE:              ".cpp",
              E_Files.HEADER:              "",
              E_Files.HEADER_IMPLEMTATION: ".i",
        },
        "++": { 
              E_Files.SOURCE:              ".c++",
              E_Files.HEADER:              ".h++",
              E_Files.HEADER_IMPLEMTATION: ".h++",
        },
        "pp": { 
              E_Files.SOURCE:              ".cpp",
              E_Files.HEADER:              ".hpp",
              E_Files.HEADER_IMPLEMTATION: ".hpp",
        },
        "cc": { 
              E_Files.SOURCE:              ".cc",
              E_Files.HEADER:              ".hh",
              E_Files.HEADER_IMPLEMTATION: ".hh",
        },
        "xx": { 
              E_Files.SOURCE:              ".cxx",
              E_Files.HEADER:              ".hxx",
              E_Files.HEADER_IMPLEMTATION: ".hxx",
        },
    }
    extension_db = None # To be set by 'setup' to one of 'all_extension_db'

    def __init__(self):      
        self.__analyzer                           = None
        self.__code_generation_reload_label       = None
        self.__code_generation_on_reload_fail_adr = None
        assert self.RETURN.endswith(";")
        self.__re_RETURN                          = re.compile(r"\b%s\b" % self.RETURN[:-1])
        # NOTE: 'END_OF_STREAM' is not an error, it it caught upon the 
        #       termination token.
        self.__error_code_db = {
            E_IncidenceIDs.END_OF_STREAM:   ("",                         "E_Error_NoHandler_OnEndOfStream"),
            E_IncidenceIDs.MATCH_FAILURE:   ("E_Error_OnFailure",        "E_Error_NoHandler_OnFailure"),
            E_IncidenceIDs.SKIP_RANGE_OPEN: ("E_Error_OnSkipRangeOpen",  "E_Error_NoHandler_OnSkipRangeOpen"),
            E_IncidenceIDs.INDENTATION_BAD: ("E_Error_OnIndentationBad", "E_Error_NoHandler_OnIndentationBad"),
            E_IncidenceIDs.BAD_LEXATOM:     ("E_Error_OnBadLexatom",     "E_Error_NoHandler_OnBadLexatom"),
            E_IncidenceIDs.LOAD_FAILURE:    ("E_Error_OnLoadFailure",    "E_Error_NoHandler_OnLoadFailure"),
        }
            
    def ASSERT(self, Condition):
        return "__quex_assert(%s);" % Condition

    def FORWARD_DECLARATION(self, ClassName): 
        return "class %s;" % ClassName

    def SAFE_IDENTIFIER(self, String):
        if not String:
            return ""

        def _safe(L):
            if len(L) != 1:
                error.log("The underlying python build cannot handle character '%s'." % L)
            if L.isalpha() or L.isdigit() or L == "_": return L.lower()
            elif L == ":":                             return "_"
            else:                                      return "_x%x_" % ord(L)
        return "".join(_safe(letter) for letter in String)

    def INCLUDE_GUARD(self, Filename):
        if Filename: return self.SAFE_IDENTIFIER(Filename).upper()
        else:        return ""

    def INCREMENT_ITERATOR_THEN_ASSIGN(self, Iterator, Value):
        return "*(%s)++ = %s;" % (Iterator, Value)

    def OP(self, Big, Op, Small):
        return "%s %s %s" % (Big, Op, Small)

    def SWITCH(self, txt, Name, SwitchF):
        if SwitchF: txt = txt.replace("$$SWITCH$$ %s" % Name, "#define    %s" % Name)
        else:       txt = txt.replace("$$SWITCH$$ %s" % Name, "/* #define %s */" % Name)
        return txt

    def BUFFER_SEEK(self, Position):
        return "QUEX_NAME(Buffer_seek)(&me->buffer, %s)" % Position

    def open_template(self, PathTail):
        full_path = os.path.normpath(os.path.join(QUEX_PATH, PathTail))
        return get_file_content_or_die(full_path)

    def open_template_fh(self, PathTail):
        full_path = os.path.normpath(os.path.join(QUEX_PATH, PathTail))
        return open_file_or_die(full_path)

    def token_template_file(self):         return "%s/token/TXT-Cpp"                         % self.CODE_BASE
    def token_template_i_file(self):       return "%s/token/TXT-Cpp.i"                       % self.CODE_BASE
    def token_default_file(self):          return "%s/token/CppDefault.qx"                   % self.CODE_BASE
    def analyzer_template_file(self):      return "%s/analyzer/TXT-Cpp"                      % self.CODE_BASE
    def analyzer_template_i_file(self):    return "%s/analyzer/TXT-Cpp.i"                    % self.CODE_BASE
    def analyzer_configuration_file(self): return "%s/analyzer/configuration/TXT"            % self.CODE_BASE

    def _template_converter(self, Basename):
        path = os.path.join(QUEX_PATH, self.CODE_BASE, "lexeme_converter", Basename)
        return get_file_content_or_die(path)
    def template_converter_character_functions(self):     
        return self._template_converter("TXT-character-functions-from-encoding")
    def template_converter_character_functions_standard(self, EncodingName): 
        return self._template_converter("TXT-character-functions-from-%s" % EncodingName)
    def template_converter_string_functions(self):
        return self._template_converter("TXT-string-functions")
    def template_converter_header(self):       
        return self._template_converter("TXT-header")
    def template_converter_implementation(self):
        return self._template_converter("TXT-implementation")

    def file_name_converter_header(self, Suffix): 
        return os.path.join(Setup.output_directory, "converter-from-%s" % Suffix)
    def file_name_converter_implementation(self, Suffix): 
        return os.path.join(Setup.output_directory, "converter-from-%s.i" % Suffix)

    def DEFINE_SELF(self, Name):
        return "#   ifdef     self\n" \
               "#       undef self\n" \
               "#   endif\n" \
               "#   define self (*((QUEX_TYPE_ANALYZER*)%s))\n" % Name\

    def MODE_DEFINITION(self, ModeNameList):
        if not ModeNameList: return ""
        L = max(len(m) for m in ModeNameList)
        return "\n".join(
            "#   define %s%s    (&QUEX_NAME(%s))" % (name, " " * (L- len(name)), name)
            for name in ModeNameList
        ) + "\n"

    def MODE_UNDEFINITION(self, ModeNameList):
        if not ModeNameList: return ""
        return "\n".join(
            "#   undef %s" % name for name in ModeNameList
        ) + "\n"

    def register_analyzer(self, TheAnalyzer):
        self.__analyzer = TheAnalyzer

    def unregister_analyzer(self):
        # Unregistering an analyzer ensures that no one else works with the 
        # analyzer on something unrelated.
        self.__analyzer = None

    def EQUAL(self, X, Y):
        return "%s == %s" % (X, Y)

    def BINARY_OPERATION_LIST(self, Operator, ConditionList):
        condition_list = [ c for c in ConditionList if c ]
        if not condition_list: 
            return []
        elif len(condition_list) == 1: 
            return [ condition_list[0] ]
        else:
            result = [ "(%s)" % condition_list[0] ]
            for condition in condition_list[1:]:
                result.append(" %s " % Operator)
                result.append("(%s)" % condition)
            return result

    @property
    def analyzer(self):
        return self.__analyzer

    def _get_log2_if_power_of_2(self, X):
        assert type(X) != tuple
        if not isinstance(X, (int, long)):
            return None

        log2 = log(X, 2)
        if not log2.is_integer(): return None
        return int(log2)
            
    def __getattr__(self, Attr): 
        # Thanks to Rami Al-Rfou' who mentioned that this is the only thing to 
        # be adapted to be compliant with current version of PyPy.
        try:             return self[Attr] 
        except KeyError: raise AttributeError

    def LEXEME_START_SET(self, PositionStorage=None):
        if PositionStorage is None: return "me->buffer._lexeme_start_p = me->buffer._read_p;"
        else:                       return "me->buffer._lexeme_start_p = %s;" % PositionStorage
    def LEXEME_START_P(self):                      return "me->buffer._lexeme_start_p"
    def LEXEME_NULL(self):                         return "LexemeNull"
    def LEXEME_LENGTH(self):                       return "((size_t)(me->buffer._read_p - me->buffer._lexeme_start_p))"

    def LEXEME_MACRO_SETUP(self):
        return blue_print(templates.lexeme_macro_setup, [
            ["$$LEXEME_LENGTH$$",  self.LEXEME_LENGTH()],
            ["$$INPUT_P$$",        self.INPUT_P()],
        ])

    def LEXEME_MACRO_CLEAN_UP(self):
        return templates.lexeme_macro_clean_up

    def DEFAULT_TOKEN_COPY(self, X, Y):
        return "__QUEX_STD_memcpy((void*)%s, (void*)%s, sizeof(QUEX_TYPE_TOKEN));\n" % (X, Y)

    def INPUT_P(self):                             return "me->buffer._read_p"
    def INPUT_P_TO_LEXEME_START(self):             return "me->buffer._read_p = me->buffer._lexeme_start_p;"
    def INPUT_P_DEREFERENCE(self, Offset=0): 
        if Offset == 0:  return "*(me->buffer._read_p)"
        elif Offset > 0: return "*(me->buffer._read_p + %i)" % Offset
        else:            return "*(me->buffer._read_p - %i)" % - Offset
    def LEXEME_TERMINATING_ZERO_SET(self, RequiredF):
        if not RequiredF: return ""
        return "QUEX_LEXEME_TERMINATING_ZERO_SET(&me->buffer);\n"
    def INDENTATION_HANDLER_CALL(self, ModeName):
        name = self.NAME_IN_NAMESPACE_MAIN("%s_on_indentation" % ModeName)
        return "".join(["    if( QUEX_NAME(indentation_handler_is_active)(me) ) {\n",
                "        %s(me, (QUEX_TYPE_INDENTATION)me->counter._column_number_at_end, LexemeNull);\n" % name,
                "    }\n"])

    def STORE_LAST_CHARACTER(self, BeginOfLineSupportF):
        if not BeginOfLineSupportF: return ""
        # TODO: The character before lexeme start does not have to be written
        # into a special register. Simply, make sure that '_lexeme_start_p - 1'
        # is always in the buffer. This may include that on the first buffer
        # load '\n' needs to be at the beginning of the buffer before the
        # content is loaded. Not so easy; must be carefully approached.
        return "    %s\n" % self.ASSIGN("me->buffer._lexatom_before_lexeme_start", 
                                        self.INPUT_P_DEREFERENCE(-1))

    def UNDEFINE(self, NAME):
        return "\n#undef %s\n" % NAME

    @typed(Txt=(CodeFragment))
    def SOURCE_REFERENCED(self, Cf, PrettyF=False):
        if Cf is None:    return ""
        elif not PrettyF: text = Cf.get_text()
        else:             text = "".join(pretty_code(Cf.get_code()))

        return "%s%s%s" % (
            self._SOURCE_REFERENCE_BEGIN(Cf.sr),
            text,
            self._SOURCE_REFERENCE_END(Cf.sr)
        )

    def _SOURCE_REFERENCE_BEGIN(self, SourceReference):
        """Return a code fragment that returns a source reference pragma. If 
        the source reference is void, no pragma is required. 
        """
        if SourceReference.is_void(): return ""
        return "\n%s\n" % self.LINE_PRAGMA(SourceReference.file_name, SourceReference.line_n)

    def LINE_PRAGMA(self, Path, LineN):
        if LineN >= 2**15: 
            return '#   line %i "%s" /* was %i; ISO C89: 0 <= line number <= 32767 */' \
                    % (2**15 - 1, Path, LineN) 
        elif LineN <= 0:     
            return '#   line %i "%s" /* was %i; ISO C89: 0 <= line number <= 32767 */' \
                    % (1, Path, LineN) 
        else:
            return '#   line %i "%s"' % (LineN, Path) 

    def _SOURCE_REFERENCE_END(self, SourceReference=None):
        """Return a code fragment that returns a source reference pragma which
        tells about the file where the code has been pasted. If the SourceReference
        is provided, it may be checked wether the 'return pragma' is necessary.
        If not, an empty string is returned.
        """
        if SourceReference is None or not SourceReference.is_void(): 
            return '\n<<<<LINE_PRAGMA_WITH_CURRENT_LINE_N_AND_FILE_NAME>>>>\n'
        else:
            return ""

    def NAMESPACE_OPEN(self, NameList):
        if not NameList: return ""
        return " ".join(("    " * i + "namespace %s {" % name) for i, name in enumerate(NameList))

    def NAMESPACE_CLOSE(self, NameList):
        if not NameList: return ""
        return " ".join("} /* close %s */" % name for name in NameList)

    def NAMESPACE_REFERENCE(self, NameList, TrailingDelimiterF=True):
        if NameList and NameList[0]: result = "::".join(NameList)
        else:                        result = ""
        if TrailingDelimiterF: return result + "::"
        else:                  return result

    @typed(Name=(None, str,unicode), NameList=(None, list))
    def NAME_IN_NAMESPACE(self, Name, NameList):
        if NameList and NameList[0]: 
            return "%s%s" % (self.NAMESPACE_REFERENCE(NameList), Name)
        elif Name:
            return Name
        else:
            return ""

    def COMMENT(self, Comment):
        """Eliminated Comment Terminating character sequence from 'Comment'
           and comment it into a single line comment.
           For compatibility with C89, we use Slash-Star comments only, no '//'.
        """
        comment = Comment.replace("/*", "SLASH_STAR").replace("*/", "STAR_SLASH")
        return "/* %s */\n" % comment

    def ML_COMMENT(self, Comment, IndentN=4):
        indent_str = " " * IndentN
        comment = Comment.replace("/*", "SLASH_STAR").replace("*/", "STAR_SLASH").replace("\n", "\n%s * " % indent_str)
        return "%s/* %s\n%s */\n" % (indent_str, comment, indent_str)

    def COMMENT_STATE_MACHINE(self, txt, SM):
        txt.append(self.ML_COMMENT(
                        "BEGIN: STATE MACHINE\n"        + \
                        SM.get_string(NormalizeF=False) + \
                        "END: STATE MACHINE")) 

    def TOKEN_SET_MEMBER(self, Member, Value):
        return "self.token_p()->%s = %s;" % (Member, Value)

    def TOKEN_SEND(self, TokenName):
        return "self.send(%s);" % TokenName

    def TOKEN_SEND_N(self, N, TokenName):
        return "self.send_n(%s, (size_t)%s);\n" % (TokenName, N)

    def TOKEN_SEND_TEXT(self, TokenName, Begin, End):
        return "self.send_text(%s, %s, %s);" % (TokenName, Begin, End)

    def DEFAULT_COUNTER_FUNCTION_NAME(self, ModeName):
        return self.NAME_IN_NAMESPACE_MAIN("%s_counter" % ModeName)

    def DEFAULT_COUNTER_CALL(self):
        return "QUEX_FUNCTION_COUNT_ARBITRARY(&self, LexemeBegin, LexemeEnd);\n"

    def RUN_TIME_COUNTER_PROLOG(self, FunctionName):
        return "#ifdef      QUEX_FUNCTION_COUNT_ARBITRARY\n"                             \
               "#   undef   QUEX_FUNCTION_COUNT_ARBITRARY\n"                             \
               "#endif\n"                                                    \
               "#ifdef      QUEX_OPTION_COUNTER\n"                         \
               "#    define QUEX_FUNCTION_COUNT_ARBITRARY(ME, BEGIN, END) \\\n"          \
               "            do {                              \\\n"          \
               "                %s((ME), (BEGIN), (END));     \\\n"          \
               "                __quex_debug_counter();       \\\n"          \
               "            } while(0)\n"                                    \
               "#else\n"                                                     \
               "#    define QUEX_FUNCTION_COUNT_ARBITRARY(ME, BEGIN, END) /* empty */\n" \
               "#endif\n"                                                    \
               % FunctionName

    @typed(TypeStr=(str,unicode), MaxTypeNameL=(int,long), VariableName=(str,unicode))
    def CLASS_MEMBER_DEFINITION(self, TypeStr, MaxTypeNameL, VariableName):
        return "    %s%s %s;" % (TypeStr, " " * (MaxTypeNameL - len(TypeStr)), VariableName)

    def VARIABLE_DECLARATION(self, variable):
        if not condition.do(variable.condition):
            return ""

        if variable.constant_f: const_str = "const "
        else:                   const_str = ""

        if variable.initial_value: init_value_str = variable.init_value
        else:                      init_value_str = ""

        return "%s%s %s%s;" % (const_str, variable.type, variable.name, init_value_str)

    def MEMBER_VARIABLE_DECLARATION(self, variable):
        return self.VARIABLE_DECLARATION(variable)

    def MEMBER_FUNCTION_DECLARATION(self, signature):
        if not condition.do(signature.condition):
            return ""
        def argument_str(arg_type, arg_name, default):
            if default:
                return "%s %s = %s" % (arg_type, arg_name, default) 
            else:
                return "%s %s" % (arg_type, arg_name) 
        argument_list_str = ", ".join(argument_str(arg_type, arg_name, default) 
                                      for arg_type, arg_name, default in signature.argument_list)
        if signature.return_type != "void": return_str = "return "
        else:                               return_str = ""

        call_argument_list  = ["this"] + [ arg_name for arg_type, arg_name, default in signature.argument_list ]
        call_definition_str = "QUEX_NAME(MF_%s)(%s)" % (signature.function_name,
                                                        ", ".join(call_argument_list))
        return "%s %s(%s) { %s%s; }" % (signature.return_type, signature.function_name, 
                                        argument_list_str, return_str, call_definition_str)

    def MEMBER_FUNCTION_ASSIGNMENT(self, MemberFunctionSignatureList):
        return ""

    def REGISTER_NAME(self, Register):
        return {
            E_R.InputP:          "(me->buffer._read_p)",
            E_R.InputPBeforeReload: "read_p_before_reload",
            E_R.PositionDelta:      "position_delta",
            E_R.Column:          "(me->counter._column_number_at_end)",
            E_R.Line:            "(me->counter._line_number_at_end)",
            E_R.LexemeStartP:    "(me->buffer._lexeme_start_p)",
            E_R.BackupStreamPositionOfLexemeStartP: "(me->buffer._backup_lexatom_index_of_lexeme_start_p)",
            E_R.LexemeStartBeforeReload: "lexeme_start_before_reload_p)",
            E_R.CountReferenceP: "count_reference_p",
            E_R.LexemeEnd:       "LexemeEnd",
            E_R.Counter:         "counter",
            E_R.LoopRestartP:    "loop_restart_p",
            E_R.LoadResult:      "load_result",
        }[Register]

    def DEFINE_NESTED_RANGE_COUNTER(self):
        return "#define Counter %s" % self.REGISTER_NAME(E_R.Counter)

    def COMMAND_LIST(self, OpList, dial_db=None):
        return [ 
            "%s\n" % self.COMMAND(cmd, dial_db) for cmd in OpList
        ]

    @typed(dial_db=DialDB)
    def COMMAND(self, Op, dial_db=None):
        if Op.id == E_Op.Accepter:
            txt = []
            for i, element in enumerate(Op.content):
                block = "last_acceptance = %s; __quex_debug(\"last_acceptance = %s\\n\");\n" \
                        % (self.ACCEPTANCE(element.acceptance_id), self.ACCEPTANCE(element.acceptance_id))
                txt.extend(
                    self.IF_ACCEPTANCE_CONDITION_SET(i==0, 
                                                     element.acceptance_condition_set, 
                                                     block)
                )
            return "".join(txt)

        elif Op.id == E_Op.RouterByLastAcceptance:
            case_list = [
                (self.ACCEPTANCE(element.acceptance_id), 
                 self.position_and_goto(element, dial_db))
                for element in Op.content
            ]
            txt = self.BRANCH_TABLE_ON_STRING("last_acceptance", case_list)
            result = "".join(self.GET_PLAIN_STRINGS(txt, dial_db))
            return result

        elif Op.id == E_Op.RouterOnStateKey:
            case_list = [
                (state_key, self.GOTO(door_id, dial_db)) for state_key, door_id in Op.content
            ]
            if Op.content.register == E_R.PathIterator:
                key_txt = "path_iterator - path_walker_%i_path_base" % Op.content.mega_state_index 
            elif Op.content.register == E_R.TemplateStateKey:
                key_txt = "state_key"
            else:
                assert False

            txt = self.BRANCH_TABLE(key_txt, case_list)
            result = "".join(self.GET_PLAIN_STRINGS(txt, dial_db))
            return result

        elif Op.id == E_Op.IfPreContextSetPositionAndGoto:
            block = self.position_and_goto(Op.content.router_element, dial_db)
            txt   = self.IF_ACCEPTANCE_CONDITION_SET(True, 
                                                     Op.content.acceptance_condition_set,
                                                     block)
            return "".join(txt)

        elif Op.id == E_Op.QuexDebug:
            return '__quex_debug("%s");\n' % Op.content.string

        elif Op.id == E_Op.QuexAssertNoPassage:
            return self.UNREACHABLE

        elif Op.id == E_Op.GotoDoorId:
            return self.GOTO(Op.content.door_id, dial_db)

        elif Op.id == E_Op.GotoDoorIdIfCounterEqualZero:
            return "if( %s == 0 ) %s\n" % (self.REGISTER_NAME(E_R.Counter), 
                                           self.GOTO(Op.content.door_id, dial_db))

        elif Op.id == E_Op.GotoDoorIdIfInputPNotEqualPointer:
            return "if( %s != %s ) %s\n" % (self.INPUT_P(), 
                                            self.REGISTER_NAME(Op.content.pointer), 
                                            self.GOTO(Op.content.door_id, dial_db))

        elif Op.id == E_Op.IndentationHandlerCall:
            return self.INDENTATION_HANDLER_CALL(Op.content.mode_name)

        elif Op.id == E_Op.Assign:
            txt = "%s = %s" % (self.REGISTER_NAME(Op.content[0]), self.REGISTER_NAME(Op.content[1]))
            if Op.content.condition == "COLUMN":
                txt = "__QUEX_IF_COUNT_COLUMNS(%s)" % txt
            return "    %s;\n" % txt

        elif Op.id == E_Op.AssignConstant:
            register = Op.content.register
            value    = Op.content.value 

            if  register == E_R.Column:
                assignment = "%s = (size_t)%s" % (self.REGISTER_NAME(register), value)
                return "    __QUEX_IF_COUNT_COLUMNS(%s);\n" % assignment
            elif register == E_R.Line:
                assignment = "%s = (size_t)%s" % (self.REGISTER_NAME(register), value)
                return "    __QUEX_IF_COUNT_LINES(%s);\n" % assignment
            else:
                assignment = "%s = %s" % (self.REGISTER_NAME(register), value)
                return "    %s;\n" % assignment

        elif Op.id == E_Op.AssignPointerDifference:
            return "    %s = %s - %s;\n" % (self.REGISTER_NAME(Op.content.result), 
                                            self.REGISTER_NAME(Op.content.big),
                                            self.REGISTER_NAME(Op.content.small))

        elif Op.id == E_Op.PointerAssignMin:
            txt = "%s = %s < %s ? %s : %s" % (self.REGISTER_NAME(Op.content.result), 
                                              self.REGISTER_NAME(Op.content.a),
                                              self.REGISTER_NAME(Op.content.b),
                                              self.REGISTER_NAME(Op.content.a),
                                              self.REGISTER_NAME(Op.content.b))
            if Op.content.condition == "COLUMN":
                txt = "__QUEX_IF_COUNT_COLUMNS(%s)" % txt
            return "    %s;\n" % txt

        elif Op.id == E_Op.PointerAdd:
            txt = "%s = &%s[%s]" % (self.REGISTER_NAME(Op.content.pointer), 
                                    self.REGISTER_NAME(Op.content.pointer),
                                    self.REGISTER_NAME(Op.content.offset))
            if Op.content.condition == "COLUMN":
                txt = "__QUEX_IF_COUNT_COLUMNS(%s)" % txt
            return "    %s;\n" % txt

        elif Op.id == E_Op.ColumnCountAdd:
            if "%s" % Op.content.value == "LoopRestartP": print_callstack()
            return "__QUEX_IF_COUNT_COLUMNS_ADD((size_t)%s);\n" % self.VALUE_STRING(Op.content.value) 

        elif Op.id == E_Op.ColumnCountGridAdd:
            return "".join(self.COUNTER_COLUMN_GRID_STEP(Op.content.grid_size))

        elif Op.id == E_Op.ColumnCountReferencePSet:
            pointer_name = self.REGISTER_NAME(Op.content.pointer)
            offset       = Op.content.offset
            return self.REFERENCE_P_RESET(pointer_name, offset)

        elif Op.id == E_Op.ColumnCountReferencePDeltaAdd:
            return self.REFERENCE_P_COLUMN_ADD(self.REGISTER_NAME(Op.content.pointer), 
                                               Op.content.column_n_per_chunk, 
                                               Op.content.subtract_one_f) 

        elif Op.id == E_Op.LineCountAdd:
            txt = []
            if Op.content.value != 0:
                txt.append("__QUEX_IF_COUNT_LINES_ADD((size_t)%s);\n" % self.VALUE_STRING(Op.content.value))
            return "".join(txt)

        elif Op.id == E_Op.StoreInputPosition:
            # Assume that checking for the pre-context is just overhead that 
            # does not accelerate anything.
            if Op.content.offset == 0:
                return "    position[%i] = me->buffer._read_p; __quex_debug(\"position[%i] = input_p;\\n\");\n" \
                       % (Op.content.position_register, Op.content.position_register)
            else:
                return "    position[%i] = me->buffer._read_p - %i; __quex_debug(\"position[%i] = input_p - %i;\\n\");\n" \
                       % (Op.content.position_register, Op.content.offset, Op.content.position_register, Op.content.offset)

        elif Op.id == E_Op.PreContextOK:
            value = Op.content.acceptance_condition_id 
            return   "    pre_context_%i_fulfilled_f = 1;\n"                         % value \
                   + "    __quex_debug(\"pre_context_%i_fulfilled_f = true\\n\");\n" % value

        elif Op.id == E_Op.TemplateStateKeySet:
            value = Op.content.state_key
            return   "    state_key = %i;\n"                      % value \
                   + "    __quex_debug(\"state_key = %i\\n\");\n" % value

        elif Op.id == E_Op.PathIteratorSet:
            offset_str = ""
            if Op.content.offset != 0: offset_str = " + %i" % Op.content.offset
            txt =   "    path_iterator  = path_walker_%i_path_%i%s;\n"                   \
                  % (Op.content.path_walker_id, Op.content.path_id, offset_str)        \
                  + "    __quex_debug(\"path_iterator = (Pathwalker: %i, Path: %i, Offset: %s)\\n\");\n" \
                  % (Op.content.path_walker_id, Op.content.path_id, offset_str)
            return txt

        elif Op.id == E_Op.PrepareAfterReload:
            on_success_adr = Op.content.on_success_door_id.related_address
            on_failure_adr = Op.content.on_failure_door_id.related_address

            dial_db.mark_address_as_routed(on_success_adr)
            dial_db.mark_address_as_routed(on_failure_adr)

            return   "    target_state_index = QUEX_LABEL(%i); target_state_else_index = QUEX_LABEL(%i);\n"  \
                   % (on_success_adr, on_failure_adr)                                                        

        elif Op.id == E_Op.LexemeResetTerminatingZero:
            return "    QUEX_LEXEME_TERMINATING_ZERO_UNDO(&me->buffer);\n"

        elif Op.id == E_Op.InputPDereference:
            return "    %s\n" % self.ASSIGN("input", self.INPUT_P_DEREFERENCE())

        elif Op.id == E_Op.Increment:
            return "    ++%s;\n" % self.REGISTER_NAME(Op.content.register)

        elif Op.id == E_Op.Decrement:
            return "    --%s;\n" % self.REGISTER_NAME(Op.content.register)

        else:
            assert False, "Unknown command '%s'" % Op.id

    def SAFE_STRING(self, String):
        def get(Letter):
            if Letter in ['\\', '"', '\n', '\t', '\r', '\a', '\v']: return "\\" + Letter
            else:                                                   return Letter 

        return "".join(get(letter) for letter in String)

    def TERMINAL_CODE(self, TerminalStateList, TheAnalyzer, dial_db): 
        text = [
            templates._terminal_state_prolog
        ]
        terminal_door_id_list = []
        for terminal in sorted(TerminalStateList, key=lambda x: x.incidence_id()):
            terminal_door_id_list.append(terminal.door_id)

            t_txt = ["%s\n    __quex_debug(\"* TERMINAL %s\\n\");\n" % \
                     (self.LABEL(terminal.door_id), self.SAFE_STRING(terminal.name()))]
            code  = terminal.code(TheAnalyzer)
            assert none_isinstance(code, list)
            t_txt.extend(code)
            t_txt.append("\n")

            text.extend(t_txt)

        text.append(
            "if(0) {\n"
            "    /* Avoid unreferenced labels. */\n"
        )
        text.extend(
            "    %s\n" % self.GOTO(door_id, dial_db)
            for door_id in terminal_door_id_list
        )
        text.append("}\n")
        return text

    @typed(dial_db=DialDB)
    def ANALYZER_FUNCTION(self, ModeName, Setup, VariableDefs, 
                          FunctionBody, dial_db, ModeNameList):
        return templates._analyzer_function(ModeName, Setup, VariableDefs, 
                                            FunctionBody, dial_db, ModeNameList)

    def REENTRY_PREPARATION(self, PreConditionIDList, OnAfterMatchCode, dial_db):
        return templates.reentry_preparation(self, PreConditionIDList, OnAfterMatchCode, dial_db)

    @typed(dial_db=DialDB)
    def HEADER_DEFINITIONS(self, dial_db):
        return blue_print(cpp_header_definition_str, [
            ("$$CONTINUE_WITH_ON_AFTER_MATCH$$", self.LABEL_STR_BY_ADR(DoorID.continue_with_on_after_match(dial_db).related_address)),
            ("$$RETURN_WITH_ON_AFTER_MATCH$$",   self.LABEL_STR_BY_ADR(DoorID.return_with_on_after_match(dial_db).related_address)),
        ])

    def RETURN_THIS(self, Value):
        return "return %s;" % Value

    def CALL_MODE_HAS_ENTRY_FROM(self, ModeName):
        return   "#   ifdef QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK\n" \
               + "    QUEX_NAME(%s).has_entry_from(FromMode);\n" % ModeName \
               + "#   endif\n"

    def CALL_MODE_HAS_EXIT_TO(self, ModeName):
        return   "#   ifdef QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK\n" \
               + "    QUEX_NAME(%s).has_exit_to(ToMode);\n" % ModeName \
               + "#   endif\n"

    def LABEL_PLAIN(self, Label):
        return "%s:" % Label.strip()

    @typed(DoorId=DoorID)
    def LABEL(self, DoorId):
        return "%s:" % self.LABEL_STR_BY_ADR(DoorId.related_address)

    @typed(DoorId=DoorID)
    def LABEL_STR(self, DoorId):
        return "%s" % self.LABEL_STR_BY_ADR(DoorId.related_address)

    def LABEL_STR_BY_ADR(self, Adr):
        return "_%s" % Adr

    @typed(DoorId=DoorID)
    def GOTO(self, DoorId, dial_db):
        if DoorId.last_acceptance_f():
            return "QUEX_GOTO_TERMINAL(last_acceptance);"
        return self.GOTO_ADDRESS(DoorId.related_address, dial_db)

    def GOTO_BY_VARIABLE(self, VariableName):
        return "QUEX_GOTO_STATE(%s);" % VariableName 

    def GOTO_STRING(self, LabelStr):
        return "goto %s;" % LabelStr

    @typed(dial_db=DialDB)
    def GOTO_ADDRESS(self, Address, dial_db):
        dial_db.mark_address_as_gotoed(Address)
        return "goto %s;" % self.LABEL_STR_BY_ADR(Address)

    def COUNTER_SHIFT_VALUES(self):
        return "__QUEX_IF_COUNT_SHIFT_VALUES();\n" 

    def COUNTER_LINE_ADD(self, Arg):
        return "__QUEX_IF_COUNT_LINES_ADD(%s);\n" % Arg

    def COUNTER_COLUM_ADD(self, Arg):
        return "__QUEX_IF_COUNT_COLUMNS_ADD(%s);\n" % Arg

    def COUNTER_COLUM_SET(self, Value):
        return "__QUEX_IF_COUNT_COLUMNS_SET(%i);\n" % Value

    def COUNTER_COLUMN_GRID_STEP(self, GridWidth, StepN=1):
        """A grid step is an addition which depends on the current value 
        of a variable. It sets the value to the next valid value on a grid
        with a given width. The general solution is 

                  x  = (x - x % GridWidth) # go back to last grid.
                  x += GridWidth           # go to next grid step.

        For 'GridWidth' as a power of '2' there is a slightly more
        efficient solution.
        """
        assert GridWidth > 0
        TypeName     = "size_t"
        VariableName = "self.counter._column_number_at_end"
        IfMacro      = "__QUEX_IF_COUNT_COLUMNS"

        grid_with_str = self.VALUE_STRING(GridWidth)
        log2          = self._get_log2_if_power_of_2(GridWidth)
        if log2 is not None:
            # For k = a potentials of 2, the expression 'x - x % k' can be written as: x & ~mask(log2) !
            # Thus: x = x - x % k + k = x & mask + k
            mask = (1 << int(log2)) - 1
            if mask != 0: cut_str = "%s &= ~ ((%s)0x%X)" % (VariableName, TypeName, mask)
            else:         cut_str = ""
        else:
            cut_str = "%s -= (%s %% (%s))" % (VariableName, VariableName, grid_with_str)

        add_str = "%s += %s + 1" % (VariableName, self.MULTIPLY_WITH(grid_with_str, StepN))

        result = []
        if IfMacro is None: 
            result.append("%s -= 1;\n" % VariableName)
            if cut_str: result.append("%s;" % cut_str)
            result.append("%s;\n" % add_str)
        else:               
            result.append("%s(%s -= 1);\n" % (IfMacro, VariableName))
            if cut_str: result.append("%s(%s);\n" % (IfMacro, cut_str))
            result.append("%s(%s);\n" % (IfMacro, add_str))

        return result

    def MULTIPLY_WITH(self, FactorStr, NameOrValue):
        if isinstance(NameOrValue, (str, unicode)):
            return "%s * %s" % (FactorStr, self.VALUE_STRING(NameOrValue))

        x = NameOrValue

        if x == 0:
            return "0"
        elif x == 1:
            return FactorStr
        elif x < 1:
            x    = int(round(1.0 / x))
            log2 = self._get_log2_if_power_of_2(x)
            if log2 is not None:
                return "%s >> %i" % (FactorStr, int(log2))
            else:
                return "%s / %s" % (FactorStr, self.VALUE_STRING(x))
        else:
            log2 = self._get_log2_if_power_of_2(x)
            if log2 is not None:
                return "%s << %i" % (FactorStr, int(log2))
            else:
                return "%s * %s" % (FactorStr, self.VALUE_STRING(x))

    def VALUE_STRING(self, NameOrValue):
        if isinstance(NameOrValue, (str, unicode)):
            return "self.%s" % NameOrValue
        elif hasattr(NameOrValue, "is_integer") and NameOrValue.is_integer():
            return "%i" % NameOrValue
        else:
            return "%s" % NameOrValue

    def REFERENCE_P_COLUMN_ADD(self, IteratorName, ColumnCountPerChunk, SubtractOneF):
        """Add reference pointer count to current column. There are two cases:
           (1) The character at the end is part of the 'constant column count region'.
               --> We do not need to go one back. 
           (2) The character at the end is NOT part of the 'constant column count region'.
               --> We need to go one back (SubtractOneF=True).

           The second case happens, for example, when a 'grid' (tabulator) character is
           hit. Then, one needs to get before the tabulator before one jumps to the 
           next position.
        """
        minus_one = { True: " - 1", False: "" }[SubtractOneF]
        delta_str = "(%s - %s%s)" % (IteratorName, self.REGISTER_NAME(E_R.CountReferenceP), minus_one)
        return "__QUEX_IF_COUNT_COLUMNS_ADD((size_t)(%s));\n" \
               % self.MULTIPLY_WITH(delta_str, ColumnCountPerChunk)

    def REFERENCE_P_RESET(self, IteratorName, Offset=0):
        name = self.REGISTER_NAME(E_R.CountReferenceP)
        if   Offset > 0:
            return "__QUEX_IF_COUNT_COLUMNS(%s = %s + %i);\n" % (name, IteratorName, Offset) 
        elif Offset < 0:
            return "__QUEX_IF_COUNT_COLUMNS(%s = %s - %i);\n" % (name, IteratorName, - Offset) 
        else:
            return "__QUEX_IF_COUNT_COLUMNS(%s = %s);\n" % (name, IteratorName)

    def INCLUDE(self, Path, Condition=None):
        if   not Path:                    return ""
        elif not condition.do(Condition): return ""
        else:                             return "#include \"%s\"" % Path

    def ENGINE_TEXT_EPILOG(self):
        if Setup.analyzer_derived_class_file: header = self.INCLUDE(Setup.analyzer_derived_class_file)
        else:                                 header = self.INCLUDE(Setup.output_header_file)
        footer = self.FOOTER_IN_IMPLEMENTATION()
        return implementation_headers_txt.replace("$$HEADER$$", header) \
                                         .replace("$$FOOTER$$", footer)

    def FOOTER_IN_IMPLEMENTATION(self):
        return ""
    
    def MODE_GOTO(self, Mode):
        return "self.enter_mode(%s);" % Mode

    def MODE_GOSUB(self, Mode):
        return "self.push_mode(%s);" % Mode

    def MODE_GOUP(self):
        return "self.pop_mode();"

    def NAME_IN_NAMESPACE_MAIN(self, Name):
        return "QUEX_NAME(%s)" % Name

    def ACCEPTANCE(self, AcceptanceID):
        if   AcceptanceID == E_IncidenceIDs.MATCH_FAILURE: return "((QUEX_TYPE_ACCEPTANCE_ID)-1)"
        elif AcceptanceID == E_IncidenceIDs.BAD_LEXATOM:   return "((QUEX_TYPE_ACCEPTANCE_ID)-2)"
        else:                                              return "%i" % AcceptanceID

    @typed(Condition=list)
    def IF_PLAIN(self, FirstF, Condition, Consequence):
        if not Condition:
            if FirstF: return [ "%s" % "".join(Consequence) ]
            else:      return [ "else { %s }" % "".join(Consequence) ]
        else:
            if not FirstF: else_str = "else "
            else:          else_str = ""
            return [ 
                "%sif( %s ) {\n" % (else_str, " ".join(Condition)),
                "%s\n" % "".join(Consequence), 
                "}\n" 
            ]

    def IF(self, LValue, Operator, RValue, FirstF=True, SimpleF=False, SpaceF=False):
        if isinstance(RValue, (str,unicode)): condition = "%s %s %s"   % (LValue, Operator, RValue)
        else:                                 condition = "%s %s 0x%X" % (LValue, Operator, RValue)
        if not SimpleF:
            if FirstF: return "if( %s ) {\n"          % condition
            else:      return "\n} else if( %s ) {\n" % condition
        else:
            if FirstF: 
                if SpaceF: return "if     ( %s ) " % condition
                else:      return "if( %s ) "      % condition
            else:          return "else if( %s ) " % condition

    def IF_INPUT(self, Condition, Value, FirstF=True, NewlineF=True):
        return self.IF("input", Condition, Value, FirstF, SimpleF=not NewlineF)

    def IF_X(self, Condition, Value, Index, Length):
        """Index  = index of decision in list of if-else-if.
           Length = total number of decisions in if-else-if block.

        Calls 'IF' with the 'SpaceF=True' so that the first if-statement
        contains a 'pretty space' that makes it aligned with the remaining 
        decisions.
        """
        return self.IF("input", Condition, Value, Index==0, SimpleF=True, SpaceF=(Length>2))

    def IF_ACCEPTANCE_CONDITION_SET(self, FirstF, AccConditionSet, Consequence):
        def append_if_pre_context(acc_condition_id, result):
            if acc_condition_id == E_AcceptanceCondition.BEGIN_OF_LINE:
                code = "me->buffer._lexatom_before_lexeme_start == '\\n'"
            elif acc_condition_id == E_AcceptanceCondition.BEGIN_OF_STREAM:
                code = "QUEX_NAME(Buffer_is_begin_of_stream)(&me->buffer)"
            elif isinstance(acc_condition_id, (int, long)):
                code = "pre_context_%i_fulfilled_f" % acc_condition_id
            else:
                return False
            result.append(code)
            return True

        def append_if_post_context(acc_condition_id, result):
            if acc_condition_id == E_AcceptanceCondition.END_OF_STREAM:
                code = "QUEX_NAME(Buffer_is_end_of_stream)(&me->buffer)"
            else:
                return False
            result.append(code)
            return True

        remainder = list(AccConditionSet)
        pre_condition_list = []
        do_and_delete_if(remainder, append_if_pre_context, pre_condition_list)
        post_condition_list = []
        do_and_delete_if(remainder, append_if_post_context, post_condition_list)

        # Combinate logically: Or(pre-contexts) And Or(post-contexts)
        pre_combined  = self.BINARY_OPERATION_LIST(self.OR, pre_condition_list)
        post_combined = self.BINARY_OPERATION_LIST(self.OR, post_condition_list)
        all_combined  = self.BINARY_OPERATION_LIST(self.AND, ["".join(pre_combined), 
                                                              "".join(post_combined)])

        return self.IF_PLAIN(FirstF, all_combined, Consequence)

    def PRE_CONTEXT_RESET(self, PreConditionIDList):
        if PreConditionIDList is None: return ""
        return "".join([
            "    %s\n" % self.ASSIGN("pre_context_%s_fulfilled_f" % acceptance_condition_id, 0)
            for acceptance_condition_id in PreConditionIDList
        ])

    def ON_BAD_INDENTATION(self, OnBadIndentationTxt, BadIndentationIid, dial_db):
        return [
            "#define BadCharacter (me->buffer._read_p[-1])\n",
            "%s\n" % OnBadIndentationTxt,
            "#undef  BadCharacter\n",
            "%s\n" % self.GOTO(DoorID.global_reentry(dial_db), dial_db)
        ]

    def TRANSITION_MAP_TARGET(self, Interval, Target):
        assert isinstance(Target, str)
        if not Setup.comment_transitions_f:
            return Target
        else:
            return "%s %s" % (Target, self.COMMENT(Interval.get_utf8_string()))

    def ASSIGN(self, X, Y):
        return "%s = %s;" % (X, Y)

    def SIGNATURE(self, Prolog, FunctionName, ReturnType, ArgList):
        return "%s %s %s(%s)" % (Prolog, ReturnType, FunctionName, 
                                 ", ".join("%s %s" % (type_str, name_str) for type_str, name_str in ArgList))

    def STATE_DEBUG_INFO(self, TheState, GlobalEntryF):
        assert isinstance(TheState, Processor)

        if isinstance(TheState, TemplateState):
            return "    __quex_debug_template_state(%i, state_key);\n" \
                   % TheState.index
        elif isinstance(TheState, PathWalkerState):
            return "    __quex_debug_path_walker_state(%i, path_walker_%s_path_base, path_iterator);\n" \
                   % (TheState.index, TheState.index)
        elif GlobalEntryF: 
            return "    __quex_debug_init_state(%i);\n" % TheState.index
        elif TheState.index == E_StateIndices.DROP_OUT:
            return "    __quex_debug(\"Drop-Out Catcher\\n\");\n"
        elif isinstance(TheState.index, (int, long)):
            return "    __quex_debug_state(%i);\n" % TheState.index
        else:
            return ""

    @typed(X=RouterContentElement)
    def POSITIONING(self, X):
        Positioning = X.positioning
        Register    = X.position_register
        if   Positioning == E_TransitionN.VOID: 
            return   "    __quex_assert(position[%i] != (void*)0);\n" % Register \
                   + "    me->buffer._read_p = position[%i];\n" % Register
        # "_read_p = lexeme_start_p + 1" is done by TERMINAL_FAILURE. 
        elif Positioning == E_TransitionN.LEXEME_START_PLUS_ONE: 
            return "    %s = %s + 1;\n" % (self.INPUT_P(), self.LEXEME_START_P())
        elif Positioning > 0:     
            return "    me->buffer._read_p -= %i;\n" % Positioning
        elif Positioning == 0:    
            return ""
        else:
            assert False 

    def CONDITION_SEQUENCE(self, ConditionList, ConsequenceList, ElseConsequence=None):
        assert all(type(condition) == list for condition in ConditionList)
        txt = flatten_list_of_lists(
            self.IF_PLAIN((i==0), cc[0], Consequence=cc[1])
            for i, cc in enumerate(izip(ConditionList, ConsequenceList))
        )
        if ElseConsequence:
            txt.extend([self.ELSE, ElseConsequence, self.END_IF])
        return txt

    def COMPARISON_SEQUENCE(self, IntervalEffectSequence, get_decision):
        """Get a sequence of comparisons that map intervals to effects as given
        by 'IntervalEffectSequence'. The if-statements are coming out of 
        'get_decision'. The 'IntervalEffectSequence' is a list of pairs

                          (Interval, Effect-Text)

        meaning, that if 'input' is inside Interval, the 'Effect-Text' shall be
        executed.

        RETURNS: C-code that implements the comparison sequences.
        """
        L = len(IntervalEffectSequence)

        if   L == 0: return []
        elif L == 1: return ["%s\n" % IntervalEffectSequence[0][1]]

        sequence = [
            (get_decision(entry[0], i, L), entry[1])
            for i, entry in enumerate(IntervalEffectSequence)
        ]

        max_L = max(len(cause) for cause, effect in sequence)

        return [
            "%s %s%s\n" % (cause, " " * (max_L - len(cause)), effect)
            for cause, effect in sequence
        ]

    def CASE_STR(self, Format):
        return {
            "hex": "case 0x%X: ", 
            "dec": "case %i: "
        }[Format]

    def CASE_SELECT(self, Variable, CaseCodeList, Default):
        txt = ["switch( %s ) {\n" % Variable ]

        done_set = set([])
        for case, code in CaseCodeList:
            if case in done_set: continue
            done_set.add(case)
            txt.append("case %s: {\n" % case)
            if type(code) == list: txt.extend(code)
            else:                  txt.append(code)
            txt.append("}\n")

        txt.append("default: {\n")
        if type(code) == list: txt.extend(code)
        else:                  txt.append(code)
        txt.append("}\n")


        txt.append("}\n")

        return txt

    def BRANCH_TABLE(self, Selector, CaseList, CaseFormat="hex", DefaultConsequence=None):
        case_str = self.CASE_STR(CaseFormat)

        def case_integer(item, C, get_content):
            if item is None: return ["default: %s\n" % get_content(C)]
            return [ "%s %s\n" % (case_str % item, get_content(C)) ]

        return self._branch_table_core(Selector, CaseList, case_integer, DefaultConsequence)

    def BRANCH_TABLE_ON_STRING(self, Selector, CaseList):
        def case_string(item, C, get_content):
            if item is None: return ["default: %s\n" % get_content(C)]
            return [ "case %s: %s\n" % (item, get_content(C)) ]

        return self._branch_table_core(Selector, CaseList, case_string)

    def BRANCH_TABLE_ON_INTERVALS(self, Selector, CaseList, CaseFormat="hex", 
                                  DefaultConsequence=None):
        case_str = self.CASE_STR(CaseFormat)

        def case_list(From, To):
            return "".join("%s" % (case_str % i) for i in xrange(From, To))

        def case_list_iterable(item):
            # Next number divisible by '8' and greater than first_border
            first_border = int(item.begin / 8) * 8 + 8
            # Last number divisible by '8' and lesser than last_border
            last_border  = int((item.end - 1) / 8) * 8

            if first_border != item.begin:
                yield "%s\n" % case_list(item.begin, first_border)
            for begin in xrange(first_border, last_border-7, 8):
                yield "%s\n" % case_list(begin, begin + 8)
            yield "%s" % case_list(last_border, item.end)

        def case_interval(item, C, get_content):
            if item is None: return ["default: %s\n" % get_content(C)]

            size = item.end - item.begin
            if size == 1: 
                txt = [ case_str % (item.end-1) ]
            elif size <= 8: 
                txt = [ case_list(item.begin, item.end) ]
            else:
                txt = [
                    text
                    for text in case_list_iterable(item)
                ] 
            txt.append("%s\n" % get_content(C))
            return txt

        return self._branch_table_core(Selector, CaseList, case_interval, 
                                       DefaultConsequence)

    def _branch_table_core(self, Selector, CaseList, get_case, DefaultConsequence=None):

        def get_content(C):
            if type(C) == list: return "".join(C)
            else:               return C

        def iterable(CaseList, DefaultConsequence):
            if not CaseList:
                yield None, DefaultConsequence
                return

            item, effect = CaseList[0]
            for item_ahead, effect_ahead in CaseList[1:]:
                if effect_ahead == effect: 
                    yield item, ""
                else:
                    yield item, effect
                item   = item_ahead
                effect = effect_ahead
            yield item, effect
            if DefaultConsequence is not None:
                yield None, DefaultConsequence

        # TODO: Express as 'CASE_SELECT'
        txt = [ "switch( %s ) {\n" % Selector ]
        txt.extend(
            flatten_list_of_lists(
                get_case(item, text, get_content)
                for item, text in iterable(CaseList, DefaultConsequence)
            )
        )
        txt.append("}\n")
        return txt

    def REPLACE_INDENT(self, txt_list, Start=0):
        for i, x in enumerate(islice(txt_list, Start, None), Start):
            if isinstance(x, int): txt_list[i] = "    " * x
        return txt_list

    def INDENT(self, txt_list, Add=1, Start=0):
        for i, x in enumerate(islice(txt_list, Start, None), Start):
            if isinstance(x, int): txt_list[i] += Add

    def GET_PLAIN_STRINGS(self, txt_list, dial_db):
        self.REPLACE_INDENT(txt_list)
        return get_plain_strings(txt_list, dial_db)

    def VARIABLE_DEFINITIONS(self, VariableDB):
        # ROBUSTNESS: Require 'target_state_index' and 'target_state_else_index'
        #             ALWAYS. Later, they are referenced in dead code to avoid
        #             warnings of unused variables.
        # BOTH: -- Used in QUEX_GOTO_STATE in case of no computed goto-s.
        #       -- During reload.
        VariableDB.require("target_state_index")
        VariableDB.require("target_state_else_index")

        assert type(VariableDB) != dict
        return templates._local_variable_definitions(VariableDB.get()) 

    def RAISE_ERROR_FLAG(self, Name):
        return "self.error_code_set_if_first(%s);\n" % Name

    def RAISE_ERROR_FLAG_BY_INCIDENCE_ID(self, IncidenceId):
        if not IncidenceId: return ""
        return self.RAISE_ERROR_FLAG(self.__error_code_db[IncidenceId][0])

    def RAISE_ERROR_FLAG_BY_TERMINAL_TYPE(self, TerminalType):
        incidence_id = standard_incidence_db_get_incidence_id(TerminalType)
        return self.RAISE_ERROR_FLAG_BY_INCIDENCE_ID(incidence_id)

    def EXIT_ON_MISSING_HANDLER(self, IncidenceId):
        return [
            self.RAISE_ERROR_FLAG(self.__error_code_db[IncidenceId][1]),
            "%s\n"  % self.TOKEN_SEND("QUEX_SETTING_TOKEN_ID_TERMINATION"),
            '%s;\n' % self.PURE_RETURN
        ]

    def suspicious_RETURN_in_event_handler(self, IncidenceId, EventHandlerTxt):
        if IncidenceId not in self.__error_code_db: return False
        return self.__re_RETURN.search(EventHandlerTxt) is not None

    def EXIT_ON_TERMINATION(self):
        # NOT: "Lng.PURE_RETURN" because the terminal end of stream 
        #      exits anyway immediately--after 'on_after_match'.
        return "%s\n" % self.TOKEN_SEND("QUEX_SETTING_TOKEN_ID_TERMINATION")

    def ON_BUFFER_BEFORE_CHANGE_default(self):
        return ""

    @typed(dial_db=DialDB)
    def RELOAD_PROCEDURE(self, ForwardF, dial_db, variable_db):
        assert self.__code_generation_reload_label is None

        if ForwardF:
            txt = cpp_reload_forward_str
        else:
            txt = cpp_reload_backward_str

        variable_db.require_registers([E_R.LoadResult])

        adr_bad_lexatom  = DoorID.incidence(E_IncidenceIDs.BAD_LEXATOM, dial_db).related_address
        adr_load_failure = DoorID.incidence(E_IncidenceIDs.LOAD_FAILURE, dial_db).related_address

        txt = blue_print(txt, [
            ("$$ON_BAD_LEXATOM$$",  self.LABEL_STR_BY_ADR(adr_bad_lexatom)),
            ("$$ON_LOAD_FAILURE$$", self.LABEL_STR_BY_ADR(adr_load_failure)),
            ("$$LOAD_RESULT$$",     self.REGISTER_NAME(E_R.LoadResult)),
            ("$$BUFFER_LOAD_FW$$",  self.NAME_IN_NAMESPACE_MAIN("Buffer_load_forward")),
            ("$$BUFFER_LOAD_BW$$",  self.NAME_IN_NAMESPACE_MAIN("Buffer_load_backward"))
        ])

        dial_db.mark_address_as_gotoed(adr_bad_lexatom)
        dial_db.mark_address_as_gotoed(adr_load_failure)

        return txt 

    def straighten_open_line_pragmas_new(self, Txt, FileName):
        if Txt is None: return None

        line_pragma_txt = self._SOURCE_REFERENCE_END().strip()

        new_content = []
        for line_n, line in enumerate(Txt.splitlines(), start=1):
            if line.strip() != line_pragma_txt:
                new_content.append(line)
            else:
                new_content.append(self.LINE_PRAGMA(FileName, line_n))
        return "\n".join(new_content)
        
    def straighten_open_line_pragmas(self, FileName):
        line_pragma_txt = self._SOURCE_REFERENCE_END().strip()

        new_content = []
        line_n      = 1 # NOT: 0!
        fh          = open_file_or_die(FileName)
        while 1 + 1 == 2:
            line = fh.readline()
            line_n += 1
            if not line: 
                break
            elif line.strip() != line_pragma_txt:
                new_content.append(line)
            else:
                line_n += 1
                new_content.append(self.LINE_PRAGMA(FileName, line_n))
        fh.close()
        write_safely_and_close(FileName, "".join(new_content))

    @typed(X=RouterContentElement, dial_db=DialDB)
    def position_and_goto(self, X, dial_db):
        """Generate code to (i) position the input pointer and
                            (ii) jump to terminal.
        """
        door_id = DoorID.incidence(X.acceptance_id, dial_db)
        dial_db.mark_address_as_gotoed(door_id.related_address)
        return [
           self.POSITIONING(X),
           self.GOTO(door_id, dial_db)
        ]

    def type_definitions(self, excluded=set()):
        if Setup._debug_QUEX_TYPE_LEXATOM_EXT: type_lexatom = "QUEX_TYPE_LEXATOM_EXT"
        else:                                  type_lexatom = Setup.lexatom.type

        token_descr = token_db.token_type_definition
        type_def_list = [
            ("lexatom_t",        type_lexatom),
            ("token_id_t",       token_descr.token_id_type),
            ("token_line_n_t",   token_descr.line_number_type.get_pure_text()),
            ("token_column_n_t", token_descr.column_number_type.get_pure_text()),
            ("acceptance_id_t",  "int"),
            ("indentation_t",    "int")
        ]

        if not blackboard.required_support_indentation_count():
            excluded.add("indentation_t")

        acn = Setup.analyzer_class_name
        if Setup._debug_QUEX_TYPE_LEXATOM_EXT:
            def_str =   "#ifndef    QUEX_TYPE_LEXATOM_EXT\n" \
                      + "#   define QUEX_TYPE_LEXATOM_EXT %s\n" % Setup.lexatom.type \
                      + "#endif\n"
        else:
            def_str =   "#ifdef     QUEX_TYPE_LEXATOM_EXT\n" \
                      + "#   error \"QUEX_TYPE_LEXATOM_EXT has been defined, but lexer was not generated with '--debug-QUEX_TYPE_LEXATOM_EXT'.\"\n" \
                      + "#endif\n"

        def_str += "\n".join("typedef %s %s_%s;" % (original, acn, customized_name) 
                             for customized_name, original in type_def_list 
                             if customized_name not in excluded)

        return self.FRAME_IN_NAMESPACE_MAIN(def_str)

    def FRAME_IN_NAMESPACE_MAIN(self, Code):
        return "QUEX_NAMESPACE_MAIN_OPEN\n%s\nQUEX_NAMESPACE_MAIN_CLOSE\n" % Code

    def adapt_to_configuration(self, Txt):
        if not Txt: return Txt

        # Types
        replacements = self.type_replacements()

        # Namespaces
        replacements.extend([
            ("QUEX_NAMESPACE_MAIN_OPEN",   self.NAMESPACE_OPEN(Setup.analyzer_name_space)),
            ("QUEX_NAMESPACE_MAIN_CLOSE",  self.NAMESPACE_CLOSE(Setup.analyzer_name_space)),
            ("QUEX_NAMESPACE_TOKEN_OPEN",  self.NAMESPACE_OPEN(Setup.token_class_name_space)),
            ("QUEX_NAMESPACE_TOKEN_CLOSE", self.NAMESPACE_CLOSE(Setup.token_class_name_space)),
            ("QUEX_NAMESPACE_QUEX_OPEN",   self.NAMESPACE_OPEN(Setup._quex_lib_name_space)),
            ("QUEX_NAMESPACE_QUEX_CLOSE",  self.NAMESPACE_CLOSE(Setup._quex_lib_name_space)),
        ])

        # Inline
        replacements.append(
            ("QUEX_INLINE", self.INLINE)
        )

        # TokenIds
        def tid(Name):
            return "%s%s" % (Setup.token_id_prefix, Name)

        replacements.extend([
            ("QUEX_SETTING_TOKEN_ID_UNINITIALIZED",  tid("UNINITIALIZED")),
            ("QUEX_SETTING_TOKEN_ID_TERMINATION",    tid("TERMINATION")),
            ("QUEX_SETTING_TOKEN_ID_INDENT",         tid("INDENT")),
            ("QUEX_SETTING_TOKEN_ID_DEDENT",         tid("DEDENT")),
            ("QUEX_SETTING_TOKEN_ID_NODENT",         tid("NODENT")),
        ])

        txt = blue_print(Txt, replacements, CommonStart="QUEX_")

        # txt = self.Match_QUEX_SETTING.sub(r"%s_SETTING_\1" % Setup.analyzer_class_name, txt)
        # txt = self.Match_QUEX_OPTION.sub(r"%s_OPTION_\1" % Setup.analyzer_class_name, txt)

        # QUEX_NAME
        txt = self.replace_naming(txt)

        # INCLUDE GUARDS
        txt = self.Match_QUEX_INCLUDE_GUARD_TOKEN.sub(r"QUEX_INCLUDE_GUARD_%s__TOKEN__\1" % Setup.token_class_name_safe, txt)
        txt = self.Match_QUEX_INCLUDE_GUARD_QUEX.sub(r"QUEX_INCLUDE_GUARD_%s__QUEX__\1"   % Setup._quex_lib_name_safe, txt)
        txt = self.Match_QUEX_INCLUDE_GUARD.sub(r"QUEX_INCLUDE_GUARD_%s__\1"              % Setup.analyzer_name_safe, txt)
        return txt

    def replace_naming(self, txt):
        def _replace(txt, re0, re1, Prefix, NameSpace):
            txt = re0.sub(r"%s\1" % self.name_spaced_prefix(Prefix), txt) 
            txt = re1.sub(r"%s\1" % self.name_spaced_prefix(Prefix, NameSpace), txt)
            return txt

        # Analyzer
        txt = _replace(txt, self.Match_QUEX_NAME, self.Match_QUEX_GNAME,
                       Setup.analyzer_class_name, Setup.analyzer_name_space)

        # Token
        txt = _replace(txt, self.Match_QUEX_NAME_TOKEN, self.Match_QUEX_GNAME_TOKEN,
                       Setup.token_class_name, Setup.token_class_name_space)

        # QuexLib
        txt = _replace(txt, self.Match_QUEX_NAME_LIB, self.Match_QUEX_GNAME_LIB,
                       Setup._quex_lib_prefix, Setup._quex_lib_name_space)

        return txt

    def name_spaced_prefix(self, Prefix, NameSpace=None):
        if Prefix: prefix = "%s_" % Prefix
        else:      prefix = ""
        
        return self.NAME_IN_NAMESPACE(prefix, NameSpace)

    def type_replacements(self, DirectF=False):
        if DirectF:
            token_descr = token_db.token_type_definition
            type_memento        = "(void*)"
            type_lexatom        = Setup.lexatom.type
            type_token_id       = token_descr.token_id_type
            type_token_line_n   = token_descr.line_number_type.get_pure_text()
            type_token_column_n = token_descr.column_number_type.get_pure_text()
            type_acceptance_id  = "int"
            type_indentation    = "int"
        else:
            acn = Setup.analyzer_class_name
            type_memento        = "%s_Memento" % acn
            type_lexatom        = "%s_lexatom_t" % acn
            type_token_id       = "%s_token_id_t" % acn
            type_token_line_n   = "%s_token_line_n_t" % acn
            type_token_column_n = "%s_token_column_n_t" % acn
            type_acceptance_id  = "%s_acceptance_id_t" % acn
            type_indentation    = "%s_indentation_t" % acn

        return [
             ("QUEX_TYPE_TOKEN",          self.NAME_IN_NAMESPACE(Setup.token_class_name, Setup.token_class_name_space)),
             ("QUEX_TYPE0_TOKEN",         Setup.token_class_name),
             ("QUEX_TYPE_ANALYZER",       self.NAME_IN_NAMESPACE(Setup.analyzer_class_name, Setup.analyzer_name_space)),
             ("QUEX_TYPE0_ANALYZER",      Setup.analyzer_class_name),
             ("QUEX_TYPE_MEMENTO",        self.NAME_IN_NAMESPACE("%s_Memento" % Setup.analyzer_class_name, Setup.analyzer_name_space)),
             ("QUEX_TYPE0_MEMENTO",       type_memento),
             ("QUEX_TYPE_LEXATOM",        type_lexatom),
             ("QUEX_TYPE_TOKEN_ID",       type_token_id),
             ("QUEX_TYPE_TOKEN_LINE_N",   type_token_line_n),
             ("QUEX_TYPE_TOKEN_COLUMN_N", type_token_column_n),
             ("QUEX_TYPE_ACCEPTANCE_ID",  type_acceptance_id),
             ("QUEX_TYPE_INDENTATION",    type_indentation),
        ]

implementation_headers_txt = """
$$HEADER$$
$$INC: analyzer/C-adaptions.h$$
$$INC: implementations.i$$

$$FOOTER$$
"""

cpp_reload_forward_str = """
    __quex_debug3("RELOAD_FORWARD: success->%i; failure->%i", 
                  (int)target_state_index, (int)target_state_else_index);
    __quex_assert(*(me->buffer._read_p) == QUEX_SETTING_BUFFER_LIMIT_CODE);
    
    __quex_debug_reload_before();                 
    /* Callbacks: 'on_buffer_before_change()' and 'on_buffer_overflow()'
     * are called during load process upon occurrence.                        */
    $$LOAD_RESULT$$ = $$BUFFER_LOAD_FW$$(&me->buffer, (QUEX_TYPE_LEXATOM**)position, PositionRegisterN);
    __quex_debug_reload_after($$LOAD_RESULT$$);

    switch( $$LOAD_RESULT$$ ) {
    case E_LoadResult_DONE:           QUEX_GOTO_STATE(target_state_index);      
    case E_LoadResult_NO_MORE_DATA:   QUEX_GOTO_STATE(target_state_else_index); 
    case E_LoadResult_ENCODING_ERROR: goto $$ON_BAD_LEXATOM$$;
    case E_LoadResult_OVERFLOW:       QUEX_NAME(MF_error_code_set_if_first)(me, E_Error_Buffer_Overflow_LexemeTooLong); RETURN;
    default:                          __quex_assert(false);
    }
"""

cpp_reload_backward_str = """
    __quex_debug3("RELOAD_BACKWARD: success->%i; failure->%i", 
                  (int)target_state_index, (int)target_state_else_index);
    __quex_assert(input == QUEX_SETTING_BUFFER_LIMIT_CODE);

    __quex_debug_reload_before();                 
    /* Callbacks: 'on_buffer_before_change()' and 'on_buffer_overflow()'
     * are called during load process upon occurrence.                        */
    $$LOAD_RESULT$$ = $$BUFFER_LOAD_BW$$(&me->buffer);
    __quex_debug_reload_after($$LOAD_RESULT$$);

    switch( $$LOAD_RESULT$$ ) {
    case E_LoadResult_DONE:           QUEX_GOTO_STATE(target_state_index);      
    case E_LoadResult_NO_MORE_DATA:   QUEX_GOTO_STATE(target_state_else_index); 
    case E_LoadResult_ENCODING_ERROR: goto $$ON_BAD_LEXATOM$$;
    case E_LoadResult_FAILURE:        QUEX_NAME(MF_error_code_set_if_first)(me, E_Error_OnLoadFailure); RETURN; 
    default:                          __quex_assert(false);
    }
"""

cpp_header_definition_str = """
$$INC: buffer/Buffer$$
$$INC: token/TokenQueue$$

#ifdef    CONTINUE
#   undef CONTINUE
#endif
#define   CONTINUE do { goto $$CONTINUE_WITH_ON_AFTER_MATCH$$; } while(0)

#ifdef    RETURN
#   undef RETURN
#endif
#define   RETURN   do { goto $$RETURN_WITH_ON_AFTER_MATCH$$; } while(0)
"""
