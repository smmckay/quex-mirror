#include <data/check.h>

#ifdef __QUEX_OPTION_COUNTER
void
QUEX_NAME(TEST_MODE_counter)(QUEX_TYPE_ANALYZER* me, QUEX_TYPE_LEXATOM* LexemeBegin, QUEX_TYPE_LEXATOM* LexemeEnd)
{
#   define self (*me)
/*  'QUEX_GOTO_STATE' requires 'QUEX_LABEL_STATE_ROUTER' */
#   define QUEX_LABEL_STATE_ROUTER _58
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

    /* (192 from BEFORE_ENTRY)  */
    loop_restart_p = (me->buffer._read_p);

    input = *(me->buffer._read_p);

_30:
    loop_restart_p = (me->buffer._read_p);


    __quex_debug("Init State\n");
    __quex_debug_state(192);
switch( input ) {
case 0x9: goto _7;
case 0xA: goto _6;
case 0x80: case 0x81: case 0x82: case 0x83: case 0x84: case 0x85: case 0x86: case 0x87: 
case 0x88: case 0x89: case 0x8A: case 0x8B: case 0x8C: case 0x8D: case 0x8E: case 0x8F: 
case 0x90: case 0x91: case 0x92: case 0x93: case 0x94: case 0x95: case 0x96: case 0x97: 
case 0x98: case 0x99: case 0x9A: case 0x9B: case 0x9C: case 0x9D: case 0x9E: case 0x9F: 
case 0xA0: case 0xA1: case 0xA2: case 0xA3: case 0xA4: case 0xA5: case 0xA6: case 0xA7: 
case 0xA8: case 0xA9: case 0xAA: case 0xAB: case 0xAC: case 0xAD: case 0xAE: case 0xAF: 
case 0xB0: case 0xB1: case 0xB2: case 0xB3: case 0xB4: case 0xB5: case 0xB6: case 0xB7: 
case 0xB8: case 0xB9: case 0xBA: case 0xBB: case 0xBC: case 0xBD: case 0xBE: case 0xBF: goto _10;
case 0xC0: case 0xC1: goto _19;
case 0xC2: case 0xC3: case 0xC4: case 0xC5: case 0xC6: case 0xC7: 
case 0xC8: case 0xC9: case 0xCA: case 0xCB: case 0xCC: case 0xCD: case 0xCE: case 0xCF: 
case 0xD0: case 0xD1: case 0xD2: case 0xD3: case 0xD4: case 0xD5: case 0xD6: case 0xD7: 
case 0xD8: case 0xD9: case 0xDA: case 0xDB: case 0xDC: case 0xDD: case 0xDE: case 0xDF: goto _4;
case 0xE0: goto _13;
case 0xE1: case 0xE2: case 0xE3: case 0xE4: case 0xE5: case 0xE6: case 0xE7: 
case 0xE8: case 0xE9: case 0xEA: case 0xEB: case 0xEC: case 0xED: case 0xEE: case 0xEF: goto _3;
case 0xF0: goto _5;
case 0xF1: case 0xF2: case 0xF3: case 0xF4: case 0xF5: case 0xF6: case 0xF7: goto _12;
case 0xF8: goto _2;
case 0xF9: case 0xFA: case 0xFB: goto _14;
case 0xFC: goto _11;
case 0xFD: goto _9;
case 0xFE: case 0xFF: goto _10;
default: goto _8;
}


    __quex_assert_no_passage();
_24:
    /* (192 from 211)  */
    goto _30;


    __quex_assert_no_passage();
_19:
    /* (DROP_OUT from 202) (DROP_OUT from 196) (DROP_OUT from 210) (DROP_OUT from 192) (DROP_OUT from 204) (DROP_OUT from 193)  */

        me->buffer._read_p = me->buffer._lexeme_start_p + 1;
goto _33;

    __quex_debug("Drop-Out Catcher\n");


    __quex_assert_no_passage();
_20:
    /* (DROP_OUT from 197)  */
    goto _26;


    __quex_assert_no_passage();
_22:
    /* (DROP_OUT from 199)  */
    goto _28;


    __quex_assert_no_passage();
_23:
    /* (DROP_OUT from 201)  */
    goto _34;


    __quex_assert_no_passage();
_21:
    /* (DROP_OUT from 198)  */
    goto _27;


    __quex_assert_no_passage();
_2:
    /* (193 from 192)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(193);
if     ( input >= 0xC0 )  goto _10;
else if( input >= 0x88 )  goto _12;
else if( input >= 0x80 )  goto _19;
else                      goto _10;


    __quex_assert_no_passage();
_3:
    /* (194 from 196) (194 from 192) (194 from 203) (194 from 208)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(194);
if     ( input >= 0xC0 )  goto _10;
else if( input >= 0x80 )  goto _4;
else                      goto _10;


    __quex_assert_no_passage();
_4:
    /* (195 from 194) (195 from 192) (195 from 209) (195 from 204)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(195);
if     ( input >= 0xC0 )  goto _10;
else if( input >= 0x80 )  goto _8;
else                      goto _10;


    __quex_assert_no_passage();
_5:
    /* (196 from 192)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(196);
if     ( input >= 0xC0 )  goto _10;
else if( input >= 0x90 )  goto _3;
else if( input >= 0x80 )  goto _19;
else                      goto _10;


    __quex_assert_no_passage();
_6:
    /* (197 from 192)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(197);
goto _20;


    __quex_assert_no_passage();
_7:
    /* (198 from 192)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(198);
goto _21;


    __quex_assert_no_passage();
_8:
    /* (199 from 210) (199 from 195) (199 from 192)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(199);
goto _22;


    __quex_assert_no_passage();
_9:
    /* (200 from 192)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(200);
if     ( input >= 0xC0 )  goto _10;
else if( input == 0xBF )  goto _15;
else if( input >= 0x80 )  goto _14;
else                      goto _10;


    __quex_assert_no_passage();
_10:
    /* (201 from 192) (201 from 210) (201 from 203) (201 from 209) (201 from 202) (201 from 195) (201 from 205) (201 from 208) (201 from 194) (201 from 204) (201 from 200) (201 from 193) (201 from 196) (201 from 207)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(201);
goto _23;


    __quex_assert_no_passage();
_11:
    /* (202 from 192)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(202);
if     ( input >= 0xC0 )  goto _10;
else if( input >= 0x84 )  goto _14;
else if( input >= 0x80 )  goto _19;
else                      goto _10;


    __quex_assert_no_passage();
_12:
    /* (203 from 192) (203 from 193) (203 from 207) (203 from 205)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(203);
if     ( input >= 0xC0 )  goto _10;
else if( input >= 0x80 )  goto _3;
else                      goto _10;


    __quex_assert_no_passage();
_13:
    /* (204 from 192)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(204);
if     ( input >= 0xC0 )  goto _10;
else if( input >= 0xA0 )  goto _4;
else if( input >= 0x80 )  goto _19;
else                      goto _10;


    __quex_assert_no_passage();
_14:
    /* (205 from 200) (205 from 192) (205 from 202)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(205);
if     ( input >= 0xC0 )  goto _10;
else if( input >= 0x80 )  goto _12;
else                      goto _10;


    __quex_assert_no_passage();
_15:
    /* (207 from 200)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(207);
if     ( input >= 0xC0 )  goto _10;
else if( input == 0xBF )  goto _16;
else if( input >= 0x80 )  goto _12;
else                      goto _10;


    __quex_assert_no_passage();
_16:
    /* (208 from 207)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(208);
if     ( input >= 0xC0 )  goto _10;
else if( input == 0xBF )  goto _17;
else if( input >= 0x80 )  goto _3;
else                      goto _10;


    __quex_assert_no_passage();
_17:
    /* (209 from 208)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(209);
if     ( input >= 0xC0 )  goto _10;
else if( input == 0xBF )  goto _18;
else if( input >= 0x80 )  goto _4;
else                      goto _10;


    __quex_assert_no_passage();
_18:
    /* (210 from 209)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(210);
if     ( input >= 0xC0 )  goto _10;
else if( input == 0xBF )  goto _19;
else if( input >= 0x80 )  goto _8;
else                      goto _10;

    /* (*) Terminal states _______________________________________________________
     *
     * States that implement actions of the 'winner patterns.                     */
_25:
    __quex_debug("* TERMINAL <LOOP EXIT>\n");
    (me->buffer._read_p) = loop_restart_p;

goto _0;

_26:
    __quex_debug("* TERMINAL <LOOP 2>\n");
__QUEX_IF_COUNT_LINES_ADD((size_t)1);

    __QUEX_IF_COUNT_COLUMNS((me->counter._column_number_at_end) = (size_t)1);

if( me->buffer._read_p != LexemeEnd ) goto _24;

goto _0;

_27:
    __quex_debug("* TERMINAL <LOOP 3>\n");
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end -= 1);
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end &= ~ ((size_t)0x3));
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end += 4 + 1);

