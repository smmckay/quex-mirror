/* -*- C++ -*- vim: set syntax=cpp: */
#ifndef QUEX_INCLUDE_GUARD__BUFFER__BUFFER_FILL_I
#define QUEX_INCLUDE_GUARD__BUFFER__BUFFER_FILL_I

$$INC: buffer/Buffer$$

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE const void*
QUEX_NAME(Buffer_fill)(QUEX_NAME(Buffer)*  me, 
                       const void*         ContentBegin,
                       const void*         ContentEnd)
/* RETURNS: Pointer to first element that has not been filled into buffer.
 *          == ContentBegin, in case that nothing has been filled.          */
{
    ptrdiff_t      copy_n;
    void*          begin_p;
    const void*    end_p;

    /* Prepare the buffer for the reception of new input and acquire the
     * border pointers of where new content can be filled.                   */
    if( ! ContentBegin ) {
        return (void*)ContentBegin;
    }
    else if( ! me->fill_prepare(me, &begin_p, &end_p) ) {
        return (void*)ContentBegin;
    }
    __quex_assert(ContentEnd);

    /* Copy as much as possible of the new content into the designated
     * region in memory. This may be the engine's buffer or a 'raw' buffer
     * whose content still needs to be converted.                            */
    copy_n = (ptrdiff_t)QUEX_GNAME_LIB(MemoryManager_insert)((uint8_t*)begin_p,  
                                                             (uint8_t*)end_p,
                                                             (uint8_t*)ContentBegin, 
                                                             (uint8_t*)ContentEnd);

    /* Flush into buffer what has been filled from &begin[0] to 
     * &begin[inserted_byte_n].                                              */
    me->fill_finish(me, &((uint8_t*)begin_p)[copy_n]);

    /* Report a pointer to the first content element that has not yet 
     * been treated (== ContentEnd if all complete).                         */
    return (const void*)&((uint8_t*)ContentBegin)[copy_n];
}

QUEX_INLINE bool
QUEX_NAME(Buffer_fill_prepare)(QUEX_NAME(Buffer)*  me, 
                               void**              begin_p, 
                               const void**        end_p)
/* SETS: *begin_p: position where the next content needs to be filled. 
 *       *end_p:   address directly behind the last byte that can be filled.
 *
 * The content may be filled into the engine's buffer or an intermediate 
 * 'raw' buffer which still needs to be converted.                          */
{
    ptrdiff_t  free_space;
    ptrdiff_t  move_distance;
    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    move_distance = QUEX_NAME(Buffer_move_get_max_distance_towards_begin)(me); 

    if(    0 == move_distance 
        && ! QUEX_NAME(Buffer_callbacks_on_cannot_move_towards_begin)(me, &move_distance) ) {
        *begin_p = (void*)0;
        *end_p   = (const void*)0;
        return false;
    }

    if( move_distance ) {
        (void)QUEX_NAME(Buffer_move_towards_begin)(me, move_distance,
                                                   (QUEX_TYPE_LEXATOM**)0, 0);
    }

    free_space = me->content_space_end(me) - me->content_end(me);
    
    if( 0 == free_space ) {
        *begin_p = (void*)0;
        *end_p   = (const void*)0;
        return false;
    }

    /* Get the pointers for the border where to fill content.               */
    me->filler->derived.fill_prepare(me->filler, me, begin_p, end_p);

    if( *end_p <= *begin_p ) {
        *begin_p = (void*)0;
        *end_p   = (const void*)0;
        return false;
    }

    __quex_assert(*end_p >= *begin_p);
    QUEX_BUFFER_ASSERT_CONSISTENCY(me);
    return true;
}

QUEX_INLINE void
QUEX_NAME(Buffer_fill_finish)(QUEX_NAME(Buffer)* me,
                              const void*        FilledEndP)
/* Uses the content that has been inserted until 'FilledEndP' to fill the
 * engine's lexatom buffer (if it is not already done). A fille of type
 * 'LexatomLoader_Converter' takes the content of the raw buffer and converts
 * it into the engine's buffer from 'me->content_end(me)' to 'me->content_space_end(me)'.
 *                                                                           */
{
    __quex_assert((QUEX_TYPE_LEXATOM*)FilledEndP <= me->content_space_end(me));

    /* Place new content in the engine's buffer.                             */
    ptrdiff_t inserted_lexatom_n = me->filler->derived.fill_finish(me->filler, 
                                                                   me->content_end(me),
                                                                   me->content_space_end(me), 
                                                                   FilledEndP);

    /* Assume: content from 'input.end_p' to 'input.end_p[CharN]'
     * has been filled with data.                                            */
    if( me->filler->_byte_order_reversion_active_f ) {
        QUEX_NAME(LexatomLoader_reverse_byte_order)(me->content_end(me), 
                                                   &me->content_end(me)[inserted_lexatom_n]);
    }

    /* -- Manual buffer filling requires the end-of-stream pointer always
     *    to be set. 
     * -- The 'lexatom_index_begin' has been set in 'fill_prepare()'.
     *    '-1' => no change.
     * -- The 'lexatom_index_end_of_stream' can now be set, since it is
     *    known how many lexatoms have been inserted.
     *                                                                       */
    QUEX_NAME(Buffer_register_content)(me, &me->content_end(me)[inserted_lexatom_n], -1);
    QUEX_NAME(Buffer_register_eos)(me, me->input.lexatom_index_begin + me->content_size(me));

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);
}

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* QUEX_INCLUDE_GUARD__BUFFER__BUFFER_FILL_I */
