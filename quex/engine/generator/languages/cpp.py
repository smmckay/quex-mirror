from   quex.engine.misc.string_handling           import blue_print
from   quex.engine.analyzer.door_id_address_label import Label, \
                                                         DoorID, \
                                                         dial_db, \
                                                         IfDoorIdReferencedCode, \
                                                         IfDoorIdReferencedLabel
from   quex.engine.interval_handling              import NumberSet
from   quex.blackboard import E_IncidenceIDs
from   operator import itemgetter
from   copy     import copy
#

def __nice(SM_ID): 
    return repr(SM_ID).replace("L", "")

#________________________________________________________________________________
# C++
#

def _local_variable_definitions(VariableDB):
    if len(VariableDB) == 0: return ""

    def __group_by_condition(VariableDB):
        result = {}
        for variable in VariableDB.itervalues():

            variable_list = result.get(variable.condition)
            if variable_list is None: 
                variable_list              = [[], []]
                result[variable.condition] = variable_list

            if not variable.condition_negated_f: variable_list[0].append(variable)
            else:                                variable_list[1].append(variable)

        return result

    def __code(txt, variable):
        variable_type = variable.variable_type
        variable_init = variable.initial_value
        variable_name = variable.name

        if variable.element_n is not None: 
            if variable.element_n != 0:
                variable_name += "[%s]" % repr(variable.element_n)
                if variable_type.find("QUEX_TYPE_GOTO_LABEL") != -1: 
                    variable_name = "(" + variable_name + ")"
            else:
                variable_type += "*"
                variable_init  = ["0x0"]

        if variable_init is None: 
            value = ["/* un-initilized */"]
        else:
            if type(variable_init) != list: variable_init = [ variable_init ]
            value = [" = "] + variable_init

        txt.append("    %s%s %s%s" % \
                   (variable_type, 
                    " " * (30-len(variable_type)), variable_name, 
                    " " * (30 - len(variable_name))))
        txt.extend(value)
        txt.append(";\n")

    # L   = max(map(lambda info: len(info[0]), VariableDB.keys()))
    txt       = []
    for raw_name, variable in sorted(VariableDB.items()):
        if variable.priority_f == False: continue

        if variable.condition is not None:
            if variable.condition_negated_f == False: 
                txt.append("#   ifdef %s\n"  % variable.condition)
            else:
                txt.append("#   ifndef %s\n" %  variable.condition)

        __code(txt, variable)

        if variable.condition is not None:
            txt.append("#   endif /* %s */\n" % variable.condition)

        del VariableDB[variable.name]

    grouped_variable_list = __group_by_condition(VariableDB)
    unconditioned_name_set = set([])
    for condition, groups in sorted(grouped_variable_list.iteritems()):
        if condition is not None: continue
        for variable in groups[0]:
            unconditioned_name_set.add(variable.name)

    for condition, groups in sorted(grouped_variable_list.iteritems()):

        condition_group, negated_condition_group = groups

        if condition is None:
            for variable in condition_group:
                __code(txt, variable)
        else:
            if len(condition_group) != 0:
                txt.append("#   ifdef %s\n"  % condition)

                for variable in condition_group:
                    if variable.name in unconditioned_name_set: continue
                    __code(txt, variable)

            if len(negated_condition_group) != 0:
                if len(condition_group) != 0: txt.append("#   else /* not %s */\n" % condition)
                else:                         txt.append("#   ifndef %s\n"         % condition)

                for variable in negated_condition_group:
                    if variable.name in unconditioned_name_set: continue
                    __code(txt, variable)

            txt.append("#   endif /* %s */\n" % condition)
            
    return txt
         
