
#include "TestAnalyzer.h"

#include <quex/code_base/analyzer/C-adaptions.h>
/* The file 'multi.i' contains implementations which are the same for all 
 * possibly generated analyzers. If QUEX_OPTION_MULTI is defined, it is
 * NOT supposed to be included here. If not--in which case we have a single
 * analzer--then it is included.                                             */
#include <quex/code_base/single.i>

QUEX_NAMESPACE_MAIN_OPEN
QUEX_NAME(Mode) QUEX_NAME(M) = {
    /* id                */ QUEX_NAME(ModeID_M),
    /* name              */ "M",
#   if      defined(QUEX_OPTION_INDENTATION_TRIGGER) \
       && ! defined(QUEX_OPTION_INDENTATION_DEFAULT_HANDLER)
    /* on_indentation    */ QUEX_NAME(Mode_on_indentation_null_function),
#   endif
    /* on_entry          */ QUEX_NAME(Mode_on_entry_exit_null_function),
    /* on_exit           */ QUEX_NAME(Mode_on_entry_exit_null_function),
#   if      defined(QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK)
    /* has_base          */ QUEX_NAME(M_has_base),
    /* has_entry_from    */ QUEX_NAME(M_has_entry_from),
    /* has_exit_to       */ QUEX_NAME(M_has_exit_to),
#   endif
    /* analyzer_function */ QUEX_NAME(M_analyzer_function)
};

QUEX_NAME(Mode)* (QUEX_NAME(mode_db)[__QUEX_SETTING_MAX_MODE_CLASS_N]) = {
    &QUEX_NAME(M)
};
#ifndef __QUEX_INDICATOR_DUMPED_TOKEN_ID_DEFINED
    static QUEX_TYPE_TOKEN_ID    QUEX_NAME_TOKEN(DumpedTokenIdObject);
#endif
#define self  (*(QUEX_TYPE_DERIVED_ANALYZER*)me)
#define __self_result_token_id    QUEX_NAME_TOKEN(DumpedTokenIdObject)

void
QUEX_NAME(M_on_entry)(QUEX_TYPE_ANALYZER* me, const QUEX_NAME(Mode)* FromMode) {
    (void)me;
    (void)FromMode;
#   ifdef QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK
    QUEX_NAME(M).has_entry_from(FromMode);
#   endif

}

void
QUEX_NAME(M_on_exit)(QUEX_TYPE_ANALYZER* me, const QUEX_NAME(Mode)* ToMode)  {
    (void)me;
    (void)ToMode;
#   ifdef QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK
    QUEX_NAME(M).has_exit_to(ToMode);
#   endif

}

#if defined(QUEX_OPTION_INDENTATION_TRIGGER) 
void
QUEX_NAME(M_on_indentation)(QUEX_TYPE_ANALYZER*    me, 
                                        QUEX_TYPE_INDENTATION  Indentation, 
                                        QUEX_TYPE_LEXATOM*   Begin) {
    (void)me;
    (void)Indentation;
    (void)Begin;
    return;
}
#endif

#ifdef QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK
bool
QUEX_NAME(M_has_base)(const QUEX_NAME(Mode)* Mode) {
    (void)Mode;
    return false;
}
bool
QUEX_NAME(M_has_entry_from)(const QUEX_NAME(Mode)* Mode) {
    (void)Mode;

    switch( Mode->id ) {
    case QUEX_NAME(ModeID_M): return true;
    default:
        if( Mode->has_base(&QUEX_NAME(M)) ) return true;
    }
    __QUEX_STD_fprintf(stderr, "mode '%s' is not one of (and not a derived mode of): M, \n", Mode->name);
    __quex_assert(false);
    return false;
    
}
bool
QUEX_NAME(M_has_exit_to)(const QUEX_NAME(Mode)* Mode) {
    (void)Mode;

    switch( Mode->id ) {
    case QUEX_NAME(ModeID_M): return true;
    default:
        if( Mode->has_base(&QUEX_NAME(M)) ) return true;
    }
    __QUEX_STD_fprintf(stderr, "mode '%s' is not one of (and not a derived mode of): M, \n", Mode->name);
    __quex_assert(false);
    return false;
    
}
#endif    
#undef self
#undef __self_result_token_id
QUEX_NAMESPACE_MAIN_CLOSE

