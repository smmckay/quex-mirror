/* vim:set ft=c: -*- C++ -*- */
#ifndef __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_MOVE_I
#define __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_MOVE_I

#include <quex/code_base/asserts>
#include <quex/code_base/definitions>
#include <quex/code_base/buffer/Buffer>
#include <quex/code_base/buffer/asserts>

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE ptrdiff_t
QUEX_NAME(Buffer_move_towards_begin)(QUEX_NAME(Buffer)*  me, 
                                     ptrdiff_t           MoveDistance,
                                     QUEX_TYPE_LEXATOM** position_register,
                                     const size_t        PositionRegisterN)
/* MOVES the buffer's content towards the BEGIN.
 * MODIFIES all memory related pointers of the buffer and indices.
 *
 *                                                               EndP
 *                                         |<---- move size ---->|
 *     Before:   | . . . . . . . . . . . . .x.x.x.x.x.x.x.x.x.x.x| 
 *               |<---- move distance -----|                     |
 *                  .----------------------'                     |
 *               .-'                            .----------------'
 *               |                     .-------'
 *     After:    |x.x.x.x.x.x.x.x.x.x.x| . . . . . . . . . . . . | 
 *               |<---- move_size ---->|
 *
 * RETURNS: Number of lexatoms that have been moved.                       
 *
 * CALLS:   callbacks 'on_buffer_change'.
 *
 * RETURNS: Number of free lexatoms from 'content_end' the end of buffer.     */
{
    ptrdiff_t move_size;

    if( MoveDistance ) {
        /* If content has not been moved already, notify change!              */
        QUEX_NAME(Buffer_callbacks_on_buffer_before_change)(me);

        move_size = QUEX_NAME(Buffer_move_size_towards_begin)(me, MoveDistance);

        if( MoveDistance && move_size ) {
            __QUEX_STD_memmove((void*)me->content_begin(me), 
                               (void*)&me->content_begin(me)[MoveDistance],
                               (size_t)move_size * sizeof(QUEX_TYPE_LEXATOM));
        }

        QUEX_NAME(Buffer_pointers_add_offset)(me, - MoveDistance, 
                                              position_register, PositionRegisterN); 
        __quex_assert(me->content_end(me) == &me->content_begin(me)[move_size]);
        (void)move_size;
        QUEX_IF_ASSERTS_poison(&me->content_end(me)[1], me->content_space_end(me));
    }

    return me->content_space_end(me) - me->content_end(me);
}

QUEX_INLINE ptrdiff_t
QUEX_NAME(Buffer_move_towards_end)(QUEX_NAME(Buffer)* me, 
                                   ptrdiff_t          MoveDistance)
/* MOVES the buffer's content towards the END.
 * MODIFIES all memory related pointers of the buffer and indices.
 *
 *          BeginP
 *            |<--- move size---->|                         
 *            |x.x.x.x.x.x.x.x.x.x| . . . . . . . . . . . . . . |
 *            |                   '--------------.               
 *            '------------.                      '-------------.
 *                          '---------------.                   |
 *            :------- move distance------->|                   |
 *            | . . . . . . . . . . . . . . |x.x.x.x.x.x.x.x.x.x| 
 *                               
 * RETURNS: Number of lexatoms that need to be filled, starting from the 
 *          buffer's content begin.                                           */
{
    QUEX_TYPE_LEXATOM*  BeginP           = me->content_begin(me);
    const ptrdiff_t     ContentSpaceSize = me->content_space_size(me);
    ptrdiff_t           move_size;

    if( MoveDistance ) {
        /* If content has not been moved already, notify change!              */
        QUEX_NAME(Buffer_callbacks_on_buffer_before_change)(me);

        QUEX_NAME(Buffer_move_backup_lexatom_index_of_lexeme_start)(me, MoveDistance);

        if( MoveDistance <= ContentSpaceSize ) {
            move_size = ContentSpaceSize - MoveDistance;

            if( MoveDistance && move_size ) {
                __QUEX_STD_memmove((void*)&BeginP[MoveDistance], BeginP, 
                                   (size_t)move_size * sizeof(QUEX_TYPE_LEXATOM));
            }

            QUEX_IF_ASSERTS_poison(BeginP, &BeginP[MoveDistance]); 
        }
        QUEX_NAME(Buffer_pointers_add_offset)(me, MoveDistance, (QUEX_TYPE_LEXATOM**)0, 0);
    }
    return QUEX_MIN(me->content_space_end(me) - me->content_begin(me), 
                    MoveDistance);
}

QUEX_INLINE ptrdiff_t
QUEX_NAME(Buffer_move_towards_begin_undo)(QUEX_NAME(Buffer)*           me,
                                          QUEX_NAME(BufferInvariance)* bi,
                                          ptrdiff_t                    MoveDistance)
