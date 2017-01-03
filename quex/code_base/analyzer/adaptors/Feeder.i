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
 * (C) 2016 Frank-Rene Schaefer.                                             */

#ifndef __QUEX_INCLUDE_GUARD__ANALYZER__ADAPTORS__FEEDER_I
#define __QUEX_INCLUDE_GUARD__ANALYZER__ADAPTORS__FEEDER_I

#include "quex/code_base/analyzer/adaptors/Feeder"

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE QUEX_TYPE_TOKEN*
QUEX_NAME(FeederBase_deliver)(QUEX_NAME(FeederBase)* me);

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
    /* Initialization                                                        */
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
     * 'fill()' returns a pointer to the first not-eaten byte.               */
    me->external_chunk.end_p   = EndP;
    me->external_chunk.begin_p = me->base.lexer->buffer.fill(&me->base.lexer->buffer, BeginP, EndP);
}

QUEX_INLINE QUEX_TYPE_TOKEN*
QUEX_NAME(Feeder_deliver)(QUEX_TYPE_FEEDER* me)
{
    QUEX_TYPE_TOKEN* token = QUEX_NAME(FeederBase_deliver)(&me->base);

    while( ! token && me->external_chunk.begin_p != me->external_chunk.end_p ) {
        /* Refill required.
         * => Try to get more out of the remainder of the external chunk.    */
        me->external_chunk.begin_p = me->base.lexer->buffer.fill(&me->base.lexer->buffer, 
                                                                 me->external_chunk.begin_p, 
                                                                 me->external_chunk.end_p);
        token = QUEX_NAME(FeederBase_deliver)(&me->base);
    }
    return token;
}

QUEX_INLINE QUEX_TYPE_TOKEN*
QUEX_NAME(FeederBase_deliver)(QUEX_NAME(FeederBase)* me)
/* RETURNS: NULL, requires refill.
 *          Pointer to token, that has been identified 
 *          (This may be the 'BYE' token).                                   */
{
    if( ! me->last_incomplete_lexeme_p ) {
        me->last_incomplete_lexeme_p = me->lexer->buffer._read_p;
    }

    if( me->stream_terminating_token_id == QUEX_NAME(receive)(me->lexer) ) {
        /* This was the very last token to be received.                      */
        me->last_incomplete_lexeme_p = (QUEX_TYPE_LEXATOM*)0;
        return me->lexer->token;
    }
    else if( me->lexer->buffer._read_p < me->lexer->buffer.input.end_p ) {
        /* Lexeme is completely inside the boundaries of the content.
         * => Return it, there is no previous (see entry of function).       */
        me->last_incomplete_lexeme_p = (QUEX_TYPE_LEXATOM*)0;
        return me->lexer->token;
    }
    else if(    me->lexer->buffer._lexeme_start_p == &me->lexer->buffer._memory._front[1] 
             && me->lexer->buffer._read_p         == &me->lexer->buffer._memory._back[0] )  {
        me->lexer->buffer.on_overflow(&me->lexer->buffer, /* ForwardF */true);
        return (QUEX_TYPE_TOKEN*)0;                         /* There's more! */
    }
    else {
        /* Detected 'Termination'
         * => Previous token may be incomplete.
         * => 'last_incomplete_lexeme_p' at position of last token.          */
        me->lexer->buffer._read_p = me->lexer->buffer._lexeme_start_p; 
        me->last_incomplete_lexeme_p = (QUEX_TYPE_LEXATOM*)0;
        return (QUEX_TYPE_TOKEN*)0;                         /* There's more! */
    }
}

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__ANALYZER__ADAPTORS__FEEDER_I */

