#include <data/check.h>

void
Lexer_TEST_MODE_counter_on_arbitrary_lexeme(struct Lexer_tag* me, Lexer_lexatom_t* LexemeBegin, Lexer_lexatom_t* LexemeEnd)
{
#   define self (*me)
/*  'QUEX_GOTO_STATE' requires 'QUEX_LABEL_STATE_ROUTER' */
#   define QUEX_LABEL_STATE_ROUTER _55
    Lexer_lexatom_t    input                   = (Lexer_lexatom_t)(0x00);
    Lexer_goto_label_t target_state_else_index = (Lexer_goto_label_t)-1;
    Lexer_goto_label_t target_state_index      = (Lexer_goto_label_t)-1;
    Lexer_lexatom_t*   loop_restart_p          = (Lexer_lexatom_t*)0x0;
    (void)me;
    me->counter._column_number_at_begin = me->counter._column_number_at_end;
    me->counter._line_number_at_begin = me->counter._line_number_at_end;
    /* Allow LexemeBegin == LexemeEnd (e.g. END_OF_STREAM)
     * => Caller does not need to check
     * BUT, if so quit immediately after 'shift values'.
     */
    __quex_assert(LexemeBegin <= LexemeEnd);
    if( LexemeBegin == LexemeEnd ) {
        return;
    }
    me->buffer._read_p = LexemeBegin;

    /* (18 from BEFORE_ENTRY)  */
    loop_restart_p = (me->buffer._read_p);

    input = *(me->buffer._read_p);

_31:
    loop_restart_p = (me->buffer._read_p);


    __quex_debug_init_state(18);
switch( input ) {
case 0x9: goto _3;
case 0xA: goto _2;
case 0x61: case 0x62: case 0x63: case 0x64: goto _4;
case 0x78: goto _5;
case 0x80: case 0x81: case 0x82: case 0x83: case 0x84: case 0x85: case 0x86: case 0x87: 
case 0x88: case 0x89: case 0x8A: case 0x8B: case 0x8C: case 0x8D: case 0x8E: case 0x8F: 
case 0x90: case 0x91: case 0x92: case 0x93: case 0x94: case 0x95: case 0x96: case 0x97: 
case 0x98: case 0x99: case 0x9A: case 0x9B: case 0x9C: case 0x9D: case 0x9E: case 0x9F: 
case 0xA0: case 0xA1: case 0xA2: case 0xA3: case 0xA4: case 0xA5: case 0xA6: case 0xA7: 
case 0xA8: case 0xA9: case 0xAA: case 0xAB: case 0xAC: case 0xAD: case 0xAE: case 0xAF: 
case 0xB0: case 0xB1: case 0xB2: case 0xB3: case 0xB4: case 0xB5: case 0xB6: case 0xB7: 
case 0xB8: case 0xB9: case 0xBA: case 0xBB: case 0xBC: case 0xBD: case 0xBE: case 0xBF: goto _7;
case 0xC0: case 0xC1: goto _16;
case 0xC2: case 0xC3: case 0xC4: case 0xC5: case 0xC6: case 0xC7: 
case 0xC8: case 0xC9: case 0xCA: case 0xCB: case 0xCC: case 0xCD: case 0xCE: case 0xCF: 
case 0xD0: case 0xD1: case 0xD2: case 0xD3: case 0xD4: case 0xD5: case 0xD6: case 0xD7: 
case 0xD8: case 0xD9: case 0xDA: case 0xDB: case 0xDC: case 0xDD: case 0xDE: case 0xDF: goto _15;
case 0xE0: goto _8;
case 0xE1: case 0xE2: case 0xE3: case 0xE4: case 0xE5: case 0xE6: case 0xE7: 
case 0xE8: case 0xE9: case 0xEA: case 0xEB: case 0xEC: case 0xED: case 0xEE: goto _9;
case 0xEF: goto _10;
case 0xF0: goto _11;
case 0xF1: case 0xF2: case 0xF3: goto _12;
case 0xF4: goto _13;
case 0xF5: case 0xF6: case 0xF7: 
case 0xF8: case 0xF9: case 0xFA: case 0xFB: case 0xFC: case 0xFD: goto _16;
case 0xFE: case 0xFF: goto _7;
default: goto _6;
}


    __quex_assert_no_passage();
_23:
    /* (18 from 51)  */
    goto _31;


    __quex_assert_no_passage();
_16:
    /* (DROP_OUT from 28) (DROP_OUT from 18) (DROP_OUT from 33) (DROP_OUT from 31)  */

    me->buffer._read_p = me->buffer._lexeme_start_p + 1;
goto _34;

    __quex_debug("Drop-Out Catcher\n");


    __quex_assert_no_passage();
_17:
    /* (DROP_OUT from 19)  */
goto _25;


    __quex_assert_no_passage();
_18:
    /* (DROP_OUT from 20)  */
goto _26;


    __quex_assert_no_passage();
_19:
    /* (DROP_OUT from 21)  */
goto _27;


    __quex_assert_no_passage();
_20:
    /* (DROP_OUT from 22)  */
goto _28;


    __quex_assert_no_passage();
_21:
    /* (DROP_OUT from 23)  */
goto _29;


    __quex_assert_no_passage();
_22:
    /* (DROP_OUT from 24)  */
goto _35;


    __quex_assert_no_passage();
_12:
    /* (32 from 18)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(32);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0x80 )  goto _9;
else                      goto _7;


    __quex_assert_no_passage();
_13:
    /* (33 from 18)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(33);
switch( input ) {
case 0x80: case 0x81: case 0x82: case 0x83: case 0x84: case 0x85: case 0x86: case 0x87: 
case 0x88: case 0x89: case 0x8A: case 0x8B: case 0x8C: case 0x8D: case 0x8E: goto _9;
case 0x8F: goto _10;
case 0x90: case 0x91: case 0x92: case 0x93: case 0x94: case 0x95: case 0x96: case 0x97: 
case 0x98: case 0x99: case 0x9A: case 0x9B: case 0x9C: case 0x9D: case 0x9E: case 0x9F: 
case 0xA0: case 0xA1: case 0xA2: case 0xA3: case 0xA4: case 0xA5: case 0xA6: case 0xA7: 
case 0xA8: case 0xA9: case 0xAA: case 0xAB: case 0xAC: case 0xAD: case 0xAE: case 0xAF: 
case 0xB0: case 0xB1: case 0xB2: case 0xB3: case 0xB4: case 0xB5: case 0xB6: case 0xB7: 
case 0xB8: case 0xB9: case 0xBA: case 0xBB: case 0xBC: case 0xBD: case 0xBE: case 0xBF: goto _16;
default: goto _7;
}


    __quex_assert_no_passage();
_14:
    /* (41 from 31)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(41);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0x80 )  goto _15;
else                      goto _7;


    __quex_assert_no_passage();
_15:
    /* (50 from 29) (50 from 28) (50 from 30) (50 from 41) (50 from 18)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(50);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0x80 )  goto _6;
else                      goto _7;


    __quex_assert_no_passage();
_2:
    /* (19 from 18)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(19);
goto _17;


    __quex_assert_no_passage();
_3:
    /* (20 from 18)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(20);
goto _18;


    __quex_assert_no_passage();
_4:
    /* (21 from 18)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(21);
goto _19;


    __quex_assert_no_passage();
_5:
    /* (22 from 18)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(22);
goto _20;


    __quex_assert_no_passage();
_6:
    /* (23 from 50) (23 from 18)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(23);
goto _21;


    __quex_assert_no_passage();
_7:
    /* (24 from 33) (24 from 29) (24 from 30) (24 from 31) (24 from 18) (24 from 50) (24 from 41) (24 from 32) (24 from 28)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(24);
goto _22;


    __quex_assert_no_passage();
_8:
    /* (28 from 18)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(28);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0xA0 )  goto _15;
else if( input >= 0x80 )  goto _16;
else                      goto _7;


    __quex_assert_no_passage();
_9:
    /* (29 from 31) (29 from 32) (29 from 33) (29 from 18)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(29);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0x80 )  goto _15;
else                      goto _7;


    __quex_assert_no_passage();
_10:
    /* (30 from 33) (30 from 18)  */

    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(30);
if     ( input >= 0xC0 )  goto _7;
else if( input >= 0x80 )  goto _15;
else                      goto _7;


    __quex_assert_no_passage();
_11:
    /* (31 from 18)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(31);
switch( input ) {
case 0x80: case 0x81: case 0x82: case 0x83: case 0x84: case 0x85: case 0x86: case 0x87: 
case 0x88: case 0x89: case 0x8A: case 0x8B: case 0x8C: case 0x8D: case 0x8E: case 0x8F: goto _16;
case 0x90: goto _14;
case 0x91: case 0x92: case 0x93: case 0x94: case 0x95: case 0x96: case 0x97: 
case 0x98: case 0x99: case 0x9A: case 0x9B: case 0x9C: case 0x9D: case 0x9E: case 0x9F: 
case 0xA0: case 0xA1: case 0xA2: case 0xA3: case 0xA4: case 0xA5: case 0xA6: case 0xA7: 
case 0xA8: case 0xA9: case 0xAA: case 0xAB: case 0xAC: case 0xAD: case 0xAE: case 0xAF: 
case 0xB0: case 0xB1: case 0xB2: case 0xB3: case 0xB4: case 0xB5: case 0xB6: case 0xB7: 
case 0xB8: case 0xB9: case 0xBA: case 0xBB: case 0xBC: case 0xBD: case 0xBE: case 0xBF: goto _9;
default: goto _7;
}

    /* (*) Terminal states _______________________________________________________
     *
     * States that implement actions of the 'winner patterns.                     */
_24:
    __quex_debug("* TERMINAL <LOOP EXIT>\n");
    (me->buffer._read_p) = loop_restart_p;

goto _0;

_25:
    __quex_debug("* TERMINAL <LOOP TERMINAL 12>\n");
me->counter._line_number_at_end += ((size_t)1); __quex_debug_counter();

     (me->counter._column_number_at_end) = (size_t)1;

if( me->buffer._read_p != LexemeEnd ) goto _23;

goto _0;

_26:
    __quex_debug("* TERMINAL <LOOP TERMINAL 13>\n");

self.counter._column_number_at_end -= 1;
self.counter._column_number_at_end &= ~ ((size_t)0x3);
self.counter._column_number_at_end += 4 + 1;


if( me->buffer._read_p != LexemeEnd ) goto _23;

goto _0;

_27:
    __quex_debug("* TERMINAL <LOOP TERMINAL 14>\n");
me->counter._column_number_at_end += ((size_t)1); __quex_debug_counter();

if( me->buffer._read_p != LexemeEnd ) goto _23;

goto _0;

_28:
    __quex_debug("* TERMINAL <LOOP TERMINAL 15>\n");
me->counter._column_number_at_end += ((size_t)4711); __quex_debug_counter();

if( me->buffer._read_p != LexemeEnd ) goto _23;

goto _0;

_29:
    __quex_debug("* TERMINAL <LOOP TERMINAL 16>\n");
me->counter._column_number_at_end += ((size_t)1); __quex_debug_counter();

if( me->buffer._read_p != LexemeEnd ) goto _23;

goto _0;

if(0) {
    /* Avoid unreferenced labels. */
    goto _24;
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
    __quex_assert_no_passage();
    goto _55; /* prevent unused label */
_55:

#undef self


#undef QUEX_LABEL_STATE_ROUTER


     goto _55; /* in QUEX_GOTO_STATE       */
     goto _35; /* to BAD_LEXATOM           */

    /* Avoid compiler warning: 'Unused labels' */

    goto _34;
    (void)target_state_index;
    (void)target_state_else_index;
}
