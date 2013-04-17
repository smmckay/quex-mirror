# PURPOSE: Providing a database for code generation in different programming languages.
#          A central object 'db' contains for each keyword, such as '$if' '$else' a correspondent
#          keyword or sequence that corresponds to it in the given language. Some code
#          elements are slighly more complicated. Therefore the db returns for some keywords
#          a function that generates the correspondent code fragment.
# 
# NOTE: The language of reference is C++. At the current state the python code generation 
#       is only suited for unit test of state transitions, no state machine code generation.
#       Basics for other languages are in place (VisualBasic, Perl, ...) but no action has been
#       taken to seriously implement them.
#
# AUTHOR: Frank-Rene Schaefer
# ABSOLUTELY NO WARRANTY
#########################################################################################################
import quex.engine.generator.languages.cpp       as     cpp
from   quex.engine.generator.languages.address   import get_address, \
                                                        db, \
                                                        get_label, \
                                                        get_plain_strings, \
                                                        Address
from   quex.blackboard                           import E_StateIndices,  \
                                                        E_AcceptanceIDs, \
                                                        E_InputActions,  \
                                                        E_TransitionN,   \
                                                        E_PreContextIDs
import quex.engine.analyzer.state.entry_action           as entry_action
from   quex.engine.analyzer.state.core                   import AnalyzerState
from   quex.engine.analyzer.mega_state.template.state    import TemplateState
from   quex.engine.analyzer.mega_state.path_walker.state import PathWalkerState
from   copy                                              import copy

from   itertools import islice
from   math      import log
import re

#________________________________________________________________________________
# C++
#    
CppBase = {
    "$class-member-def":   lambda TypeStr, MaxTypeNameL, VariableName, MaxVariableL:
                           "    %s%s %s;" % (TypeStr, " " * (MaxTypeNameL - len(TypeStr)), VariableName),
    "$indentation_add":          cpp.__indentation_add,
    "$indentation_check_space":  cpp.__indentation_check_whitespace,
    #
    "$analyzer-func":           cpp.__analyzer_function,
    "$terminal-code":           cpp.__terminal_states,      
    "$header-definitions":      cpp.__header_definitions,
    "$frame":                   cpp.__frame_of_all,
    "$code_base":               "/quex/code_base/",
    "$token-default-file":      "/token/CppDefault.qx",
    "$token_template_file":     "/token/TXT-Cpp",
    "$token_template_i_file":   "/token/TXT-Cpp.i",
    "$analyzer_template_file":  "/analyzer/TXT-Cpp",
    "$file_extension":          ".cpp",
}

