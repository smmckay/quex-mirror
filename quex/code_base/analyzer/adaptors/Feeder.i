/* -*- C++ -*- vim: set syntax=cpp: 
 * 
 * PURPOSE: Feeder -- coordinates the lexical analysis based on input that
 *                    is fed manually by the caller of the lexical analyser.
 *
 * This file implements an adaptor to a lexical analyzer's class in order to
 * specify a specific 'data feeding scenario'. Where 'normal' lexical analysis
 * relies on filling in the background from some stream or socket, feeding
 * and gavaging implies manual interaction of the consumer of the caller.
 *
 * Feeding can be applied if data chunks arrive in arbitrary sizes. During
 * feeding those chunks are presented to the 'Feeder'. The feeder feeds sub-
 * chunks of those-as big as possible-into the lexical analyzers buffer. The
 * process involves a 'copying' operation. Once a Feeder deliver's a Null
 * token, it can be assumed that all content has been copied or consumed. The
 * memory pointed to can then be freed and new content can be presented to
 * the feeder.
 *
 * PROCEDURE:
 *
 * Data that comes from a framework must be fed using the 'feed()' function.
 * Then, the 'deliver()' function needs to be called. It delivers tokens found
 * until it returns Null. This indicates that all data has been consumed and
 * new data is required to continue analysis. The user must then call 'feed()'
 * again.
 *
 * The constructor of a feeder receives a 'StreamTerminatingTokenId' that 
 * tells when the stream is absolutely terminated. The caller must check
 * the received token against this id and terminate in case that it arrived.
 *
 * EXAMPLES: See the demo's '010' directory.
 *
 * (C) 2016 Frank-Rene Schaefer.                                              */

#ifndef __QUEX_INCLUDE_GUARD__ANALYZER__ADAPTORS__FEEDER_I
#define __QUEX_INCLUDE_GUARD__ANALYZER__ADAPTORS__FEEDER_I

#include "quex/code_base/analyzer/adaptors/Feeder"

QUEX_NAMESPACE_MAIN_OPEN

#if ! defined( __QUEX_OPTION_PLAIN_C)

QUEX_INLINE
QUEX_NAME(Feeder)::QUEX_NAME(Feeder)(QUEX_TYPE_ANALYZER* lexer,
                                     QUEX_TYPE_TOKEN_ID  StreamTerminatingTokenId)
{ QUEX_NAME(Feeder_construct)(this, lexer, StreamTerminatingTokenId); }

QUEX_INLINE void
QUEX_NAME(Feeder)::feed(const void* BeginP, const void* EndP)
{ QUEX_NAME(Feeder_feed)(this, BeginP, EndP); }

QUEX_INLINE QUEX_TYPE_TOKEN* 
QUEX_NAME(Feeder)::deliver()
{ return QUEX_NAME(Feeder_deliver)(this); }

#endif

QUEX_INLINE void
QUEX_NAME(Feeder_construct)(QUEX_TYPE_FEEDER*   me, 
                            QUEX_TYPE_ANALYZER* lexer,
                            QUEX_TYPE_TOKEN_ID  StreamTerminatingTokenId)
{
    /* Initialization                                                         */
    me->base.lexer                       = lexer;
    me->base.last_incomplete_lexeme_p    = (QUEX_TYPE_LEXATOM*)0;
    me->base.stream_terminating_token_id = StreamTerminatingTokenId;

    me->external_chunk.begin_p   = (void*)0;
    me->external_chunk.end_p     = (void*)0;

#   ifdef __QUEX_OPTION_PLAIN_C
    me->feed    = QUEX_NAME(Feeder_feed);
    me->deliver = QUEX_NAME(Feeder_deliver);
#   endif
}

QUEX_INLINE void
QUEX_NAME(Feeder_feed)(QUEX_TYPE_FEEDER* me, const void* BeginP, const void* EndP)
{
    /* Copy buffer content into the analyzer's buffer-as much as possible.
     * 'fill()' returns a pointer to the first not-eaten byte.                */
    me->external_chunk.end_p   = EndP;
    me->external_chunk.begin_p = me->base.lexer->buffer.fill(&me->base.lexer->buffer, BeginP, EndP);
}