__function_signature = """
#include <quex/code_base/temporary_macros_on>

__QUEX_TYPE_ANALYZER_RETURN_VALUE  
QUEX_NAME($$STATE_MACHINE_NAME$$_analyzer_function)(QUEX_TYPE_ANALYZER* me) 
{
    /* NOTE: Different modes correspond to different analyzer functions. The 
     *       analyzer functions are all located inside the main class as static
     *       functions. That means, they are something like 'globals'. They 
     *       receive a pointer to the lexical analyzer, since static members do
     *       not have access to the 'this' pointer.                          */
#   if defined(QUEX_OPTION_TOKEN_POLICY_SINGLE)
    register QUEX_TYPE_TOKEN_ID __self_result_token_id 
           = (QUEX_TYPE_TOKEN_ID)__QUEX_SETTING_TOKEN_ID_UNINITIALIZED;
#   endif
#   ifdef     self
#       undef self
#   endif
#   define self (*((QUEX_TYPE_ANALYZER*)me))
#   define QUEX_LABEL_STATE_ROUTER $$LABEL_STATE_ROUTER$$ /* Required by QUEX_GOTO_STATE */
"""

comment_on_post_context_position_init_str = """
    /* Post context positions do not have to be reset or initialized. If a state
     * is reached which is associated with 'end of post context' it is clear what
     * post context is meant. This results from the ways the state machine is 
     * constructed. Post context position's live cycle:
     *
     * (1)   unitialized (don't care)
     * (1.b) on buffer reload it may, or may not be adapted (don't care)
     * (2)   when a post context begin state is passed, then it is **SET** (now: take care)
     * (2.b) on buffer reload it **is adapted**.
     * (3)   when a terminal state of the post context is reached (which can only be reached
     *       for that particular post context), then the post context position is used
     *       to reset the input position.                                              */
"""

def __analyzer_function(StateMachineName, Setup,
                        variable_definitions, function_body, ModeNameList=[]):
    """EngineClassName = name of the structure that contains the engine state.
                         if a mode of a complete quex environment is created, this
                         is the mode name. otherwise, any name can be chosen. 
       SingleModeAnalyzerF = False if a mode for a quex engine is to be created. True
                           if a stand-alone lexical engine is required (without the
                           complete mode-handling framework of quex).
    """              
    Lng = Setup.language_db
    SingleModeAnalyzerF = Setup.single_mode_analyzer_f

    txt = [blue_print(__function_signature, [
        ("$$STATE_MACHINE_NAME$$", StateMachineName),
        ("$$LABEL_STATE_ROUTER$$", Label.global_state_router()),
    ])]
    txt.extend(variable_definitions)

    if len(ModeNameList) != 0 and not SingleModeAnalyzerF: 
        L = max(map(lambda name: len(name), ModeNameList))
        for name in ModeNameList:
            txt.append("#   define %s%s    (QUEX_NAME(%s))\n" % (name, " " * (L- len(name)), name))

    txt.extend([
        comment_on_post_context_position_init_str,
        "#   if    defined(QUEX_OPTION_AUTOMATIC_ANALYSIS_CONTINUATION_ON_MODE_CHANGE) \\\n",
        "       || defined(QUEX_OPTION_ASSERTS)\n",
        "    me->DEBUG_analyzer_function_at_entry = me->current_analyzer_function;\n",
        "#   endif\n",
    ])

    txt.append("%s:\n" % Label.global_reentry())

    # -- entry to the actual function body
    txt.append("    %s\n" % Lng.LEXEME_START_SET())
    txt.append("    QUEX_LEXEME_TERMINATING_ZERO_UNDO(&me->buffer);\n")
    
    txt.extend(function_body)

    # -- prevent the warning 'unused variable'
    txt.append( 
        "\n"                                                                                              \
        "    /* Prevent compiler warning 'unused variable': use variables once in a part of the code*/\n" \
        "    /* that is never reached (and deleted by the compiler anyway).*/\n")

    # Mode Names are defined as macros, so the following is not necessary.
    # for mode_name in ModeNameList:
    #    txt.append("    (void)%s;\n" % mode_name)
    txt.append(                                                             \
        "    (void)QUEX_LEXEME_NULL;\n"                                     \
        "    (void)QUEX_NAME_TOKEN(DumpedTokenIdObject);\n"                 \
        "    QUEX_ERROR_EXIT(\"Unreachable code has been reached.\\n\");\n") 

    ## This was once we did not know ... if there was a goto to the initial state or not.
    ## txt += "        goto %s;\n" % label.get(StateMachineName, InitialStateIndex)
    if len(ModeNameList) != 0 and not SingleModeAnalyzerF: 
        L = max(map(lambda name: len(name), ModeNameList))
        for name in ModeNameList:
            txt.append("#   undef %s\n" % name)

    txt.append("#   undef self\n")
    txt.append("#   undef QUEX_LABEL_STATE_ROUTER\n")
    txt.append("}\n")

    txt.append("#include <quex/code_base/temporary_macros_off>\n")
    return txt