/* Restore the buffer's raw memory to what it was before in the 'FORWARD' case. 
 * It is assumed that the buffer's parameters in
 *
 *                         me->input
 *
 * remained UNTOUCHED during the moving and loading of the caller function.
 * That is, they indicate the situation to be restored.                       */
{
    QUEX_TYPE_LEXATOM* BeginP = me->content_begin(me);
    QUEX_TYPE_LEXATOM* EndP   = me->content_space_end(me);
    ptrdiff_t          move_size;
    ptrdiff_t          load_request_n;

    QUEX_NAME(BufferInvariance_restore)(bi, me);

    move_size = QUEX_NAME(Buffer_move_size_towards_begin)(me, MoveDistance);
    
    /* Character with lexatom index 'MinCharacterIndexInBuffer' has
     * not been loaded. => Buffer must be setup as before.                    */
    if( move_size && MoveDistance ) {
        /* NOT NECESSARY:
         *
         * QUEX_NAME(Buffer_callbacks_on_buffer_before_change)(me, BeginP);
         *
         * Because, this function is to be called only after 'move_...' which
         * must have called the 'on_buffer_before_change()'.                  */
        __QUEX_STD_memmove((void*)&BeginP[MoveDistance], (void*)BeginP, 
                           (size_t)move_size * sizeof(QUEX_TYPE_LEXATOM));
        load_request_n = (ptrdiff_t)MoveDistance;
    }
    else {
        load_request_n = me->content_size(me);
    }
    __quex_assert(&BeginP[load_request_n] <= EndP);
    (void)EndP;
    return load_request_n;
}

QUEX_INLINE ptrdiff_t
QUEX_NAME(Buffer_move_get_max_distance_towards_begin)(QUEX_NAME(Buffer)*  me) 
/* RETURNS: Max. move distance towards begin without loosing lexeme start.
 *
 *   0,   if nothing can be moved, anyway.
 *   > 1  number of positions that the content may be moved towards the
 *        begin of the buffer.                                                */
{
    QUEX_TYPE_LEXATOM*  region_p;
    const ptrdiff_t     ContentSpaceSize = me->content_space_size(me);
    const ptrdiff_t     FallBackN        = (ptrdiff_t)QUEX_SETTING_BUFFER_MIN_FALLBACK_N;

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);
    __quex_assert(FallBackN >= 0);

    if( me->_read_p - me->_lexeme_start_p >= ContentSpaceSize - FallBackN ) { 
        /* OVERFLOW: If stretch from _read_p to _lexeme_start_p 
         * spans the whole buffer, then nothing can be loaded.                */
        return 0;
    }
    else if( QUEX_NAME(Buffer_is_end_of_stream_inside)(me) ) {
        /* Refuse the move, if the end of stream is inside buffer.            */
        return 0;
    }

    /* Determine from where the region-to-be-moved BEGINS, what its size is
     * and how far it is to be moved.                                         */
    region_p  = me->_read_p;
    if( me->_lexeme_start_p ) {
        region_p = QUEX_MIN(region_p, me->_lexeme_start_p);
    }
    if( region_p - me->content_begin(me) <= FallBackN ) {
        return 0;
    }
    region_p  = &((region_p)[- FallBackN]);

    return /* move distance */region_p - me->content_begin(me);
}

QUEX_INLINE ptrdiff_t        
QUEX_NAME(Buffer_move_get_max_distance_towards_end)(QUEX_NAME(Buffer)* me)
/* RETURNS: Move Distance
 *
 *  -1,   if the lexeme starts at a position so that it covers so much that 
 *        nothing may be moved.
 *   0,   if nothing can be moved, anyway.
 *   > 1  number of positions that the content may be moved towards the
 *        begin of the buffer.                                                */
{
    ptrdiff_t  backward_walk_distance;  
    ptrdiff_t  move_distance;
    ptrdiff_t  move_distance_reasonable;
    ptrdiff_t  move_distance_max;
    ptrdiff_t  move_distance_nominal;

    /* Move distance restrict by: -- begin of stream (lexatom_index_begin == 0)
     *                            -- '_read_p' must remain in buffer.         */
    move_distance_max = QUEX_MIN(me->input.lexatom_index_begin, 
                                 me->content_space_end(me) - me->_read_p - 1);

    if( me->_backup_lexatom_index_of_lexeme_start_p == (QUEX_TYPE_STREAM_POSITION)-1 ) {
        /* There is still content in the buffer that might be useful for
         * forward lexical analyis. Load only a decent amount backward.   */
        move_distance_reasonable = QUEX_MAX((ptrdiff_t)(QUEX_SETTING_BUFFER_MIN_FALLBACK_N + 256), 
                                            me->content_space_size(me) / 4);

        if( me->_lexeme_start_p && me->_lexeme_start_p > me->_read_p ) {
            backward_walk_distance = me->_lexeme_start_p - me->_read_p;
        }
        else {
            backward_walk_distance = 0;
        }
       
        /* Provide backward data so that lexer might go backward twice as 
         * far as it already went.                                        */
        move_distance_nominal = QUEX_MAX(move_distance_reasonable, 
                                         backward_walk_distance * 2);
    }
    else {
        /* Next step forward requires a total reload anyway.
         * Go forward as much as possible.                                */
        move_distance_nominal = move_distance_max;
    }

    move_distance = QUEX_MIN(move_distance_max, move_distance_nominal);
    /* 'move_distance_max >= 0' => 'move_distance >= 0'                       */

    return move_distance;
}

