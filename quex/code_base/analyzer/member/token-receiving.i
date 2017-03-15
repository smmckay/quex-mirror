/* -*- C++ -*-   vim: set syntax=cpp: */
#ifndef __QUEX_INCLUDE_GUARD__ANALYZER__MEMBER__TOKEN_RECEIVING_I
#define __QUEX_INCLUDE_GUARD__ANALYZER__MEMBER__TOKEN_RECEIVING_I

#ifndef QUEX_TYPE_ANALYZER
#   error "This file requires the macro 'QUEX_TYPE_ANALYZER' to be defined."
#endif

#include <quex/code_base/token/TokenPolicy>
#include <quex/code_base/definitions>

QUEX_NAMESPACE_MAIN_OPEN

#   define self (*me)
      
QUEX_INLINE void
QUEX_NAME(receive)(QUEX_TYPE_ANALYZER* me, QUEX_TYPE_TOKEN** result_pp)
{ 
    __QUEX_IF_TOKEN_REPETITION_SUPPORT(register QUEX_TYPE_TOKEN* result_p = 0x0);

#   if defined(QUEX_OPTION_ASSERTS) && defined(QUEX_OPTION_USER_MANAGED_TOKEN_MEMORY)
    if( QUEX_NAME(TokenQueue_begin)(&me->_token_queue) == 0x0 ) {
        QUEX_ERROR_EXIT("Token queue has not been set before call to .receive().\n"
                        "Please, consider function 'token_queue_memory_set()'.");
    }
#   endif

#   if defined(QUEX_OPTION_TOKEN_REPETITION_SUPPORT)
    if( __QUEX_SETTING_TOKEN_ID_REPETITION_TEST(self_token_p()->_id) ) {
        if( QUEX_NAME_TOKEN(repetition_n_get)(self_token_p()) != 0 ) { 
            __QUEX_REPEATED_TOKEN_DECREMENT_N(self_token_p());
            *result_pp = self_token_p();  
            return;
        } else { 
            /* Pop the repeated token from the queue */
            (void)QUEX_NAME(TokenQueue_pop)(&me->_token_queue);
        }
    }
#   endif
    /* Tokens are in queue --> take next token from queue */ 
    if( QUEX_NAME(TokenQueue_is_empty)(&me->_token_queue) == false ) {        
        *result_pp = QUEX_NAME(TokenQueue_pop)(&me->_token_queue);
        return;  
    } 
    else if( me->error_code != E_Error_None ) {
        /* This should never happen. But, in case
         * => Set 'TERMINATION' and return.                               */
        *result_pp = self_token_p();  
        if( *result_pp ) { 
            (*result_pp)->_id = __QUEX_SETTING_TOKEN_ID_TERMINATION;
        }
        return;
    }

    /* Restart filling the queue from begin */
    QUEX_NAME(TokenQueue_reset)(&me->_token_queue);

    /* Analyze until there is some content in the queue */
    do {
        me->current_analyzer_function(me);
        QUEX_ASSERT_TOKEN_QUEUE_AFTER_WRITE(&me->_token_queue);
#   if defined(QUEX_OPTION_AUTOMATIC_ANALYSIS_CONTINUATION_ON_MODE_CHANGE)
    } while( QUEX_NAME(TokenQueue_is_empty)(&self._token_queue) );
#   else
    } while( false );
#   endif
    

#   if defined(QUEX_OPTION_TOKEN_REPETITION_SUPPORT)
    result_p = self_token_p();
    if( __QUEX_SETTING_TOKEN_ID_REPETITION_TEST(result_p->_id) ) {
        QUEX_ASSERT_REPEATED_TOKEN_NOT_ZERO(result_p);
        /* First rep. is sent below. */
        if( QUEX_NAME_TOKEN(repetition_n_get)(result_p) == 1 ) {
            (void)QUEX_NAME(TokenQueue_pop)(&me->_token_queue);
        } else {
            __QUEX_REPEATED_TOKEN_DECREMENT_N(result_p); 
        }
        *result_pp = result_p;
        return;
    } else 
#   endif
    {
        *result_pp = QUEX_NAME(TokenQueue_pop)(&me->_token_queue);
        return;
    }
}


#ifndef __QUEX_OPTION_PLAIN_C
QUEX_INLINE void QUEX_MEMBER(receive)(QUEX_TYPE_TOKEN** token_pp) 
{ QUEX_NAME(receive)(this, token_pp); }
#endif

#undef self

QUEX_NAMESPACE_MAIN_CLOSE
#endif