__terminal_state_prolog  = """
    /* (*) Terminal states _______________________________________________________
     *
     * States that implement actions of the 'winner patterns.                     */
"""

__lexeme_macro_setup = """
    /* Lexeme setup: 
     *
     * There is a temporary zero stored at the end of each lexeme, if the action 
     * references to the 'Lexeme'. 'LexemeNull' provides a reference to an empty
     * zero terminated string.                                                    */
#if defined(QUEX_OPTION_ASSERTS)
#   define Lexeme       QUEX_NAME(access_Lexeme)((const char*)__FILE__, (size_t)__LINE__, &me->buffer)
#   define LexemeBegin  QUEX_NAME(access_LexemeBegin)((const char*)__FILE__, (size_t)__LINE__, &me->buffer)
#   define LexemeL      QUEX_NAME(access_LexemeL)((const char*)__FILE__, (size_t)__LINE__, &me->buffer)
#   define LexemeEnd    QUEX_NAME(access_LexemeEnd)((const char*)__FILE__, (size_t)__LINE__, &me->buffer)
#else
#   define Lexeme       (me->buffer._lexeme_start_p)
#   define LexemeBegin  Lexeme
#   define LexemeL      $$LEXEME_LENGTH$$
#   define LexemeEnd    $$INPUT_P$$
#endif

#define LexemeNull      (&QUEX_LEXEME_NULL)
"""

__lexeme_macro_clean_up = """
#   undef Lexeme
#   undef LexemeBegin
#   undef LexemeEnd
#   undef LexemeNull
#   undef LexemeL
"""

__return_if_queue_full_or_simple_analyzer = """
#   ifndef __QUEX_OPTION_PLAIN_ANALYZER_OBJECT
#   ifdef  QUEX_OPTION_TOKEN_POLICY_QUEUE
    if( QUEX_NAME(TokenQueue_is_full)(&self._token_queue) ) {
        return;
    }
#   else
    if( self_token_get_id() != __QUEX_SETTING_TOKEN_ID_UNINITIALIZED) {
        return __self_result_token_id;
    }
#   endif
#   endif
"""
__return_if_mode_changed = """
    /*  If a mode change happened, then the function must first return and
     *  indicate that another mode function is to be called. At this point, 
     *  we to force a 'return' on a mode change. 
     *
     *  Pseudo Code: if( previous_mode != current_mode ) {
     *                   return 0;
     *               }
     *
     *  When the analyzer returns, the caller function has to watch if a mode 
     *  change occurred. If not it can call this function again.             */
#   if    defined(QUEX_OPTION_AUTOMATIC_ANALYSIS_CONTINUATION_ON_MODE_CHANGE) \
       || defined(QUEX_OPTION_ASSERTS)
    if( me->DEBUG_analyzer_function_at_entry != me->current_analyzer_function ) 
#   endif
    { 
#       if defined(QUEX_OPTION_AUTOMATIC_ANALYSIS_CONTINUATION_ON_MODE_CHANGE)
        self_token_set_id(__QUEX_SETTING_TOKEN_ID_UNINITIALIZED);
        __QUEX_PURE_RETURN;
#       elif defined(QUEX_OPTION_ASSERTS)
        QUEX_ERROR_EXIT("Mode change without immediate return from the lexical analyzer.");
#       endif
    }
"""

