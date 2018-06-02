/* -*- C++ -*-   vim: set syntax=cpp:
 * (C) Frankt-Rene Schaefer
 * ABSOLUTELY NO WARRANTY               */
#ifndef QUEX_INCLUDE_GUARD_$$LEXER_CLASS$$__ANALYZER__MEMBER__MISC_I
#define QUEX_INCLUDE_GUARD_$$LEXER_CLASS$$__ANALYZER__MEMBER__MISC_I

#if defined(QUEX_OPTION_COUNTER)
$$INC: analyzer/Counter$$
#endif
$$INC: buffer/Buffer_print$$
$$INC: buffer/lexatoms/LexatomLoader$$
$$INC: lexeme_base$$

QUEX_NAMESPACE_MAIN_OPEN

#ifdef QUEX_OPTION_INDENTATION_TRIGGER
QUEX_INLINE void 
QUEX_NAME(indentation_handler_switch)(QUEX_TYPE_ANALYZER* me, bool ActiveF)
{ me->_indentation_handler_active_f = ActiveF; }

QUEX_INLINE bool 
QUEX_NAME(indentation_handler_is_active)(QUEX_TYPE_ANALYZER* me)
{ return me->_indentation_handler_active_f; }
#endif

QUEX_INLINE void 
QUEX_NAME(MF_error_code_clear)(QUEX_TYPE_ANALYZER* me)
{ me->error_code = E_Error_None; }

QUEX_INLINE void 
QUEX_NAME(MF_error_code_set_void)(QUEX_TYPE_ANALYZER* me)
{ me->error_code = E_Error_Uninitialized; }

QUEX_INLINE bool 
QUEX_NAME(MF_error_code_is_void)(QUEX_TYPE_ANALYZER* me)
{ return me->error_code == E_Error_Uninitialized; }

QUEX_INLINE void 
QUEX_NAME(MF_error_code_set_if_first)(QUEX_TYPE_ANALYZER* me, E_Error ErrorCode)
/* Never overwrite an error code
 * => original error is maintained.                                           */
{ if( me->error_code == E_Error_None ) me->error_code = ErrorCode; }

QUEX_INLINE QUEX_TYPE_TOKEN*  
QUEX_NAME(MF_token_p)(QUEX_TYPE_ANALYZER* me)
{
    return me->_token_queue.write_iterator; 
}

QUEX_INLINE void 
QUEX_NAME(MF_send)(QUEX_TYPE_ANALYZER* me, 
                   QUEX_TYPE_TOKEN_ID  Id)
{ QUEX_NAME(TokenQueue_push)(&me->_token_queue, Id); }

QUEX_INLINE void 
QUEX_NAME(MF_send_n)(QUEX_TYPE_ANALYZER* me, 
                     QUEX_TYPE_TOKEN_ID  Id, 
                     size_t              RepetitionN)
{ QUEX_NAME(TokenQueue_push_repeated)(&me->_token_queue, Id, RepetitionN); }

QUEX_INLINE bool 
QUEX_NAME(MF_send_text)(QUEX_TYPE_ANALYZER* me, 
                        QUEX_TYPE_TOKEN_ID  Id,
                        QUEX_TYPE_LEXATOM*  BeginP, 
                        QUEX_TYPE_LEXATOM*  EndP)
{ return QUEX_NAME(TokenQueue_push_text)(&me->_token_queue, Id, BeginP, EndP); }

QUEX_INLINE bool 
QUEX_NAME(MF_send_string)(QUEX_TYPE_ANALYZER* me,
                          QUEX_TYPE_TOKEN_ID  Id,
                          QUEX_TYPE_LEXATOM*  ZeroTerminatedString)
{ 
    const size_t Length = QUEX_NAME(lexeme_length)((const QUEX_TYPE_LEXATOM*)ZeroTerminatedString);

    return QUEX_NAME(TokenQueue_push_text)(&me->_token_queue, Id, ZeroTerminatedString, 
                                           ZeroTerminatedString + (ptrdiff_t)Length + 1); 
}

QUEX_INLINE bool
QUEX_NAME(MF_byte_order_reversion)(QUEX_TYPE_ANALYZER* me)
{ 
    __quex_assert(0 != me->buffer.filler);
    return me->buffer.filler->_byte_order_reversion_active_f; 
}

QUEX_INLINE void     
QUEX_NAME(MF_byte_order_reversion_set)(QUEX_TYPE_ANALYZER* me, bool Value)
{ 
    __quex_assert(0 != me->buffer.filler);
    me->buffer.filler->_byte_order_reversion_active_f = Value; 
}

