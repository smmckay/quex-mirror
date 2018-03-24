
#include "test_environment/TestAnalyzer.h"
#include "test_environment/lib/analyzer/C-adaptions.h"
/* The file 'multi.i' contains implementations which are the same for all 
 * possibly generated analyzers. If QUEX_OPTION_MULTI is defined, it is
 * NOT supposed to be included here. If not--in which case we have a single
 * analzer--then it is included.                                             */
#include "test_environment/lib/single.i"

QUEX_NAMESPACE_MAIN_OPEN
QUEX_NAME(Mode) QUEX_NAME(M) = {
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
    {
    /* on_buffer_before_change */ QUEX_NAME(M_on_buffer_before_change),
    /* on_buffer_overflow      */ QUEX_NAME(M_on_buffer_overflow),
    /* aux                     */ (void*)0,
    },

    /* analyzer_function */ QUEX_NAME(M_analyzer_function)
};

#   ifdef     self
#       undef self
#   endif
#   define self (*((QUEX_TYPE_ANALYZER*)me))
#define LexemeNull  (&QUEX_LEXEME_NULL)
#define RETURN      return

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
                QUEX_TYPE_LEXATOM*     Begin) 
{
    (void)me;
    (void)Indentation;
    (void)Begin;
#   ifdef     self
#       undef self
#   endif
#   define self (*((QUEX_TYPE_ANALYZER*)me))

#   define M    (&QUEX_NAME(M))

#   define Lexeme        Begin
#   define LexemeEnd     (me->buffer._read_p)

    QUEX_NAME(IndentationStack)*  stack = &me->counter._indentation_stack;
    QUEX_TYPE_INDENTATION*        start = 0x0;
    (void)start;

    __quex_assert((long)Indentation >= 0);

    if( Indentation > *(stack->back) ) {
        ++(stack->back);
        if( stack->back == stack->memory_end ) {
            QUEX_NAME(MF_error_code_set_if_first)(me, E_Error_Indentation_StackOverflow);
            return;
        }
        *(stack->back) = Indentation;
self.send(&self, QUEX_TOKEN_ID(INDENT));
        return;
    }
    else if( Indentation == *(stack->back) ) {
self.send(&self, QUEX_TOKEN_ID(NODENT));
    }
    else  {
        start = stack->back;
        --(stack->back);
#       if ! defined(QUEX_OPTION_TOKEN_REPETITION_SUPPORT)
#       define First true
self.send(&self, QUEX_TOKEN_ID(DEDENT));
#       undef  First
#       endif
        while( Indentation < *(stack->back) ) {
            --(stack->back);
#           if ! defined(QUEX_OPTION_TOKEN_REPETITION_SUPPORT)
#           define First false
self.send(&self, QUEX_TOKEN_ID(DEDENT));
#           undef  First
#           endif
        }

        if( Indentation == *(stack->back) ) { 
            /* 'Landing' must happen on indentation border. */
#           if defined(QUEX_OPTION_TOKEN_REPETITION_SUPPORT)
#           define ClosedN (start - stack->back)
self.send_n(&self, QUEX_TOKEN_ID(DEDENT), (size_t)ClosedN);

#           undef  ClosedN
#           endif
        } else { 
#            define IndentationStackSize ((size_t)(1 + start - stack->front))
#            define IndentationStack(I)  (*(stack->front + I))
#            define IndentationUpper     (*(stack->back))
#            define IndentationLower     ((stack->back == stack->front) ? *(stack->front) : *(stack->back - 1))
#            define ClosedN              (start - stack->back)
             QUEX_NAME(MF_error_code_set_if_first)(me,  
                                                E_Error_Indentation_DedentNotOnIndentationBorder);

#            undef IndentationStackSize 
#            undef IndentationStack  
#            undef IndentationUpper     
#            undef IndentationLower     
#            undef ClosedN
             return;
        }
    }

#   undef Lexeme    
#   undef LexemeEnd 
#   define M    (&QUEX_NAME(M))

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
if( Mode == &QUEX_NAME(M) ) {

    return true;

    }

    else if( Mode->has_base(&QUEX_NAME(M)) ) {

    return true;

    }

    else {
    return false;
    }
}

