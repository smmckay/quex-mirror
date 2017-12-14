/* -*- C++ -*-   vim: set syntax=cpp:
 * (C) Frankt-Rene Schaefer
 * ABSOLUTELY NO WARRANTY               */
#ifndef __QUEX_INCLUDE_GUARD__ANALYZER__MEMBER__MISC_I
#define __QUEX_INCLUDE_GUARD__ANALYZER__MEMBER__MISC_I

#if defined(QUEX_OPTION_COUNTER)
#   include <quex/code_base/analyzer/Counter>
#endif
#include <quex/code_base/token/TokenPolicy>
#include <quex/code_base/buffer/Buffer_print>

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE QUEX_TYPE_LEXATOM*  
QUEX_NAME(lexeme_start_pointer_get)(QUEX_TYPE_ANALYZER* me) 
{ return me->buffer._lexeme_start_p; }

QUEX_INLINE QUEX_TYPE_LEXATOM* 
QUEX_NAME(input_pointer_get)(QUEX_TYPE_ANALYZER* me)
{ return me->buffer._read_p; }

QUEX_INLINE void
QUEX_NAME(input_pointer_set)(QUEX_TYPE_ANALYZER* me, QUEX_TYPE_LEXATOM* Adr)
{ me->buffer._read_p = Adr; }

QUEX_INLINE QUEX_TYPE_TOKEN*  
QUEX_NAME(token_p)(QUEX_TYPE_ANALYZER* me)
{
#   define self  (*(QUEX_TYPE_DERIVED_ANALYZER*)me)
    return self_write_token_p();
#   undef self
}

QUEX_INLINE bool
QUEX_NAME(token_queue_is_empty)(QUEX_TYPE_ANALYZER* me)
{ 
    return QUEX_NAME(TokenQueue_is_empty)(&me->_token_queue); 
}

QUEX_INLINE void
QUEX_NAME(token_queue_remainder_get)(QUEX_TYPE_ANALYZER*  me,
                                     QUEX_TYPE_TOKEN**    begin, 
                                     QUEX_TYPE_TOKEN**    end)
{ QUEX_NAME(TokenQueue_remainder_get)(&me->_token_queue, begin, end); }

QUEX_INLINE const char* 
QUEX_NAME(version)(QUEX_TYPE_ANALYZER* me)
{ 
    (void)me;
    return          QUEX_STRING(QUEX_TYPE_ANALYZER)           \
           ": Version "         QUEX_SETTING_ANALYZER_VERSION \
           ". Date "            QUEX_SETTING_BUILD_DATE       \
           "Generated by Quex " QUEX_SETTING_VERSION ".";
}

QUEX_INLINE bool
QUEX_NAME(byte_order_reversion)(QUEX_TYPE_ANALYZER* me)
{ 
    __quex_assert(me->buffer.filler);
    return me->buffer.filler->_byte_order_reversion_active_f; 
}

QUEX_INLINE void     
QUEX_NAME(byte_order_reversion_set)(QUEX_TYPE_ANALYZER* me, bool Value)
{ 
    __quex_assert(me->buffer.filler);
    me->buffer.filler->_byte_order_reversion_active_f = Value; 
}


QUEX_INLINE void
QUEX_NAME(print_this)(QUEX_TYPE_ANALYZER* me)
{
    const char*       handler_name = (const char*)0;

    __QUEX_STD_printf("  mode:       %s;\n", 
                      me->__current_mode_p == 0x0 ? "0x0" : me->__current_mode_p->name);
    __QUEX_STD_printf("  error_code: %s;\n", E_Error_NAME(me->error_code));

    if( me->error_code != E_Error_None ) {
        handler_name = E_Error_MISSING_HANDLER_NAME(me->error_code);
        if( handler_name ) {
            __QUEX_STD_printf("              (* '%s' has not been specified for mode*)\n", 
                              handler_name);
        }
    }

    __QUEX_IF_COUNT(QUEX_NAME(Counter_print_this)(&me->counter));

    __QUEX_STD_printf("  _mode_stack: ");
    QUEX_NAME(ModeStack_print)(&me->_mode_stack);

    QUEX_NAME(Buffer_print_this)(&me->buffer);

    QUEX_NAME(user_print)(me);

    if( me->error_code != E_Error_None ) {
        QUEX_NAME(Buffer_print_content_detailed)(&me->buffer);
        __QUEX_STD_printf("\n\n");
    }
}

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__ANALYZER__MEMBER__MISC_I */