/* #include "TestAnalyzer.h"*/
#include "quex/code_base/converter_helper/from-unicode-buffer.i"
#include <quex/code_base/analyzer/headers.i>
#include <quex/code_base/analyzer/C-adaptions.h>
QUEX_NAMESPACE_MAIN_OPEN
QUEX_TYPE_LEXATOM  QUEX_LEXEME_NULL_IN_ITS_NAMESPACE = (QUEX_TYPE_LEXATOM)0;
#ifdef      __QUEX_COUNT_VOID
#   undef   __QUEX_COUNT_VOID
#endif
#ifdef      __QUEX_OPTION_COUNTER
#    define __QUEX_COUNT_VOID(ME, BEGIN, END) \
            do {                              \
                QUEX_NAME(M_counter)((ME), (BEGIN), (END));     \
                __quex_debug_counter();       \
            } while(0)
#else
#    define __QUEX_COUNT_VOID(ME, BEGIN, END) /* empty */
#endif
#ifdef __QUEX_OPTION_COUNTER
static void
QUEX_NAME(M_counter)(QUEX_TYPE_ANALYZER* me, QUEX_TYPE_LEXATOM* LexemeBegin, QUEX_TYPE_LEXATOM* LexemeEnd)
{
#   define self (*me)
/*  'QUEX_GOTO_STATE' requires 'QUEX_LABEL_STATE_ROUTER' */
#   define QUEX_LABEL_STATE_ROUTER _18
    QUEX_TYPE_LEXATOM              input                          = (QUEX_TYPE_LEXATOM)(0x00);
    QUEX_TYPE_GOTO_LABEL           target_state_else_index        = QUEX_GOTO_LABEL_VOID;
    QUEX_TYPE_GOTO_LABEL           target_state_index             = QUEX_GOTO_LABEL_VOID;
#   ifdef QUEX_OPTION_COLUMN_NUMBER_COUNTING
    QUEX_TYPE_LEXATOM*             count_reference_p              = (QUEX_TYPE_LEXATOM*)0x0;
#   endif /* QUEX_OPTION_COLUMN_NUMBER_COUNTING */
    (void)me;
    __QUEX_IF_COUNT_SHIFT_VALUES();
    /* Allow LexemeBegin == LexemeEnd (e.g. END_OF_STREAM)
     * => Caller does not need to check
     * BUT, if so quit immediately after 'shift values'.
     */
    __quex_assert(LexemeBegin <= LexemeEnd);
    if( LexemeBegin == LexemeEnd ) {
        return;
    }
    me->buffer._read_p = LexemeBegin;

    /* (21 from BEFORE_ENTRY)  */
    __QUEX_IF_COUNT_COLUMNS(count_reference_p = (me->buffer._read_p));

__QUEX_IF_COUNT_COLUMNS(count_reference_p = (me->buffer._read_p));

    input = *(me->buffer._read_p);

_13:
    __quex_debug("Init State\n");
    __quex_debug_state(21);
if     ( input >= 0xB )  goto _2;
else if( input == 0xA )  goto _3;
else if( input == 0x9 )  goto _4;
else                     goto _2;


    __quex_assert_no_passage();
_8:
    /* (21 from 25)  */
    goto _13;


    __quex_assert_no_passage();
_5:
    /* (DROP_OUT from 22)  */
    goto _10;

    __quex_debug("Drop-Out Catcher\n");


    __quex_assert_no_passage();
_6:
    /* (DROP_OUT from 23)  */
    goto _11;


    __quex_assert_no_passage();
_7:
    /* (DROP_OUT from 24)  */
    goto _12;


    __quex_assert_no_passage();
_2:
    /* (24 from 21)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(24);
goto _7;


    __quex_assert_no_passage();
_3:
    /* (22 from 21)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(22);
goto _5;


    __quex_assert_no_passage();
_4:
    /* (23 from 21)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(23);
goto _6;

    /* (*) Terminal states _______________________________________________________
     *
     * States that implement actions of the 'winner patterns.                     */
_9:
    __quex_debug("* TERMINAL <LOOP EXIT>\n");
    --(me->buffer._read_p);

__QUEX_IF_COUNT_COLUMNS_ADD((size_t)(((me->buffer._read_p) - count_reference_p)));

goto _0;

_10:
    __quex_debug("* TERMINAL <LOOP 5>\n");
__QUEX_IF_COUNT_LINES_ADD((size_t)1);

    __QUEX_IF_COUNT_COLUMNS((me->counter._column_number_at_end) = (size_t)1);

__QUEX_IF_COUNT_COLUMNS(count_reference_p = (me->buffer._read_p));

if( me->buffer._read_p != LexemeEnd ) goto _8;

goto _0;

_11:
    __quex_debug("* TERMINAL <LOOP 6>\n");
__QUEX_IF_COUNT_COLUMNS_ADD((size_t)(((me->buffer._read_p) - count_reference_p - 1)));

__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end -= 1);
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end &= ~ ((size_t)0x3));
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end += 4 + 1);