def lexeme_macro_definitions(Setup):
    
    lexeme_null_object_name = "QUEX_NAME(LexemeNullObject)"
    if Setup.external_lexeme_null_object != "":
        lexeme_null_object_name = Setup.external_lexeme_null_object

    txt = [ __terminal_state_prolog ]

    txt.append(blue_print(__lexeme_macro_setup, [
          ["$$LEXEME_LENGTH$$",      Setup.language_db.LEXEME_LENGTH()],
          ["$$INPUT_P$$",            Setup.language_db.INPUT_P()],
          ["$$LEXEME_NULL_OBJECT$$", lexeme_null_object_name],
    ]))

    return "".join(txt)

def reentry_preparation(Lng, PreConditionIDList, OnAfterMatchTerminal):
    TerminalFailureRef = "QUEX_LABEL(%i)" % dial_db.get_address_by_door_id(DoorID.incidence(E_IncidenceIDs.MATCH_FAILURE))
    """Reentry preperation (without returning from the function."""
    # (*) Unset all pre-context flags which may have possibly been set
    if PreConditionIDList is None:
        unset_pre_context_flags_str = ""
    else:
        unset_pre_context_flags_str = "".join([
            "    " + Lng.ASSIGN("pre_context_%s_fulfilled_f" % __nice(pre_context_id), 0)
            for pre_context_id in PreConditionIDList
        ])

    if OnAfterMatchTerminal is not None:
        on_after_match_str = OnAfterMatchTerminal.code()
    else:
        on_after_match_str = ""

    txt = [ 
        "\n",
        "%s:"  % Label.return_with_on_after_match(), 
        "/* RETURN -- after executing 'on_after_match' code. */\n",
        on_after_match_str,
        "    __QUEX_PURE_RETURN;\n",
        "\n",
        "%s:" % Label.continue_with_on_after_match(), 
        "/* CONTINUE -- after executing 'on_after_match' code. */\n",
        on_after_match_str,
        "%s:" % Label.continue_without_on_after_match(),
        "/* CONTINUE -- without executing 'on_after_match' (e.g. on FAILURE). */\n",
        "\n",
        __return_if_queue_full_or_simple_analyzer,
        "\n",
        __return_if_mode_changed,
        "\n",
        unset_pre_context_flags_str,
        "\n",
        "%s\n" % Lng.GOTO_BY_DOOR_ID(DoorID.global_reentry()), 
        "\n",
        "/* Avoid compiler warnings 'unreferenced label'. */\n",
        # 'return_with_on_after_match', 'continue_with_on_after_match' and
        # 'continue_with_on_after_match' need to be implemented always, because
        # they are possibly used in macros. We cannot determine whether macros
        # are used or not. 
        Lng.UNREACHABLE_BEGIN(),
        Lng.GOTO_BY_DOOR_ID(DoorID.return_with_on_after_match()),
        Lng.GOTO_BY_DOOR_ID(DoorID.continue_with_on_after_match()),
        Lng.GOTO_BY_DOOR_ID(DoorID.continue_without_on_after_match()),
        Lng.UNREACHABLE_END(),
        "\n",
        __lexeme_macro_clean_up,
    ]

    return txt

def __frame_of_all(Code, Setup):
    # namespace_ref   = Lng.NAMESPACE_REFERENCE(Setup.analyzer_name_space)
    # if len(namespace_ref) > 2 and namespace_ref[:2] == "::":  namespace_ref = namespace_ref[2:]
    # if len(namespace_ref) > 2 and namespace_ref[-2:] == "::": namespace_ref = namespace_ref[:-2]
    # "using namespace " + namespace_ref + ";\n"       + \

    implementation_header_str = ""
    if Setup.language == "C":
        implementation_header_str += "#if defined(__QUEX_OPTION_CONVERTER_HELPER)\n"
        implementation_header_str += "#   include \"%s\"\n" % Setup.get_file_reference(Setup.output_buffer_codec_header_i)
        implementation_header_str += "#endif\n"
        implementation_header_str += "#include <quex/code_base/analyzer/headers.i>\n"
        implementation_header_str += "#include <quex/code_base/analyzer/C-adaptions.h>\n"

    lexeme_null_definition = ""
    if Setup.external_lexeme_null_object == "":
        # LexemeNull has been defined elsewhere.
        lexeme_null_definition = "QUEX_TYPE_CHARACTER  QUEX_LEXEME_NULL_IN_ITS_NAMESPACE = (QUEX_TYPE_CHARACTER)0;\n"

    return "".join(["/* #include \"%s\"*/\n" % Setup.get_file_reference(Setup.output_header_file),
                    implementation_header_str,
                    "QUEX_NAMESPACE_MAIN_OPEN\n",
                    lexeme_null_definition,
                    Code,
                    "QUEX_NAMESPACE_MAIN_CLOSE\n"])                     