if( me->buffer._read_p != LexemeEnd ) goto _24;

goto _0;

_28:
    __quex_debug("* TERMINAL <LOOP 4>\n");
__QUEX_IF_COUNT_COLUMNS_ADD((size_t)1);

if( me->buffer._read_p != LexemeEnd ) goto _24;

goto _0;

if(0) {
    /* Avoid unreferenced labels. */
    goto _25;
    goto _26;
    goto _27;
    goto _28;
}
_34: /* TERMINAL: BAD_LEXATOM */
;
_33: /* TERMINAL: FAILURE     */
goto _0;
_0:
/* Assert: lexeme in codec's character boundaries. */

     __quex_assert(me->buffer._read_p == LexemeEnd);
    return;
#   ifndef QUEX_OPTION_COMPUTED_GOTOS
    __quex_assert_no_passage();
_58:
#   endif /* QUEX_OPTION_COMPUTED_GOTOS */

#undef self


#undef QUEX_LABEL_STATE_ROUTER

#    if ! defined(QUEX_OPTION_COMPUTED_GOTOS)
     goto _58; /* in QUEX_GOTO_STATE       */
     goto _34; /* to BAD_LEXATOM           */
#    endif
    /* Avoid compiler warning: 'Unused labels' */

    goto _33;
    (void)target_state_index;
    (void)target_state_else_index;
}
#endif /* __QUEX_OPTION_COUNTER */
