/* -*- C++ -*-   vim: set syntax=cpp: */
#ifndef __QUEX_INCLUDE_GUARD__ANALYZER__MEMBER__TOKEN_RECEIVING_I
#define __QUEX_INCLUDE_GUARD__ANALYZER__MEMBER__TOKEN_RECEIVING_I

#ifndef QUEX_TYPE_ANALYZER
#   error "This file requires the macro 'QUEX_TYPE_ANALYZER' to be defined."
#endif

#include <quex/code_base/token/TokenPolicy>
#include <quex/code_base/definitions>

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE void
QUEX_NAME(receive)(QUEX_TYPE_ANALYZER* me, QUEX_TYPE_TOKEN** result_pp)
{ 
    *result_pp = QUEX_NAME(TokenQueue_pop)(&me->_token_queue);
    if( *result_pp ) {
        return;
    }
    else if( me->error_code != E_Error_None ) {
        QUEX_NAME(TokenQueue_set_token_TERMINATION)(&me->_token_queue);
    }
    else {
        /* Restart filling the queue from begin                                   */
        QUEX_NAME(TokenQueue_reset)(&me->_token_queue); /* Use 1st token of queue */

        /* Analyze until there is some content in the queue                       */
        do {
            me->current_analyzer_function(me);

            QUEX_ASSERT_TOKEN_QUEUE_AFTER_WRITE(&me->_token_queue);

            if( me->error_code != E_Error_None ) {
                QUEX_NAME(TokenQueue_set_token_TERMINATION)(&me->_token_queue);
                break;
            }

        } while( QUEX_NAME(TokenQueue_is_empty)(&me->_token_queue) );
    }
    
    *result_pp = QUEX_NAME(TokenQueue_pop)(&me->_token_queue);
}

#ifndef __QUEX_OPTION_PLAIN_C
QUEX_INLINE void QUEX_MEMBER(receive)(QUEX_TYPE_TOKEN** token_pp) 
{ QUEX_NAME(receive)(this, token_pp); }
#endif


QUEX_NAMESPACE_MAIN_CLOSE
#endif
