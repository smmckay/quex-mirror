#include <stdio.h>
#include <stdint.h>
#include <assert.h>

typedef DEF_CHARACTER_TYPE   Lexer_lexatom_t;
typedef Lexer_lexatom_t*   QUEX_TYPE_LEXATOM_POSITION;
typedef long                 QUEX_TYPE_GOTO_LABEL;

typedef struct Lexer_tag {
    struct {
        size_t  _line_number_at_begin;
        size_t  _column_number_at_begin;
        size_t  _line_number_at_end;
        size_t  _column_number_at_end;
    } counter;
    struct {
        QUEX_TYPE_LEXATOM_POSITION _read_p;
        QUEX_TYPE_LEXATOM_POSITION _lexeme_start_p;
    } buffer;
} Lexer;

typedef int Lexer_goto_label_t;
#define QUEX_GOTO_LABEL_VOID    ((Lexer_goto_label_t)(-1))


#ifdef DEF_DEBUG_TRACE
#   define __quex_debug(X)               printf("%s:%i: @%i/%i %s\n", __FILE__, __LINE__, me->buffer._read_p - LexemeBegin, LexemeEnd - LexemeBegin, X); \
                                         assert(me->buffer._read_p >= LexemeBegin); \
                                         assert(me->buffer._read_p <= LexemeEnd); 
#   define __quex_debug_state(X)         printf("%s:%i: @%i/%i STATE %i\n", __FILE__, __LINE__, me->buffer._read_p - LexemeBegin, LexemeEnd - LexemeBegin, X); 
#   define __quex_debug_drop_out(X)      printf("%s:%i: @%i/%i DROP_OUT %i\n", __FILE__, __LINE__, me->buffer._read_p - LexemeBegin, LexemeEnd - LexemeBegin, X); 
#else
#   define __quex_debug(X) 
#   define __quex_debug_state(X)
#   define __quex_debug_init_state(X, Y)
#   define __quex_debug_drop_out(X)
#endif
#define __quex_debug_counter(X) 
#define __quex_assert(X)   assert(X)
#define __quex_assert_no_passage()    assert(0)
#define QUEX_ERROR_EXIT(X) assert(0)
#define QUEX_NAME(X)       Lexer_ ## X

#define __QUEX_IF_COUNT_LINES(X)       X
#define __QUEX_IF_COUNT_LINES_ADD(X)   (me->counter._line_number_at_end += X)
#define __QUEX_IF_COUNT_COLUMNS(X)     X
#define __QUEX_IF_COUNT_COLUMNS_SET(X) (me->counter._column_number_at_end = X)
#define __QUEX_IF_COUNT_COLUMNS_ADD(X) (me->counter._column_number_at_end += X)
#define __QUEX_IF_COUNT_SHIFT_VALUES() \
        me->counter._line_number_at_begin = me->counter._line_number_at_end;    \
        me->counter._column_number_at_begin = me->counter._column_number_at_end;


void
DEF_COUNTER_FUNCTION(struct Lexer_tag*  me, 
                     Lexer_lexatom_t* LexemeBegin, 
                     Lexer_lexatom_t* LexemeEnd);