__QUEX_IF_COUNT_COLUMNS(count_reference_p = (me->buffer._read_p));

if( me->buffer._read_p != LexemeEnd ) goto _8;

goto _0;

_12:
    __quex_debug("* TERMINAL <LOOP 7>\n");
if( me->buffer._read_p != LexemeEnd ) goto _8;

__QUEX_IF_COUNT_COLUMNS_ADD((size_t)(((me->buffer._read_p) - count_reference_p)));

goto _0;

if(0) {
    /* Avoid unreferenced labels. */
    goto _9;
    goto _10;
    goto _11;
    goto _12;
}
_20: /* TERMINAL: BAD_LEXATOM */
;
_19: /* TERMINAL: FAILURE     */
goto _0;
_0:
/* Assert: lexeme in codec's character boundaries. */

     __quex_assert(me->buffer._read_p == LexemeEnd);
    return;
#   ifndef QUEX_OPTION_COMPUTED_GOTOS
    __quex_assert_no_passage();
_18:
#   endif /* QUEX_OPTION_COMPUTED_GOTOS */

#undef self


#undef QUEX_LABEL_STATE_ROUTER

#    if ! defined(QUEX_OPTION_COMPUTED_GOTOS)
     goto _18; /* in QUEX_GOTO_STATE       */
     goto _20; /* to BAD_LEXATOM           */
#    endif
    /* Avoid compiler warning: 'Unused labels' */

    goto _19;
    (void)target_state_index;
    (void)target_state_else_index;
}
#endif /* __QUEX_OPTION_COUNTER */

#include <quex/code_base/buffer/Buffer>
#ifdef QUEX_OPTION_TOKEN_POLICY_QUEUE
#   include <quex/code_base/token/TokenQueue>
#endif

#ifdef    CONTINUE
#   undef CONTINUE
#endif
#define   CONTINUE do { goto _0; } while(0)

#ifdef    RETURN
#   undef RETURN
#endif
#define   RETURN   do { goto _2; } while(0)

__QUEX_TYPE_ANALYZER_RETURN_VALUE  
QUEX_NAME(M_analyzer_function)(QUEX_TYPE_ANALYZER* me) 
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
/*  'QUEX_GOTO_STATE' requires 'QUEX_LABEL_STATE_ROUTER' */
#   define QUEX_LABEL_STATE_ROUTER _21
#   define M    (QUEX_NAME(M))

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
#   define LexemeL      ((size_t)(me->buffer._read_p - me->buffer._lexeme_start_p))
#   define LexemeEnd    me->buffer._read_p
#endif

#define LexemeNull      (&QUEX_LEXEME_NULL)
    E_LoadResult                   load_result                    = E_LoadResult_VOID;
    QUEX_TYPE_LEXATOM**            position                       = 0x0;
    QUEX_TYPE_GOTO_LABEL           target_state_else_index        = QUEX_GOTO_LABEL_VOID;
    const size_t                   PositionRegisterN              = (size_t)0;
    QUEX_TYPE_LEXATOM              input                          = (QUEX_TYPE_LEXATOM)(0x00);
    QUEX_TYPE_GOTO_LABEL           target_state_index             = QUEX_GOTO_LABEL_VOID;

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
#   if    defined(QUEX_OPTION_AUTOMATIC_ANALYSIS_CONTINUATION_ON_MODE_CHANGE) \
       || defined(QUEX_OPTION_ASSERTS)
    me->DEBUG_analyzer_function_at_entry = me->current_analyzer_function;
#   endif
_20:
    me->buffer._lexeme_start_p = me->buffer._read_p;
    QUEX_LEXEME_TERMINATING_ZERO_UNDO(&me->buffer);
_10:
    /* (18 from BEFORE_ENTRY) (18 from RELOAD_FORWARD)  */

    input = *(me->buffer._read_p);


    __quex_debug("Init State\n");
    __quex_debug_state(18);
if     ( input == 0x58 )  goto _11;
else if( input == 0x0 )   goto _14;
else                      goto _12;


    __quex_assert_no_passage();
_13:
    /* (DROP_OUT from 19)  */
    goto _1;
_17:
    __quex_debug("Drop-Out Catcher\n");


    __quex_assert_no_passage();