QUEX_INLINE const char*
QUEX_NAME(MF_input_name)(QUEX_TYPE_ANALYZER* me)
{ return me->__input_name; }

QUEX_INLINE bool
QUEX_NAME(MF_input_name_set)(QUEX_TYPE_ANALYZER* me, const char* InputNameP)
/* Sets the 'input name', i.e. some string that identifies the input stream.
 * In case of failure '.__input_name' is set to NULL.
 *
 * RETURNS: true, for success. false, else.                                   */
{ 
    if( me->__input_name ) {
        QUEXED(MemoryManager_free)(me->__input_name, E_MemoryObjectType_INPUT_NAME);
    }
    if(  ! InputNameP ) {
        me->__input_name = (char*)0;
        return true;
    }
    else {
        me->__input_name = QUEXED(MemoryManager_clone_string)(InputNameP);
        return me->__input_name ? true : false;
    }
}

QUEX_INLINE const char* 
QUEX_NAME(MF_version)(QUEX_TYPE_ANALYZER* me)
{ 
    (void)me;
    return          QUEX_STRING(QUEX_TYPE_ANALYZER)           \
           ": Version "         QUEX_SETTING_ANALYZER_VERSION \
           ". Date "            QUEX_SETTING_BUILD_DATE       \
           "Generated by Quex " QUEX_SETTING_VERSION ".";
}

QUEX_INLINE void
QUEX_NAME(MF_print_this)(QUEX_TYPE_ANALYZER* me)
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
#   ifdef QUEX_OPTION_INDENTATION_TRIGGER
    __QUEX_STD_printf("  _indentation_handler_active_f: %s;\n" , 
                      me->_indentation_handler_active_f ? "true" : "false");
#   endif

    __QUEX_STD_printf("  _mode_stack: ");
    QUEX_NAME(ModeStack_print)(&me->_mode_stack);

    QUEX_NAME(Buffer_print_this)(&me->buffer);

    QUEX_NAME(user_print)(me);

    if( me->error_code != E_Error_None ) {
        QUEX_NAME(Buffer_print_content_detailed)(&me->buffer);
        __QUEX_STD_printf("\n\n");
    }
}

#ifdef  QUEX_OPTION_COUNTER_LINE
QUEX_INLINE size_t QUEX_NAME(MF_line_number)(const QUEX_TYPE_ANALYZER* me)            { return QUEX_NAME(MF_line_number_at_begin)(me); }
QUEX_INLINE size_t QUEX_NAME(MF_line_number_at_begin)(const QUEX_TYPE_ANALYZER* me)   { return me->counter._line_number_at_begin; }
QUEX_INLINE size_t QUEX_NAME(MF_line_number_at_end)(const QUEX_TYPE_ANALYZER* me)     { return me->counter._line_number_at_end; }
QUEX_INLINE void   QUEX_NAME(MF_line_number_set)(QUEX_TYPE_ANALYZER* me, size_t Value) { me->counter._line_number_at_end = Value; }
#endif
#ifdef  QUEX_OPTION_COUNTER_COLUMN
QUEX_INLINE size_t QUEX_NAME(MF_column_number)(const QUEX_TYPE_ANALYZER* me)          { return QUEX_NAME(MF_column_number_at_begin)(me); }
QUEX_INLINE size_t QUEX_NAME(MF_column_number_at_begin)(const QUEX_TYPE_ANALYZER* me) { return me->counter._column_number_at_begin; }
QUEX_INLINE size_t QUEX_NAME(MF_column_number_at_end)(const QUEX_TYPE_ANALYZER* me)   { return me->counter._column_number_at_end; }
QUEX_INLINE void   QUEX_NAME(MF_column_number_set)(QUEX_TYPE_ANALYZER* me, size_t Value) { me->counter._column_number_at_end = Value; }
#endif
#ifdef   QUEX_OPTION_INDENTATION_TRIGGER
QUEX_INLINE size_t  QUEX_NAME(MF_indentation)(const QUEX_TYPE_ANALYZER* me)           
{ return (size_t)(me->counter._indentation_stack.back - me->counter._indentation_stack.front) + (size_t)1; }
#endif


QUEX_NAMESPACE_MAIN_CLOSE


#endif /* QUEX_INCLUDE_GUARD_$$LEXER_CLASS$$__ANALYZER__MEMBER__MISC_I */