bool
QUEX_NAME(M_has_exit_to)(const QUEX_NAME(Mode)* Mode) {
    (void)Mode;
if( Mode == &QUEX_NAME(M) ) {

    return true;

    }

    else if( Mode->has_base(&QUEX_NAME(M)) ) {

    return true;

    }

    else {
    return false;
    }
}
#endif    

void
QUEX_NAME(M_on_buffer_before_change)(void* me /* 'aux' -> 'self' via 'me' */)
{
    const QUEX_TYPE_LEXATOM* BufferBegin = self.buffer.begin(&self.buffer);
    const QUEX_TYPE_LEXATOM* BufferEnd   = self.buffer.end(&self.buffer);
    (void)me; (void)BufferBegin; (void)BufferEnd;

}

QUEX_INLINE void
QUEX_NAME(Buffer_print_overflow_message)(QUEX_NAME(Buffer)* buffer); 

void
QUEX_NAME(M_on_buffer_overflow)(void*  me /* 'aux' -> 'self' via 'me' */)
{
    const QUEX_TYPE_LEXATOM* LexemeBegin = self.buffer._lexeme_start_p;
    const QUEX_TYPE_LEXATOM* LexemeEnd   = self.buffer._read_p;
    const size_t             BufferSize  = (size_t)(self.buffer.size(&self.buffer)); 


    /* Try to double the size of the buffer, by default.                      */
    if( ! QUEX_NAME(Buffer_nested_negotiate_extend)(&self.buffer, 2.0) ) {
        QUEX_NAME(MF_error_code_set_if_first)(&self, E_Error_Buffer_Overflow_LexemeTooLong);
        QUEX_NAME(Buffer_print_overflow_message)(&self.buffer);
    }

    (void)me; (void)LexemeBegin; (void)LexemeEnd; (void)BufferSize;
}
#undef self
#undef LexemeNull
#undef RETURN
QUEX_NAMESPACE_MAIN_CLOSE

/* #include "test_environment/test_environment/TestAnalyzer.h"*/
#include "test_environment/lib/analyzer/headers.i"
#include "test_environment/lib/analyzer/C-adaptions.h"


/* START: User defined header content _________________________________________
 *        The 'footer' content relies on class definitions made above.        */


QUEX_NAMESPACE_MAIN_OPEN
#ifdef      QUEX_FUNCTION_COUNT_ARBITRARY
#   undef   QUEX_FUNCTION_COUNT_ARBITRARY
#endif
#ifdef      QUEX_OPTION_COUNTER
#    define QUEX_FUNCTION_COUNT_ARBITRARY(ME, BEGIN, END) \
            do {                              \
                QUEX_NAME(M_counter)((ME), (BEGIN), (END));     \
                __quex_debug_counter();       \
            } while(0)