_12:
    /* (DROP_OUT from 18)  */
        me->buffer._read_p = me->buffer._lexeme_start_p + 1;
goto _8;
    goto _17;


    __quex_assert_no_passage();
_11:
    /* (19 from 18)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(19);
goto _13;

    /* (*) Terminal states _______________________________________________________
     *
     * States that implement actions of the 'winner patterns.                     */
_3:
    __quex_debug("* TERMINAL BAD_LEXATOM\n");
__QUEX_COUNT_VOID(&self, LexemeBegin, LexemeEnd);
{
__QUEX_STD_printf("\n");
QUEX_NAME(Buffer_show_debug_content)(&me->buffer);
__QUEX_STD_printf("\n");
QUEX_ERROR_EXIT("\nMode 'M': Bad lexatom (character encoding error) detected!\n"
                "The 'on_bad_lexatom' handler has not been specified.\n");
}
    /* Bad lexatom detection FORCES a return from the lexical analyzer, so that no
     * tokens can be filled after the termination token.
     */
goto _2;
_4:
    __quex_debug("* TERMINAL LOAD_FAILURE\n");
__QUEX_COUNT_VOID(&self, LexemeBegin, LexemeEnd);
{
__QUEX_STD_printf("\n");
QUEX_NAME(Buffer_show_debug_content)(&me->buffer);
__QUEX_STD_printf("\n");
QUEX_ERROR_EXIT("\nMode 'M': General failure while loading buffer.\n"
                "The 'on_load_failure' handler has not been specified.\n");
}
    /* Load failure FORCES a return from the lexical analyzer, so that no
     * tokens can be filled after the termination token.
     */
goto _2;
_5:
    __quex_debug("* TERMINAL OVERFLOW\n");
__QUEX_COUNT_VOID(&self, LexemeBegin, LexemeEnd);
QUEX_LEXEME_TERMINATING_ZERO_SET(&me->buffer);
{
__QUEX_STD_printf("\n");
QUEX_NAME(Buffer_show_debug_content)(&me->buffer);
__QUEX_STD_printf("\n");
QUEX_ERROR_EXIT("\nMode 'M': Lexeme exceeds buffer size.\n"
                "The 'on_overflow' handler has not been specified.\n");
}
    /* Lexeme size exceeds buffer size. No further buffer load possible.
     */
goto _2;
_6:
    __quex_debug("* TERMINAL END_OF_STREAM\n");
__QUEX_COUNT_VOID(&self, LexemeBegin, LexemeEnd);
{
self_send(__QUEX_SETTING_TOKEN_ID_TERMINATION);

}
    /* End of Stream FORCES a return from the lexical analyzer, so that no
     * tokens can be filled after the termination token.
     */
goto _2;
_8:
    __quex_debug("* TERMINAL FAILURE\n");
__QUEX_COUNT_VOID(&self, LexemeBegin, LexemeEnd);
{
__QUEX_STD_printf("\n");
QUEX_NAME(Buffer_show_debug_content)(&me->buffer);
__QUEX_STD_printf("\n");
QUEX_ERROR_EXIT("\nMode 'M': Match failure, no pattern matched!\n"
                "The 'on_failure' handler has not been specified.\n");
}
goto _7;
_9:
    __quex_debug("* TERMINAL SKIP_RANGE_OPEN\n");
__QUEX_COUNT_VOID(&self, LexemeBegin, LexemeEnd);
{
#define Counter counter
__QUEX_STD_printf("\n");
QUEX_NAME(Buffer_show_debug_content)(&me->buffer);
__QUEX_STD_printf("\n");
QUEX_ERROR_EXIT("\nMode 'M': End of file occurred before closing skip range delimiter!\n"
                "The 'on_skip_range_open' handler has not been specified.\n");
}
    /* End of Stream appeared, while scanning for end of skip-range.
     */
goto _2;
_1:
    __quex_debug("* TERMINAL X\n");
__QUEX_IF_COUNT_SHIFT_VALUES();
__QUEX_IF_COUNT_COLUMNS_ADD(1);
{

#   line 2 "nothing.qx"
self_send(QUEX_TKN_X);
QUEX_SETTING_AFTER_SEND_CONTINUE_OR_RETURN();


#   line 524 "TestAnalyzer.c"

}
goto _0;
if(0) {
    /* Avoid unreferenced labels. */
    goto _3;
    goto _4;
    goto _5;
    goto _6;
    goto _8;
    goto _9;
    goto _1;
}
#   ifndef QUEX_OPTION_COMPUTED_GOTOS
    __quex_assert_no_passage();
