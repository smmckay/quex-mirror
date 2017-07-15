#include <data/check.h>

#ifdef QUEX_OPTION_COUNTER
void
QUEX_NAME(TEST_MODE_counter)(QUEX_TYPE_ANALYZER* me, QUEX_TYPE_LEXATOM* LexemeBegin, QUEX_TYPE_LEXATOM* LexemeEnd)
{
#   define self (*me)
/*  'QUEX_GOTO_STATE' requires 'QUEX_LABEL_STATE_ROUTER' */
#   define QUEX_LABEL_STATE_ROUTER _78
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

_39:
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
case 0xB8: case 0xB9: case 0xBA: case 0xBB: case 0xBC: case 0xBD: case 0xBE: case 0xBF: goto _6;
case 0xC0: case 0xC1: goto _26;
case 0xC2: case 0xC3: case 0xC4: case 0xC5: case 0xC6: case 0xC7: 
case 0xC8: case 0xC9: case 0xCA: case 0xCB: case 0xCC: case 0xCD: case 0xCE: case 0xCF: 
case 0xD0: case 0xD1: case 0xD2: case 0xD3: case 0xD4: case 0xD5: case 0xD6: case 0xD7: 
case 0xD8: case 0xD9: case 0xDA: case 0xDB: case 0xDC: case 0xDD: case 0xDE: case 0xDF: goto _7;
case 0xE0: goto _8;
case 0xE1: case 0xE2: case 0xE3: case 0xE4: case 0xE5: case 0xE6: case 0xE7: 
case 0xE8: case 0xE9: case 0xEA: case 0xEB: case 0xEC: case 0xED: case 0xEE: goto _9;
case 0xEF: goto _10;
case 0xF0: goto _11;
case 0xF1: case 0xF2: case 0xF3: case 0xF4: case 0xF5: case 0xF6: goto _12;
case 0xF7: goto _13;
case 0xF8: goto _14;
case 0xF9: case 0xFA: goto _15;
case 0xFB: goto _16;
case 0xFC: goto _17;
case 0xFD: goto _18;
case 0xFE: case 0xFF: goto _6;
default: goto _5;
}


    __quex_assert_no_passage();
_32:
    /* (13 from 99)  */
    goto _39;


    __quex_assert_no_passage();
_26:
    /* (DROP_OUT from 28) (DROP_OUT from 22) (DROP_OUT from 25) (DROP_OUT from 40) (DROP_OUT from 31) (DROP_OUT from 13)  */

        me->buffer._read_p = me->buffer._lexeme_start_p + 1;
goto _42;

    __quex_debug("Drop-Out Catcher\n");


    __quex_assert_no_passage();
_27:
    /* (DROP_OUT from 14)  */
    goto _34;


    __quex_assert_no_passage();
_28:
    /* (DROP_OUT from 15)  */
    goto _35;


    __quex_assert_no_passage();
_29:
    /* (DROP_OUT from 16)  */
    goto _36;


    __quex_assert_no_passage();
_30:
    /* (DROP_OUT from 17)  */
    goto _37;


    __quex_assert_no_passage();
_31:
    /* (DROP_OUT from 18)  */
    goto _43;


    __quex_assert_no_passage();