#else
#    define QUEX_FUNCTION_COUNT_ARBITRARY(ME, BEGIN, END) /* empty */
#endif
#ifdef QUEX_OPTION_COUNTER
static void
QUEX_NAME(M_counter)(QUEX_TYPE_ANALYZER* me, QUEX_TYPE_LEXATOM* LexemeBegin, QUEX_TYPE_LEXATOM* LexemeEnd)
{
#   define self (*me)
/*  'QUEX_GOTO_STATE' requires 'QUEX_LABEL_STATE_ROUTER' */
#   define QUEX_LABEL_STATE_ROUTER _18
    QUEX_TYPE_LEXATOM              input                          = (QUEX_TYPE_LEXATOM)(0x00);
    QUEX_TYPE_GOTO_LABEL           target_state_else_index        = QUEX_GOTO_LABEL_VOID;
    QUEX_TYPE_GOTO_LABEL           target_state_index             = QUEX_GOTO_LABEL_VOID;
#   ifdef QUEX_OPTION_COUNTER_COLUMN
    QUEX_TYPE_LEXATOM*             count_reference_p              = (QUEX_TYPE_LEXATOM*)0x0;
#   endif /* QUEX_OPTION_COUNTER_COLUMN */
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

    /* (22 from BEFORE_ENTRY)  */
    __QUEX_IF_COUNT_COLUMNS(count_reference_p = (me->buffer._read_p));

__QUEX_IF_COUNT_COLUMNS(count_reference_p = (me->buffer._read_p));

    input = *(me->buffer._read_p);

_13:
    __quex_debug_init_state(22);
if     ( input >= 0xB )  goto _4;
else if( input == 0xA )  goto _2;
else if( input == 0x9 )  goto _3;
else                     goto _4;


    __quex_assert_no_passage();
_8:
    /* (22 from 27)  */
    goto _13;


    __quex_assert_no_passage();
_5:
    /* (DROP_OUT from 23)  */
goto _10;

    __quex_debug("Drop-Out Catcher\n");


    __quex_assert_no_passage();
_6:
    /* (DROP_OUT from 24)  */
goto _11;


    __quex_assert_no_passage();
_7:
    /* (DROP_OUT from 25)  */
goto _12;


    __quex_assert_no_passage();
_3:
    /* (24 from 22)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(24);
goto _6;


    __quex_assert_no_passage();
_4:
    /* (25 from 22)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(25);
goto _7;


    __quex_assert_no_passage();
_2:
    /* (23 from 22)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(23);
goto _5;

    /* (*) Terminal states _______________________________________________________
     *
     * States that implement actions of the 'winner patterns.                     */
_9:
    __quex_debug("* TERMINAL <LOOP EXIT>\n");
    --(me->buffer._read_p);

__QUEX_IF_COUNT_COLUMNS_ADD((size_t)(((me->buffer._read_p) - count_reference_p)));

goto _0;

_10:
    __quex_debug("* TERMINAL <LOOP 6>\n");
__QUEX_IF_COUNT_LINES_ADD((size_t)1);

    __QUEX_IF_COUNT_COLUMNS((me->counter._column_number_at_end) = (size_t)1);

__QUEX_IF_COUNT_COLUMNS(count_reference_p = (me->buffer._read_p));

if( me->buffer._read_p != LexemeEnd ) goto _8;

goto _0;

_11:
    __quex_debug("* TERMINAL <LOOP 7>\n");
__QUEX_IF_COUNT_COLUMNS_ADD((size_t)(((me->buffer._read_p) - count_reference_p - 1)));

__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end -= 1);
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end &= ~ ((size_t)0x3));
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end += 4 + 1);

__QUEX_IF_COUNT_COLUMNS(count_reference_p = (me->buffer._read_p));

if( me->buffer._read_p != LexemeEnd ) goto _8;

goto _0;

_12:
    __quex_debug("* TERMINAL <LOOP 8>\n");
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
#endif /* QUEX_OPTION_COUNTER */

#include "test_environment/lib/buffer/Buffer"
#include "test_environment/lib/token/TokenQueue"

#ifdef    CONTINUE
#   undef CONTINUE
#endif
#define   CONTINUE do { goto _17; } while(0)

#ifdef    RETURN
#   undef RETURN
#endif
#define   RETURN   do { goto _16; } while(0)

