/* -*- C++ -*- vim: set syntax=cpp: 
 * PURPOSE: Token Queue 
 *
 * A token queue is a queue where read and write cycles are separate.
 * That is, when the queue is filled, it is not read until the 
 * filling terminated. Then, the read does not terminate before there
 * is no more token left.
 *
 * Wrap-arround is neither necessary nor meaningful!
 *
 * (C) 2004-2017 Frank-Rene Schaefer                                          */
#ifndef QUEX_INCLUDE_GUARD__TOKEN__TOKEN_QUEUE_I
#define QUEX_INCLUDE_GUARD__TOKEN__TOKEN_QUEUE_I

$$INC: definitions$$
$$INC: asserts$$
$$INC: quex/MemoryManager$$

/* NOTE: QUEX_TYPE_TOKEN must be defined at this place!                       */

$$INC: token/TokenQueue$$

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE void             
QUEX_NAME(TokenQueue_push_core)(QUEX_NAME(TokenQueue)* me, QUEX_TYPE_TOKEN_ID Id);

QUEX_INLINE bool
QUEX_NAME(TokenQueue_construct)(QUEX_NAME(TokenQueue)* me, 
                                QUEX_TYPE_ANALYZER*    lexer,
                                const size_t           N)
/* me:     The token queue.
 * Memory: Pointer to memory of token queue, 0x0 --> no initial memory.
 * N:      Number of token objects that the array can carry.                  */
{
    QUEX_TYPE_TOKEN*   iterator   = 0x0;
    QUEX_TYPE_TOKEN*   memory     = (QUEX_TYPE_TOKEN*)QUEX_NNAME_LIB(MemoryManager_allocate)(
                                             N * sizeof(QUEX_TYPE_TOKEN),
                                             E_MemoryObjectType_TOKEN_ARRAY);
    QUEX_TYPE_TOKEN*   memory_end = &memory[N];

    if( ! memory ) {
        QUEX_NAME(TokenQueue_resources_absent_mark)(me);
        return false;
    }

    __quex_assert(memory != 0x0);

    /* Call placement new (plain constructor) for all tokens in chunk.        */
    for(iterator = memory; iterator != memory_end; ++iterator) {
        QUEX_NAME_TOKEN(construct)(iterator);
    }
    QUEX_NAME(TokenQueue_init)(me, memory, memory_end); 
    me->the_lexer = lexer;
    return true;
}

QUEX_INLINE void
QUEX_NAME(TokenQueue_reset)(QUEX_NAME(TokenQueue)* me) 
{                                                    
    me->read_iterator  = (QUEX_TYPE_TOKEN*)me->begin; 
    me->write_iterator = (QUEX_TYPE_TOKEN*)me->begin; 
}

QUEX_INLINE void
QUEX_NAME(TokenQueue_init)(QUEX_NAME(TokenQueue)* me, 
                           QUEX_TYPE_TOKEN*       Memory, 
                           QUEX_TYPE_TOKEN*       MemoryEnd) 
{
    me->begin = Memory;                           
    me->end   = MemoryEnd;                        
    QUEX_NAME(TokenQueue_reset)(me);                                
}

QUEX_INLINE void
QUEX_NAME(TokenQueue_resources_absent_mark)(QUEX_NAME(TokenQueue)* me) 
{
    me->begin          = (QUEX_TYPE_TOKEN*)0;                           
    me->end            = (QUEX_TYPE_TOKEN*)0;
    me->read_iterator  = (QUEX_TYPE_TOKEN*)0; 
    me->write_iterator = (QUEX_TYPE_TOKEN*)0; 
    me->the_lexer      = (QUEX_TYPE_ANALYZER*)0; 
}

QUEX_INLINE bool
QUEX_NAME(TokenQueue_resources_absent)(QUEX_NAME(TokenQueue)* me) 
{
    return    me->begin          == (QUEX_TYPE_TOKEN*)0                           
           && me->end            == (QUEX_TYPE_TOKEN*)0
           && me->read_iterator  == (QUEX_TYPE_TOKEN*)0 
           && me->write_iterator == (QUEX_TYPE_TOKEN*)0
           && me->the_lexer      == (QUEX_TYPE_ANALYZER*)0;
}