_2:
    /* (14 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(14);
if     ( input >= 0xFE )  goto _6;
else if( input >= 0xC0 )  goto _27;
else if( input >= 0x80 )  goto _6;
else                      goto _27;


    __quex_assert_no_passage();
_3:
    /* (15 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(15);
if     ( input >= 0xFE )  goto _6;
else if( input >= 0xC0 )  goto _28;
else if( input >= 0x80 )  goto _6;
else                      goto _28;


    __quex_assert_no_passage();
_4:
    /* (16 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(16);
if     ( input >= 0xFE )  goto _6;
else if( input >= 0xC0 )  goto _29;
else if( input >= 0x80 )  goto _6;
else                      goto _29;


    __quex_assert_no_passage();
_5:
    /* (17 from 40) (17 from 19) (17 from 13)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(17);
if     ( input >= 0xFE )  goto _6;
else if( input >= 0xC0 )  goto _30;
else if( input >= 0x80 )  goto _6;
else                      goto _30;


    __quex_assert_no_passage();
_6:
    /* (18 from 52) (18 from 31) (18 from 32) (18 from 47) (18 from 22) (18 from 27) (18 from 38) (18 from 17) (18 from 28) (18 from 18) (18 from 23) (18 from 34) (18 from 13) (18 from 24) (18 from 14) (18 from 29) (18 from 40) (18 from 19) (18 from 30) (18 from 56) (18 from 25) (18 from 36) (18 from 15) (18 from 26) (18 from 16)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(18);
if     ( input >= 0xFE )  goto _6;
else if( input >= 0xC0 )  goto _31;
else if( input >= 0x80 )  goto _6;
else                      goto _31;


    __quex_assert_no_passage();
_7:
    /* (19 from 56) (19 from 38) (19 from 13) (19 from 23) (19 from 22) (19 from 24)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(19);
if     ( input >= 0xC0 )  goto _6;
else if( input >= 0x80 )  goto _5;
else                      goto _6;


    __quex_assert_no_passage();
_8:
    /* (22 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(22);
if     ( input >= 0xC0 )  goto _6;
else if( input >= 0xA0 )  goto _7;
else if( input >= 0x80 )  goto _26;
else                      goto _6;


    __quex_assert_no_passage();
_9:
    /* (23 from 25) (23 from 52) (23 from 27) (23 from 36) (23 from 13) (23 from 26)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(23);
if     ( input >= 0xC0 )  goto _6;
else if( input >= 0x80 )  goto _7;
else                      goto _6;


    __quex_assert_no_passage();
_10:
    /* (24 from 27) (24 from 13)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(24);
if     ( input >= 0xC0 )  goto _6;
else if( input >= 0x80 )  goto _7;
else                      goto _6;


    __quex_assert_no_passage();
_11:
    /* (25 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(25);
switch( input ) {
case 0x80: case 0x81: case 0x82: case 0x83: case 0x84: case 0x85: case 0x86: case 0x87: 
case 0x88: case 0x89: case 0x8A: case 0x8B: case 0x8C: case 0x8D: case 0x8E: case 0x8F: goto _26;
case 0x90: goto _25;
case 0x91: case 0x92: case 0x93: case 0x94: case 0x95: case 0x96: case 0x97: 
case 0x98: case 0x99: case 0x9A: case 0x9B: case 0x9C: case 0x9D: case 0x9E: case 0x9F: 
case 0xA0: case 0xA1: case 0xA2: case 0xA3: case 0xA4: case 0xA5: case 0xA6: case 0xA7: 
case 0xA8: case 0xA9: case 0xAA: case 0xAB: case 0xAC: case 0xAD: case 0xAE: case 0xAF: 
case 0xB0: case 0xB1: case 0xB2: case 0xB3: case 0xB4: case 0xB5: case 0xB6: case 0xB7: 
case 0xB8: case 0xB9: case 0xBA: case 0xBB: case 0xBC: case 0xBD: case 0xBE: case 0xBF: goto _9;
default: goto _6;
}


    __quex_assert_no_passage();
_12:
    /* (26 from 30) (26 from 13) (26 from 28) (26 from 34) (26 from 29) (26 from 47)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(26);
if     ( input >= 0xC0 )  goto _6;
else if( input >= 0x80 )  goto _9;
else                      goto _6;


    __quex_assert_no_passage();
_13:
    /* (27 from 30) (27 from 13)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(27);
if     ( input >= 0xC0 )  goto _6;
else if( input == 0xBF )  goto _10;
else if( input >= 0x80 )  goto _9;
else                      goto _6;


    __quex_assert_no_passage();
_14:
    /* (28 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(28);
switch( input ) {
case 0x80: case 0x81: case 0x82: case 0x83: case 0x84: case 0x85: case 0x86: case 0x87: goto _26;
case 0x88: goto _24;
case 0x89: case 0x8A: case 0x8B: case 0x8C: case 0x8D: case 0x8E: case 0x8F: 
case 0x90: case 0x91: case 0x92: case 0x93: case 0x94: case 0x95: case 0x96: case 0x97: 
case 0x98: case 0x99: case 0x9A: case 0x9B: case 0x9C: case 0x9D: case 0x9E: case 0x9F: 
case 0xA0: case 0xA1: case 0xA2: case 0xA3: case 0xA4: case 0xA5: case 0xA6: case 0xA7: 
case 0xA8: case 0xA9: case 0xAA: case 0xAB: case 0xAC: case 0xAD: case 0xAE: case 0xAF: 
case 0xB0: case 0xB1: case 0xB2: case 0xB3: case 0xB4: case 0xB5: case 0xB6: case 0xB7: 
case 0xB8: case 0xB9: case 0xBA: case 0xBB: case 0xBC: case 0xBD: case 0xBE: case 0xBF: goto _12;
default: goto _6;
}


    __quex_assert_no_passage();
_15:
    /* (29 from 13) (29 from 31) (29 from 32)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(29);
if     ( input >= 0xC0 )  goto _6;
else if( input >= 0x80 )  goto _12;
else                      goto _6;


    __quex_assert_no_passage();
_16:
    /* (30 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(30);
if     ( input >= 0xC0 )  goto _6;
else if( input == 0xBF )  goto _13;
else if( input >= 0x80 )  goto _12;
else                      goto _6;


    __quex_assert_no_passage();
_17:
    /* (31 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(31);
switch( input ) {
case 0x80: case 0x81: case 0x82: case 0x83: goto _26;
case 0x84: goto _23;
case 0x85: case 0x86: case 0x87: 
case 0x88: case 0x89: case 0x8A: case 0x8B: case 0x8C: case 0x8D: case 0x8E: case 0x8F: 
case 0x90: case 0x91: case 0x92: case 0x93: case 0x94: case 0x95: case 0x96: case 0x97: 
case 0x98: case 0x99: case 0x9A: case 0x9B: case 0x9C: case 0x9D: case 0x9E: case 0x9F: 
case 0xA0: case 0xA1: case 0xA2: case 0xA3: case 0xA4: case 0xA5: case 0xA6: case 0xA7: 
case 0xA8: case 0xA9: case 0xAA: case 0xAB: case 0xAC: case 0xAD: case 0xAE: case 0xAF: 
case 0xB0: case 0xB1: case 0xB2: case 0xB3: case 0xB4: case 0xB5: case 0xB6: case 0xB7: 
case 0xB8: case 0xB9: case 0xBA: case 0xBB: case 0xBC: case 0xBD: case 0xBE: case 0xBF: goto _15;
default: goto _6;
}


    __quex_assert_no_passage();
_18:
    /* (32 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(32);
if     ( input >= 0xC0 )  goto _6;
else if( input == 0xBF )  goto _19;
else if( input >= 0x80 )  goto _15;
else                      goto _6;


    __quex_assert_no_passage();
_19:
    /* (34 from 32)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(34);
if     ( input >= 0xC0 )  goto _6;
else if( input == 0xBF )  goto _20;
else if( input >= 0x80 )  goto _12;
else                      goto _6;


    __quex_assert_no_passage();
_20:
    /* (36 from 34)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(36);
if     ( input >= 0xC0 )  goto _6;
else if( input == 0xBF )  goto _21;
else if( input >= 0x80 )  goto _9;
else                      goto _6;


    __quex_assert_no_passage();
_21:
    /* (38 from 36)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(38);
if     ( input >= 0xC0 )  goto _6;
else if( input == 0xBF )  goto _22;
else if( input >= 0x80 )  goto _7;
else                      goto _6;


    __quex_assert_no_passage();
_22:
    /* (40 from 38)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(40);
if     ( input >= 0xC0 )  goto _6;
else if( input == 0xBF )  goto _26;
else if( input >= 0x80 )  goto _5;
else                      goto _6;


    __quex_assert_no_passage();
_23:
    /* (47 from 31)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(47);
if     ( input >= 0xC0 )  goto _6;
else if( input >= 0x81 )  goto _12;
else if( input == 0x80 )  goto _24;
else                      goto _6;


    __quex_assert_no_passage();
_24:
    /* (52 from 47) (52 from 28)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(52);
if     ( input >= 0xC0 )  goto _6;
else if( input >= 0x81 )  goto _9;
else if( input == 0x80 )  goto _25;
else                      goto _6;


    __quex_assert_no_passage();
_25:
    /* (56 from 25) (56 from 52)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(56);
if     ( input >= 0xC0 )  goto _6;
else if( input >= 0x80 )  goto _7;
else                      goto _6;

    /* (*) Terminal states _______________________________________________________
     *
     * States that implement actions of the 'winner patterns.                     */