_21:
    switch( target_state_index ) {
        case 6: { goto _6;}
        case 10: { goto _10;}

        default:
            __QUEX_STD_fprintf(stderr, "State router: index = %i\n", (int)target_state_index);
            QUEX_ERROR_EXIT("State router: unknown index.\n");
    }
#   endif /* QUEX_OPTION_COMPUTED_GOTOS */


    __quex_assert_no_passage();
_14:
    /* (RELOAD_FORWARD from 18)  */
    target_state_index = QUEX_LABEL(10); target_state_else_index = QUEX_LABEL(6);



    __quex_debug3("RELOAD_FORWARD: success->%i; failure->%i", 
                  (int)target_state_index, (int)target_state_else_index);
    __quex_assert(*(me->buffer._read_p) == QUEX_SETTING_BUFFER_LIMIT_CODE);
    
    __quex_debug_reload_before();                 
    load_result = QUEX_NAME(Buffer_load_forward)(&me->buffer, (QUEX_TYPE_LEXATOM**)position, PositionRegisterN);
    __quex_debug_reload_after(load_result);

    switch( load_result ) {
    case E_LoadResult_DONE:              QUEX_GOTO_STATE(target_state_index);      
    case E_LoadResult_BAD_LEXATOM:       goto _3;
    case E_LoadResult_FAILURE:           goto _4;
    case E_LoadResult_NO_SPACE_FOR_LOAD: goto _5;
    case E_LoadResult_NO_MORE_DATA:      QUEX_GOTO_STATE(target_state_else_index); 
    default:                             __quex_assert(false);
    }

_2:
/* RETURN -- after executing 'on_after_match' code. */
    __QUEX_PURE_RETURN;


_0:
/* CONTINUE -- after executing 'on_after_match' code. */

_7:
/* CONTINUE -- without executing 'on_after_match' (e.g. on FAILURE). */


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
#   if    defined(QUEX_OPTION_AUTOMATIC_ANALYSIS_CONTINUATION_ON_MODE_CHANGE)        || defined(QUEX_OPTION_ASSERTS)
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


goto _20;

    __quex_assert_no_passage();

    /* Following labels are referenced in macros. It cannot be detected
     * whether the macros are applied in user code or not. To avoid compiler.
     * warnings of unused labels, they are referenced in unreachable code.   */
    goto _2; /* in RETURN                */
    goto _0; /* in CONTINUE              */
    goto _7; /* in CONTINUE and skippers */
#   if ! defined(QUEX_OPTION_COMPUTED_GOTOS)
    goto _21; /* in QUEX_GOTO_STATE       */
#   endif

    /* Prevent compiler warning 'unused variable'.                           */
    (void)QUEX_LEXEME_NULL;
    (void)QUEX_NAME_TOKEN(DumpedTokenIdObject);
    /* target_state_index and target_state_else_index appear when 
     * QUEX_GOTO_STATE is used without computed goto-s.                      */
    (void)target_state_index;
    (void)target_state_else_index;

#   undef Lexeme
#   undef LexemeBegin
#   undef LexemeEnd
#   undef LexemeNull
#   undef LexemeL
#   undef M
#   undef self
#   undef QUEX_LABEL_STATE_ROUTER
}
QUEX_NAMESPACE_MAIN_CLOSE


QUEX_NAMESPACE_TOKEN_OPEN

const char*
QUEX_NAME_TOKEN(map_id_to_name)(const QUEX_TYPE_TOKEN_ID TokenID)
{
   static char  error_string[64];
   static const char  uninitialized_string[] = "<UNINITIALIZED>";
   static const char  termination_string[]   = "<TERMINATION>";
#  if defined(QUEX_OPTION_INDENTATION_TRIGGER)
   static const char  indent_string[]        = "<INDENT>";
   static const char  dedent_string[]        = "<DEDENT>";
   static const char  nodent_string[]        = "<NODENT>";
#  endif
   static const char  token_id_str_X[]             = "X";
       

   /* NOTE: This implementation works only for token id types that are 
    *       some type of integer or enum. In case an alien type is to
    *       used, this function needs to be redefined.                  */
   switch( TokenID ) {
   default: {
       __QUEX_STD_sprintf(error_string, "<UNKNOWN TOKEN-ID: %i>", (int)TokenID);
       return error_string;
   }
   case QUEX_TKN_TERMINATION:    return termination_string;
   case QUEX_TKN_UNINITIALIZED:  return uninitialized_string;
#  if defined(QUEX_OPTION_INDENTATION_TRIGGER)
   case QUEX_TKN_INDENT:         return indent_string;
   case QUEX_TKN_DEDENT:         return dedent_string;
   case QUEX_TKN_NODENT:         return nodent_string;
#  endif
   case QUEX_TKN_X:             return token_id_str_X;

   }
}

