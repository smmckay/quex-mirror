#include <data/check.h>

#ifdef QUEX_OPTION_COUNTER
void
QUEX_NAME(TEST_MODE_counter)(QUEX_TYPE_ANALYZER* me, QUEX_TYPE_LEXATOM* LexemeBegin, QUEX_TYPE_LEXATOM* LexemeEnd)
{
#   define self (*me)
/*  'QUEX_GOTO_STATE' requires 'QUEX_LABEL_STATE_ROUTER' */
#   define QUEX_LABEL_STATE_ROUTER _56
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

_31:
    loop_restart_p = (me->buffer._read_p);


    __quex_debug("Init State\n");
    __quex_debug_state(13);
switch( input ) {
case 0x9: goto _3;
case 0xA: goto _2;
case 0x30: case 0x31: case 0x32: case 0x33: case 0x34: case 0x35: case 0x36: case 0x37: 
case 0x38: case 0x39: goto _4;
case 0x80: case 0x81: case 0x82: case 0x83: case 0x84: case 0x85: case 0x86: case 0x87: 
case 0x88: case 0x89: case 0x8A: case 0x8B: case 0x8C: case 0x8D: case 0x8E: case 0x8F: 
case 0x90: case 0x91: case 0x92: case 0x93: case 0x94: case 0x95: case 0x96: case 0x97: 
case 0x98: case 0x99: case 0x9A: case 0x9B: case 0x9C: case 0x9D: case 0x9E: case 0x9F: 
case 0xA0: case 0xA1: case 0xA2: case 0xA3: case 0xA4: case 0xA5: case 0xA6: case 0xA7: 
case 0xA8: case 0xA9: case 0xAA: case 0xAB: case 0xAC: case 0xAD: case 0xAE: case 0xAF: 
case 0xB0: case 0xB1: case 0xB2: case 0xB3: case 0xB4: case 0xB5: case 0xB6: case 0xB7: 
case 0xB8: case 0xB9: case 0xBA: case 0xBB: case 0xBC: case 0xBD: case 0xBE: case 0xBF: goto _7;
case 0xC0: case 0xC1: goto _17;
case 0xC2: case 0xC3: goto _8;
case 0xC4: case 0xC5: case 0xC6: case 0xC7: 
case 0xC8: case 0xC9: case 0xCA: case 0xCB: case 0xCC: case 0xCD: case 0xCE: case 0xCF: 
case 0xD0: case 0xD1: case 0xD2: case 0xD3: case 0xD4: case 0xD5: case 0xD6: case 0xD7: 
case 0xD8: case 0xD9: case 0xDA: case 0xDB: case 0xDC: case 0xDD: case 0xDE: case 0xDF: goto _15;
case 0xE0: goto _9;
case 0xE1: case 0xE2: case 0xE3: case 0xE4: case 0xE5: case 0xE6: case 0xE7: 
case 0xE8: case 0xE9: case 0xEA: case 0xEB: case 0xEC: case 0xED: case 0xEE: goto _10;
case 0xEF: goto _11;
case 0xF0: goto _12;
case 0xF1: case 0xF2: case 0xF3: goto _13;
case 0xF4: goto _14;
case 0xF5: case 0xF6: case 0xF7: 
case 0xF8: case 0xF9: case 0xFA: case 0xFB: case 0xFC: case 0xFD: goto _17;
case 0xFE: case 0xFF: goto _7;
default: goto _5;
}


    __quex_assert_no_passage();
_24:
    /* (13 from 48)  */
    goto _31;


    __quex_assert_no_passage();
_17:
    /* (DROP_OUT from 28) (DROP_OUT from 25) (DROP_OUT from 30) (DROP_OUT from 13)  */

        me->buffer._read_p = me->buffer._lexeme_start_p + 1;
goto _34;

    __quex_debug("Drop-Out Catcher\n");


    __quex_assert_no_passage();
_18:
    /* (DROP_OUT from 14)  */
    goto _26;


    __quex_assert_no_passage();
_19:
    /* (DROP_OUT from 15)  */
    goto _27;


    __quex_assert_no_passage();
_20:
    /* (DROP_OUT from 16)  */
    goto _28;


    __quex_assert_no_passage();
_21:
    /* (DROP_OUT from 17)  */
    goto _29;


    __quex_assert_no_passage();
_22:
    /* (DROP_OUT from 18)  */
    goto _25;


    __quex_assert_no_passage();
_23:
    /* (DROP_OUT from 19)  */
    goto _35;


    __quex_assert_no_passage();
_2:
    /* (14 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(14);
if     ( input >= 0xFE )  goto _7;
else if( input >= 0xC0 )  goto _18;
else if( input >= 0x80 )  goto _7;
else                      goto _18;


    __quex_assert_no_passage();
_3:
    /* (15 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(15);
if     ( input >= 0xFE )  goto _7;
else if( input >= 0xC0 )  goto _19;
else if( input >= 0x80 )  goto _7;
else                      goto _19;


    __quex_assert_no_passage();
_4:
    /* (16 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(16);
if     ( input >= 0xFE )  goto _7;
else if( input >= 0xC0 )  goto _20;
else if( input >= 0x80 )  goto _7;
else                      goto _20;


    __quex_assert_no_passage();
_5:
    /* (17 from 20) (17 from 13)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(17);
if     ( input >= 0xFE )  goto _7;
else if( input >= 0xC0 )  goto _21;
else if( input >= 0x80 )  goto _7;
else                      goto _21;


    __quex_assert_no_passage();
_6:
    /* (18 from 33)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(18);
if     ( input >= 0xFE )  goto _7;
else if( input >= 0xC0 )  goto _22;
else if( input >= 0x80 )  goto _7;
else                      goto _22;


    __quex_assert_no_passage();
_7:
    /* (19 from 18) (19 from 25) (19 from 14) (19 from 28) (19 from 17) (19 from 38) (19 from 20) (19 from 13) (19 from 27) (19 from 16) (19 from 30) (19 from 26) (19 from 19) (19 from 33) (19 from 15) (19 from 29)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(19);
if     ( input >= 0xFE )  goto _7;
else if( input >= 0xC0 )  goto _23;
else if( input >= 0x80 )  goto _7;
else                      goto _23;


    __quex_assert_no_passage();
_8:
    /* (20 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(20);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0x80 )  goto _5;
else                      goto _7;


    __quex_assert_no_passage();
_9:
    /* (25 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(25);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0xA0 )  goto _15;
else if( input >= 0x80 )  goto _17;
else                      goto _7;


    __quex_assert_no_passage();
_10:
    /* (26 from 13) (26 from 28) (26 from 30) (26 from 29)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(26);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0x80 )  goto _15;
else                      goto _7;


    __quex_assert_no_passage();
_11:
    /* (27 from 30) (27 from 13)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(27);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0x80 )  goto _15;
else                      goto _7;


    __quex_assert_no_passage();
_12:
    /* (28 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(28);
switch( input ) {
case 0x80: case 0x81: case 0x82: case 0x83: case 0x84: case 0x85: case 0x86: case 0x87: 
case 0x88: case 0x89: case 0x8A: case 0x8B: case 0x8C: case 0x8D: case 0x8E: case 0x8F: goto _17;
case 0x90: goto _16;
case 0x91: case 0x92: case 0x93: case 0x94: case 0x95: case 0x96: case 0x97: 
case 0x98: case 0x99: case 0x9A: case 0x9B: case 0x9C: case 0x9D: case 0x9E: case 0x9F: 
case 0xA0: case 0xA1: case 0xA2: case 0xA3: case 0xA4: case 0xA5: case 0xA6: case 0xA7: 
case 0xA8: case 0xA9: case 0xAA: case 0xAB: case 0xAC: case 0xAD: case 0xAE: case 0xAF: 
case 0xB0: case 0xB1: case 0xB2: case 0xB3: case 0xB4: case 0xB5: case 0xB6: case 0xB7: 
case 0xB8: case 0xB9: case 0xBA: case 0xBB: case 0xBC: case 0xBD: case 0xBE: case 0xBF: goto _10;
default: goto _7;
}


    __quex_assert_no_passage();
_13:
    /* (29 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(29);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0x80 )  goto _10;
else                      goto _7;


    __quex_assert_no_passage();
_14:
    /* (30 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(30);
switch( input ) {
case 0x80: case 0x81: case 0x82: case 0x83: case 0x84: case 0x85: case 0x86: case 0x87: 
case 0x88: case 0x89: case 0x8A: case 0x8B: case 0x8C: case 0x8D: case 0x8E: goto _10;
case 0x8F: goto _11;
case 0x90: case 0x91: case 0x92: case 0x93: case 0x94: case 0x95: case 0x96: case 0x97: 
case 0x98: case 0x99: case 0x9A: case 0x9B: case 0x9C: case 0x9D: case 0x9E: case 0x9F: 
case 0xA0: case 0xA1: case 0xA2: case 0xA3: case 0xA4: case 0xA5: case 0xA6: case 0xA7: 
case 0xA8: case 0xA9: case 0xAA: case 0xAB: case 0xAC: case 0xAD: case 0xAE: case 0xAF: 
case 0xB0: case 0xB1: case 0xB2: case 0xB3: case 0xB4: case 0xB5: case 0xB6: case 0xB7: 
case 0xB8: case 0xB9: case 0xBA: case 0xBB: case 0xBC: case 0xBD: case 0xBE: case 0xBF: goto _17;
default: goto _7;
}


    __quex_assert_no_passage();
_15:
    /* (33 from 25) (33 from 26) (33 from 27) (33 from 13) (33 from 38)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(33);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0x80 )  goto _6;
else                      goto _7;


    __quex_assert_no_passage();
_16:
    /* (38 from 28)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(38);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0x80 )  goto _15;
else                      goto _7;

    /* (*) Terminal states _______________________________________________________
     *
     * States that implement actions of the 'winner patterns.                     */
_25:
    __quex_debug("* TERMINAL <LOOP EXIT>\n");
    (me->buffer._read_p) = loop_restart_p;

goto _0;

_26:
    __quex_debug("* TERMINAL <LOOP 8>\n");
__QUEX_IF_COUNT_LINES_ADD((size_t)1);

    __QUEX_IF_COUNT_COLUMNS((me->counter._column_number_at_end) = (size_t)1);

if( me->buffer._read_p != LexemeEnd ) goto _24;

goto _0;

_27:
    __quex_debug("* TERMINAL <LOOP 9>\n");
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end -= 1);
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end &= ~ ((size_t)0x3));
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end += 4 + 1);