_33:
    __quex_debug("* TERMINAL <LOOP EXIT>\n");
    (me->buffer._read_p) = loop_restart_p;

goto _0;

_34:
    __quex_debug("* TERMINAL <LOOP 8>\n");
__QUEX_IF_COUNT_LINES_ADD((size_t)1);

    __QUEX_IF_COUNT_COLUMNS((me->counter._column_number_at_end) = (size_t)1);

if( me->buffer._read_p != LexemeEnd ) goto _32;

goto _0;

_35:
    __quex_debug("* TERMINAL <LOOP 9>\n");
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end -= 1);
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end &= ~ ((size_t)0x3));
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end += 4 + 1);

if( me->buffer._read_p != LexemeEnd ) goto _32;

goto _0;

_36:
    __quex_debug("* TERMINAL <LOOP 10>\n");
__QUEX_IF_COUNT_COLUMNS_ADD((size_t)10);

if( me->buffer._read_p != LexemeEnd ) goto _32;

goto _0;

_37:
    __quex_debug("* TERMINAL <LOOP 11>\n");
__QUEX_IF_COUNT_COLUMNS_ADD((size_t)1);

if( me->buffer._read_p != LexemeEnd ) goto _32;

goto _0;

if(0) {
    /* Avoid unreferenced labels. */
    goto _33;
    goto _34;
    goto _35;
    goto _36;
    goto _37;
}
_43: /* TERMINAL: BAD_LEXATOM */
;
_42: /* TERMINAL: FAILURE     */
goto _0;
_0:
/* Assert: lexeme in codec's character boundaries. */

     __quex_assert(me->buffer._read_p == LexemeEnd);
    return;
#   ifndef QUEX_OPTION_COMPUTED_GOTOS
    __quex_assert_no_passage();
_78:
#   endif /* QUEX_OPTION_COMPUTED_GOTOS */

#undef self


#undef QUEX_LABEL_STATE_ROUTER

#    if ! defined(QUEX_OPTION_COMPUTED_GOTOS)
     goto _78; /* in QUEX_GOTO_STATE       */
     goto _43; /* to BAD_LEXATOM           */
#    endif
    /* Avoid compiler warning: 'Unused labels' */

    goto _42;
    (void)target_state_index;
    (void)target_state_else_index;
}
#endif /* QUEX_OPTION_COUNTER */
