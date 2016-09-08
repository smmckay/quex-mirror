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

#if ! defined( __QUEX_OPTION_PLAIN_C)

QUEX_NAME(Feeder)::QUEX_NAME(Feeder)(QUEX_TYPE_ANALYZER* lexer)
{ QUEX_NAME(Feeder_construct)(this, lexer); }

QUEX_NAME(Feeder)::~QUEX_NAME(Feeder)()
{ QUEX_NAME(Feeder_destruct)(this); }

QUEX_TYPE_TOKEN* QUEX_NAME(Feeder)::deliver()
{ return QUEX_NAME(Feeder_deliver)(this); }

#endif

void
QUEX_NAME(Feeder_construct)(QUEX_TYPE_FEEDER*   me, 
                            QUEX_TYPE_ANALYZER* lexer)
{
    /* Initialization */
    QUEX_NAME_TOKEN(construct)(&me->second_token);
    me->lexer                    = lexer;
    me->last_incomplete_lexeme_p = (QUEX_TYPE_LEXATOM*)0;

#   ifdef __QUEX_OPTION_PLAIN_C
    me->destruct         = Feeder_destruct;
    me->deliver          = Feeder_deliver;
#   endif
}

QUEX_TYPE_TOKEN*
QUEX_NAME(Feeder_deliver)(QUEX_TYPE_FEEDER* me)
/* RETURNS: NULL, requires refill.
 *          Pointer to token, that has been identified 
 *          (This may be the 'BYE' token).                                   */
{
    if( ! me->last_incomplete_lexeme_p ) {
        me->last_incomplete_lexeme_p = me->lexer->input_pointer_get();
    }

    (void)me->lexer->receive();

    if( me->lexer->input_pointer_get() < me->lexer->buffer.input.end_p ) {
        /* Lexeme is completely inside the boundaries of the content.
         * => Return it, there is no previous (see entry of function).       */
        me->last_incomplete_lexeme_p = (QUEX_TYPE_LEXATOM*)0;
        return me->lexer->token;
    }
    else if( me->lexer->lexeme_start_pointer_get() == &me->lexer->buffer._memory._front[1] )  {
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

void
QUEX_NAME(Feeder_destruct)(QUEX_TYPE_FEEDER* me)
{
    QUEX_NAME_TOKEN(destruct)(&me->second_token);
}

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__ANALYZER__FEEDER_I */
