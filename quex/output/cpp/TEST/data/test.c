#include <data/check.h>

#ifdef QUEX_OPTION_COUNTER
void
QUEX_NAME(TEST_MODE_counter)(QUEX_TYPE_ANALYZER* me, QUEX_TYPE_LEXATOM* LexemeBegin, QUEX_TYPE_LEXATOM* LexemeEnd)
{
#   define self (*me)
/*  'QUEX_GOTO_STATE' requires 'QUEX_LABEL_STATE_ROUTER' */
#   define QUEX_LABEL_STATE_ROUTER _62
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

    /* (122 from BEFORE_ENTRY)  */
    loop_restart_p = (me->buffer._read_p);

    input = *(me->buffer._read_p);

_33:
    loop_restart_p = (me->buffer._read_p);


    __quex_debug("Init State\n");
    __quex_debug_state(122);
switch( input ) {
case 0x9: goto _2;
case 0xA: goto _15;
case 0x30: case 0x31: case 0x32: case 0x33: case 0x34: case 0x35: case 0x36: case 0x37: 
case 0x38: case 0x39: goto _11;
case 0x80: case 0x81: case 0x82: case 0x83: case 0x84: case 0x85: case 0x86: case 0x87: 
case 0x88: case 0x89: case 0x8A: case 0x8B: case 0x8C: case 0x8D: case 0x8E: case 0x8F: 
case 0x90: case 0x91: case 0x92: case 0x93: case 0x94: case 0x95: case 0x96: case 0x97: 
case 0x98: case 0x99: case 0x9A: case 0x9B: case 0x9C: case 0x9D: case 0x9E: case 0x9F: 
case 0xA0: case 0xA1: case 0xA2: case 0xA3: case 0xA4: case 0xA5: case 0xA6: case 0xA7: 
case 0xA8: case 0xA9: case 0xAA: case 0xAB: case 0xAC: case 0xAD: case 0xAE: case 0xAF: 
case 0xB0: case 0xB1: case 0xB2: case 0xB3: case 0xB4: case 0xB5: case 0xB6: case 0xB7: 
case 0xB8: case 0xB9: case 0xBA: case 0xBB: case 0xBC: case 0xBD: case 0xBE: case 0xBF: goto _7;
case 0xC0: case 0xC1: goto _20;
case 0xC2: case 0xC3: case 0xC4: case 0xC5: case 0xC6: case 0xC7: 
case 0xC8: case 0xC9: case 0xCA: case 0xCB: case 0xCC: case 0xCD: case 0xCE: case 0xCF: 
case 0xD0: case 0xD1: case 0xD2: case 0xD3: case 0xD4: case 0xD5: case 0xD6: case 0xD7: 
case 0xD8: case 0xD9: case 0xDA: case 0xDB: case 0xDC: case 0xDD: case 0xDE: case 0xDF: goto _4;
case 0xE0: goto _14;
case 0xE1: case 0xE2: case 0xE3: case 0xE4: case 0xE5: case 0xE6: case 0xE7: 
case 0xE8: case 0xE9: case 0xEA: case 0xEB: case 0xEC: case 0xED: case 0xEE: case 0xEF: goto _6;
case 0xF0: goto _5;
case 0xF1: case 0xF2: case 0xF3: case 0xF4: case 0xF5: case 0xF6: case 0xF7: goto _10;
case 0xF8: goto _13;
case 0xF9: case 0xFA: case 0xFB: goto _8;
case 0xFC: goto _3;
case 0xFD: goto _9;
case 0xFE: case 0xFF: goto _7;
default: goto _12;
}


    __quex_assert_no_passage();
_26:
    /* (122 from 209)  */
    goto _33;


    __quex_assert_no_passage();
_20:
    /* (DROP_OUT from 167) (DROP_OUT from 124) (DROP_OUT from 139) (DROP_OUT from 126) (DROP_OUT from 140) (DROP_OUT from 122)  */

        me->buffer._read_p = me->buffer._lexeme_start_p + 1;
goto _36;

    __quex_debug("Drop-Out Catcher\n");


    __quex_assert_no_passage();
_21:
    /* (DROP_OUT from 123)  */
    goto _29;


    __quex_assert_no_passage();
_22:
    /* (DROP_OUT from 129)  */
    goto _37;


    __quex_assert_no_passage();
_23:
    /* (DROP_OUT from 136)  */
    goto _30;


    __quex_assert_no_passage();
_24:
    /* (DROP_OUT from 137)  */
    goto _31;


    __quex_assert_no_passage();
_25:
    /* (DROP_OUT from 141)  */
    goto _28;


    __quex_assert_no_passage();
_7:
    /* (129 from 167) (129 from 164) (129 from 166) (129 from 127) (129 from 140) (129 from 126) (129 from 135) (129 from 122) (129 from 131) (129 from 125) (129 from 134) (129 from 162) (129 from 139) (129 from 124)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(129);
goto _22;


    __quex_assert_no_passage();
_8:
    /* (131 from 122) (131 from 134) (131 from 124)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(131);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0x80 )  goto _10;
else                      goto _7;


    __quex_assert_no_passage();
_9:
    /* (134 from 122)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(134);
if     ( input >= 0xC0 )  goto _7;
else if( input == 0xBF )  goto _16;
else if( input >= 0x80 )  goto _8;
else                      goto _7;


    __quex_assert_no_passage();
_10:
    /* (135 from 162) (135 from 122) (135 from 131) (135 from 139)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(135);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0x80 )  goto _6;
else                      goto _7;


    __quex_assert_no_passage();
_11:
    /* (136 from 122)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(136);
goto _23;


    __quex_assert_no_passage();
_12:
    /* (137 from 122) (137 from 125) (137 from 167)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(137);
goto _24;


    __quex_assert_no_passage();
_13:
    /* (139 from 122)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(139);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0x88 )  goto _10;
else if( input >= 0x80 )  goto _20;
else                      goto _7;


    __quex_assert_no_passage();
_14:
    /* (140 from 122)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(140);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0xA0 )  goto _4;
else if( input >= 0x80 )  goto _20;
else                      goto _7;


    __quex_assert_no_passage();
_15:
    /* (141 from 122)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(141);
goto _25;


    __quex_assert_no_passage();
_16:
    /* (162 from 134)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(162);
if     ( input >= 0xC0 )  goto _7;
else if( input == 0xBF )  goto _17;
else if( input >= 0x80 )  goto _10;
else                      goto _7;


    __quex_assert_no_passage();
_17:
    /* (164 from 162)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(164);
if     ( input >= 0xC0 )  goto _7;
else if( input == 0xBF )  goto _18;
else if( input >= 0x80 )  goto _6;
else                      goto _7;


    __quex_assert_no_passage();
_18:
    /* (166 from 164)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(166);
if     ( input >= 0xC0 )  goto _7;
else if( input == 0xBF )  goto _19;
else if( input >= 0x80 )  goto _4;
else                      goto _7;


    __quex_assert_no_passage();
_19:
    /* (167 from 166)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(167);
if     ( input >= 0xC0 )  goto _7;
else if( input == 0xBF )  goto _20;
else if( input >= 0x80 )  goto _12;
else                      goto _7;


    __quex_assert_no_passage();
_2:
    /* (123 from 122)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(123);
goto _21;


    __quex_assert_no_passage();
_3:
    /* (124 from 122)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(124);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0x84 )  goto _8;
else if( input >= 0x80 )  goto _20;
else                      goto _7;


    __quex_assert_no_passage();
_4:
    /* (125 from 140) (125 from 166) (125 from 127) (125 from 122)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(125);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0x80 )  goto _12;
else                      goto _7;


    __quex_assert_no_passage();
_5:
    /* (126 from 122)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(126);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0x90 )  goto _6;
else if( input >= 0x80 )  goto _20;
else                      goto _7;


    __quex_assert_no_passage();
_6:
    /* (127 from 126) (127 from 135) (127 from 164) (127 from 122)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(127);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0x80 )  goto _4;
else                      goto _7;

    /* (*) Terminal states _______________________________________________________
     *
     * States that implement actions of the 'winner patterns.                     */
_27:
    __quex_debug("* TERMINAL <LOOP EXIT>\n");
    (me->buffer._read_p) = loop_restart_p;

goto _0;

_28:
    __quex_debug("* TERMINAL <LOOP 8>\n");
__QUEX_IF_COUNT_LINES_ADD((size_t)1);

    __QUEX_IF_COUNT_COLUMNS((me->counter._column_number_at_end) = (size_t)1);

if( me->buffer._read_p != LexemeEnd ) goto _26;

goto _0;

_29:
    __quex_debug("* TERMINAL <LOOP 9>\n");
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end -= 1);
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end &= ~ ((size_t)0x3));
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end += 4 + 1);