class LanguageDB_Cpp(dict):
    def __init__(self, DB):      
        self.update(DB)
        self.__analyzer                                   = None
        self.__code_generation_switch_cases_add_statement = None
        self.__code_generation_reload_label               = None
        self.__code_generation_on_reload_fail_adr         = None
        self.__state_machine_identifier                   = None
        self.Match_goto                                   = re.compile("\\bgoto\\b")
        self.Match_QUEX_GOTO_RELOAD                       = re.compile("\\bQUEX_GOTO_RELOAD_")

    def register_analyzer(self, TheAnalyzer):
        self.__analyzer = TheAnalyzer

    def code_generation_switch_cases_add_statement(self, Value):
        assert Value is None or self.__code_generation_switch_cases_add_statement is None
        self.__code_generation_switch_cases_add_statement = Value

    def code_generation_reload_label_set(self, Value):
        assert Value is None or self.__code_generation_reload_label is None
        self.__code_generation_reload_label = Value

    def code_generation_on_reload_fail_adr_set(self, Value):
        assert Value is None or self.__code_generation_on_reload_fail_adr is None
        self.__code_generation_on_reload_fail_adr = Value

    def set_state_machine_identifier(self, SM_Id):
        self.__state_machine_identifier = SM_Id

    @property
    def analyzer(self):
        return self.__analyzer

    def _get_log2_if_power_of_2(self, X):
        if not isinstance(X, (int, long)):
            return None
        log2 = log(X)/log(2)
        if not log2.is_integer(): return None
        return log2
            
    def __getattr__(self, Attr): 
        # Thanks to Rami Al-Rfou' who mentioned that this is the only thing to 
        # be adapted to be compliant with current version of PyPy.
        try:             return self[Attr] 
        except KeyError: raise AttributeError

    RETURN                  = "return;"
    UNREACHABLE             = "__quex_assert_no_passage();"
    ELSE                    = "} else {\n"

    PATH_ITERATOR_INCREMENT  = "++(path_iterator);"
    BUFFER_LIMIT_CODE        = "QUEX_SETTING_BUFFER_LIMIT_CODE"
    STATE_LABEL_VOID         = "QUEX_GOTO_LABEL_VOID"
    COMMENT_DELIMITERS       = [["/*", "*/", ""], ["//", "\n", ""], ["\"", "\"", "\\\""]]
    def LEXEME_START_SET(self, PositionStorage=None):
        if PositionStorage is None: return "me->buffer._lexeme_start_p = me->buffer._input_p;"
        else:                       return "me->buffer._lexeme_start_p = %s;" % PositionStorage
    def LEXEME_LENGTH(self):
        return "((size_t)(me->buffer._input_p - me->buffer._lexeme_start_p))"
    def CHARACTER_BEGIN_P_SET(self):
        return "character_begin_p = me->buffer._input_p;\n"

    def INPUT_P(self):                             return "me->buffer._input_p"
    def INPUT_P_INCREMENT(self):                   return "++(me->buffer._input_p);"
    def INPUT_P_DECREMENT(self):                   return "--(me->buffer._input_p);"
    def INPUT_P_ADD(self, Offset):                 return "QUEX_NAME(Buffer_input_p_add_offset)(&me->buffer, %i);" % Offset
    def INPUT_P_TO_LEXEME_START(self):             return "me->buffer._input_p = me->buffer._lexeme_start_p;"
    def INPUT_P_TO_CHARACTER_BEGIN_P(self):        return "me->buffer._input_p = character_begin_p;"
    def LEXEME_START_TO_CHARACTER_BEGIN_P(self):   return "me->buffer._lexeme_start_p = character_begin_p;"
    def CHARACTER_BEGIN_P_TO_LEXEME_START_P(self): return "character_begin_p = me->buffer._lexeme_start_p;"
    def INPUT_P_DEREFERENCE(self, Offset=0): 
        if Offset == 0: return "*(me->buffer._input_p)"
        else:           return "QUEX_NAME(Buffer_input_get_offset)(&me->buffer, %i)" % Offset

    def NAMESPACE_OPEN(self, NameList):
        txt = ""
        i = -1
        for name in NameList:
            i += 1
            txt += "    " * i + "namespace %s {\n" % name
        return txt

    def NAMESPACE_CLOSE(self, NameList):
        txt = ""
        for name in NameList:
            txt += "} /* Closing Namespace '%s' */\n" % name
        return txt

    def NAMESPACE_REFERENCE(self, NameList):
        return reduce(lambda x, y: x + "::" + y, [""] + NameList) + "::"

    def COMMENT(self, txt, Comment):
        """Eliminated Comment Terminating character sequence from 'Comment'
           and comment it into a single line comment.
           For compatibility with C89, we use Slash-Star comments only, no '//'.
        """
        comment = Comment.replace("/*", "SLASH_STAR").replace("*/", "STAR_SLASH")
        txt.append("/* %s */\n" % comment)

    def ML_COMMENT(self, txt, Comment, IndentN=4):
        indent_str = " " * IndentN
        comment = Comment.replace("/*", "SLASH_STAR").replace("*/", "STAR_SLASH").replace("\n", "\n%s * " % indent_str)
        txt.append("%s/* %s\n%s */" % (indent_str, comment, indent_str))

    def COMMAND(self, EntryAction):
        if isinstance(EntryAction, entry_action.Accepter):
            else_str = ""
            txt      = []
            for element in EntryAction:
                if   element.pre_context_id == E_PreContextIDs.BEGIN_OF_LINE:
                    txt.append("    %sif( me->buffer._character_before_lexeme_start == '\\n' )" % else_str)
                elif element.pre_context_id != E_PreContextIDs.NONE:
                    txt.append("    %sif( pre_context_%i_fulfilled_f ) " % (else_str, element.pre_context_id))
                else:
                    txt.append("    %s" % else_str)
                txt.append("{ last_acceptance = %s; __quex_debug(\"last_acceptance = %s\\n\"); }\n" \
                           % (self.ACCEPTANCE(element.pattern_id), self.ACCEPTANCE(element.pattern_id)))
                else_str = "else "
            return "".join(txt)

        elif isinstance(EntryAction, entry_action.StoreInputPosition):
            # Assume that checking for the pre-context is just overhead that 
            # does not accelerate anything.
            if EntryAction.offset == 0:
                return "    position[%i] = me->buffer._input_p; __quex_debug(\"position[%i] = input_p;\\n\");\n" \
                       % (EntryAction.position_register, EntryAction.position_register)
            else:
                return "    position[%i] = me->buffer._input_p - %i; __quex_debug(\"position[%i] = input_p - %i;\\n\");\n" \
                       % (EntryAction.position_register, EntryAction.offset, EntryAction.offset)

        elif isinstance(EntryAction, entry_action.PreConditionOK):
            return   "    pre_context_%i_fulfilled_f = 1;\n"                         \
                   % EntryAction.pre_context_id                                      \
                   + "    __quex_debug(\"pre_context_%i_fulfilled_f = true\\n\");\n" \
                   % EntryAction.pre_context_id

        elif isinstance(EntryAction, entry_action.SetTemplateStateKey):
            return   "    state_key = %i;\n"                      \
                   % EntryAction.value                            \
                   + "    __quex_debug(\"state_key = %i\\n\");\n" \
                   % EntryAction.value

        elif isinstance(EntryAction, entry_action.SetPathIterator):
            offset_str = ""
            if EntryAction.offset != 0: offset_str = " + %i" % EntryAction.offset
            txt =   "    path_iterator  = path_walker_%i_path_%i%s;\n"                   \
                  % (EntryAction.path_walker_id, EntryAction.path_id, offset_str)        \
                  + "    __quex_debug(\"path_iterator = (Pathwalker: %i, Path: %i, Offset: %i)\\n\");\n" \
                  % (EntryAction.path_walker_id, EntryAction.path_id, EntryAction.offset)
            return txt

        else:
            assert False, "Unknown Entry Action"

    def ADDRESS_BY_DOOR_ID(self, DoorId):
        ## print "## %s --> %s" % (DoorId, get_address("$entry", DoorId, U=True, R=True))
        return get_address("$entry", DoorId, U=True, R=True)

    def ADDRESS(self, StateIndex, FromStateIndex):
        if self.__analyzer is None: 
            return self.ADDRESS_BY_DOOR_ID(entry_action.DoorID(StateIndex, None))

        if FromStateIndex is None:
            # Return the '0' Door, the door without actions
            return self.ADDRESS_BY_DOOR_ID(entry_action.DoorID(StateIndex, DoorIndex=0)) 

        door_id = self.__analyzer.state_db[StateIndex].entry.get_door_id(StateIndex, FromStateIndex)

        assert isinstance(door_id, entry_action.DoorID)

        return self.ADDRESS_BY_DOOR_ID(door_id)

    def ADDRESS_DROP_OUT(self, StateIndex):
        return get_address("$drop-out", StateIndex)

    def ADDRESS_ON_FAILURE(self, UsedF=False):
        return get_address("$terminal-FAILURE", Arg=self.__state_machine_identifier, U=UsedF)

    def __label_name(self, StateIndex, FromStateIndex):
        if StateIndex in E_StateIndices:
            assert StateIndex != E_StateIndices.DROP_OUT
            assert StateIndex != E_StateIndices.RELOAD_PROCEDURE
            return {
                E_StateIndices.END_OF_PRE_CONTEXT_CHECK:    "END_OF_PRE_CONTEXT_CHECK",
                E_StateIndices.ANALYZER_REENTRY:            "__REENTRY",
            }[StateIndex]

        return "_%i" % self.ADDRESS(StateIndex, FromStateIndex)

    def __label_name_by_door_id(self, DoorId):
        return "_%i" % self.ADDRESS_BY_DOOR_ID(DoorId)

    def LABEL(self, StateIndex, FromStateIndex=None, NewlineF=True):
        label = self.__label_name(StateIndex, FromStateIndex)
        if NewlineF: return label + ":\n"
        return label + ":"

    def LABEL_BY_ADDRESS(self, Address):
        if Address is None:
            return "QUEX_GOTO_LABEL_VOID"
        else:
            return "QUEX_LABEL(%i)" % Address

    def ADDRESS_LABEL(self, Address):
        return "_%i" % Address

    def LABEL_BY_DOOR_ID(self, DoorId):
        label = self.__label_name_by_door_id(DoorId)
        # if NewlineF: return label + ":\n"
        return label + ":"

    def LABEL_DROP_OUT(self, StateIndex):
        return "_%s:" % self.ADDRESS_DROP_OUT(StateIndex)

    def LABEL_ON_FAILURE(self):
        return "_%s:" % self.ADDRESS_ON_FAILURE()

    def LABEL_SHARED_ENTRY(self, TemplateIndex, EntryN=None):
        if EntryN is None: return "_%i_shared_entry:\n"    % TemplateIndex
        else:              return "_%i_shared_entry_%i:\n" % (TemplateIndex, EntryN)

    def LABEL_BACKWARD_INPUT_POSITION_DETECTOR(self, StateMachineID):
        return "%s:" % self.LABEL_NAME_BACKWARD_INPUT_POSITION_DETECTOR(StateMachineID) 

    def LABEL_NAME_BACKWARD_INPUT_POSITION_DETECTOR(self, StateMachineID):
        return "BIP_DETECTOR_%i" % StateMachineID

    def LABEL_NAME_BACKWARD_INPUT_POSITION_RETURN(self, StateMachineID):
        return "BIP_DETECTOR_%i_DONE" % StateMachineID

    def GOTO(self, TargetStateIndex, FromStateIndex=None):
        # Only for normal 'forward analysis' the from state is of interest.
        # Because, only during forward analysis some actions depend on the 
        # state from where we come.
        result = "goto %s;" % self.__label_name(TargetStateIndex, FromStateIndex)
        return result

    def GOTO_ADDRESS(self, Address):
        """Skippers and Indentation Counters circumvent the 'TransitionID -> DoorID'
        mapping. They rely on providing directly an address as target of the goto.
        """
        return "goto %s;" % self.ADDRESS_LABEL(Address)

    def GOTO_BY_VARIABLE(self, VariableName):
        return "QUEX_GOTO_STATE(%s);" % VariableName 

    def GOTO_BY_DOOR_ID(self, DoorId):
        # Only for normal 'forward analysis' the from state is of interest.
        # Because, only during forward analysis some actions depend on the 
        # state from where we come.
        result = "goto %s;" % self.__label_name_by_door_id(DoorId)
        return result

    def GOTO_DROP_OUT(self, StateIndex):
        return "goto %s;" % get_label("$drop-out", StateIndex, U=True, R=True)

    def GOTO_RELOAD(self, StateIndex, InitStateIndexF, EngineType):
        """On reload a special section is entered that tries to reload data. Reload
           has two possible results:
           
           -- Data has been loaded: Now, a new input character can be determined
              and the current transition map can be reentered. For convenience, 
              'RELOAD' expects to jump to right before the place where the input
              pointer is adapted.

           -- No data available to be loaded: Then the current state's drop-out
              section must be entered. The forward init state immediate jumps
              to 'end of stream'.

           Thus: The reload behavior can be determined based on **one** state index.
                 The related drop-out label can be determined here.
        """
        # 'DoorIndex == 0' is the entry into the state without any actions.
        on_success = get_address("$entry", entry_action.DoorID(StateIndex, DoorIndex=0), U=True)

        if self.__code_generation_on_reload_fail_adr is not None:
            on_fail = self.__code_generation_on_reload_fail_adr
        else:
            if InitStateIndexF and EngineType.is_FORWARD():
                on_fail = get_address("$terminal-EOF", U=True) 
            else:
                on_fail = get_address("$drop-out", StateIndex, U=True, R=True) 

        get_label("$state-router", U=True)            # Mark as 'referenced'

        reload_label = self.__code_generation_reload_label
        if self.__code_generation_reload_label is None:
            direction = EngineType.direction_str() 
            assert direction is not None
            reload_label = get_label("$reload-%s" % direction, U=True)   

        return "QUEX_GOTO_RELOAD(%s, %s, %s);" % (reload_label, on_success, on_fail)

    def GOTO_TERMINAL(self, AcceptanceID):
        if AcceptanceID == E_AcceptanceIDs.VOID: 
            return "QUEX_GOTO_TERMINAL(last_acceptance);"
        elif AcceptanceID == E_AcceptanceIDs.FAILURE:
            return "goto _%i; /* TERMINAL_FAILURE */" % self.ADDRESS_ON_FAILURE(UsedF=True)
        else:
            assert isinstance(AcceptanceID, (int, long))
            return "goto TERMINAL_%i;" % AcceptanceID

    def GOTO_SHARED_ENTRY(self, TemplateIndex, EntryN=None):
        if EntryN is None: return "goto _%i_shared_entry;"    % TemplateIndex
        else:              return "goto _%i_shared_entry_%i;" % (TemplateIndex, EntryN)

    def GRID_STEP(self, VariableName, TypeName, GridWidth, StepN=1, IfMacro=None):
        """A grid step is an addition which depends on the current value 
        of a variable. It sets the value to the next valid value on a grid
        with a given width. The general solution is 

                  x  = (x - x % GridWidth) # go back to last grid.
                  x += GridWidth           # go to next grid step.

        For 'GridWidth' as a power of '2' there is a slightly more
        efficient solution.
        """

        grid_with_str = self.VALUE_STRING(GridWidth)
        log2          = self._get_log2_if_power_of_2(GridWidth)
        if log2 is not None:
            # For k = a potentials of 2, the expression 'x - x % k' can be written as: x & ~mask(log2) !
            # Thus: x = x - x % k + k = x & mask + k
            mask = (1 << int(log2)) - 1
            cut_str = "%s &= ~ ((%s)0x%X)" \
                      % (VariableName, TypeName, mask)
        else:
            cut_str = "%s -= (%s %% (%s))" \
                      % (VariableName, VariableName, grid_with_str)

        add_str = "%s += %s" % (VariableName, self.MULTIPLY_WITH(grid_with_str, StepN))

        if IfMacro is None: 
            return [ cut_str, ";\n", 0, add_str, ";\n" ]
        else:               
            return [ "%s(%s);\n" % (IfMacro, cut_str), 0, "%s(%s);\n" % (IfMacro, add_str) ]

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

    def REFERENCE_P_COLUMN_ADD(self, txt, IteratorName, ColumnCountPerChunk): # , SubtractOneF=False):
        # if SubtractOneF: delta_str = "(%s - reference_p - 1)" % IteratorName
        delta_str = "(%s - reference_p)" % IteratorName         
        txt.append("__QUEX_IF_COUNT_COLUMNS_ADD((size_t)(%s));\n" \
                   % self.MULTIPLY_WITH(delta_str, ColumnCountPerChunk))

    def REFERENCE_P_RESET(self, txt, IteratorName, AddOneF=True):
        if AddOneF:
            txt.append("__QUEX_IF_COUNT_COLUMNS(reference_p = %s + 1);\n" % IteratorName)
        else:
            txt.append("__QUEX_IF_COUNT_COLUMNS(reference_p = %s);\n" % IteratorName)
    
    def MODE_GOTO(self, Mode):
        return "QUEX_NAME(enter_mode)(&self, &%s);" % Mode

    def MODE_GOSUB(self, Mode):
        return "QUEX_NAME(push_mode)(&self, &%s);" % Mode

    def MODE_GOUP(self):
        return "QUEX_NAME(pop_mode)(&self);"

    def ACCEPTANCE(self, AcceptanceID):
        if AcceptanceID == E_AcceptanceIDs.FAILURE: return "((QUEX_TYPE_ACCEPTANCE_ID)-1)"
        else:                                       return "%i" % AcceptanceID

    def IF(self, LValue, Operator, RValue, FirstF=True):
        if isinstance(RValue, (str,unicode)): test = "%s %s %s"   % (LValue, Operator, RValue)
        else:                                 test = "%s %s 0x%X" % (LValue, Operator, RValue)
        if FirstF: return "if( %s ) {\n"        % test
        else:      return "} else if( %s ) {\n" % test

    def END_IF(self, LastF=True):
        return { True: "}", False: "" }[LastF]

    def IF_INPUT(self, Condition, Value, FirstF=True):
        return self.IF("input", Condition, Value, FirstF)

    def IF_PRE_CONTEXT(self, txt, FirstF, PreContextID, Consequence):

        if PreContextID == E_PreContextIDs.NONE:
            if FirstF: opening = [];           indent = 0; closing = []
            else:      opening = ["else {\n"]; indent = 1; closing = [1, "}\n"]
        else:
            condition = self.PRE_CONTEXT_CONDITION(PreContextID) 
            indent  = 0
            if FirstF: opening = ["if( %s ) {\n" % condition]
            else:      opening = ["else if( %s ) {\n" % condition]
            closing = [0, "}\n"]

        txt.extend(opening)
        txt.append(indent)
        if isinstance(Consequence, (str, unicode)): txt.append(Consequence)
        else:                                       txt.extend(Consequence)
        txt.extend(closing)
        return

    def PRE_CONTEXT_CONDITION(self, PreContextID):
        if PreContextID == E_PreContextIDs.BEGIN_OF_LINE: 
            return "me->buffer._character_before_lexeme_start == '\\n'"
        elif PreContextID == E_PreContextIDs.NONE:
            return "true"
        elif isinstance(PreContextID, (int, long)):
            return "pre_context_%i_fulfilled_f" % PreContextID
        else:
            assert False

    def ASSIGN(self, X, Y):
        return "%s = %s;" % (X, Y)

    def ACCESS_INPUT(self, txt=None, InputAction=E_InputActions.DEREF, Indent=0):
        code = {
            E_InputActions.DEREF:                ["%s\n" % self.ASSIGN("input", self.INPUT_P_DEREFERENCE())],

            E_InputActions.INCREMENT:            ["%s\n" % self.INPUT_P_INCREMENT()],
            
            E_InputActions.INCREMENT_THEN_DEREF: [        "%s\n" % self.INPUT_P_INCREMENT(),
                                                  Indent, "%s\n" % self.ASSIGN("input", self.INPUT_P_DEREFERENCE())], 
            
            E_InputActions.DECREMENT:            ["%s\n" % self.INPUT_P_DECREMENT()], 
            
            E_InputActions.DECREMENT_THEN_DEREF: [        "%s\n" % self.INPUT_P_DECREMENT(),
                                                  Indent, "%s\n" % self.ASSIGN("input", self.INPUT_P_DEREFERENCE())], 
        }[InputAction]

        if txt is None: return "".join(code)

        txt.extend(code)

    def STATE_ENTRY(self, txt, TheState, FromStateIndex=None, NewlineF=True, BIPD_ID=None):
        label = None
        if    TheState.init_state_f \
          and TheState.engine_type.is_BACKWARD_INPUT_POSITION():
            label = "%s:\n" % self.LABEL_NAME_BACKWARD_INPUT_POSITION_DETECTOR(BIPD_ID) 
        else:
            index = TheState.index

        if label is None: label = self.LABEL(index, FromStateIndex, NewlineF)
        txt.append(label)

    def STATE_DEBUG_INFO(self, txt, TheState):
        if isinstance(TheState, TemplateState):
            txt.append("__quex_debug_template_state(%i, state_key);\n" \
                       % TheState.index)
        elif isinstance(TheState, PathWalkerState):
            txt.append("__quex_debug_path_walker_state(%i, path_walker_%s_path_base, path_iterator);\n" \
                       % (TheState.index, TheState.index))
        else:
            assert isinstance(TheState, AnalyzerState)
            if TheState.init_state_forward_f: 
                txt.append("__quex_debug(\"Init State\\n\");\n")
                txt.append(1)
            txt.append("__quex_debug_state(%i);\n" % TheState.index)
        return 

    def POSITION_REGISTER(self, Index):
        return "position[%i]" % Index

    def POSITIONING(self, Positioning, Register):
        if   Positioning == E_TransitionN.VOID: 
            return   "__quex_assert(position[%i] != 0x0);\n" % Register \
                   + "me->buffer._input_p = position[%i];\n" % Register
        # "_input_p = lexeme_start_p + 1" is done by TERMINAL_FAILURE. 
        elif Positioning == E_TransitionN.LEXEME_START_PLUS_ONE: 
            return ""
        elif Positioning > 0:     
            return "me->buffer._input_p -= %i; " % Positioning
        elif Positioning == 0:    
            return ""
        else:
            assert False 

    def SELECTION(self, Selector, CaseList, CaseFormat="hex"):

        def __case(txt, item, Content=""):
            def format(N):
                return {"hex": "case 0x%X: ", 
                        "dec": "case %i: "}[CaseFormat] % N

            if isinstance(item, list):        
                for elm in item[:-1]:
                    txt.append(1) # 1 indentation
                    txt.append("%s\n" % format(elm))
                txt.append(1) # 1 indentation
                txt.append(format(item[-1]))

            elif isinstance(item, (int, long)): 
                txt.append(1) # 1 indentation
                txt.append(format(item))

            else: 
                txt.append(1) # 1 indentation
                txt.append("case %s: "  % item)

            if type(Content) == list: txt.extend(Content)
            elif len(Content) != 0:   txt.append(Content)

            if      self.__code_generation_switch_cases_add_statement is not None \
                and self.Match_goto.search(txt[-1]) is None                       \
                and self.Match_QUEX_GOTO_RELOAD.search(txt[-1]) is None:
                txt.append(1)
                txt.append(self.__code_generation_switch_cases_add_statement)
            txt.append("\n")

        txt = [ 0, "switch( %s ) {\n" % Selector ]

        item, consequence = CaseList[0]
        for item_ahead, consequence_ahead in CaseList[1:]:
            if consequence_ahead == consequence: __case(txt, item)
            else:                                __case(txt, item, consequence)
            item        = item_ahead
            consequence = consequence_ahead

        __case(txt, item, consequence)

        txt.append("\n")
        txt.append(0)       # 0 indentation
        txt.append("}")
        return txt

    def REPLACE_INDENT(self, txt_list, Start=0):
        for i, x in enumerate(islice(txt_list, Start, None), Start):
            if isinstance(x, int): txt_list[i] = "    " * x
        return txt_list

    def INDENT(self, txt_list, Add=1, Start=0):
        for i, x in enumerate(islice(txt_list, Start, None), Start):
            if isinstance(x, int): txt_list[i] += Add

    def GET_PLAIN_STRINGS(self, txt_list):
        self.REPLACE_INDENT(txt_list)
        return get_plain_strings(txt_list)

    def VARIABLE_DEFINITIONS(self, VariableDB):
        assert type(VariableDB) != dict
        return cpp._local_variable_definitions(VariableDB.get()) 

    def RELOAD_SPECIAL(self, BeforeReloadAction, AfterReloadAction):
        assert self.__code_generation_reload_label is not None
        assert type(BeforeReloadAction) == list
        assert type(AfterReloadAction) == list

        result = [ 
           cpp_reload_forward_str[0],
           "%s:\n" % self.__code_generation_reload_label,
           cpp_reload_forward_str[1],
        ]
        result.extend(BeforeReloadAction)
        result.append(cpp_reload_forward_str[2])
        result.extend(AfterReloadAction)
        result.append(cpp_reload_forward_str[3])

        return result

    def RELOAD(self):
        assert self.__code_generation_reload_label is None
        forward_str = "".join([
            cpp_reload_forward_str[0],
            "__RELOAD_FORWARD:\n",
            cpp_reload_forward_str[1],
            cpp_reload_forward_str[2],
            cpp_reload_forward_str[3],
        ])

        txt = [
            Address("$reload-FORWARD",  None, forward_str),
            Address("$reload-BACKWARD", None, cpp_reload_backward_str)
        ]
        return txt

