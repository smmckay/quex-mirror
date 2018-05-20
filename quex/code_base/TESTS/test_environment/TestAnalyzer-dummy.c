
#include "test_environment/TestAnalyzer.h"
#include "test_environment/lib/analyzer/C-adaptions.h"
/* The file 'multi.i' contains implementations which are the same for all
* possibly generated analyzers. If QUEX_OPTION_MULTI is defined, it is
* NOT supposed to be included here. If not--in which case we have a single
* analzer--then it is included.                                             */
#include "test_environment/lib/single.i"


TestAnalyzer_Mode TestAnalyzer_M = {
/* name              */ "M",
#   if      defined(QUEX_OPTION_INDENTATION_TRIGGER) \
&& ! defined(QUEX_OPTION_INDENTATION_DEFAULT_HANDLER)
/* on_indentation    */ TestAnalyzer_Mode_on_indentation_null_function,
#   endif
/* on_entry          */ TestAnalyzer_Mode_on_entry_exit_null_function,
/* on_exit           */ TestAnalyzer_Mode_on_entry_exit_null_function,
#   if      defined(QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK)
/* has_base          */ TestAnalyzer_M_has_base,
/* has_entry_from    */ TestAnalyzer_M_has_entry_from,
/* has_exit_to       */ TestAnalyzer_M_has_exit_to,
#   endif
{
/* on_buffer_before_change */ TestAnalyzer_M_on_buffer_before_change,
/* on_buffer_overflow      */ TestAnalyzer_M_on_buffer_overflow,
/* aux                     */ (void*)0,
},

/* analyzer_function */ TestAnalyzer_M_analyzer_function
};
TestAnalyzer_Mode TestAnalyzer_M2 = {
/* name              */ "M2",
#   if      defined(QUEX_OPTION_INDENTATION_TRIGGER) \
&& ! defined(QUEX_OPTION_INDENTATION_DEFAULT_HANDLER)
/* on_indentation    */ TestAnalyzer_Mode_on_indentation_null_function,
#   endif
/* on_entry          */ TestAnalyzer_Mode_on_entry_exit_null_function,
/* on_exit           */ TestAnalyzer_Mode_on_entry_exit_null_function,
#   if      defined(QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK)
/* has_base          */ TestAnalyzer_M2_has_base,
/* has_entry_from    */ TestAnalyzer_M2_has_entry_from,
/* has_exit_to       */ TestAnalyzer_M2_has_exit_to,
#   endif
{
/* on_buffer_before_change */ TestAnalyzer_M2_on_buffer_before_change,
/* on_buffer_overflow      */ TestAnalyzer_M2_on_buffer_overflow,
/* aux                     */ (void*)0,
},

/* analyzer_function */ TestAnalyzer_M2_analyzer_function
};

#   ifdef     self
#       undef self
#   endif
#   define self (*((QUEX_TYPE_ANALYZER*)me))
#define LexemeNull  (&QUEX_LEXEME_NULL)
#define RETURN      return

void
TestAnalyzer_M_on_entry(QUEX_TYPE_ANALYZER* me, const TestAnalyzer_Mode* FromMode) {
(void)me;
(void)FromMode;
#   ifdef QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK
TestAnalyzer_M.has_entry_from(FromMode);
#   endif

}

void
TestAnalyzer_M_on_exit(QUEX_TYPE_ANALYZER* me, const TestAnalyzer_Mode* ToMode)  {
(void)me;
(void)ToMode;
#   ifdef QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK
TestAnalyzer_M.has_exit_to(ToMode);
#   endif

}


