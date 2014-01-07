#include <data/check.h>

#ifdef __QUEX_OPTION_COUNTER
void
QUEX_NAME(TEST_MODE_counter)(QUEX_TYPE_ANALYZER* me, QUEX_TYPE_CHARACTER* LexemeBegin, QUEX_TYPE_CHARACTER* LexemeEnd)
{
#   define self (*me)
    QUEX_TYPE_CHARACTER            input                          = (QUEX_TYPE_CHARACTER)(0x00);
    (void)me; (void)LexemeBegin; (void)LexemeEnd;
    __QUEX_IF_COUNT_SHIFT_VALUES();
    __quex_assert(LexemeBegin <= LexemeEnd);
    me->buffer._input_p = LexemeBegin;
_3: /* (38 from 45) (38 from NONE) */
    input = *(me->buffer._input_p);



    __quex_debug("Init State\n");
    __quex_debug_state(38);
    if( input < 0x4D ) {
        if( input == 0x4C ) {
            goto _4;
        
} else if( input >= 0x26 ) {
            goto _5;
        
} else if( input == 0x25 ) {
            goto _8;
        } else {
            goto _5;
        
}
    } else {
        if( input < 0x6E ) {
            goto _5;
        
} else if( input == 0x6E ) {
            goto _6;
        
} else if( input == 0x6F ) {
            goto _7;
        
} else if( input < 0x100 ) {
            goto _5;
        } else {

        
}
    
}

    __quex_debug_drop_out(38);
    __quex_debug("Character counting terminated.\n");
    goto _2;


    __quex_assert_no_passage();


    __quex_assert_no_passage();
_4: /* (39 from 38) */
    ++(me->buffer._input_p);
    input = *(me->buffer._input_p);
    goto _12;

_12:

    __quex_debug_state(39);
    __quex_debug_drop_out(39);
goto _14;

    __quex_assert_no_passage();
_5: /* (40 from 38) */
    ++(me->buffer._input_p);
    input = *(me->buffer._input_p);
    goto _15;

_15:

    __quex_debug_state(40);
    __quex_debug_drop_out(40);
goto _17;

    __quex_assert_no_passage();
_6: /* (41 from 38) */
    ++(me->buffer._input_p);
    input = *(me->buffer._input_p);
    goto _18;

_18:

    __quex_debug_state(41);
    __quex_debug_drop_out(41);
goto _20;

    __quex_assert_no_passage();
_7: /* (42 from 38) */
    ++(me->buffer._input_p);
    input = *(me->buffer._input_p);
    goto _21;

_21:

    __quex_debug_state(42);
    __quex_debug_drop_out(42);
goto _23;

    __quex_assert_no_passage();
_8: /* (43 from 38) */
    ++(me->buffer._input_p);
    input = *(me->buffer._input_p);
    goto _24;

_24:

    __quex_debug_state(43);
    __quex_debug_drop_out(43);
goto _26;
    /* (*) Terminal states _______________________________________________________
     *
     * States that implement actions of the 'winner patterns.                     */
_14: __quex_debug("* TERMINAL [004C] \n");
__QUEX_IF_COUNT_COLUMNS_ADD((size_t)0);
if( me->buffer._input_p == LexemeEnd ) goto _2;;
goto _3;
_17: __quex_debug("* TERMINAL [0000, 0024] [0026, 004B] [004D, 006D] [0070, 00FF] \n");
__QUEX_IF_COUNT_COLUMNS_ADD((size_t)1);
if( me->buffer._input_p == LexemeEnd ) goto _2;;
goto _3;
_20: __quex_debug("* TERMINAL [006E] \n");
__QUEX_IF_COUNT_COLUMNS_ADD((size_t)2);
if( me->buffer._input_p == LexemeEnd ) goto _2;;
goto _3;
_23: __quex_debug("* TERMINAL [006F] \n");
__QUEX_IF_COUNT_COLUMNS_ADD((size_t)3);
if( me->buffer._input_p == LexemeEnd ) goto _2;;
goto _3;
_26: __quex_debug("* TERMINAL [0025] \n");
__QUEX_IF_COUNT_LINES_ADD((size_t)1);
__QUEX_IF_COUNT_COLUMNS_SET((size_t)1);
if( me->buffer._input_p == LexemeEnd ) goto _2;;
goto _3;
_2: __quex_debug("* TERMINAL -- Exit --\n");
goto _1;
_1:
    __quex_assert(me->buffer._input_p == LexemeEnd); /* Otherwise, lexeme violates codec character boundaries. */
   return;
#  undef self
}
#endif /* __QUEX_OPTION_COUNTER */