cpp_reload_forward_str = ["""
    __quex_assert_no_passage();
""",
"""
    __quex_debug1("__RELOAD_FORWARD");
    __quex_assert(*(me->buffer._input_p) == QUEX_SETTING_BUFFER_LIMIT_CODE);
    if( me->buffer._memory._end_of_file_p == 0x0 ) {
""",
"""
        __quex_debug_reload_before(); /* Leave macro here to report source position. */
        QUEX_NAME(buffer_reload_forward)(&me->buffer, (QUEX_TYPE_CHARACTER_POSITION*)position, PositionRegisterN);
""",
"""
        __quex_debug_reload_after();
        QUEX_GOTO_STATE(target_state_index);
    }
    __quex_debug("reload impossible\\n");
    QUEX_GOTO_STATE(target_state_else_index);
"""]

cpp_reload_backward_str = """
    __quex_assert_no_passage();
__RELOAD_BACKWARD:
    __quex_debug1("__RELOAD_BACKWARD");
    __quex_assert(input == QUEX_SETTING_BUFFER_LIMIT_CODE);
    if( QUEX_NAME(Buffer_is_begin_of_file)(&me->buffer) == false ) {
        __quex_debug_reload_before(); /* Leave macro here to report source position. */
        QUEX_NAME(buffer_reload_backward)(&me->buffer);
        __quex_debug_reload_after();
        QUEX_GOTO_STATE(target_state_index);
    }
    __quex_debug("reload impossible\\n");
    QUEX_GOTO_STATE(target_state_else_index);
"""