#if defined(QUEX_OPTION_INDENTATION_TRIGGER)
void
TestAnalyzer_M_on_indentation(QUEX_TYPE_ANALYZER*    me,
TestAnalyzer_indentation_t  Indentation,
TestAnalyzer_lexatom_t*     Begin)
{
(void)me;
(void)Indentation;
(void)Begin;
#   ifdef     self
#       undef self
#   endif
#   define self (*((QUEX_TYPE_ANALYZER*)me))

#   define M     (&TestAnalyzer_M)
#   define M2    (&TestAnalyzer_M2)

#   define Lexeme        Begin
#   define LexemeEnd     (me->buffer._read_p)

TestAnalyzer_IndentationStack*  stack = &me->counter._indentation_stack;
TestAnalyzer_indentation_t*        start = 0x0;
(void)start;

__quex_assert((long)Indentation >= 0);

if( Indentation > *(stack->back) ) {
++(stack->back);
if( stack->back == stack->memory_end ) {
TestAnalyzer_MF_error_code_set_if_first(me, E_Error_Indentation_StackOverflow);
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
TestAnalyzer_MF_error_code_set_if_first(me,
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
#   undef M
#   undef M2

}
#endif


#ifdef QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK
bool
TestAnalyzer_M_has_base(const TestAnalyzer_Mode* Mode) {
(void)Mode;
return false;
}

bool
TestAnalyzer_M_has_entry_from(const TestAnalyzer_Mode* Mode) {
(void)Mode;
if( Mode == &TestAnalyzer_M ) {

return true;

}

else if( Mode == &TestAnalyzer_M2 ) {

return true;

}

else if( Mode->has_base(&TestAnalyzer_M) ) {

return true;

}

else if( Mode->has_base(&TestAnalyzer_M2) ) {

return true;

}

else {
return false;
}
}

bool
TestAnalyzer_M_has_exit_to(const TestAnalyzer_Mode* Mode) {
(void)Mode;
if( Mode == &TestAnalyzer_M ) {

return true;

}

else if( Mode == &TestAnalyzer_M2 ) {

return true;

}

else if( Mode->has_base(&TestAnalyzer_M) ) {

return true;

}

else if( Mode->has_base(&TestAnalyzer_M2) ) {

return true;

}

else {
return false;
}
}
#endif

void
TestAnalyzer_M_on_buffer_before_change(void* me /* 'aux' -> 'self' via 'me' */)
{
const TestAnalyzer_lexatom_t* BufferBegin = self.buffer.begin(&self.buffer);
const TestAnalyzer_lexatom_t* BufferEnd   = self.buffer.end(&self.buffer);
(void)me; (void)BufferBegin; (void)BufferEnd;

}

static void
TestAnalyzer_Buffer_print_overflow_message(TestAnalyzer_Buffer* buffer);

void
TestAnalyzer_M_on_buffer_overflow(void*  me /* 'aux' -> 'self' via 'me' */)
{
const TestAnalyzer_lexatom_t* LexemeBegin = self.buffer._lexeme_start_p;
const TestAnalyzer_lexatom_t* LexemeEnd   = self.buffer._read_p;
const size_t             BufferSize  = (size_t)(self.buffer.size(&self.buffer));


/* Try to double the size of the buffer, by default.                      */
if( ! TestAnalyzer_Buffer_nested_negotiate_extend(&self.buffer, 2.0) ) {
TestAnalyzer_MF_error_code_set_if_first(&self, E_Error_Buffer_Overflow_LexemeTooLong);
TestAnalyzer_Buffer_print_overflow_message(&self.buffer);
}

(void)me; (void)LexemeBegin; (void)LexemeEnd; (void)BufferSize;
}

void
TestAnalyzer_M2_on_entry(QUEX_TYPE_ANALYZER* me, const TestAnalyzer_Mode* FromMode) {
(void)me;
(void)FromMode;
#   ifdef QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK
TestAnalyzer_M2.has_entry_from(FromMode);
#   endif

}

void
TestAnalyzer_M2_on_exit(QUEX_TYPE_ANALYZER* me, const TestAnalyzer_Mode* ToMode)  {
(void)me;
(void)ToMode;
#   ifdef QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK
TestAnalyzer_M2.has_exit_to(ToMode);
#   endif

}


#if defined(QUEX_OPTION_INDENTATION_TRIGGER)
void
TestAnalyzer_M2_on_indentation(QUEX_TYPE_ANALYZER*    me,
TestAnalyzer_indentation_t  Indentation,
TestAnalyzer_lexatom_t*     Begin)
{
(void)me;
(void)Indentation;
(void)Begin;
#   ifdef     self
#       undef self
#   endif
#   define self (*((QUEX_TYPE_ANALYZER*)me))

#   define M     (&TestAnalyzer_M)
#   define M2    (&TestAnalyzer_M2)

#   define Lexeme        Begin
#   define LexemeEnd     (me->buffer._read_p)

TestAnalyzer_IndentationStack*  stack = &me->counter._indentation_stack;
TestAnalyzer_indentation_t*        start = 0x0;
(void)start;

__quex_assert((long)Indentation >= 0);

if( Indentation > *(stack->back) ) {
++(stack->back);
if( stack->back == stack->memory_end ) {
TestAnalyzer_MF_error_code_set_if_first(me, E_Error_Indentation_StackOverflow);
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
TestAnalyzer_MF_error_code_set_if_first(me,
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
#   undef M
#   undef M2

}
#endif


#ifdef QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK
bool
TestAnalyzer_M2_has_base(const TestAnalyzer_Mode* Mode) {
(void)Mode;
return false;
}

bool
TestAnalyzer_M2_has_entry_from(const TestAnalyzer_Mode* Mode) {
(void)Mode;
if( Mode == &TestAnalyzer_M ) {

return true;

}

else if( Mode == &TestAnalyzer_M2 ) {

return true;

}

else if( Mode->has_base(&TestAnalyzer_M) ) {

return true;

}

else if( Mode->has_base(&TestAnalyzer_M2) ) {

return true;

}

else {
return false;
}
}

bool
TestAnalyzer_M2_has_exit_to(const TestAnalyzer_Mode* Mode) {
(void)Mode;
if( Mode == &TestAnalyzer_M ) {

return true;

}

else if( Mode == &TestAnalyzer_M2 ) {

return true;

}

else if( Mode->has_base(&TestAnalyzer_M) ) {

return true;

}

else if( Mode->has_base(&TestAnalyzer_M2) ) {

return true;

}

else {
return false;
}
}
#endif

void
TestAnalyzer_M2_on_buffer_before_change(void* me /* 'aux' -> 'self' via 'me' */)
{
const TestAnalyzer_lexatom_t* BufferBegin = self.buffer.begin(&self.buffer);
const TestAnalyzer_lexatom_t* BufferEnd   = self.buffer.end(&self.buffer);
(void)me; (void)BufferBegin; (void)BufferEnd;

}

static void
TestAnalyzer_Buffer_print_overflow_message(TestAnalyzer_Buffer* buffer);

void
TestAnalyzer_M2_on_buffer_overflow(void*  me /* 'aux' -> 'self' via 'me' */)
{
const TestAnalyzer_lexatom_t* LexemeBegin = self.buffer._lexeme_start_p;
const TestAnalyzer_lexatom_t* LexemeEnd   = self.buffer._read_p;
const size_t             BufferSize  = (size_t)(self.buffer.size(&self.buffer));


/* Try to double the size of the buffer, by default.                      */
if( ! TestAnalyzer_Buffer_nested_negotiate_extend(&self.buffer, 2.0) ) {
TestAnalyzer_MF_error_code_set_if_first(&self, E_Error_Buffer_Overflow_LexemeTooLong);
TestAnalyzer_Buffer_print_overflow_message(&self.buffer);
}

(void)me; (void)LexemeBegin; (void)LexemeEnd; (void)BufferSize;
}
#undef self
#undef LexemeNull
#undef RETURN


/* #include "test_environment/test_environment/TestAnalyzer.h"*/
#include "test_environment/lib/analyzer/headers.i"
#include "test_environment/lib/analyzer/C-adaptions.h"


/* START: User defined header content _________________________________________
*        The 'footer' content relies on class definitions made above.        */



#ifdef      QUEX_FUNCTION_COUNT_ARBITRARY
#   undef   QUEX_FUNCTION_COUNT_ARBITRARY
#endif
#ifdef      QUEX_OPTION_COUNTER
#    define QUEX_FUNCTION_COUNT_ARBITRARY(ME, BEGIN, END) \
do {                              \
TestAnalyzer_M_counter((ME), (BEGIN), (END));     \
__quex_debug_counter();       \
} while(0)
#else
#    define QUEX_FUNCTION_COUNT_ARBITRARY(ME, BEGIN, END) /* empty */
#endif
#ifdef QUEX_OPTION_COUNTER
static void
TestAnalyzer_M_counter(QUEX_TYPE_ANALYZER* me, TestAnalyzer_lexatom_t* LexemeBegin, TestAnalyzer_lexatom_t* LexemeEnd)
{
#   define self (*me)
/*  'QUEX_GOTO_STATE' requires 'QUEX_LABEL_STATE_ROUTER' */
#   define QUEX_LABEL_STATE_ROUTER _18
TestAnalyzer_lexatom_t              input                          = (TestAnalyzer_lexatom_t)(0x00);
QUEX_TYPE_GOTO_LABEL           target_state_else_index        = QUEX_GOTO_LABEL_VOID;
QUEX_TYPE_GOTO_LABEL           target_state_index             = QUEX_GOTO_LABEL_VOID;
#   ifdef QUEX_OPTION_COUNTER_COLUMN
TestAnalyzer_lexatom_t*             count_reference_p              = (TestAnalyzer_lexatom_t*)0x0;
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

/* (43 from BEFORE_ENTRY)  */
__QUEX_IF_COUNT_COLUMNS(count_reference_p = (me->buffer._read_p));

__QUEX_IF_COUNT_COLUMNS(count_reference_p = (me->buffer._read_p));

input = *(me->buffer._read_p);

_13:
__quex_debug_init_state(43);
if     ( input >= 0xB )  goto _4;
else if( input == 0xA )  goto _2;
else if( input == 0x9 )  goto _3;
else                     goto _4;


__quex_assert_no_passage();
_8:
/* (43 from 48)  */
goto _13;


__quex_assert_no_passage();
_5:
/* (DROP_OUT from 44)  */
goto _10;

__quex_debug("Drop-Out Catcher\n");


__quex_assert_no_passage();
_6:
/* (DROP_OUT from 45)  */
goto _11;


__quex_assert_no_passage();
_7:
/* (DROP_OUT from 46)  */
goto _12;


__quex_assert_no_passage();
_2:
/* (44 from 43)  */
++(me->buffer._read_p);

input = *(me->buffer._read_p);


__quex_debug_state(44);
goto _5;


__quex_assert_no_passage();
_3:
/* (45 from 43)  */
++(me->buffer._read_p);

input = *(me->buffer._read_p);


__quex_debug_state(45);
goto _6;


__quex_assert_no_passage();
_4:
/* (46 from 43)  */
++(me->buffer._read_p);

input = *(me->buffer._read_p);


__quex_debug_state(46);
goto _7;

/* (*) Terminal states _______________________________________________________
*
* States that implement actions of the 'winner patterns.                     */
_9:
__quex_debug("* TERMINAL <LOOP EXIT>\n");
--(me->buffer._read_p);

__QUEX_IF_COUNT_COLUMNS_ADD((size_t)(((me->buffer._read_p) - count_reference_p)));

goto _0;

_10:
__quex_debug("* TERMINAL <LOOP 10>\n");
__QUEX_IF_COUNT_LINES_ADD((size_t)1);

__QUEX_IF_COUNT_COLUMNS((me->counter._column_number_at_end) = (size_t)1);

__QUEX_IF_COUNT_COLUMNS(count_reference_p = (me->buffer._read_p));

if( me->buffer._read_p != LexemeEnd ) goto _8;

goto _0;

_11:
__quex_debug("* TERMINAL <LOOP 11>\n");
__QUEX_IF_COUNT_COLUMNS_ADD((size_t)(((me->buffer._read_p) - count_reference_p - 1)));

__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end -= 1);
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end &= ~ ((size_t)0x3));
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end += 4 + 1);

__QUEX_IF_COUNT_COLUMNS(count_reference_p = (me->buffer._read_p));

if( me->buffer._read_p != LexemeEnd ) goto _8;

goto _0;

_12:
__quex_debug("* TERMINAL <LOOP 12>\n");
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
TestAnalyzer_M_analyzer_function(QUEX_TYPE_ANALYZER* me)
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
#   define M     (&TestAnalyzer_M)
#   define M2    (&TestAnalyzer_M2)
/*  'QUEX_GOTO_STATE' requires 'QUEX_LABEL_STATE_ROUTER' */
#   define QUEX_LABEL_STATE_ROUTER _20

/* Lexeme setup:
*
* There is a temporary zero stored at the end of each lexeme, if the action
* references to the 'Lexeme'. 'LexemeNull' provides a reference to an empty
* zero terminated string.                                                    */
#if defined(QUEX_OPTION_ASSERTS)
#   define Lexeme       TestAnalyzer_access_Lexeme((const char*)__FILE__, (size_t)__LINE__, &me->buffer)
#   define LexemeBegin  TestAnalyzer_access_LexemeBegin((const char*)__FILE__, (size_t)__LINE__, &me->buffer)
#   define LexemeL      TestAnalyzer_access_LexemeL((const char*)__FILE__, (size_t)__LINE__, &me->buffer)
#   define LexemeEnd    TestAnalyzer_access_LexemeEnd((const char*)__FILE__, (size_t)__LINE__, &me->buffer)
#else
#   define Lexeme       (me->buffer._lexeme_start_p)
#   define LexemeBegin  Lexeme
#   define LexemeL      ((size_t)(me->buffer._read_p - me->buffer._lexeme_start_p))
#   define LexemeEnd    me->buffer._read_p
#endif

#define LexemeNull      (&QUEX_LEXEME_NULL)
E_LoadResult                   load_result                    = E_LoadResult_VOID;
TestAnalyzer_lexatom_t**            position                       = 0x0;
QUEX_TYPE_GOTO_LABEL           target_state_else_index        = QUEX_GOTO_LABEL_VOID;
const size_t                   PositionRegisterN              = (size_t)0;
TestAnalyzer_lexatom_t              input                          = (TestAnalyzer_lexatom_t)(0x00);
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
/* (38 from RELOAD_FORWARD) (38 from BEFORE_ENTRY)  */

input = *(me->buffer._read_p);


__quex_debug_init_state(38);
if     ( input == 0x58 )  goto _7;
else if( input == 0x0 )   goto _10;
else                      goto _8;


__quex_assert_no_passage();
_9:
/* (DROP_OUT from 39)  */
goto _0;
_13:
__quex_debug("Drop-Out Catcher\n");


__quex_assert_no_passage();
_8:
/* (DROP_OUT from 38)  */
me->buffer._read_p = me->buffer._lexeme_start_p + 1;
goto _4;
goto _13;


__quex_assert_no_passage();
_7:
/* (39 from 38)  */
++(me->buffer._read_p);

input = *(me->buffer._read_p);


__quex_debug_state(39);
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
return;;

}
/* Bad lexatom detection FORCES a return from the lexical analyzer, so that no
* tokens can be filled after the termination token.
*/
return;
_2:
__quex_debug("* TERMINAL LOAD_FAILURE\n");
QUEX_FUNCTION_COUNT_ARBITRARY(&self, LexemeBegin, LexemeEnd);
{
self.error_code_set_if_first(&self, E_Error_OnLoadFailure);
self.error_code_set_if_first(&self, E_Error_NoHandler_OnLoadFailure);
self.send(&self, QUEX_TOKEN_ID(TERMINATION));
return;;

}
/* Load failure FORCES a return from the lexical analyzer, so that no
* tokens can be filled after the termination token.
*/
return;
_3:
__quex_debug("* TERMINAL END_OF_STREAM\n");
QUEX_FUNCTION_COUNT_ARBITRARY(&self, LexemeBegin, LexemeEnd);
{
self.send(&self, QUEX_TOKEN_ID(TERMINATION));

}
/* End of Stream FORCES a return from the lexical analyzer, so that no
* tokens can be filled after the termination token.
*/
return;
_4:
__quex_debug("* TERMINAL FAILURE\n");
QUEX_FUNCTION_COUNT_ARBITRARY(&self, LexemeBegin, LexemeEnd);
{
self.error_code_set_if_first(&self, E_Error_NoHandler_OnFailure);
self.send(&self, QUEX_TOKEN_ID(TERMINATION));
return;;

}
return;
_5:
__quex_debug("* TERMINAL SKIP_RANGE_OPEN\n");
QUEX_FUNCTION_COUNT_ARBITRARY(&self, LexemeBegin, LexemeEnd);
{
#define Counter counter
self.error_code_set_if_first(&self, E_Error_OnSkipRangeOpen);
self.error_code_set_if_first(&self, E_Error_NoHandler_OnSkipRangeOpen);
self.send(&self, QUEX_TOKEN_ID(TERMINATION));
return;;

}
/* End of Stream appeared, while scanning for end of skip-range.
*/
return;
_0:
__quex_debug("* TERMINAL X\n");
__QUEX_IF_COUNT_SHIFT_VALUES();
__QUEX_IF_COUNT_COLUMNS_ADD(1);
{

#   line 3 "test_environment/nothing.qx"
self.send(&self, QUEX_TKN_X);
return;


#   line 885 "test_environment/TestAnalyzer.c"


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
/* (RELOAD_FORWARD from 38)  */
target_state_index = QUEX_LABEL(6); target_state_else_index = QUEX_LABEL(3);



__quex_debug3("RELOAD_FORWARD: success->%i; failure->%i",
(int)target_state_index, (int)target_state_else_index);
__quex_assert(*(me->buffer._read_p) == QUEX_SETTING_BUFFER_LIMIT_CODE);

__quex_debug_reload_before();
/* Callbacks: 'on_buffer_before_change()' and 'on_buffer_overflow()'
* are called during load process upon occurrence.                        */
load_result = TestAnalyzer_Buffer_load_forward(&me->buffer, (TestAnalyzer_lexatom_t**)position, PositionRegisterN);
__quex_debug_reload_after(load_result);

switch( load_result ) {
case E_LoadResult_DONE:           QUEX_GOTO_STATE(target_state_index);
case E_LoadResult_NO_MORE_DATA:   QUEX_GOTO_STATE(target_state_else_index);
case E_LoadResult_ENCODING_ERROR: goto _1;
case E_LoadResult_OVERFLOW:       TestAnalyzer_MF_error_code_set_if_first(me, E_Error_Buffer_Overflow_LexemeTooLong); RETURN;
default:                          __quex_assert(false);
}

_16:
/* RETURN -- after executing 'on_after_match' code. */
return;


_17:
/* CONTINUE -- after executing 'on_after_match' code. */

_18:
/* CONTINUE -- without executing 'on_after_match' (e.g. on FAILURE). */


/* Mode change = another function takes over the analysis.
* => After mode change the analyzer function needs to be quit!
* ASSERT: 'CONTINUE' after mode change is not allowed.                   */
__quex_assert(   me->DEBUG_analyzer_function_at_entry
== me->current_analyzer_function);


if( TestAnalyzer_TokenQueue_is_full(&self._token_queue) ) {
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
#   undef M2
#   undef self
#   undef QUEX_LABEL_STATE_ROUTER
}
#ifdef      QUEX_FUNCTION_COUNT_ARBITRARY
#   undef   QUEX_FUNCTION_COUNT_ARBITRARY
#endif
#ifdef      QUEX_OPTION_COUNTER
#    define QUEX_FUNCTION_COUNT_ARBITRARY(ME, BEGIN, END) \
do {                              \
TestAnalyzer_M_counter((ME), (BEGIN), (END));     \
__quex_debug_counter();       \
} while(0)
#else
#    define QUEX_FUNCTION_COUNT_ARBITRARY(ME, BEGIN, END) /* empty */
#endif

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
TestAnalyzer_M2_analyzer_function(QUEX_TYPE_ANALYZER* me)
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
#   define M     (&TestAnalyzer_M)
#   define M2    (&TestAnalyzer_M2)
/*  'QUEX_GOTO_STATE' requires 'QUEX_LABEL_STATE_ROUTER' */
#   define QUEX_LABEL_STATE_ROUTER _20

/* Lexeme setup:
*
* There is a temporary zero stored at the end of each lexeme, if the action
* references to the 'Lexeme'. 'LexemeNull' provides a reference to an empty
* zero terminated string.                                                    */
#if defined(QUEX_OPTION_ASSERTS)
#   define Lexeme       TestAnalyzer_access_Lexeme((const char*)__FILE__, (size_t)__LINE__, &me->buffer)
#   define LexemeBegin  TestAnalyzer_access_LexemeBegin((const char*)__FILE__, (size_t)__LINE__, &me->buffer)
#   define LexemeL      TestAnalyzer_access_LexemeL((const char*)__FILE__, (size_t)__LINE__, &me->buffer)
#   define LexemeEnd    TestAnalyzer_access_LexemeEnd((const char*)__FILE__, (size_t)__LINE__, &me->buffer)
#else
#   define Lexeme       (me->buffer._lexeme_start_p)
#   define LexemeBegin  Lexeme
#   define LexemeL      ((size_t)(me->buffer._read_p - me->buffer._lexeme_start_p))
#   define LexemeEnd    me->buffer._read_p
#endif

#define LexemeNull      (&QUEX_LEXEME_NULL)
E_LoadResult                   load_result                    = E_LoadResult_VOID;
TestAnalyzer_lexatom_t**            position                       = 0x0;
QUEX_TYPE_GOTO_LABEL           target_state_else_index        = QUEX_GOTO_LABEL_VOID;
const size_t                   PositionRegisterN              = (size_t)0;
TestAnalyzer_lexatom_t              input                          = (TestAnalyzer_lexatom_t)(0x00);
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
/* (40 from BEFORE_ENTRY) (40 from RELOAD_FORWARD)  */

input = *(me->buffer._read_p);


__quex_debug_init_state(40);
if     ( input == 0x58 )  goto _7;
else if( input == 0x0 )   goto _10;
else                      goto _8;


__quex_assert_no_passage();
_9:
/* (DROP_OUT from 41)  */
goto _0;
_13:
__quex_debug("Drop-Out Catcher\n");


__quex_assert_no_passage();
_8:
/* (DROP_OUT from 40)  */
me->buffer._read_p = me->buffer._lexeme_start_p + 1;
goto _4;
goto _13;


__quex_assert_no_passage();
_7:
/* (41 from 40)  */
++(me->buffer._read_p);

input = *(me->buffer._read_p);


__quex_debug_state(41);
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
return;;

}
/* Bad lexatom detection FORCES a return from the lexical analyzer, so that no
* tokens can be filled after the termination token.
*/
return;
_2:
__quex_debug("* TERMINAL LOAD_FAILURE\n");
QUEX_FUNCTION_COUNT_ARBITRARY(&self, LexemeBegin, LexemeEnd);
{
self.error_code_set_if_first(&self, E_Error_OnLoadFailure);
self.error_code_set_if_first(&self, E_Error_NoHandler_OnLoadFailure);
self.send(&self, QUEX_TOKEN_ID(TERMINATION));
return;;

}
/* Load failure FORCES a return from the lexical analyzer, so that no
* tokens can be filled after the termination token.
*/
return;
_3:
__quex_debug("* TERMINAL END_OF_STREAM\n");
QUEX_FUNCTION_COUNT_ARBITRARY(&self, LexemeBegin, LexemeEnd);
{
self.send(&self, QUEX_TOKEN_ID(TERMINATION));

}
/* End of Stream FORCES a return from the lexical analyzer, so that no
* tokens can be filled after the termination token.
*/
return;
_4:
__quex_debug("* TERMINAL FAILURE\n");
QUEX_FUNCTION_COUNT_ARBITRARY(&self, LexemeBegin, LexemeEnd);
{
self.error_code_set_if_first(&self, E_Error_NoHandler_OnFailure);
self.send(&self, QUEX_TOKEN_ID(TERMINATION));
return;;

}
return;
_5:
__quex_debug("* TERMINAL SKIP_RANGE_OPEN\n");
QUEX_FUNCTION_COUNT_ARBITRARY(&self, LexemeBegin, LexemeEnd);
{
#define Counter counter
self.error_code_set_if_first(&self, E_Error_OnSkipRangeOpen);
self.error_code_set_if_first(&self, E_Error_NoHandler_OnSkipRangeOpen);
self.send(&self, QUEX_TOKEN_ID(TERMINATION));
return;;

}
/* End of Stream appeared, while scanning for end of skip-range.
*/
return;
_0:
__quex_debug("* TERMINAL X\n");
__QUEX_IF_COUNT_SHIFT_VALUES();
__QUEX_IF_COUNT_COLUMNS_ADD(1);
{

#   line 4 "test_environment/nothing.qx"
self.send(&self, QUEX_TKN_X);
return;


#   line 1193 "test_environment/TestAnalyzer.c"


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
/* (RELOAD_FORWARD from 40)  */
target_state_index = QUEX_LABEL(6); target_state_else_index = QUEX_LABEL(3);



__quex_debug3("RELOAD_FORWARD: success->%i; failure->%i",
(int)target_state_index, (int)target_state_else_index);
__quex_assert(*(me->buffer._read_p) == QUEX_SETTING_BUFFER_LIMIT_CODE);

__quex_debug_reload_before();
/* Callbacks: 'on_buffer_before_change()' and 'on_buffer_overflow()'
* are called during load process upon occurrence.                        */
load_result = TestAnalyzer_Buffer_load_forward(&me->buffer, (TestAnalyzer_lexatom_t**)position, PositionRegisterN);
__quex_debug_reload_after(load_result);

switch( load_result ) {
case E_LoadResult_DONE:           QUEX_GOTO_STATE(target_state_index);
case E_LoadResult_NO_MORE_DATA:   QUEX_GOTO_STATE(target_state_else_index);
case E_LoadResult_ENCODING_ERROR: goto _1;
case E_LoadResult_OVERFLOW:       TestAnalyzer_MF_error_code_set_if_first(me, E_Error_Buffer_Overflow_LexemeTooLong); RETURN;
default:                          __quex_assert(false);
}

_16:
/* RETURN -- after executing 'on_after_match' code. */
return;


_17:
/* CONTINUE -- after executing 'on_after_match' code. */

_18:
/* CONTINUE -- without executing 'on_after_match' (e.g. on FAILURE). */


/* Mode change = another function takes over the analysis.
* => After mode change the analyzer function needs to be quit!
* ASSERT: 'CONTINUE' after mode change is not allowed.                   */
__quex_assert(   me->DEBUG_analyzer_function_at_entry
== me->current_analyzer_function);


if( TestAnalyzer_TokenQueue_is_full(&self._token_queue) ) {
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
#   undef M2
#   undef self
#   undef QUEX_LABEL_STATE_ROUTER
}





#if defined(__QUEX_OPTION_PLAIN_C)
static void
TestAnalyzer_member_functions_assign(QUEX_TYPE_ANALYZER* me)
{
me->reset = TestAnalyzer_MF_reset;
me->reset_file_name = TestAnalyzer_MF_reset_file_name;
me->reset_ByteLoader = TestAnalyzer_MF_reset_ByteLoader;
me->reset_memory = TestAnalyzer_MF_reset_memory;
me->include_push_file_name = TestAnalyzer_MF_include_push_file_name;
me->include_push_ByteLoader = TestAnalyzer_MF_include_push_ByteLoader;
me->include_push_memory = TestAnalyzer_MF_include_push_memory;
me->include_pop = TestAnalyzer_MF_include_pop;
me->include_stack_delete = TestAnalyzer_MF_include_stack_delete;
me->include_detect_recursion = TestAnalyzer_MF_include_detect_recursion;
me->run = TestAnalyzer_MF_run;
me->receive = TestAnalyzer_MF_receive;
me->token_p = TestAnalyzer_MF_token_p;
me->send = TestAnalyzer_MF_send;
me->send_n = TestAnalyzer_MF_send_n;
me->send_text = TestAnalyzer_MF_send_text;
me->send_string = TestAnalyzer_MF_send_string;
me->mode = TestAnalyzer_MF_mode;
me->set_mode_brutally = TestAnalyzer_MF_set_mode_brutally;
me->enter_mode = TestAnalyzer_MF_enter_mode;
me->pop_mode = TestAnalyzer_MF_pop_mode;
me->pop_drop_mode = TestAnalyzer_MF_pop_drop_mode;
me->push_mode = TestAnalyzer_MF_push_mode;
me->line_number = TestAnalyzer_MF_line_number;
me->line_number_at_begin = TestAnalyzer_MF_line_number_at_begin;
me->line_number_at_end = TestAnalyzer_MF_line_number_at_end;
me->line_number_set = TestAnalyzer_MF_line_number_set;
me->column_number = TestAnalyzer_MF_column_number;
me->column_number_at_begin = TestAnalyzer_MF_column_number_at_begin;
me->column_number_at_end = TestAnalyzer_MF_column_number_at_end;
me->column_number_set = TestAnalyzer_MF_column_number_set;
me->version = TestAnalyzer_MF_version;
me->print_this = TestAnalyzer_MF_print_this;
me->input_name = TestAnalyzer_MF_input_name;
me->input_name_set = TestAnalyzer_MF_input_name_set;
me->tell = TestAnalyzer_MF_tell;
me->seek = TestAnalyzer_MF_seek;
me->seek_forward = TestAnalyzer_MF_seek_forward;
me->seek_backward = TestAnalyzer_MF_seek_backward;
me->undo = TestAnalyzer_MF_undo;
me->undo_n = TestAnalyzer_MF_undo_n;
me->byte_order_reversion = TestAnalyzer_MF_byte_order_reversion;
me->byte_order_reversion_set = TestAnalyzer_MF_byte_order_reversion_set;
me->error_code_clear = TestAnalyzer_MF_error_code_clear;
me->error_code_is_void = TestAnalyzer_MF_error_code_is_void;
me->error_code_set_void = TestAnalyzer_MF_error_code_set_void;
me->error_code_set_if_first = TestAnalyzer_MF_error_code_set_if_first;
me->collect_user_memory = TestAnalyzer_MF_collect_user_memory;
me->resources_absent_mark = TestAnalyzer_MF_resources_absent_mark;
me->resources_absent = TestAnalyzer_MF_resources_absent;
}
#endif

bool
TestAnalyzer_user_constructor(QUEX_TYPE_ANALYZER* me)
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
TestAnalyzer_user_destructor(QUEX_TYPE_ANALYZER* me)
{
(void)me;

#define self  (*(QUEX_TYPE_DERIVED_ANALYZER*)me)
/* START: User's constructor extensions _______________________________________*/

/* END: _______________________________________________________________________*/
#undef self
}

bool
TestAnalyzer_user_reset(QUEX_TYPE_ANALYZER* me)
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
TestAnalyzer_user_print(QUEX_TYPE_ANALYZER* me)
{
(void)me;

#define self  (*(QUEX_TYPE_DERIVED_ANALYZER*)me)
/* START: User's constructor extensions _______________________________________*/

/* END: _______________________________________________________________________*/
#undef self
}

bool
TestAnalyzer_user_memento_pack(QUEX_TYPE_ANALYZER* me,
const char*         InputName,
TestAnalyzer_Memento* memento)
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
TestAnalyzer_user_memento_unpack(QUEX_TYPE_ANALYZER*  me,
TestAnalyzer_Memento*  memento)
{
(void)me; (void)memento;

#define self  (*(QUEX_TYPE_DERIVED_ANALYZER*)me)
/* START: User's memento 'unpack' _____________________________________________*/

/* END: _______________________________________________________________________*/
#undef self
}





/* -*- C++ -*-   vim: set syntax=cpp:
* (C) 2004-2009 Frank-Rene Schaefer
* ABSOLUTELY NO WARRANTY
*/
#ifndef __QUEX_INCLUDE_GUARD__TOKEN__GENERATED____TESTANALYZER_TOKEN_I
#define __QUEX_INCLUDE_GUARD__TOKEN__GENERATED____TESTANALYZER_TOKEN_I

#ifndef    __QUEX_OPTION_PLAIN_C
#   define __QUEX_OPTION_PLAIN_C
#endif

#include "test_environment/TestAnalyzer-token.h"
#include "test_environment/TestAnalyzer-token_ids.h"

static void
TestAnalyzer_Token_set(TestAnalyzer_Token*            __this,
const TestAnalyzer_token_id_t ID)
{ __this->id = ID; }

static void
TestAnalyzer_Token_construct(TestAnalyzer_Token* __this)
{
#   define self (*__this)
#   define LexemeNull  (&TestAnalyzer_LexemeNull)
(void)__this;

#   line 33 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

self.number = 0;
self.text   = LexemeNull;


#   line 1475 "test_environment/TestAnalyzer.c"


#   undef  LexemeNull
#   undef  self
}

static void
TestAnalyzer_Token_copy_construct(TestAnalyzer_Token*       __this,
const TestAnalyzer_Token* __That)
{
TestAnalyzer_Token_construct(__this);
TestAnalyzer_Token_copy(__this, __That);
}

static void
TestAnalyzer_Token_destruct(TestAnalyzer_Token* __this)
{
#   define self (*__this)
#   define LexemeNull  (&TestAnalyzer_LexemeNull)
if( ! __this ) return;


#   line 38 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

if( self.text != LexemeNull ) {
QUEXED(MemoryManager_free)((void*)self.text,
E_MemoryObjectType_TEXT);
self.text = LexemeNull;
}


#   line 1505 "test_environment/TestAnalyzer.c"


#   undef  LexemeNull
#   undef  self
}

static void
TestAnalyzer_Token_copy(TestAnalyzer_Token*       __this,
const TestAnalyzer_Token* __That)
{
#   define self  (*__this)
#   define Other (*__That)
#   define LexemeNull  (&TestAnalyzer_LexemeNull)
(void)__this;
(void)__That;

#   line 46 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

self.id  = Other.id;

if( self.text != LexemeNull ) {
QUEXED(MemoryManager_free)((void*)self.text, E_MemoryObjectType_TEXT);
}
if( Other.text != LexemeNull ) {
self.text = TestAnalyzer_lexeme_clone(self.text,
TestAnalyzer_lexeme_length(Other.text));
if( ! self.text ) self.text = LexemeNull;
}
self.number = Other.number;
#   ifdef     QUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN
__QUEX_IF_COUNT_LINES(self._line_n     = Other._line_n);
__QUEX_IF_COUNT_COLUMNS(self._column_n = Other._column_n);
#   endif


#   line 1539 "test_environment/TestAnalyzer.c"


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
static bool
TestAnalyzer_Token_take_text(TestAnalyzer_Token*            __this,
const TestAnalyzer_lexatom_t* Begin,
const TestAnalyzer_lexatom_t* End)
/* RETURNS: true -- if the token claims ownership over the given memory.
*          false -- if no ownership is claimed.                             */
{
#   define self       (*__this)
#   ifdef  LexemeNull
#   error  "Error LexemeNull shall not be defined here."
#   endif
#   define LexemeNull  (&TestAnalyzer_LexemeNull)
(void)__this;
(void)Begin;
(void)End;

#   line 64 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"


#       if 0
/* Hint for debug: To check take_text change "#if 0" to "#if 1" */
{
const TestAnalyzer_lexatom_t* it = (void*)0x0;
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
self.text = TestAnalyzer_lexeme_clone(Begin, (size_t)(End - Begin));
if( ! self.text ) self.text = LexemeNull;
*((TestAnalyzer_lexatom_t*)(self.text + (End - Begin))) = (TestAnalyzer_lexatom_t)0;
} else {
self.text = LexemeNull;
}

#       if 0
/* Hint for debug: To check take_text change "#if 0" to "#if 1"       */
{
const TestAnalyzer_lexatom_t* it = 0x0;
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


#   line 1620 "test_environment/TestAnalyzer.c"


#   undef  LexemeNull
#   undef  self
/* Default: no ownership.                                                */
return false;
}
#endif

#ifdef QUEX_OPTION_TOKEN_REPETITION_SUPPORT
static size_t
TestAnalyzer_Token_repetition_n_get(TestAnalyzer_Token* __this)
{
#   define self        (*__this)
#   define LexemeNull  (&TestAnalyzer_LexemeNull)
(void)__this;

#   line 121 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

return self.number;


#   line 1641 "test_environment/TestAnalyzer.c"


#   undef  LexemeNull
#   undef  self
}

static void
TestAnalyzer_Token_repetition_n_set(TestAnalyzer_Token* __this, size_t N)
{
#   define self        (*__this)
#   define LexemeNull  (&TestAnalyzer_LexemeNull)
(void)__this;
(void)N;

#   line 117 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

self.number = N;


#   line 1659 "test_environment/TestAnalyzer.c"


#   undef  LexemeNull
#   undef  self
}
#endif /* QUEX_OPTION_TOKEN_REPETITION_SUPPORT */

static const char*
TestAnalyzer_Token_map_id_to_name(const TestAnalyzer_token_id_t TokenID)
{
switch( TokenID ) {
default: {
return "<NUMERIC VALUE OF TOKEN-ID UNDEFINED>";
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


#   line 125 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

const char*
TestAnalyzer_Token_get_string(TestAnalyzer_Token* me, char*   buffer, size_t  BufferSize)
{
const char*  token_id_str = TestAnalyzer_Token_map_id_to_name(me->id);
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
writerator = TestAnalyzer_lexeme_to_pretty_char(me->text, writerator, BufferEnd);

/* Closing Quote */
if( BufferEnd - writerator > 1 ) {
*writerator++ = '\'';
}
*writerator = '\0';
return buffer;
}

#include <test_environment/converter-from-lexeme.i>
#include <test_environment/lib/lexeme_base.i>


#   line 1724 "test_environment/TestAnalyzer.c"



#endif /* __QUEX_INCLUDE_GUARD__TOKEN__GENERATED____TESTANALYZER_TOKEN_I */

TestAnalyzer_lexatom_t   TestAnalyzer_LexemeNull = (TestAnalyzer_lexatom_t)0;





bool UserConstructor_UnitTest_return_value = true;
bool UserReset_UnitTest_return_value       = true;
bool UserMementoPack_UnitTest_return_value = true;