if( me->buffer._read_p != LexemeEnd ) goto _26;

goto _0;

_30:
    __quex_debug("* TERMINAL <LOOP 10>\n");
__QUEX_IF_COUNT_COLUMNS_ADD((size_t)10);

if( me->buffer._read_p != LexemeEnd ) goto _26;

goto _0;

_31:
    __quex_debug("* TERMINAL <LOOP 11>\n");
__QUEX_IF_COUNT_COLUMNS_ADD((size_t)1);

if( me->buffer._read_p != LexemeEnd ) goto _26;

goto _0;

if(0) {
    /* Avoid unreferenced labels. */
    goto _27;
    goto _28;
    goto _29;
    goto _30;
    goto _31;
}
_37: /* TERMINAL: BAD_LEXATOM */
;
_36: /* TERMINAL: FAILURE     */
goto _0;
_0:
/* Assert: lexeme in codec's character boundaries. */

     __quex_assert(me->buffer._read_p == LexemeEnd);
    return;
#   ifndef QUEX_OPTION_COMPUTED_GOTOS
    __quex_assert_no_passage();
_62:
#   endif /* QUEX_OPTION_COMPUTED_GOTOS */

#undef self


#undef QUEX_LABEL_STATE_ROUTER

#    if ! defined(QUEX_OPTION_COMPUTED_GOTOS)
     goto _62; /* in QUEX_GOTO_STATE       */
     goto _37; /* to BAD_LEXATOM           */
#    endif
    /* Avoid compiler warning: 'Unused labels' */

    goto _36;
    (void)target_state_index;
    (void)target_state_else_index;
}
#endif /* QUEX_OPTION_COUNTER */