def __get_if_in_character_set(ValueList):
    assert type(ValueList) == list
    assert len(ValueList) > 0
    txt = "if( "
    for value in ValueList:
        txt += "input == %i || " % value

    txt = txt[:-3] + ") {\n"
    return txt

def __get_if_in_interval(TriggerSet):
    assert TriggerSet.__class__.__name__ == "Interval"
    assert TriggerSet.size() >= 2

    if TriggerSet.size() == 2:
        return "if( input == %i || input == %i ) {\n" % (TriggerSet.begin, TriggerSet.end - 1)
    else:
        return "if( input >= %i && input < %i ) {\n" % (TriggerSet.begin, TriggerSet.end)

def __condition(txt, CharSet):
    first_f = True
    for interval in CharSet.get_intervals(PromiseToTreatWellF=True):
        if first_f: first_f = False
        else:       txt.append(" || ")

        if interval.end - interval.begin == 1:
            txt.append("(C) == 0x%X"                % interval.begin)
        elif interval.end - interval.begin == 2:
            txt.append("(C) == 0x%X || (C) == 0x%X" % (interval.begin, interval.end - 1))
        else:
            txt.append("(C) <= 0x%X && (C) < 0x%X" % (interval.begin, interval.end))

def __indentation_add(Info):
    # (0) If all involved counts are single spaces, the 'counting' can be done
    #     easily by subtracting 'end - begin', no adaption.
    indent_txt = " " * 16
    if Info.homogeneous_spaces():
        return ""

    def __do(txt, CharSet, Operation):
        txt.append(indent_txt + "if( ")
        __condition(txt, CharSet)
        txt.append(" ) { ")
        txt.append(Operation)
        txt.append(" }\\\n")

    txt       = []
    spaces_db = {} # Sort same space counts together
    grid_db   = {} # Sort same grid counts together
    for name, count_parameter in Info.count_db.items():
        count         = count_parameter.get()
        character_set = Info.character_set_db[name].get()
        if count == "bad": continue
        # grid counts are indicated by negative integer for count.
        if count >= 0:
            spaces_db.setdefault(count, NumberSet()).unite_with(character_set)
        else:
            grid_db.setdefault(count, NumberSet()).unite_with(character_set)

    for count, character_set in spaces_db.items():
        __do(txt, character_set, "(I) += %i;" % count)

    for count, character_set in grid_db.items():
        __do(txt, character_set, "(I) += (%i - ((I) %% %i));" % (abs(count), abs(count)))

    return "".join(txt)

def __indentation_check_whitespace(Info):
    all_character_list = map(lambda x: x.get(), Info.character_set_db.values())
    assert len(all_character_list) != 0

    number_set = all_character_list[0]
    for character_set in all_character_list[1:]:
        number_set.unite_with(character_set)

    txt = []
    __condition(txt, number_set)
    return "".join(txt)

def __get_switch_block(VariableName, CaseCodePairList):
    txt = [0, "switch( %s ) {\n" % VariableName]
    next_i = 0
    L = len(CaseCodePairList)
    CaseCodePairList.sort(key=itemgetter(0))
    for case, code in CaseCodePairList: 
        next_i += 1
        txt.append(1)
        case_label = "0x%X" % case
        if next_i != L and CaseCodePairList[next_i][1] == code:
            txt.append("case %s: %s\n" % (case_label, " " * (7 - len(case_label))))
        else:
            txt.append("case %s: %s" % (case_label, " " * (7 - len(case_label))))
            if type(code) == list: txt.extend(code)
            else:                  txt.append(code)
            txt.append("\n")
            
    txt.append(0)
    txt.append("}\n")
    return txt


