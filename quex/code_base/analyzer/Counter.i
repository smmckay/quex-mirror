#ifndef QUEX_INCLUDE_GUARD__ANALYZER__COUNTER_I
#define QUEX_INCLUDE_GUARD__ANALYZER__COUNTER_I

$$INC: definitions$$
$$INC: analyzer/asserts$$
$$INC: analyzer/Counter$$

QUEX_NAMESPACE_MAIN_OPEN

    QUEX_INLINE bool
    QUEX_NAME(Counter_construct)(QUEX_NAME(Counter)* me)
    {
        $$<count-line>   me->_line_number_at_begin   = (size_t)1;$$
        $$<count-line>   me->_line_number_at_end     = (size_t)1;$$
        $$<count-column> me->_column_number_at_begin = (size_t)1;$$
        $$<count-column> me->_column_number_at_end   = (size_t)1;$$

        $$<indentation>  QUEX_NAME(IndentationStack_init)(&me->_indentation_stack);$$
        return true;
    }

    QUEX_INLINE void
    QUEX_NAME(Counter_resources_absent_mark)(QUEX_NAME(Counter)* me)
    {
        $$<count-line> me->_line_number_at_begin               = (size_t)0;$$
        $$<count-line> me->_line_number_at_end                 = (size_t)0;$$
        $$<count-column> me->_column_number_at_begin           = (size_t)0;$$
        $$<count-column> me->_column_number_at_end             = (size_t)0;$$
        $$<indentation> me->_indentation_stack.back       = (QUEX_TYPE_INDENTATION*)0;$$
        $$<indentation> me->_indentation_stack.memory_end = (QUEX_TYPE_INDENTATION*)0;$$
    }

    QUEX_INLINE bool
    QUEX_NAME(Counter_resources_absent)(QUEX_NAME(Counter)* me)
    {
        $$<count-line> if( me->_line_number_at_begin               != (size_t)0) return false;$$
        $$<count-line> if( me->_line_number_at_end                 != (size_t)0) return false;$$
        $$<count-column> if( me->_column_number_at_begin           != (size_t)0) return false;$$
        $$<count-column> if( me->_column_number_at_end             != (size_t)0) return false;$$
        $$<indentation> if( me->_indentation_stack.back       != (QUEX_TYPE_INDENTATION*)0) return false;$$
        $$<indentation> if( me->_indentation_stack.memory_end != (QUEX_TYPE_INDENTATION*)0) return false;$$
        return true;
    }

#if 0
    QUEX_INLINE void    
    QUEX_NAME(Counter_count)(QUEX_NAME(Counter)*        me, 
                             const QUEX_TYPE_LEXATOM* LexemeBegin, 
                             const QUEX_TYPE_LEXATOM* LexemeEnd)
    {
        const QUEX_TYPE_LEXATOM* it = LexemeBegin;

        __QUEX_COUNTER_SHIFT_VALUES(*me);

        while( it != LexemeEnd )
        {
            __QUEX_COUNTER_RULES(*me, it);
        }

        __QUEX_ASSERT_COUNTER_CONSISTENCY(me); \
    }

#   if ! defined(__QUEX_COUNTER_RULES_NEWLINE)
#   define __QUEX_COUNTER_RULES_NEWLINE(counter, iterator) \
           if( *iterator == (QUEX_TYPE_LEXATOM)'\n' ) {  \
               (counter)._line_number_at_end += 1;         \
               (counter)._column_number_at_end = 0;        \
           }
#   endif

    QUEX_INLINE void    
    QUEX_NAME(Counter_count_newlines)(QUEX_NAME(Counter)*        me, 
                                      const QUEX_TYPE_LEXATOM* LexemeBegin, 
                                      const QUEX_TYPE_LEXATOM* LexemeEnd)
    {
        const QUEX_TYPE_LEXATOM* it = LexemeBegin;

        __QUEX_COUNTER_SHIFT_VALUES(*me);

        while( it != LexemeEnd )
        {
            __QUEX_COUNTER_RULES_NEWLINE(*me, it);
        }
        __QUEX_ASSERT_COUNTER_CONSISTENCY(me); \
    }
#endif

    QUEX_INLINE void 
    QUEX_NAME(Counter_print_this)(QUEX_NAME(Counter)* me)
    {
        $$<indentation> QUEX_TYPE_INDENTATION* it = 0x0;$$

        __QUEX_STD_printf("  counter: ");
        if( QUEX_NAME(Counter_resources_absent)(me) ) {
            __QUEX_STD_printf("<unitialized>\n");
            return;
        }
        __QUEX_STD_printf("{\n");

$$<count-line>-----------------------------------------------------------------
        __QUEX_STD_printf("    _line_number_at_begin:   %i;\n", (int)me->_line_number_at_begin);
        __QUEX_STD_printf("    _line_number_at_end:     %i;\n", (int)me->_line_number_at_end);
$$-----------------------------------------------------------------------------
$$<count-column>---------------------------------------------------------------
        __QUEX_STD_printf("    _column_number_at_begin: %i;\n", (int)me->_column_number_at_begin);
        __QUEX_STD_printf("    _column_number_at_end:   %i;\n", (int)me->_column_number_at_end);
$$-----------------------------------------------------------------------------
$$<indentation>----------------------------------------------------------------
        __QUEX_STD_printf("    _indentation_stack: [");
        for(it  = me->_indentation_stack.front; 
               it != &me->_indentation_stack.back[1] 
            && it != &me->_indentation_stack.front[QUEX_SETTING_INDENTATION_STACK_SIZE]; 
            ++it) {
            __QUEX_STD_printf("%i, ", (int)*it);
        }
        __QUEX_STD_printf("]\n");
$$-----------------------------------------------------------------------------
        __QUEX_STD_printf("  }\n");
    }

#if defined(QUEX_OPTION_INDENTATION_TRIGGER)
	QUEX_INLINE void
	QUEX_NAME(IndentationStack_init)(QUEX_NAME(IndentationStack)* me)
	{
        *(me->front)   = 1;          /* first indentation at column = 1 */
        me->back       = me->front;
        me->memory_end = &me->front[QUEX_SETTING_INDENTATION_STACK_SIZE];
	}
#endif

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* QUEX_INCLUDE_GUARD__ANALYZER__COUNTER_I */

