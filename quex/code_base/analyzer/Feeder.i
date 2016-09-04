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
    me->prev_token_p             = &me->second_token;
    me->first_token_p            = lexer->token;
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
        me->first_token_p            = me->lexer->token;
        me->first_token_p->_id       = QUEX_TKN_TERMINATION;
        me->prev_token_p             = &me->second_token;
    }

    /* Loop until 'TERMINATION' or 'BYE' is received.                   
     *   TERMINATION => possible reload/refill
     *   BYE         => end of game                                          */
    while( 1 + 1 == 2 ) {
        /* Current token becomes previous token of next run.                 */
        me->prev_token_p = QUEX_NAME(token_p_swap)(me->lexer, me->prev_token_p);

        if( me->lexer->receive() == QUEX_TKN_TERMINATION ) {
            me->lexer->input_pointer_set(me->last_incomplete_lexeme_p);
            (void)me->lexer->token_p_swap(me->first_token_p);
            me->last_incomplete_lexeme_p = (QUEX_TYPE_LEXATOM*)0;
            return (QUEX_TYPE_TOKEN*)0;                     /* There's more! */
        }
        else if( me->prev_token_p->_id != QUEX_TKN_TERMINATION ) {
            /* Previous token not followed by 'BYE' or 'TERMINATION'.
             * => The matching was not interrupted by end of content.
             * => Lexeme is complete. Previous token can be considered.      */
            me->last_incomplete_lexeme_p = me->lexer->lexeme_start_pointer_get();
            return me->prev_token_p;
        }
    }
}

void
QUEX_NAME(Feeder_destruct)(QUEX_TYPE_FEEDER* me)
{
    QUEX_NAME_TOKEN(destruct)(&me->second_token);
}

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__ANALYZER__FEEDER_I */
