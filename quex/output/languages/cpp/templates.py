from   quex.engine.analyzer.door_id_address_label import DoorID, DialDB
from   quex.engine.misc.tools                     import typed


def __nice(SM_ID): 
    return repr(SM_ID).replace("L", "")

#________________________________________________________________________________
# C++
#

_terminal_state_prolog  = """
    /* (*) Terminal states _______________________________________________________
     *
     * States that implement actions of the 'winner patterns.                     */
"""

__function_signature = """
void  
QUEX_NAME($$STATE_MACHINE_NAME$$_analyzer_function)(QUEX_TYPE_ANALYZER* me) 
{
    /* NOTE: Different modes correspond to different analyzer functions. The 
     *       analyzer functions are all located inside the main class as static
     *       functions. That means, they are something like 'globals'. They 
     *       receive a pointer to the lexical analyzer, since static members do
     *       not have access to the 'this' pointer.                          */
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

@typed(dial_db=DialDB)
def _analyzer_function(StateMachineName, Setup, variable_definitions, 
                       function_body, dial_db, ModeNameList):
    """EngineClassName = name of the structure that contains the engine state.
                         if a mode of a complete quex environment is created, this
                         is the mode name. otherwise, any name can be chosen. 
    """              
    Lng = Setup.language_db

    function_signature_str = __function_signature.replace("$$STATE_MACHINE_NAME$$", 
                                                          StateMachineName)

    state_router_adr = DoorID.global_state_router(dial_db).related_address
    txt = [
        function_signature_str,
        # Macro definitions
        #
        Lng.DEFINE_SELF("me"),
        Lng.MODE_DEFINITION(ModeNameList),
        "/*  'QUEX_GOTO_STATE' requires 'QUEX_LABEL_STATE_ROUTER' */\n",
        "#   define QUEX_LABEL_STATE_ROUTER %s\n" % Lng.LABEL_STR_BY_ADR(state_router_adr),
        Lng.LEXEME_MACRO_SETUP(),
        #
        variable_definitions,
        #
        comment_on_post_context_position_init_str,
        "#   if defined(QUEX_OPTION_ASSERTS_EXT)\n",
        "    me->DEBUG_analyzer_function_at_entry = me->current_analyzer_function;\n",
        "#   endif\n",
        #
        # Entry to the actual function body
        #
        "%s\n" % Lng.LABEL(DoorID.global_reentry(dial_db)),
        "    %s\n" % Lng.LEXEME_START_SET(),
        "    QUEX_LEXEME_TERMINATING_ZERO_UNDO(&me->buffer);\n",
    ]

    txt.extend(function_body)

    # -- prevent the warning 'unused variable'
    txt.extend([ 
        "\n",                                                                                             
        "    __quex_assert_no_passage();\n", 
        "\n",                                                                                             
        "    /* Following labels are referenced in macros. It cannot be detected\n"
        "     * whether the macros are applied in user code or not. To avoid compiler.\n"
        "     * warnings of unused labels, they are referenced in unreachable code.   */\n"
        "    %s /* in RETURN                */\n" % Lng.GOTO(DoorID.return_with_on_after_match(dial_db), dial_db),
        "    %s /* in CONTINUE              */\n" % Lng.GOTO(DoorID.continue_with_on_after_match(dial_db), dial_db),
        "    %s /* in CONTINUE and skippers */\n" % Lng.GOTO(DoorID.continue_without_on_after_match(dial_db), dial_db),
        "#   if ! defined(QUEX_OPTION_COMPUTED_GOTOS)\n",
        "    %s /* in QUEX_GOTO_STATE       */\n" % Lng.GOTO(DoorID.global_state_router(dial_db), dial_db),
        "#   endif\n",
        "\n",
        "    /* Prevent compiler warning 'unused variable'.                           */\n",
        "    (void)QUEX_NAME(LexemeNull);\n",                                    
        "    /* target_state_index and target_state_else_index appear when \n",
        "     * QUEX_GOTO_STATE is used without computed goto-s.                      */\n",
        "    (void)target_state_index;\n",
        "    (void)target_state_else_index;\n",
        #
        # Macro undefinitions
        # 
        lexeme_macro_clean_up,
        Lng.MODE_UNDEFINITION(ModeNameList),
        "#   undef self\n",
        "#   undef QUEX_LABEL_STATE_ROUTER\n",
        "}\n",
    ])
    return txt

lexeme_macro_setup = """
    /* Lexeme setup: 
     *
     * There is a temporary zero stored at the end of each lexeme, if the action 
     * references to the 'Lexeme'. 'LexemeNull' provides a reference to an empty
     * zero terminated string.                                                    */
#if defined(QUEX_OPTION_ASSERTS_EXT)
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

#define LexemeNull      (&QUEX_NAME(LexemeNull))
"""

lexeme_macro_clean_up = """
#   undef Lexeme
#   undef LexemeBegin
#   undef LexemeEnd
#   undef LexemeNull
#   undef LexemeL
"""

__return_if_queue_full_or_simple_analyzer = """
    if( QUEX_NAME(TokenQueue_is_full)(&self._token_queue) ) {
        return;
    }
"""
__assert_no_mode_change = """
    /* Mode change = another function takes over the analysis.
     * => After mode change the analyzer function needs to be quit!
     * ASSERT: 'CONTINUE' after mode change is not allowed.                   */
    __quex_assert(   me->DEBUG_analyzer_function_at_entry 
                  == me->current_analyzer_function);
"""

def reentry_preparation(Lng, PreConditionIDList, OnAfterMatchCode, dial_db):
    """Reentry preperation (without returning from the function."""
    # (*) Unset all pre-context flags which may have possibly been set
    unset_pre_context_flags_str = Lng.PRE_CONTEXT_RESET(PreConditionIDList)
    on_after_match_str          = Lng.SOURCE_REFERENCED(OnAfterMatchCode)
    return [ 
        "\n%s\n"  % Lng.LABEL(DoorID.return_with_on_after_match(dial_db)), 
        Lng.COMMENT("RETURN -- after executing 'on_after_match' code."),
        on_after_match_str,
        "    %s\n\n" % Lng.PURE_RETURN,
        #
        "\n%s\n" % Lng.LABEL(DoorID.continue_with_on_after_match(dial_db)), 
        Lng.COMMENT("CONTINUE -- after executing 'on_after_match' code."),
        on_after_match_str,
        #
        "\n%s\n" % Lng.LABEL(DoorID.continue_without_on_after_match(dial_db)),
        Lng.COMMENT("CONTINUE -- without executing 'on_after_match' (e.g. on FAILURE)."), "\n",
        #
        __assert_no_mode_change, "\n",
        __return_if_queue_full_or_simple_analyzer, "\n",
        unset_pre_context_flags_str,
        "\n%s\n" % Lng.GOTO(DoorID.global_reentry(dial_db), dial_db), 
    ]

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