void  
QUEX_NAME(M_analyzer_function)(QUEX_TYPE_ANALYZER* me) 
{
    /* NOTE: Different modes correspond to different analyzer functions. The 
     *       analyzer functions are all located inside the main class as static
     *       functions. That means, they are something like 'globals'. They 
     *       receive a pointer to the lexical analyzer, since static members do
     *       not have access to the 'this' pointer.                          */
#   ifdef     self
#       undef self
#   endif
#   define self (*((QUEX_TYPE_ANALYZER*)me))
#   define M    (&QUEX_NAME(M))
/*  'QUEX_GOTO_STATE' requires 'QUEX_LABEL_STATE_ROUTER' */
#   define QUEX_LABEL_STATE_ROUTER _20

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
#   if defined(QUEX_OPTION_ASSERTS)
    me->DEBUG_analyzer_function_at_entry = me->current_analyzer_function;
#   endif
_19:
    me->buffer._lexeme_start_p = me->buffer._read_p;
    QUEX_LEXEME_TERMINATING_ZERO_UNDO(&me->buffer);
_6:
    /* (19 from BEFORE_ENTRY) (19 from RELOAD_FORWARD)  */

    input = *(me->buffer._read_p);


    __quex_debug_init_state(19);
if     ( input == 0x58 )  goto _7;
else if( input == 0x0 )   goto _10;
else                      goto _8;


    __quex_assert_no_passage();
_9:
    /* (DROP_OUT from 20)  */
goto _0;
_13:
    __quex_debug("Drop-Out Catcher\n");


    __quex_assert_no_passage();
_8:
    /* (DROP_OUT from 19)  */
    me->buffer._read_p = me->buffer._lexeme_start_p + 1;
goto _4;
    goto _13;


    __quex_assert_no_passage();
_7:
    /* (20 from 19)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(20);
goto _9;

    /* (*) Terminal states _______________________________________________________
     *
     * States that implement actions of the 'winner patterns.                     */
_1:
    __quex_debug("* TERMINAL BAD_LEXATOM\n");
QUEX_FUNCTION_COUNT_ARBITRARY(&self, LexemeBegin, LexemeEnd);
{
self.error_code_set_if_first(&self, E_Error_OnBadLexatom);
self.error_code_set_if_first(&self, E_Error_NoHandler_OnBadLexatom);
self.send(&self, QUEX_TOKEN_ID(TERMINATION));
__QUEX_PURE_RETURN;;

}
    /* Bad lexatom detection FORCES a return from the lexical analyzer, so that no
     * tokens can be filled after the termination token.
     */
__QUEX_PURE_RETURN;
_2:
    __quex_debug("* TERMINAL LOAD_FAILURE\n");
QUEX_FUNCTION_COUNT_ARBITRARY(&self, LexemeBegin, LexemeEnd);
{
self.error_code_set_if_first(&self, E_Error_OnLoadFailure);
self.error_code_set_if_first(&self, E_Error_NoHandler_OnLoadFailure);
self.send(&self, QUEX_TOKEN_ID(TERMINATION));
__QUEX_PURE_RETURN;;

}
    /* Load failure FORCES a return from the lexical analyzer, so that no
     * tokens can be filled after the termination token.
     */
__QUEX_PURE_RETURN;
_3:
    __quex_debug("* TERMINAL END_OF_STREAM\n");
QUEX_FUNCTION_COUNT_ARBITRARY(&self, LexemeBegin, LexemeEnd);
{
self.send(&self, QUEX_TOKEN_ID(TERMINATION));

}
    /* End of Stream FORCES a return from the lexical analyzer, so that no
     * tokens can be filled after the termination token.
     */
__QUEX_PURE_RETURN;
_4:
    __quex_debug("* TERMINAL FAILURE\n");
QUEX_FUNCTION_COUNT_ARBITRARY(&self, LexemeBegin, LexemeEnd);
{
self.error_code_set_if_first(&self, E_Error_NoHandler_OnFailure);
self.send(&self, QUEX_TOKEN_ID(TERMINATION));
__QUEX_PURE_RETURN;;

}
__QUEX_PURE_RETURN;
_5:
    __quex_debug("* TERMINAL SKIP_RANGE_OPEN\n");
QUEX_FUNCTION_COUNT_ARBITRARY(&self, LexemeBegin, LexemeEnd);
{
#define Counter counter
self.error_code_set_if_first(&self, E_Error_OnSkipRangeOpen);
self.error_code_set_if_first(&self, E_Error_NoHandler_OnSkipRangeOpen);
self.send(&self, QUEX_TOKEN_ID(TERMINATION));
__QUEX_PURE_RETURN;;

}
    /* End of Stream appeared, while scanning for end of skip-range.
     */
__QUEX_PURE_RETURN;
_0:
    __quex_debug("* TERMINAL X\n");
__QUEX_IF_COUNT_SHIFT_VALUES();
__QUEX_IF_COUNT_COLUMNS_ADD(1);
{

#   line 2 "test_environment/nothing.qx"
self.send(&self, QUEX_TKN_X);
__QUEX_PURE_RETURN;


#   line 626 "test_environment/TestAnalyzer.c"

}
RETURN;
if(0) {
    /* Avoid unreferenced labels. */
    goto _1;
    goto _2;
    goto _3;
    goto _4;
    goto _5;
    goto _0;
}
#   ifndef QUEX_OPTION_COMPUTED_GOTOS
    __quex_assert_no_passage();
_20:
switch( target_state_index ) {
case 3: {
goto _3;}
case 6: {
goto _6;}
default: {
goto _6;}
}
#   endif /* QUEX_OPTION_COMPUTED_GOTOS */


    __quex_assert_no_passage();
_10:
    /* (RELOAD_FORWARD from 19)  */
    target_state_index = QUEX_LABEL(6); target_state_else_index = QUEX_LABEL(3);



    __quex_debug3("RELOAD_FORWARD: success->%i; failure->%i", 
                  (int)target_state_index, (int)target_state_else_index);
    __quex_assert(*(me->buffer._read_p) == QUEX_SETTING_BUFFER_LIMIT_CODE);
    
    __quex_debug_reload_before();                 
    /* Callbacks: 'on_buffer_before_change()' and 'on_buffer_overflow()'
     * are called during load process upon occurrence.                        */
    load_result = QUEX_NAME(Buffer_load_forward)(&me->buffer, (QUEX_TYPE_LEXATOM**)position, PositionRegisterN);
    __quex_debug_reload_after(load_result);

    switch( load_result ) {
    case E_LoadResult_DONE:           QUEX_GOTO_STATE(target_state_index);      
    case E_LoadResult_NO_MORE_DATA:   QUEX_GOTO_STATE(target_state_else_index); 
    case E_LoadResult_ENCODING_ERROR: goto _1;
    case E_LoadResult_OVERFLOW:       QUEX_NAME(MF_error_code_set_if_first)(me, E_Error_Buffer_Overflow_LexemeTooLong); RETURN;
    default:                          __quex_assert(false);
    }

_16:
/* RETURN -- after executing 'on_after_match' code. */
    __QUEX_PURE_RETURN;


_17:
/* CONTINUE -- after executing 'on_after_match' code. */

_18:
/* CONTINUE -- without executing 'on_after_match' (e.g. on FAILURE). */


    /* Mode change = another function takes over the analysis.
     * => After mode change the analyzer function needs to be quit!
     * ASSERT: 'CONTINUE' after mode change is not allowed.                   */
    __quex_assert(   me->DEBUG_analyzer_function_at_entry 
                  == me->current_analyzer_function);


    if( QUEX_NAME(TokenQueue_is_full)(&self._token_queue) ) {
        return;
    }


goto _19;

    __quex_assert_no_passage();

    /* Following labels are referenced in macros. It cannot be detected
     * whether the macros are applied in user code or not. To avoid compiler.
     * warnings of unused labels, they are referenced in unreachable code.   */
    goto _16; /* in RETURN                */
    goto _17; /* in CONTINUE              */
    goto _18; /* in CONTINUE and skippers */
#   if ! defined(QUEX_OPTION_COMPUTED_GOTOS)
    goto _20; /* in QUEX_GOTO_STATE       */
#   endif

    /* Prevent compiler warning 'unused variable'.                           */
    (void)QUEX_LEXEME_NULL;
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


QUEX_NAMESPACE_MAIN_OPEN

#if defined(__QUEX_OPTION_PLAIN_C)
QUEX_INLINE void
QUEX_NAME(member_functions_assign)(QUEX_TYPE_ANALYZER* me)
{
    me->run = QUEX_NAME(MF_run);
    me->receive = QUEX_NAME(MF_receive);
    me->token_p = QUEX_NAME(MF_token_p);
    me->send = QUEX_NAME(MF_send);
    me->send_n = QUEX_NAME(MF_send_n);
    me->send_text = QUEX_NAME(MF_send_text);
    me->send_string = QUEX_NAME(MF_send_string);
    me->tell = QUEX_NAME(MF_tell);
    me->seek = QUEX_NAME(MF_seek);
    me->seek_forward = QUEX_NAME(MF_seek_forward);
    me->seek_backward = QUEX_NAME(MF_seek_backward);
    me->undo = QUEX_NAME(MF_undo);
    me->undo_n = QUEX_NAME(MF_undo_n);
    me->mode = QUEX_NAME(MF_mode);
    me->set_mode_brutally = QUEX_NAME(MF_set_mode_brutally);
    me->enter_mode = QUEX_NAME(MF_enter_mode);
    me->pop_mode = QUEX_NAME(MF_pop_mode);
    me->pop_drop_mode = QUEX_NAME(MF_pop_drop_mode);
    me->push_mode = QUEX_NAME(MF_push_mode);
    me->version = QUEX_NAME(MF_version);
    me->print_this = QUEX_NAME(MF_print_this);
    me->input_name = QUEX_NAME(MF_input_name);
    me->input_name_set = QUEX_NAME(MF_input_name_set);
    me->byte_order_reversion = QUEX_NAME(MF_byte_order_reversion);
    me->byte_order_reversion_set = QUEX_NAME(MF_byte_order_reversion_set);
    me->error_code_clear = QUEX_NAME(MF_error_code_clear);
    me->error_code_is_void = QUEX_NAME(MF_error_code_is_void);
    me->error_code_set_void = QUEX_NAME(MF_error_code_set_void);
    me->error_code_set_if_first = QUEX_NAME(MF_error_code_set_if_first);
}
#endif

bool
QUEX_NAME(user_constructor)(QUEX_TYPE_ANALYZER* me)
{
    (void)me;

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

void
QUEX_NAME(user_print)(QUEX_TYPE_ANALYZER* me)
{
    (void)me;

#define self  (*(QUEX_TYPE_DERIVED_ANALYZER*)me)
/* START: User's constructor extensions _______________________________________*/

/* END: _______________________________________________________________________*/
#undef self
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

#include "test_environment/TestAnalyzer-token.h"
#include "test_environment/lib/definitions"

#include "test_environment/TestAnalyzer-token.h"

QUEX_INLINE void 
quex_Token_set(quex_Token*            __this, 
                 const QUEX_TYPE_TOKEN_ID ID) 
{ __this->id = ID; }

QUEX_INLINE void 
quex_Token_construct(quex_Token* __this)
{
#   define self (*__this)
#   define LexemeNull  (&QUEX_NAME_TOKEN(LexemeNull))
    (void)__this;

#   line 25 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

       self.number = 0;
       self.text   = LexemeNull;
   

#   line 892 "test_environment/TestAnalyzer.c"

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
#   define LexemeNull  (&QUEX_NAME_TOKEN(LexemeNull))
    if( ! __this ) return;


#   line 30 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

       if( self.text != LexemeNull ) {
           QUEXED(MemoryManager_free)((void*)self.text,
                                      E_MemoryObjectType_TEXT);
           self.text = LexemeNull;
       }
   

#   line 923 "test_environment/TestAnalyzer.c"

#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE void
quex_Token_copy(quex_Token*       __this, 
                  const quex_Token* __That)
{
#   define self  (*__this)
#   define Other (*__That)
#   define LexemeNull  (&QUEX_NAME_TOKEN(LexemeNull))
    (void)__this;
    (void)__That;

#   line 38 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

        self.id  = Other.id;

        if( self.text != LexemeNull ) {
            QUEXED(MemoryManager_free)((void*)self.text, E_MemoryObjectType_TEXT);
        }
        if( Other.text != LexemeNull ) {
            self.text = QUEX_NAME_TOKEN(lexeme_clone)(self.text, 
                                                      QUEX_NAME_TOKEN(lexeme_length)(Other.text));
            if( ! self.text ) self.text = LexemeNull;
        }
        self.number = Other.number;
    #   ifdef     QUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN
        __QUEX_IF_COUNT_LINES(self._line_n     = Other._line_n);
        __QUEX_IF_COUNT_COLUMNS(self._column_n = Other._column_n);
    #   endif
   

#   line 958 "test_environment/TestAnalyzer.c"

#   undef  LexemeNull
#   undef  Other
#   undef  self
    /* If the user even misses to copy the token id, then there's
     * something seriously wrong.                                 */
    __quex_assert(__this->id == __That->id);
#   ifdef QUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN
    __QUEX_IF_COUNT_LINES(__quex_assert(__this->_line_n == __That->_line_n));
    __QUEX_IF_COUNT_COLUMNS(__quex_assert(__this->_column_n == __That->_column_n));
#   endif
}


#ifdef QUEX_OPTION_TOKEN_TAKE_TEXT_SUPPORT
QUEX_INLINE bool 
quex_Token_take_text(quex_Token*            __this, 
                       const QUEX_TYPE_LEXATOM* Begin, 
                       const QUEX_TYPE_LEXATOM* End)
/* RETURNS: true -- if the token claims ownership over the given memory.
 *          false -- if no ownership is claimed.                             */
{
#   define self       (*__this)
#   ifdef  LexemeNull
#   error  "Error LexemeNull shall not be defined here."
#   endif
#   define LexemeNull  (&QUEX_NAME_TOKEN(LexemeNull))
    (void)__this;
    (void)Begin;
    (void)End;

#   line 56 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"


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
            QUEXED(MemoryManager_free)((void*)self.text, E_MemoryObjectType_TEXT);
        }
        if( Begin != LexemeNull ) {
            __quex_assert(End >= Begin);
            self.text = QUEX_NAME_TOKEN(lexeme_clone)(Begin, (size_t)(End - Begin));
            if( ! self.text ) self.text = LexemeNull;
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
   

#   line 1040 "test_environment/TestAnalyzer.c"

#   undef  LexemeNull
#   undef  self
    /* Default: no ownership.                                                */
    return false;
}
#endif

#ifdef QUEX_OPTION_TOKEN_REPETITION_SUPPORT
QUEX_INLINE size_t 
quex_Token_repetition_n_get(quex_Token* __this)
{
#   define self        (*__this)
#   define LexemeNull  (&QUEX_NAME_TOKEN(LexemeNull))
    (void)__this;

#   line 113 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

       return self.number;
   

#   line 1062 "test_environment/TestAnalyzer.c"

#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE void 
quex_Token_repetition_n_set(quex_Token* __this, size_t N)
{
#   define self        (*__this)
#   define LexemeNull  (&QUEX_NAME_TOKEN(LexemeNull))
    (void)__this;
    (void)N;

#   line 109 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

       self.number = N;
   

#   line 1081 "test_environment/TestAnalyzer.c"

#   undef  LexemeNull
#   undef  self
}
#endif /* QUEX_OPTION_TOKEN_REPETITION_SUPPORT */

QUEX_INLINE const char*
quex_Token_map_id_to_name(const QUEX_TYPE_TOKEN_ID TokenID)
{
   static char  error_string[64];

   /* NOTE: This implementation works only for token id types that are 
    *       some type of integer or enum. In case an alien type is to
    *       used, this function needs to be redefined.                  */
   switch( TokenID ) {
   default: {
       __QUEX_STD_sprintf(error_string, "<UNKNOWN TOKEN-ID: %i>", (int)TokenID);
       return error_string;
   }

   case QUEX_TKN_TERMINATION:    return "<TERMINATION>";
   case QUEX_TKN_UNINITIALIZED:  return "<UNINITIALIZED>";
#  if defined(QUEX_OPTION_INDENTATION_TRIGGER)
   case QUEX_TKN_INDENT:         return "<INDENT>";
   case QUEX_TKN_DEDENT:         return "<DEDENT>";
   case QUEX_TKN_NODENT:         return "<NODENT>";
#  endif
   case QUEX_TKN_X:             return "X";


   }
}


#   line 117 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

        const char* 
        quex_Token_get_string(quex_Token* me, char*   buffer, size_t  BufferSize) 
        {
            const char*  token_id_str = quex_Token_map_id_to_name(me->id);
            const char*  BufferEnd    = buffer + BufferSize;
            char*        writerator   = 0;

            if( ! BufferSize ) return NULL;

            /* Token Type */
            writerator = buffer; 
            writerator += __QUEX_STD_strlcpy(writerator, token_id_str, 
                                             BufferEnd - writerator);

            /* Opening Quote */
            if( BufferEnd - writerator > 2 ) {
                *writerator++ = ' ';
                *writerator++ = '\'';
            }

            /* The String */
            QUEX_NAME_TOKEN(lexeme_to_pretty_char)(me->text, writerator, 
                                                   (size_t)(BufferEnd - writerator));
            while( *writerator ) ++writerator;

            /* Closing Quote */
            if( BufferEnd - writerator > 1 ) {
                *writerator++ = '\'';
            }
            *writerator = '\0';
            return buffer;
        }

#include "lib/lexeme_converter/from-unicode-buffer.i"
#include "test_environment/lib/lexeme.i"
   

#   line 1155 "test_environment/TestAnalyzer.c"


#include "test_environment/lib/lexeme.i"

#endif /* __QUEX_INCLUDE_GUARD__TOKEN__GENERATED__QUEX___TOKEN_I */
QUEX_NAMESPACE_TOKEN_OPEN
QUEX_TYPE_LEXATOM   QUEX_NAME_TOKEN(LexemeNull) = (QUEX_TYPE_LEXATOM)0;
QUEX_NAMESPACE_TOKEN_CLOSE




bool UserConstructor_UnitTest_return_value = true;
bool UserReset_UnitTest_return_value       = true;
bool UserMementoPack_UnitTest_return_value = true;