QUEX_INLINE void
QUEX_NAME(TokenQueue_destruct)(QUEX_NAME(TokenQueue)* me)
{
    QUEX_TYPE_TOKEN* iterator = 0x0;
    /* Call explicit destructors for all tokens in array                      */
    for(iterator = me->begin; iterator != me->end; ++iterator) {
        QUEX_NAME_TOKEN(destruct)(iterator);
    }

    QUEX_NNAME_LIB(MemoryManager_free)((void*)&me->begin[0],
                               E_MemoryObjectType_TOKEN_ARRAY);

    /* The memory chunk for the token queue itself is located inside the
     * analyzer object. Thus, no explicit free is necessary. In case of user
     * managed token queue memory the user takes care of the deletion.        */
    QUEX_NAME(TokenQueue_resources_absent_mark)(me);
}

QUEX_INLINE void   
QUEX_NAME(TokenQueue_remainder_get)(QUEX_NAME(TokenQueue)* me,
                                    QUEX_TYPE_TOKEN**      begin,
                                    QUEX_TYPE_TOKEN**      end)
{
    *begin = me->read_iterator;
    *end   = me->write_iterator;
    QUEX_NAME(TokenQueue_reset)(me);
}

QUEX_INLINE void 
QUEX_NAME(TokenQueue_memory_get)(QUEX_NAME(TokenQueue)* me,
                                 QUEX_TYPE_TOKEN**      memory,
                                 size_t*                n)
{
    *memory = me->begin;
    *n      = (size_t)(me->end - me->begin);
}

QUEX_INLINE bool 
QUEX_NAME(TokenQueue_is_full)(QUEX_NAME(TokenQueue)* me) 
{ return me->write_iterator >= me->end; }

QUEX_INLINE bool 
QUEX_NAME(TokenQueue_is_empty)(QUEX_NAME(TokenQueue)* me)
{ return me->read_iterator == me->write_iterator; }

QUEX_INLINE void             
QUEX_NAME(TokenQueue_push)(QUEX_NAME(TokenQueue)* me,
                           QUEX_TYPE_TOKEN_ID     Id)
/* Push a token and set only its token identifier.                            */
{
#   if defined(QUEX_OPTION_TOKEN_REPETITION_SUPPORT)
    QUEX_NAME_TOKEN(repetition_n_set)(me->write_iterator, 1);
#   endif
    QUEX_NAME(TokenQueue_push_core)(me, Id);
}

QUEX_INLINE void             
QUEX_NAME(TokenQueue_push_core)(QUEX_NAME(TokenQueue)* me,
                                QUEX_TYPE_TOKEN_ID     Id)
{
    if( QUEX_NAME(TokenQueue_is_full)(me) ) {
        me->the_lexer->error_code = E_Error_Token_QueueOverflow;
        return;
    }
    QUEX_ASSERT_TOKEN_QUEUE_BEFORE_SENDING(me);  

#if    defined(QUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN) 
#   if defined(QUEX_OPTION_COUNTER_LINE)
    me->write_iterator->_line_n   = me->the_lexer->counter._line_number_at_begin; 
#   endif
#   if defined(QUEX_OPTION_COUNTER_COLUMN)
    me->write_iterator->_column_n = me->the_lexer->counter._column_number_at_begin; 
#   endif
#endif
    me->write_iterator->id = Id;              
    ++(me->write_iterator);       
}

QUEX_INLINE bool             
QUEX_NAME(TokenQueue_push_text)(QUEX_NAME(TokenQueue)* me,
                                QUEX_TYPE_TOKEN_ID     Id,
                                QUEX_TYPE_LEXATOM*     BeginP,
                                QUEX_TYPE_LEXATOM*     EndP)
/* Push a token and set its 'text' member.                                    */
{
    bool ownership_transferred_to_token_f = false;
    QUEX_ASSERT_TOKEN_QUEUE_BEFORE_SENDING(me);
#   if defined(QUEX_OPTION_TOKEN_TAKE_TEXT_SUPPORT)
    ownership_transferred_to_token_f = QUEX_NAME_TOKEN(take_text)(me->write_iterator, BeginP, EndP);
    QUEX_NAME(TokenQueue_push)(me, Id);
    return ownership_transferred_to_token_f;
#   else
    (void)me; (void)Id; (void)BeginP; (void)EndP;
    __quex_assert((const char*)0 == "Token type does not support 'take text'.");
    QUEX_NAME(TokenQueue_set_token_TERMINATION)(me);
#   endif
    return ownership_transferred_to_token_f;
}

QUEX_INLINE void             
QUEX_NAME(TokenQueue_push_repeated)(QUEX_NAME(TokenQueue)* me,
                                    QUEX_TYPE_TOKEN_ID     Id,
                                    size_t                 RepetitionN)
