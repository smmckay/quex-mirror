#include <data/check.h>

#ifdef QUEX_OPTION_COUNTER
void
QUEX_NAME(TEST_MODE_counter)(QUEX_TYPE_ANALYZER* me, QUEX_TYPE_LEXATOM* LexemeBegin, QUEX_TYPE_LEXATOM* LexemeEnd)
{
#   define self (*me)
/*  'QUEX_GOTO_STATE' requires 'QUEX_LABEL_STATE_ROUTER' */
#   define QUEX_LABEL_STATE_ROUTER _31
    QUEX_TYPE_LEXATOM              input                          = (QUEX_TYPE_LEXATOM)(0x00);
    QUEX_TYPE_GOTO_LABEL           target_state_else_index        = QUEX_GOTO_LABEL_VOID;
    QUEX_TYPE_GOTO_LABEL           target_state_index             = QUEX_GOTO_LABEL_VOID;
    QUEX_TYPE_LEXATOM*             loop_restart_p                 = (QUEX_TYPE_LEXATOM*)0x0;
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

    /* (13 from BEFORE_ENTRY)  */
    loop_restart_p = (me->buffer._read_p);

    input = *(me->buffer._read_p);

_20:
    loop_restart_p = (me->buffer._read_p);


    __quex_debug("Init State\n");
    __quex_debug_state(13);
if( input < 0x30 ) {
if     ( input >= 0xB )  goto _5;
else if( input == 0xA )  goto _2;
else if( input == 0x9 )  goto _3;
else                     goto _5;
} else {
if( input < 0xD800 ) {
if( input < 0x3A )  goto _4;
else                goto _5;
} else {
if     ( input < 0xDC00 )  goto _7;
else if( input < 0xE000 )  goto _6;
else                       goto _5;
}
}


    __quex_assert_no_passage();
_13:
    /* (13 from 22)  */
    goto _20;


    __quex_assert_no_passage();
_8:
    /* (DROP_OUT from 14)  */
    goto _15;

    __quex_debug("Drop-Out Catcher\n");


    __quex_assert_no_passage();
_9:
    /* (DROP_OUT from 15)  */
    goto _16;


    __quex_assert_no_passage();
_10:
    /* (DROP_OUT from 16)  */
    goto _17;


    __quex_assert_no_passage();
_11:
    /* (DROP_OUT from 17)  */
    goto _18;


    __quex_assert_no_passage();
_12:
    /* (DROP_OUT from 18)  */
    goto _22;


    __quex_assert_no_passage();
_4:
    /* (16 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(16);
if     ( input >= 0xE000 )  goto _10;
else if( input >= 0xDC00 )  goto _6;
else                        goto _10;


    __quex_assert_no_passage();
_5:
    /* (17 from 19) (17 from 13)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(17);
if     ( input >= 0xE000 )  goto _11;
else if( input >= 0xDC00 )  goto _6;
else                        goto _11;


    __quex_assert_no_passage();
_6:
    /* (18 from 13) (18 from 17) (18 from 14) (18 from 15) (18 from 19) (18 from 16)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(18);
goto _12;


    __quex_assert_no_passage();
_7:
    /* (19 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(19);
if     ( input >= 0xE000 )  goto _6;
else if( input >= 0xDC00 )  goto _5;
else                        goto _6;


    __quex_assert_no_passage();
_2:
    /* (14 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(14);
if     ( input >= 0xE000 )  goto _8;
else if( input >= 0xDC00 )  goto _6;
else                        goto _8;


    __quex_assert_no_passage();
_3:
    /* (15 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(15);
if     ( input >= 0xE000 )  goto _9;
else if( input >= 0xDC00 )  goto _6;
else                        goto _9;

    /* (*) Terminal states _______________________________________________________
     *
     * States that implement actions of the 'winner patterns.                     */
_14:
    __quex_debug("* TERMINAL <LOOP EXIT>\n");
    (me->buffer._read_p) = loop_restart_p;

goto _0;

_15:
    __quex_debug("* TERMINAL <LOOP 8>\n");
__QUEX_IF_COUNT_LINES_ADD((size_t)1);

    __QUEX_IF_COUNT_COLUMNS((me->counter._column_number_at_end) = (size_t)1);

if( me->buffer._read_p != LexemeEnd ) goto _13;

goto _0;

_16:
    __quex_debug("* TERMINAL <LOOP 9>\n");
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end -= 1);
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end &= ~ ((size_t)0x3));
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end += 4 + 1);

if( me->buffer._read_p != LexemeEnd ) goto _13;

goto _0;

_17:
    __quex_debug("* TERMINAL <LOOP 10>\n");
__QUEX_IF_COUNT_COLUMNS_ADD((size_t)10);

if( me->buffer._read_p != LexemeEnd ) goto _13;

goto _0;

_18:
    __quex_debug("* TERMINAL <LOOP 11>\n");
__QUEX_IF_COUNT_COLUMNS_ADD((size_t)1);

if( me->buffer._read_p != LexemeEnd ) goto _13;

goto _0;

if(0) {
    /* Avoid unreferenced labels. */
    goto _14;
    goto _15;
    goto _16;
    goto _17;
    goto _18;
}
_22: /* TERMINAL: BAD_LEXATOM */
;
_32: /* TERMINAL: FAILURE     */
goto _0;
_0:
/* Assert: lexeme in codec's character boundaries. */

     __quex_assert(me->buffer._read_p == LexemeEnd);
    return;
#   ifndef QUEX_OPTION_COMPUTED_GOTOS
    __quex_assert_no_passage();
_31:
#   endif /* QUEX_OPTION_COMPUTED_GOTOS */

#undef self


#undef QUEX_LABEL_STATE_ROUTER

#    if ! defined(QUEX_OPTION_COMPUTED_GOTOS)
     goto _31; /* in QUEX_GOTO_STATE       */
     goto _22; /* to BAD_LEXATOM           */
#    endif
    /* Avoid compiler warning: 'Unused labels' */

    goto _32;
    (void)target_state_index;
    (void)target_state_else_index;
}
#endif /* QUEX_OPTION_COUNTER */