QUEX_INLINE QUEX_TYPE_TOKEN*
QUEX_NAME(Feeder_deliver)(QUEX_TYPE_FEEDER* me)
{
    QUEX_TYPE_TOKEN*  token = QUEX_NAME(FeederBase_deliver)(&me->base, 
                                                            me->external_chunk.begin_p == me->external_chunk.end_p);
    const void*       previous_begin_p;

    while( ! token && me->external_chunk.begin_p != me->external_chunk.end_p ) {
        /* Refill required.
         * => Try to get more out of the remainder of the external chunk.     */
        previous_begin_p           = me->external_chunk.begin_p;
        me->external_chunk.begin_p = me->base.lexer->buffer.fill(&me->base.lexer->buffer, 
                                                                 me->external_chunk.begin_p, 
                                                                 me->external_chunk.end_p);
        if( me->external_chunk.begin_p == previous_begin_p ) {
            /* If '_read_p' stands at beginning of buffer, no more content 
             * can be filled. Buffer size must be large enough to hold a 
             * complete token queue for one step (including skipped data).    */
            me->base.lexer->error_code = E_Error_Buffer_CannotAbsorbMoreContent;
            return (QUEX_TYPE_TOKEN*)0;
        }

        token = QUEX_NAME(FeederBase_deliver)(&me->base, 
                                              me->external_chunk.begin_p == me->external_chunk.end_p);
    }
    return token;
}

QUEX_INLINE QUEX_TYPE_TOKEN*
QUEX_NAME(FeederBase_deliver)(QUEX_NAME(FeederBase)* me, bool EndOfChunkF)
/* RETURNS: NULL, requires refill.
 *          Pointer to token, that has been identified 
 *          (This may be the 'BYE' token).                                    */
{
    QUEX_TYPE_TOKEN*       token_p;
    QUEX_TYPE_LEXATOM*     start_p;
    const QUEX_TYPE_TOKEN* last_token_in_queue_p;

    /* If token queue is not empty => it has been ensured that all tokens are
     * generated well inside the buffer's boundaries.                         */
    token_p = QUEX_NAME(TokenQueue_pop)(&me->lexer->_token_queue);
    if( token_p ) {
        return token_p;
    }
    else if( me->lexer->error_code != E_Error_None ) {
        QUEX_NAME(TokenQueue_set_token_TERMINATION)(&me->lexer->_token_queue);
        return QUEX_NAME(TokenQueue_pop)(&me->lexer->_token_queue);
    }

    /* Token queue is empty. A new step begins. 
     * Backup read position. It may be reset in case of reaching boundaries.  */
    do {
        start_p = me->lexer->buffer._read_p;

        me->lexer->current_analyzer_function(me->lexer);
        QUEX_ASSERT_TOKEN_QUEUE_AFTER_WRITE(&me->lexer->_token_queue);

        if( me->lexer->error_code != E_Error_None ) {
            QUEX_NAME(TokenQueue_reset)(&me->lexer->_token_queue);
            return (QUEX_TYPE_TOKEN*)0; 
        }

    } while( QUEX_NAME(TokenQueue_is_empty)(&me->lexer->_token_queue) );

    if( me->lexer->buffer._read_p < me->lexer->buffer.input.end_p ) {
        /* Complete token queue is generated without reaching buffer boarders.*/
        return token_p;
    }
    else {
        last_token_in_queue_p = QUEX_NAME(TokenQueue_last_token)(&me->lexer->_token_queue); 
        __quex_assert(last_token_in_queue_p); /* not empty => last token.     */
        if(    last_token_in_queue_p->_id == me->stream_terminating_token_id 
            && EndOfChunkF ) {
            /* The 'good bye' token may stand very well on the border.        */
            return token_p;
        }
        else {
            /* All generated tokens are in doubt. 
             * Reset token queue. Restart analysis with more content.         */
            QUEX_NAME(TokenQueue_reset)(&me->lexer->_token_queue);
            me->lexer->buffer._read_p = start_p;
            return (QUEX_TYPE_TOKEN*)0; 
        }
    }
}

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__ANALYZER__ADAPTORS__FEEDER_I */