/* Push a repeated token by 'RepetitionN' times. This is only addmissible for
 * TokenId-s specified in the 'repeated_token' section of the '.qx' file.     */
{
    QUEX_ASSERT_TOKEN_QUEUE_BEFORE_SENDING(me);  
    __quex_assert(RepetitionN != 0);        
#   if defined(QUEX_OPTION_TOKEN_REPETITION_SUPPORT)
    __quex_assert(QUEX_SETTING_TOKEN_ID_REPETITION_TEST(Id));
    QUEX_NAME_TOKEN(repetition_n_set)(me->write_iterator, RepetitionN);
    QUEX_NAME(TokenQueue_push_core)(me, Id);
#   else
    (void)me; (void)Id; (void)RepetitionN;
    __quex_assert((const char*)0 == "Token type does not support token repetition.");
    QUEX_NAME(TokenQueue_set_token_TERMINATION)(me);
#   endif
}

QUEX_INLINE QUEX_TYPE_TOKEN* 
QUEX_NAME(TokenQueue_pop)(QUEX_NAME(TokenQueue)* me)
{
#   if defined(QUEX_OPTION_TOKEN_REPETITION_SUPPORT)
    size_t    repetition_count;
#   endif

    __quex_assert(QUEX_NAME(TokenQueue_begin)(me) != 0x0);

    if( QUEX_NAME(TokenQueue_is_empty)(me) ) {        
        return (QUEX_TYPE_TOKEN*)0;
    }
#   if defined(QUEX_OPTION_TOKEN_REPETITION_SUPPORT)
    else if( QUEX_SETTING_TOKEN_ID_REPETITION_TEST(me->read_iterator->id) ) {
        repetition_count = QUEX_NAME_TOKEN(repetition_n_get)(me->read_iterator);
        if( repetition_count == 0 ) { 
            /* This case should never occurr!                                 */
            /* Repetition count == 0 => pop repeated token from queue.        */
            ++(me->read_iterator);
            if( QUEX_NAME(TokenQueue_is_empty)(me) ) {        
                return (QUEX_TYPE_TOKEN*)0;
            }
        }
        else if( repetition_count == 1 ) { 
            /* Repetition will be 0, so remove token from the queue.          */
            return me->read_iterator++;
        }
        else {
            QUEX_NAME_TOKEN(repetition_n_set)(me->read_iterator, 
                      (QUEX_NAME_TOKEN(repetition_n_get)(me->read_iterator) - 1));
            return me->read_iterator;  
        } 
    }
#   endif
    /* Tokens are in queue --> take next token from queue                    */ 
    return me->read_iterator++;
}

QUEX_INLINE QUEX_TYPE_TOKEN* QUEX_NAME(TokenQueue_begin)(QUEX_NAME(TokenQueue)* me)
{ return me->begin; }

QUEX_INLINE QUEX_TYPE_TOKEN* QUEX_NAME(TokenQueue_back)(QUEX_NAME(TokenQueue)* me)
{ return me->end - 1; }

QUEX_INLINE QUEX_TYPE_TOKEN* QUEX_NAME(TokenQueue_last_token)(QUEX_NAME(TokenQueue)* me)
{ return me->write_iterator == me->begin ? (QUEX_TYPE_TOKEN*)0 : &me->write_iterator[-1]; }

QUEX_INLINE size_t QUEX_NAME(TokenQueue_available_n)(QUEX_NAME(TokenQueue)* me) 
{ return (size_t)(me->end - me->write_iterator); }

QUEX_INLINE void
QUEX_NAME(TokenQueue_set_token_TERMINATION)(QUEX_NAME(TokenQueue)* me) 
/* Reset entire token queue and set the token 'TERMINATION'. This should
 * only be called in case of a detected error.                                */
{
    QUEX_NAME(TokenQueue_reset)(me);
#   if defined(QUEX_OPTION_TOKEN_TAKE_TEXT_SUPPORT)
    QUEX_NAME(TokenQueue_push_text)(me, QUEX_SETTING_TOKEN_ID_TERMINATION, 
                                    (QUEX_TYPE_LEXATOM*)0, (QUEX_TYPE_LEXATOM*)0);
#   else
    QUEX_NAME(TokenQueue_push)(me, QUEX_SETTING_TOKEN_ID_TERMINATION); 
#   endif
}

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* QUEX_INCLUDE_GUARD__TOKEN__TOKEN_QUEUE_I */