QUEX_NAMESPACE_TOKEN_CLOSE


QUEX_NAMESPACE_MAIN_OPEN

bool
QUEX_NAME(user_constructor)(QUEX_TYPE_ANALYZER* me)
{
    (void)me;

    __quex_assert(QUEX_NAME(mode_db)[QUEX_NAME(ModeID_M)] == &QUEX_NAME(M));


#define self  (*(QUEX_TYPE_DERIVED_ANALYZER*)me)
/* START: User's constructor extensions _______________________________________*/
return UserConstructor_UnitTest_return_value;
/* END: _______________________________________________________________________*/
#undef self
    return true;
}

void
QUEX_NAME(user_destructor)(QUEX_TYPE_ANALYZER* me)
{
    (void)me;

#define self  (*(QUEX_TYPE_DERIVED_ANALYZER*)me)
/* START: User's constructor extensions _______________________________________*/

/* END: _______________________________________________________________________*/
#undef self
}

bool
QUEX_NAME(user_reset)(QUEX_TYPE_ANALYZER* me)
{
    (void)me;

#define self  (*(QUEX_TYPE_DERIVED_ANALYZER*)me)
/* START: User's 'reset' ______________________________________________________*/
return UserReset_UnitTest_return_value;
/* END: _______________________________________________________________________*/
#undef self
    return true;
}

#ifdef QUEX_OPTION_INCLUDE_STACK

bool
QUEX_NAME(user_memento_pack)(QUEX_TYPE_ANALYZER* me, 
                             const char*         InputName, 
                             QUEX_NAME(Memento)* memento) 
{
    (void)me; (void)memento; (void)InputName;

#define self  (*(QUEX_TYPE_DERIVED_ANALYZER*)me)
/* START: User's memento 'pack' _______________________________________________*/
return UserMementoPack_UnitTest_return_value;
/* END: _______________________________________________________________________*/
#undef self
    return true;
}

void
QUEX_NAME(user_memento_unpack)(QUEX_TYPE_ANALYZER*  me, 
                               QUEX_NAME(Memento)*  memento)
{
    (void)me; (void)memento;

#define self  (*(QUEX_TYPE_DERIVED_ANALYZER*)me)
/* START: User's memento 'unpack' _____________________________________________*/

/* END: _______________________________________________________________________*/
#undef self
}
#endif /* QUEX_OPTION_INCLUDE_STACK */

QUEX_NAMESPACE_MAIN_CLOSE



/* -*- C++ -*-   vim: set syntax=cpp: 
 * (C) 2004-2009 Frank-Rene Schaefer
 * ABSOLUTELY NO WARRANTY
 */
#ifndef __QUEX_INCLUDE_GUARD__TOKEN__GENERATED__QUEX___TOKEN_I
#define __QUEX_INCLUDE_GUARD__TOKEN__GENERATED__QUEX___TOKEN_I

#ifndef    __QUEX_OPTION_PLAIN_C
#   define __QUEX_OPTION_PLAIN_C
#endif

#include "TestAnalyzer-token.h"
#include <quex/code_base/definitions>

QUEX_NAMESPACE_LEXEME_NULL_OPEN
extern QUEX_TYPE_LEXATOM   QUEX_LEXEME_NULL_IN_ITS_NAMESPACE;
QUEX_NAMESPACE_LEXEME_NULL_CLOSE


QUEX_INLINE void 
quex_Token_set(quex_Token*            __this, 
                 const QUEX_TYPE_TOKEN_ID ID) 
{ __this->_id = ID; }

QUEX_INLINE const char*    
quex_Token_map_id_to_name(QUEX_TYPE_TOKEN_ID);

