#include <data/check.h>

#ifdef QUEX_OPTION_COUNTER
void
TEST_MODE_counter(struct _tag* me, None_lexatom_t* LexemeBegin, None_lexatom_t* LexemeEnd)
{
#   define self (*me)
/*  'QUEX_GOTO_STATE' requires 'QUEX_LABEL_STATE_ROUTER' */
#   define QUEX_LABEL_STATE_ROUTER _22
    None_lexatom_t              input                          = (None_lexatom_t)(0x00);
    QUEX_TYPE_GOTO_LABEL           target_state_else_index        = QUEX_GOTO_LABEL_VOID;
    QUEX_TYPE_GOTO_LABEL           target_state_index             = QUEX_GOTO_LABEL_VOID;
#   ifdef QUEX_OPTION_COUNTER_COLUMN
    None_lexatom_t*             count_reference_p              = (None_lexatom_t*)0x0;
#   endif /* QUEX_OPTION_COUNTER_COLUMN */
    (void)me;
    __QUEX_COUNTER_SHIFT_COLUMNS();
    __QUEX_COUNTER_SHIFT_LINES();
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
     count_reference_p = (me->buffer._read_p);

 count_reference_p = (me->buffer._read_p);

    input = *(me->buffer._read_p);

_15:
    __quex_debug_init_state(13);
switch( input ) {
case 0x0: case 0x1: case 0x2: case 0x3: case 0x4: case 0x5: case 0x6: case 0x7: 
case 0x8: goto _4;
case 0x9: goto _3;
case 0xA: goto _2;
case 0xB: case 0xC: case 0xD: case 0xE: case 0xF: 
case 0x10: case 0x11: case 0x12: case 0x13: case 0x14: case 0x15: case 0x16: case 0x17: 
case 0x18: case 0x19: case 0x1A: case 0x1B: case 0x1C: case 0x1D: case 0x1E: case 0x1F: 
case 0x20: case 0x21: case 0x22: case 0x23: case 0x24: case 0x25: case 0x26: case 0x27: 
case 0x28: case 0x29: case 0x2A: case 0x2B: case 0x2C: case 0x2D: case 0x2E: case 0x2F: 
case 0x30: case 0x31: case 0x32: case 0x33: case 0x34: case 0x35: case 0x36: case 0x37: 
case 0x38: case 0x39: case 0x3A: case 0x3B: case 0x3C: case 0x3D: case 0x3E: case 0x3F: 
case 0x40: case 0x41: case 0x42: case 0x43: case 0x44: case 0x45: case 0x46: case 0x47: 
case 0x48: case 0x49: case 0x4A: case 0x4B: case 0x4C: case 0x4D: case 0x4E: case 0x4F: 
case 0x50: case 0x51: case 0x52: case 0x53: case 0x54: case 0x55: case 0x56: case 0x57: 
case 0x58: case 0x59: case 0x5A: case 0x5B: case 0x5C: case 0x5D: case 0x5E: case 0x5F: 
case 0x60: case 0x61: case 0x62: case 0x63: case 0x64: case 0x65: case 0x66: case 0x67: 
case 0x68: case 0x69: case 0x6A: case 0x6B: case 0x6C: case 0x6D: case 0x6E: case 0x6F: 
case 0x70: case 0x71: case 0x72: case 0x73: case 0x74: case 0x75: case 0x76: case 0x77: 
case 0x78: case 0x79: case 0x7A: case 0x7B: case 0x7C: case 0x7D: case 0x7E: case 0x7F: goto _4;
default: goto _5;
}


    __quex_assert_no_passage();
_10:
    /* (13 from 19)  */
    goto _15;


    __quex_assert_no_passage();
_8:
    /* (DROP_OUT from 16)  */
goto _14;

    __quex_debug("Drop-Out Catcher\n");


    __quex_assert_no_passage();
_6:
    /* (DROP_OUT from 14)  */
goto _12;


    __quex_assert_no_passage();
_7:
    /* (DROP_OUT from 15)  */
goto _13;


    __quex_assert_no_passage();
_9:
    /* (DROP_OUT from 18)  */
goto _17;


    __quex_assert_no_passage();
_4:
    /* (16 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(16);
goto _8;


    __quex_assert_no_passage();
_5:
    /* (18 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(18);
goto _9;


    __quex_assert_no_passage();
_2:
    /* (14 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(14);
goto _6;


    __quex_assert_no_passage();
_3:
    /* (15 from 13)  */
    ++(me->buffer._read_p);

    input = *(me->buffer._read_p);


    __quex_debug_state(15);
goto _7;

    /* (*) Terminal states _______________________________________________________
     *
     * States that implement actions of the 'winner patterns.                     */
_11:
    __quex_debug("* TERMINAL <LOOP EXIT>\n");
    --(me->buffer._read_p);

__QUEX_IF_COUNT_COLUMNS_ADD((size_t)(((me->buffer._read_p) - count_reference_p)));

goto _0;

_12:
    __quex_debug("* TERMINAL <LOOP 8>\n");
__QUEX_IF_COUNT_LINES_ADD((size_t)1);

     (me->counter._column_number_at_end) = (size_t)1;

 count_reference_p = (me->buffer._read_p);

if( me->buffer._read_p != LexemeEnd ) goto _10;

goto _0;

_13:
    __quex_debug("* TERMINAL <LOOP 9>\n");
__QUEX_IF_COUNT_COLUMNS_ADD((size_t)(((me->buffer._read_p) - count_reference_p - 1)));


self.counter._column_number_at_end -= 1;
self.counter._column_number_at_end &= ~ ((size_t)0x3);
self.counter._column_number_at_end += 4 + 1;


 count_reference_p = (me->buffer._read_p);

if( me->buffer._read_p != LexemeEnd ) goto _10;

goto _0;

_14:
    __quex_debug("* TERMINAL <LOOP 10>\n");
if( me->buffer._read_p != LexemeEnd ) goto _10;

__QUEX_IF_COUNT_COLUMNS_ADD((size_t)(((me->buffer._read_p) - count_reference_p)));

goto _0;

if(0) {
    /* Avoid unreferenced labels. */
    goto _11;
    goto _12;
    goto _13;
    goto _14;
}
_17: /* TERMINAL: BAD_LEXATOM */
;
_23: /* TERMINAL: FAILURE     */
goto _0;
_0:
/* Assert: lexeme in codec's character boundaries. */

     __quex_assert(me->buffer._read_p == LexemeEnd);
    return;
#   ifndef QUEX_OPTION_COMPUTED_GOTOS
    __quex_assert_no_passage();
_22:
#   endif /* QUEX_OPTION_COMPUTED_GOTOS */

#undef self


#undef QUEX_LABEL_STATE_ROUTER

#    if ! defined(QUEX_OPTION_COMPUTED_GOTOS)
     goto _22; /* in QUEX_GOTO_STATE       */
     goto _17; /* to BAD_LEXATOM           */
#    endif
    /* Avoid compiler warning: 'Unused labels' */

    goto _23;
    (void)target_state_index;
    (void)target_state_else_index;
}
#endif /* QUEX_OPTION_COUNTER */