if( me->buffer._read_p != LexemeEnd ) goto _24;

goto _0;

_28:
    __quex_debug("* TERMINAL <LOOP 10>\n");
__QUEX_IF_COUNT_COLUMNS_ADD((size_t)10);

if( me->buffer._read_p != LexemeEnd ) goto _24;

goto _0;

_29:
    __quex_debug("* TERMINAL <LOOP 11>\n");
__QUEX_IF_COUNT_COLUMNS_ADD((size_t)1);

if( me->buffer._read_p != LexemeEnd ) goto _24;

goto _0;

if(0) {
    /* Avoid unreferenced labels. */
    goto _25;
    goto _26;
    goto _27;
    goto _28;
    goto _29;
}
_35: /* TERMINAL: BAD_LEXATOM */
;
_34: /* TERMINAL: FAILURE     */
goto _0;
_0:
/* Assert: lexeme in codec's character boundaries. */

     __quex_assert(me->buffer._read_p == LexemeEnd);
    return;
#   ifndef QUEX_OPTION_COMPUTED_GOTOS
    __quex_assert_no_passage();
_56:
#   endif /* QUEX_OPTION_COMPUTED_GOTOS */

#undef self


#undef QUEX_LABEL_STATE_ROUTER

#    if ! defined(QUEX_OPTION_COMPUTED_GOTOS)
     goto _56; /* in QUEX_GOTO_STATE       */
     goto _35; /* to BAD_LEXATOM           */
#    endif
    /* Avoid compiler warning: 'Unused labels' */

    goto _34;
    (void)target_state_index;
    (void)target_state_else_index;
}
#endif /* QUEX_OPTION_COUNTER */