QUEX_INLINE void 
quex_Token_construct(quex_Token* __this)
{
#   define self (*__this)
#   define LexemeNull  &QUEX_LEXEME_NULL
    (void)__this;

#   line 33 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

       self.number = 0;
       self.text   = LexemeNull;
   

#   line 815 "TestAnalyzer.c"

#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE void 
quex_Token_copy_construct(quex_Token*       __this, 
                            const quex_Token* __That)
{
    QUEX_NAME_TOKEN(construct)(__this);
    QUEX_NAME_TOKEN(copy)(__this, __That);
}

QUEX_INLINE void 
quex_Token_destruct(quex_Token* __this)
{
#   define self (*__this)
#   define LexemeNull  &QUEX_LEXEME_NULL
    if( ! __this ) return;


#   line 38 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

       if( self.text != LexemeNull ) {
           QUEXED(MemoryManager_free)((void*)self.text,
                                          E_MemoryObjectType_TEXT);
           self.text = LexemeNull;
       }
   

#   line 846 "TestAnalyzer.c"

#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE void
quex_Token_copy(quex_Token*       __this, 
                  const quex_Token* __That)
{
#   define self  (*__this)
#   define Other (*__That)
#   define LexemeNull  &QUEX_LEXEME_NULL
    (void)__this;
    (void)__That;

#   line 46 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

        self._id  = Other._id;

        if( self.text != LexemeNull ) {
            QUEXED(MemoryManager_free)((void*)self.text,
                                       E_MemoryObjectType_TEXT);
        }
        if( Other.text != LexemeNull ) {
            self.text = \
               (QUEX_TYPE_LEXATOM*)
               QUEXED(MemoryManager_allocate)(
                      sizeof(QUEX_TYPE_LEXATOM) * (QUEX_NAME(strlen)(Other.text) + 1),
                      E_MemoryObjectType_TEXT);
            __QUEX_STD_memcpy((void*)self.text, (void*)Other.text, 
                                sizeof(QUEX_TYPE_LEXATOM) 
                              * (QUEX_NAME(strlen)(Other.text) + 1));
        }
        self.number = Other.number;
    #   ifdef     QUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN
        __QUEX_IF_COUNT_LINES(self._line_n     = Other._line_n);
        __QUEX_IF_COUNT_COLUMNS(self._column_n = Other._column_n);
    #   endif
   

#   line 887 "TestAnalyzer.c"

#   undef  LexemeNull
#   undef  Other
#   undef  self
    /* If the user even misses to copy the token id, then there's
     * something seriously wrong.                                 */
    __quex_assert(__this->_id == __That->_id);
#   ifdef QUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN
    __QUEX_IF_COUNT_LINES(__quex_assert(__this->_line_n == __That->_line_n));
    __QUEX_IF_COUNT_COLUMNS(__quex_assert(__this->_column_n == __That->_column_n));
#   endif
}


QUEX_INLINE bool 
quex_Token_take_text(quex_Token*              __this, 
                       QUEX_TYPE_ANALYZER*        __analyzer, 
                       const QUEX_TYPE_LEXATOM* Begin, 
                       const QUEX_TYPE_LEXATOM* End)
/* RETURNS: true -- if the token claims ownership over the given memory.
 *          false -- if no ownership is claimed.                             */
{
#   define self       (*__this)
#   define analyzer   (*__analyzer)
#   ifdef  LexemeNull
#   error  "Error LexemeNull shall not be defined here."
#   endif
#   define LexemeNull  &QUEX_LEXEME_NULL
    (void)__this;
    (void)__analyzer;
    (void)Begin;
    (void)End;

#   line 70 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"


#       if 0
        /* Hint for debug: To check take_text change "#if 0" to "#if 1" */
        {
            const QUEX_TYPE_LEXATOM* it = (void*)0x0;
            printf("previous:  '");
            if( self.text != LexemeNull ) {
                for(it = self.text; *it ; ++it) printf("%04X.", (int)*it);
                printf("%04X.", (int)*it);
            }
            printf("'\n");
            printf("take_text: '");
            for(it = Begin; it != End; ++it) printf("%04X.", (int)*it);
            printf("%04X.", (int)*it);
            printf("'\n");
        }
#       endif

        if( self.text != LexemeNull ) {
            QUEXED(MemoryManager_free)((void*)self.text,
                                          E_MemoryObjectType_TEXT);
        }
        if( Begin != LexemeNull ) {
            __quex_assert(End >= Begin);
            self.text = \
                 (QUEX_TYPE_LEXATOM*)
                 QUEXED(MemoryManager_allocate)(
                              sizeof(QUEX_TYPE_LEXATOM) * (size_t)(End - Begin + 1), 
                              E_MemoryObjectType_TEXT);
            __QUEX_STD_memcpy((void*)self.text, (void*)Begin, 
                              sizeof(QUEX_TYPE_LEXATOM) * (size_t)(End - Begin));
            /* The string is not necessarily zero terminated, so terminate it here. */
            *((QUEX_TYPE_LEXATOM*)(self.text + (End - Begin))) = (QUEX_TYPE_LEXATOM)0;
        } else {
            self.text = LexemeNull;
        }

#       if 0
        /* Hint for debug: To check take_text change "#if 0" to "#if 1"       */
        {
            const QUEX_TYPE_LEXATOM* it = 0x0;
            printf("after:     '");
            if( self.text != LexemeNull ) { 
                for(it = self.text; *it ; ++it) printf("%04X.", (int)*it);
                printf("%04X.", (int)*it);
            }
            printf("'\n");
        }
#       endif

        /* This token copied the text from the chunk into the string, 
         * so we do not claim ownership over it.                             */
        return false;
   

#   line 978 "TestAnalyzer.c"

#   undef  LexemeNull
#   undef  analyzer
#   undef  self
    /* Default: no ownership.                                                */
    return false;
}

#ifdef QUEX_OPTION_TOKEN_REPETITION_SUPPORT
QUEX_INLINE size_t 
quex_Token_repetition_n_get(quex_Token* __this)
{
#   define self        (*__this)
#   define LexemeNull  &QUEX_LEXEME_NULL
    (void)__this;
    
#   line 135 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

       return self.number;
   

#   line 1000 "TestAnalyzer.c"

#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE void 
quex_Token_repetition_n_set(quex_Token* __this, size_t N)
{
#   define self        (*__this)
#   define LexemeNull  &QUEX_LEXEME_NULL
    (void)__this;
    (void)N;
    
#   line 131 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

       self.number = N;
   

#   line 1019 "TestAnalyzer.c"

#   undef  LexemeNull
#   undef  self
}
#endif /* QUEX_OPTION_TOKEN_REPETITION_SUPPORT */


#   line 139 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

        const char* 
        quex_Token_get_string(quex_Token* me, char*   buffer, size_t  BufferSize) 
        {
            const char*  token_type_str = quex_Token_map_id_to_name(me->_id);
            const char*  BufferEnd  = buffer + BufferSize;
            const char*  iterator   = 0;
            char*        writerator = 0;

            /* Token Type */
            iterator = token_type_str;
            writerator = buffer; 
            while( (*iterator) && writerator != BufferEnd ) {
                *writerator++ = *iterator++;
            }

            /* Opening Quote */
            if( BufferEnd - writerator > 2 ) {
                *writerator++ = ' ';
                *writerator++ = '\'';
            }

            /* The String */
            quex_Token_pretty_char_text(me, writerator, (size_t)(BufferEnd - writerator));

            while( *writerator ) {
                ++writerator;
            }

            /* Closing Quote */
            if( BufferEnd - writerator > 1 ) {
                *writerator++ = '\'';
            }
            *writerator = '\0';
            return buffer;
        }

        const char* 
        quex_Token_pretty_char_text(quex_Token* me, char*   buffer, size_t  BufferSize) 
        /* Provides a somehow pretty-print of the text in the token. Note, that the buffer
         * in case of UTF8 should be 4bytes longer than the longest expected string.       */
        {
            const QUEX_TYPE_LEXATOM*  source    = me->text;
            char*                       drain     = buffer;
            const char*                 DrainEnd  = buffer + BufferSize;

            const QUEX_TYPE_LEXATOM*  SourceEnd = me->text + (size_t)(QUEX_NAME(strlen)(source)) + 1;
            QUEX_CONVERTER_STRING(identical,char)(&source, SourceEnd, &drain, DrainEnd);
            return buffer;
        }

#       if ! defined(__QUEX_OPTION_WCHAR_T_DISABLED)
        const wchar_t* 
        quex_Token_pretty_wchar_text(quex_Token* me, wchar_t*  buffer, size_t    BufferSize) 
        {
            wchar_t*                    drain     = buffer;
            const wchar_t*              DrainEnd  = buffer + (ptrdiff_t)BufferSize;
            const QUEX_TYPE_LEXATOM*  source    = me->text;
            const QUEX_TYPE_LEXATOM*  SourceEnd = me->text + (ptrdiff_t)(QUEX_NAME(strlen)(source)) + 1;

            QUEX_CONVERTER_STRING(identical,wchar)(&source, SourceEnd, &drain, DrainEnd);
            return buffer;
        }
#       endif

#include <quex/code_base/converter_helper/identity.i>
   

#   line 1096 "TestAnalyzer.c"




#endif /* __QUEX_INCLUDE_GUARD__TOKEN__GENERATED__QUEX___TOKEN_I */
bool UserConstructor_UnitTest_return_value = true;
bool UserReset_UnitTest_return_value       = true;
bool UserMementoPack_UnitTest_return_value = true;