QUEX_INLINE ptrdiff_t
QUEX_NAME(Buffer_move_size_towards_begin)(QUEX_NAME(Buffer)* me, ptrdiff_t move_distance)
{
    const ptrdiff_t ContentSize = me->content_size(me);
    if( move_distance >= ContentSize ) {
        return 0;
    }
    return ContentSize - move_distance;
}

QUEX_INLINE ptrdiff_t
QUEX_NAME(Buffer_move_get_distance_forward_to_contain)(QUEX_NAME(Buffer)*         me,
                                                       QUEX_TYPE_STREAM_POSITION* lexatom_index_to_be_contained)
{
    QUEX_TYPE_STREAM_POSITION lexatom_index_begin = me->input.lexatom_index_begin;
    QUEX_TYPE_STREAM_POSITION lexatom_index_end   = lexatom_index_begin + me->content_size(me);
    QUEX_TYPE_STREAM_POSITION new_lexatom_index_begin;
    QUEX_TYPE_STREAM_POSITION FallBackN           = QUEX_SETTING_BUFFER_MIN_FALLBACK_N;
    /* Assert to emphasize: 
     *      'lexatom_index_to_be_contained != lexatom_index_end_of_stream'
     * is correct, even if 'lexatom_index_end_of_stream' is undefined (-1).   */
    __quex_assert(*lexatom_index_to_be_contained != (QUEX_TYPE_STREAM_POSITION)-1);

    if( *lexatom_index_to_be_contained < lexatom_index_begin ) {
        return (ptrdiff_t)0;
    }
    else if( *lexatom_index_to_be_contained < lexatom_index_end ) {
        /* The '*lexatom_index_to_be_contained' already lies inside the buffer.*/
        return (ptrdiff_t)0;
    }
    else if( me->input.lexatom_index_end_of_stream != (QUEX_TYPE_STREAM_POSITION)-1 ) {
        if( *lexatom_index_to_be_contained > me->input.lexatom_index_end_of_stream ) {
            /* This position cannot be reached.                               */
            return (ptrdiff_t)0;
        }
        else if( *lexatom_index_to_be_contained == me->input.lexatom_index_end_of_stream ) {
            /* 'index end of stream' = first position AFTER the last lexatom. 
             * => There is NO lexatom at that position.                       */
            if( *lexatom_index_to_be_contained == lexatom_index_end ) {
                /* 'lexatom_index_to_be_contained' lies on border => OK!      */
                return (ptrdiff_t)0;
            } 
            else {
                /* seek for lexatom before 'lexatom_index_to_be_contained'.   */
                *lexatom_index_to_be_contained = QUEX_MAX(0, *lexatom_index_to_be_contained - 1);
            }
        }
    }

    new_lexatom_index_begin = QUEX_MAX(0, *lexatom_index_to_be_contained - FallBackN);
    __quex_assert(me->input.lexatom_index_begin         <= new_lexatom_index_begin);
    __quex_assert(new_lexatom_index_begin               <= *lexatom_index_to_be_contained);
    /* __quex_assert(new_lexatom_index_begin + ContentSpaceSize >= *lexatom_index_to_be_contained ); */

    /* Move existing content in the buffer to appropriate position.          */
    return (ptrdiff_t)(new_lexatom_index_begin - lexatom_index_begin);
}

QUEX_INLINE void
QUEX_NAME(Buffer_move_backup_lexatom_index_of_lexeme_start)(QUEX_NAME(Buffer)* me,
                                                            ptrdiff_t          MoveDistance)
/* If the buffer content is about to be moved in such a way that the lexeme
 * start is no longer inside the buffer, the lexeme start's poisiton index is
 * stored. This happens, so that at the later point in time the exact position
 * can be targetted and 'normal' analysis can continue.                       */
{
    if(    me->_lexeme_start_p
        && me->_lexeme_start_p + MoveDistance >= me->content_space_end(me)
        && me->_backup_lexatom_index_of_lexeme_start_p == (QUEX_TYPE_STREAM_POSITION)-1 ) {
        /* Lexeme start will be out of buffer. Store the position to be
         * reloaded when lexing forward restarts.                             */
        me->_backup_lexatom_index_of_lexeme_start_p =   QUEX_NAME(Buffer_tell)(me)
                                                      + (me->_lexeme_start_p - me->_read_p);
    }
}

QUEX_NAMESPACE_MAIN_CLOSE

#include <quex/code_base/buffer/lexatoms/LexatomLoader.i>
#include <quex/code_base/buffer/BufferMemory.i>

#endif /* __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_MOVE_I */

