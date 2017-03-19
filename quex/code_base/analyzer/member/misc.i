/* -*- C++ -*-   vim: set syntax=cpp:
 * (C) Frankt-Rene Schaefer
 * ABSOLUTELY NO WARRANTY               */
#ifndef __QUEX_INCLUDE_GUARD__ANALYZER__MEMBER__MISC_I
#define __QUEX_INCLUDE_GUARD__ANALYZER__MEMBER__MISC_I

#if defined(__QUEX_OPTION_COUNTER)
#   include <quex/code_base/analyzer/Counter>
#endif
#include <quex/code_base/token/TokenPolicy>
#include <quex/code_base/buffer/Buffer_print>

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE QUEX_TYPE_LEXATOM*  
QUEX_MEMBER_FUNCTIONO(lexeme_start_pointer_get) 
{ QUEX_MAP_THIS_TO_ME(QUEX_TYPE_ANALYZER) return me->buffer._lexeme_start_p; }

QUEX_INLINE QUEX_TYPE_LEXATOM* 
QUEX_MEMBER_FUNCTIONO(input_pointer_get)
{ QUEX_MAP_THIS_TO_ME(QUEX_TYPE_ANALYZER) return me->buffer._read_p; }

QUEX_INLINE void
QUEX_MEMBER_FUNCTIONO1(input_pointer_set, QUEX_TYPE_LEXATOM* Adr)
{ QUEX_MAP_THIS_TO_ME(QUEX_TYPE_ANALYZER) me->buffer._read_p = Adr; }

QUEX_INLINE void        
QUEX_NAME(set_callback_on_buffer_content_change)(QUEX_TYPE_ANALYZER*  me,
                                                 void               (*callback)(const QUEX_TYPE_LEXATOM*, 
                                                                                const QUEX_TYPE_LEXATOM*))
{ me->buffer.on_content_change = callback; }

QUEX_INLINE QUEX_TYPE_TOKEN*  
QUEX_NAME(token_p)(QUEX_TYPE_ANALYZER* me)
{
#   define self  (*(QUEX_TYPE_DERIVED_ANALYZER*)me)
    return __QUEX_CURRENT_TOKEN_P;
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

#if defined(QUEX_OPTION_USER_MANAGED_TOKEN_MEMORY)
QUEX_INLINE void    QUEX_NAME(token_queue_get)(QUEX_TYPE_ANALYZER*  me, 
                                               QUEX_TYPE_TOKEN** begin, size_t* size)
{
    QUEX_NAME(TokenQueue_memory_get)(&me->_token_queue, begin, size); 
}

QUEX_INLINE void    QUEX_NAME(token_queue_set)(QUEX_TYPE_ANALYZER*  me, 
                                               QUEX_TYPE_TOKEN*     Begin, 
                                               size_t               Size)
{
    QUEX_NAME(TokenQueue_init)(&me->_token_queue, Begin, Begin + Size); 
}
#endif


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
    QUEX_NAME(Mode)** iterator = 0x0;
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

#   ifdef QUEX_OPTION_STRING_ACCUMULATOR
    QUEX_NAME(Accumulator_print_this)(&me->accumulator);
#   endif

#   ifdef QUEX_OPTION_POST_CATEGORIZER
    QUEX_NAME(PostCategorizer_print_this)(&me->post_categorizer);
#   endif

    __QUEX_STD_printf("  _mode_stack: {\n");
    __QUEX_STD_printf("    size:    %i;\n",
                      (int)(me->_mode_stack.memory_end - me->_mode_stack.begin));
    __QUEX_STD_printf("    content: [");
    for(iterator=me->_mode_stack.end-1; iterator >= me->_mode_stack.begin; --iterator)
        __QUEX_STD_printf("%s, ", (*iterator)->name);
    __QUEX_STD_printf("]\n");
    __QUEX_STD_printf("  }\n");
    QUEX_NAME(Buffer_print_this)(&me->buffer);

    if( me->error_code != E_Error_None ) {
        QUEX_NAME(Buffer_print_content_detailed)(&me->buffer);
        __QUEX_STD_printf("\n\n");
    }
}

#if ! defined(__QUEX_OPTION_PLAIN_C)
QUEX_INLINE void        
QUEX_MEMBER(set_callback_on_buffer_content_change)(void (*callback)(const QUEX_TYPE_LEXATOM*, 
                                                                    const QUEX_TYPE_LEXATOM*))
{ QUEX_NAME(set_callback_on_buffer_content_change)(this, callback); }

QUEX_INLINE QUEX_TYPE_TOKEN*  
QUEX_MEMBER(token_p)()
{ return QUEX_NAME(token_p)(this); }

QUEX_INLINE bool
QUEX_MEMBER(token_queue_is_empty)()
{ return QUEX_NAME(token_queue_is_empty)(this); }

QUEX_INLINE void
QUEX_MEMBER(token_queue_remainder_get)(QUEX_TYPE_TOKEN**  begin, 
                                       QUEX_TYPE_TOKEN**  end)
{ QUEX_NAME(token_queue_remainder_get)(this, begin, end); }

#if defined(QUEX_OPTION_USER_MANAGED_TOKEN_MEMORY)
QUEX_INLINE void
QUEX_MEMBER(token_queue_get)(QUEX_TYPE_TOKEN** begin, size_t* size)
{ QUEX_NAME(token_queue_get)(this, begin, size); }

QUEX_INLINE void
QUEX_MEMBER(token_queue_set)(QUEX_TYPE_TOKEN* Begin, size_t Size)
{ QUEX_NAME(token_queue_set)(this, Begin, Size); }
#endif

QUEX_INLINE const char* 
QUEX_MEMBER(version)() const
{ return QUEX_NAME(version)((QUEX_TYPE_ANALYZER*)this); }

QUEX_INLINE void
QUEX_MEMBER(print_this)()
{ QUEX_NAME(print_this)(this); }

#endif

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__ANALYZER__MEMBER__MISC_I */