db["C++"] = LanguageDB_Cpp(CppBase)

#________________________________________________________________________________
# C
#    
class LanguageDB_C(LanguageDB_Cpp):
    def __init__(self, DB):      
        LanguageDB_Cpp.__init__(self, DB)
    def NAMESPACE_REFERENCE(self, NameList):
        return "".join("%s_" % name for name in NameList)

db["C"] = LanguageDB_C(CppBase)
db["C"].update([
    ("$token-default-file", "/token/CDefault.qx"),
    ("$token_template_file",    "/token/TXT-C"),
    ("$token_template_i_file",  "/token/TXT-C.i"),
    ("$analyzer_template_file", "/analyzer/TXT-C"),
    ("$file_extension",         ".c")
])

#________________________________________________________________________________
# Perl
#    
db["Perl"] = {
}

#________________________________________________________________________________
# Python
#    
db["Python"] = {
}

#________________________________________________________________________________
# Visual Basic 6
#    
db["VisualBasic6"] = {
    }

db["DOT"] = copy(db["C++"])
db["C"].update([
    ("$token-default-file", "/token/CDefault.qx"),
    ("$token_template_file",    "/token/TXT-C"),
    ("$token_template_i_file",  "/token/TXT-C.i"),
    ("$analyzer_template_file", "/analyzer/TXT-C"),
    ("$file_extension",         ".c"),
    ("$comment-delimiters", [["/*", "*/", ""], ["//", "\n", ""], ["\"", "\"", "\\\""]]),
])
