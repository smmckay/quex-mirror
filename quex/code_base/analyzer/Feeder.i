/* -*- C++ -*- vim: set syntax=cpp: */
/* 
 * PURPOSE: A 'feeder' coordinates the lexical analysis based on input that
 *          is *NOT* delivered through a byte loader in the background. 
 *
 * In cases where the user wishes to fill the lexical analyzer buffer manually,
 * caution has to be applied to avoid consuming invalid tokens and to setup
 * the stream appropriately. This coordination is safely implemented in the
 * small, but well thought-through function 'deliver' below. Examples of how
 * to use it can be found in the 'demo/010' directory.
 *
 * (C) 2016 Frank-Rene Schaefer.                                             */

#ifndef __QUEX_INCLUDE_GUARD__ANALYZER__FEEDER_I
#define __QUEX_INCLUDE_GUARD__ANALYZER__FEEDER_I

#include "quex/code_base/analyzer/Feeder"

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE QUEX_TYPE_TOKEN*
QUEX_NAME(Feeder_deliver_core)(QUEX_NAME(FeederBase)* me);

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



QUEX_INLINE
QUEX_NAME(Infiltrator)::QUEX_NAME(Infiltrator)(QUEX_TYPE_ANALYZER* lexer,
                                               QUEX_TYPE_TOKEN_ID  StreamTerminatingTokenId)
{ QUEX_NAME(Infiltrator_construct)(this, lexer, StreamTerminatingTokenId); }

QUEX_INLINE void
QUEX_NAME(Infiltrator)::access(void** begin_p, const void** end_p)
{ QUEX_NAME(Infiltrator_access)(this, begin_p, end_p); }

QUEX_INLINE bool
QUEX_NAME(Infiltrator)::gavage(ptrdiff_t ReceivedN)
{ return QUEX_NAME(Infiltrator_gavage)(this, ReceivedN); }

QUEX_INLINE QUEX_TYPE_TOKEN* 
QUEX_NAME(Infiltrator)::deliver()
{ return QUEX_NAME(Infiltrator_deliver)(this); }

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
    me->deliver = Feeder_deliver;
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
    QUEX_TYPE_TOKEN* token = QUEX_NAME(Feeder_deliver_core)(&me->base);

    while( ! token && me->external_chunk.begin_p != me->external_chunk.end_p ) {
        /* Refill required.
         * => Try to get more out of the remainder of the external chunk.    */
        me->external_chunk.begin_p = me->base.lexer->buffer.fill(&me->base.lexer->buffer, 
                                                            me->external_chunk.begin_p, 
                                                            me->external_chunk.end_p);
        token = QUEX_NAME(Feeder_deliver_core)(&me->base);
    }
    return token;
}

QUEX_INLINE QUEX_TYPE_TOKEN*
QUEX_NAME(Feeder_deliver_core)(QUEX_NAME(FeederBase)* me)
/* RETURNS: NULL, requires refill.
 *          Pointer to token, that has been identified 
 *          (This may be the 'BYE' token).                                   */
{
    if( ! me->last_incomplete_lexeme_p ) {
        me->last_incomplete_lexeme_p = me->lexer->input_pointer_get();
    }

    if( me->stream_terminating_token_id == me->lexer->receive() ) {
        /* This was the very last token to be received.                      */
        me->last_incomplete_lexeme_p = (QUEX_TYPE_LEXATOM*)0;
        return me->lexer->token;
    }
    else if( me->lexer->input_pointer_get() < me->lexer->buffer.input.end_p ) {
        /* Lexeme is completely inside the boundaries of the content.
         * => Return it, there is no previous (see entry of function).       */
        me->last_incomplete_lexeme_p = (QUEX_TYPE_LEXATOM*)0;
        return me->lexer->token;
    }
    else if(    me->lexer->lexeme_start_pointer_get() == &me->lexer->buffer._memory._front[1] 
             && me->lexer->input_pointer_get()        == &me->lexer->buffer._memory._back[0] )  {
        me->lexer->buffer.on_overflow(&me->lexer->buffer, /* ForwardF */true);
        return (QUEX_TYPE_TOKEN*)0;                         /* There's more! */
    }
    else {
        /* Detected 'Termination'
         * => Previous token may be incomplete.
         * => 'last_incomplete_lexeme_p' at position of last token.          */
        me->lexer->input_pointer_set(me->lexer->lexeme_start_pointer_get());
        me->last_incomplete_lexeme_p = (QUEX_TYPE_LEXATOM*)0;
        return (QUEX_TYPE_TOKEN*)0;                         /* There's more! */
    }
}

QUEX_INLINE void
QUEX_NAME(Infiltrator_construct)(QUEX_TYPE_INFILTRATOR*  me, 
                                 QUEX_TYPE_ANALYZER*     lexer,
                                 QUEX_TYPE_TOKEN_ID      StreamTerminatingTokenId)
{
    /* Initialization                                                        */
    me->base.lexer                       = lexer;
    me->base.last_incomplete_lexeme_p    = (QUEX_TYPE_LEXATOM*)0;
    me->base.stream_terminating_token_id = StreamTerminatingTokenId;

#   ifdef __QUEX_OPTION_PLAIN_C
    me->access  = QUEX_NAME(Infiltrator_access);
    me->gavage  = QUEX_NAME(Infiltrator_gavage);
    me->deliver = QUEX_NAME(Infiltrator_deliver);
#   endif
}
/*___________________________________________________________________________*/

QUEX_INLINE void
QUEX_NAME(Infiltrator_access)(QUEX_TYPE_INFILTRATOR* me,
                              void** begin_p, const void** end_p)
/* Provides access to internal buffer to be filled. 
 *
 * MODIFIES: [0] 'begin_p' pointing to the beginning of the buffer region that
 *                can be filled with data.
 *           [1] 'end_p' pointing to the end of the buffer's region, i.e. to
 *                the first element behind it.                               */
{
    me->base.lexer->buffer.fill_prepare(&me->base.lexer->buffer, begin_p, end_p);
}

QUEX_INLINE bool
QUEX_NAME(Infiltrator_gavage)(QUEX_TYPE_INFILTRATOR* me, ptrdiff_t ReceivedN)
{
    void*       begin_p;
    const void* end_p;

    me->base.lexer->buffer.filler->derived.get_fill_boundaries(me->base.lexer->buffer.filler,
                                                               &me->base.lexer->buffer, 
                                                               &begin_p, &end_p);
    if( ReceivedN > (const uint8_t*)end_p - (uint8_t*)begin_p ) {
        return false;
    }
    me->base.lexer->buffer.fill_finish(&me->base.lexer->buffer, 
                                       &((uint8_t*)begin_p)[ReceivedN]);
    return true;
}

QUEX_INLINE QUEX_TYPE_TOKEN*
QUEX_NAME(Infiltrator_deliver)(QUEX_TYPE_INFILTRATOR* me)
{
    return QUEX_NAME(Feeder_deliver_core)(&me->base);
}


QUEX_NAMESPACE_MAIN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__ANALYZER__FEEDER_I */
