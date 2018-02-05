/* vim:set ft=c: -*- C++ -*- */
#ifndef __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_MOVE_I
#define __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_MOVE_I

#include <quex/code_base/asserts>
#include <quex/code_base/buffer/asserts>
#include <quex/code_base/definitions>
#include <quex/code_base/buffer/Buffer>
#include <quex/code_base/buffer/asserts>

QUEX_NAMESPACE_MAIN_OPEN

#define QUEX_BUFFER_POINTER_ADD(P, BORDER, OFFSET)          \
        ((P) = (  ((P) == (QUEX_TYPE_LEXATOM*)0) ? (P)      \
                : ((BORDER) - (P) < OFFSET)     ? (BORDER) \
                : (P) + (OFFSET)))
#define QUEX_BUFFER_POINTER_SUBTRACT(P, BORDER, NEGATIVE_OFFSET)  \
        ((P) = (  ((P) == (QUEX_TYPE_LEXATOM*)0)     ? (P)        \
                : ((BORDER) - (P) > NEGATIVE_OFFSET) ? (BORDER)   \
                : (P) + (NEGATIVE_OFFSET)))

QUEX_INLINE void
QUEX_NAME(Buffer_pointers_add_offset)(QUEX_NAME(Buffer)*  me,
                                      ptrdiff_t           offset,
                                      QUEX_TYPE_LEXATOM** position_register,
                                      const size_t        PositionRegisterN)
/* Adapt points after content has been moved towards begin.
 *
 * ADAPTS: _read_p, _lexeme_start_p, position registers, end_p, 
 *         input.end_lexatom_index                                            */
{ 
    QUEX_TYPE_LEXATOM*  border = (QUEX_TYPE_LEXATOM*)0;
    QUEX_TYPE_LEXATOM** pit    = (QUEX_TYPE_LEXATOM**)0x0;
    QUEX_TYPE_LEXATOM** pEnd   = &position_register[PositionRegisterN];

    if( offset > 0 ) {
        border = me->_memory._back;
        QUEX_BUFFER_POINTER_ADD(me->_read_p,         border, offset);
        QUEX_BUFFER_POINTER_ADD(me->_lexeme_start_p, border, offset);
        QUEX_BUFFER_POINTER_ADD(me->input.end_p,     border, offset);

        for(pit = position_register; pit != pEnd; ++pit) {
            QUEX_BUFFER_POINTER_ADD(*pit, border, offset); 
        }
    }
    else if( offset < 0 ) {
        border = me->_memory._front;
        QUEX_BUFFER_POINTER_SUBTRACT(me->_read_p,         border, offset);
        QUEX_BUFFER_POINTER_SUBTRACT(me->_lexeme_start_p, border, offset);
        QUEX_BUFFER_POINTER_SUBTRACT(me->input.end_p,     border, offset);

        for(pit = position_register; pit != pEnd; ++pit) {
            QUEX_BUFFER_POINTER_SUBTRACT(*pit, border, offset); 
        }
    }
    else {
        return;
    }

    *(me->input.end_p) = (QUEX_TYPE_LEXATOM)QUEX_SETTING_BUFFER_LIMIT_CODE;

    me->input.lexatom_index_begin -= offset;

    /* input.end_p/end_lexatom_index: End lexatom index remains the SAME, 
     * since no new content has been loaded into the buffer.                 */
    __quex_assert(me->input.end_p - &me->_memory._front[1] >= offset);

    QUEX_BUFFER_ASSERT_pointers_in_range(me);
}

QUEX_INLINE ptrdiff_t
QUEX_NAME(Buffer_get_maximum_move_distance_towards_begin)(QUEX_NAME(Buffer)*  me) 
/* RETURNS: Move Distance
 *
 *  -1,   if the lexeme starts at a position so that it covers so much that 
 *        nothing may be moved.
 *   0,   if nothing can be moved, anyway.
 *   > 1  number of positions that the content may be moved towards the
 *        begin of the buffer.                                                */
{
    QUEX_TYPE_LEXATOM*  BeginP = &me->_memory._front[1];
    QUEX_TYPE_LEXATOM*  region_p;
    const ptrdiff_t     ContentSize = (ptrdiff_t)QUEX_NAME(Buffer_content_size)(me);
    const ptrdiff_t     FallBackN = (ptrdiff_t)QUEX_SETTING_BUFFER_MIN_FALLBACK_N;

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);
    __quex_assert(FallBackN >= 0);

    if( me->_read_p - me->_lexeme_start_p >= ContentSize - FallBackN ) { 
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
    if( region_p - BeginP <= FallBackN ) {
        return 0;
    }
    region_p  = &((region_p)[- FallBackN]);

    return /* move distance */region_p - BeginP;
}

QUEX_INLINE ptrdiff_t        
QUEX_NAME(Buffer_get_maximum_move_distance_towards_end)(QUEX_NAME(Buffer)* me)
/* RETURNS: Move Distance
 *
 *  -1,   if the lexeme starts at a position so that it covers so much that 
 *        nothing may be moved.
 *   0,   if nothing can be moved, anyway.
 *   > 1  number of positions that the content may be moved towards the
 *        begin of the buffer.                                                */
{
    const QUEX_TYPE_LEXATOM*  BeginP      = &me->_memory._front[1];
    QUEX_TYPE_LEXATOM*        LastP       = &me->_memory._back[-1];
    ptrdiff_t                 backward_walk_distance;  
    ptrdiff_t                 move_distance;
    ptrdiff_t                 move_distance_reasonable;
    ptrdiff_t                 move_distance_max;
    ptrdiff_t                 move_distance_nominal;

    /* Move distance restrict by: -- begin of stream (lexatom_index_begin == 0)
     *                            -- '_read_p' must remain in buffer.         */
    move_distance_max = QUEX_MIN(me->input.lexatom_index_begin, 
                                 LastP - me->_read_p);

    {
        if( me->_backup_lexatom_index_of_read_p == (QUEX_TYPE_STREAM_POSITION)-1 ) {
            /* There is still content in the buffer that might be useful for
             * forward lexical analyis. Load only a decent amount backward.   */
            move_distance_reasonable = QUEX_MAX((ptrdiff_t)(QUEX_SETTING_BUFFER_MIN_FALLBACK_N + 256), 
                                                (ptrdiff_t)((LastP - BeginP) / 4));
            if( me->_lexeme_start_p ) {
                backward_walk_distance = me->_lexeme_start_p ? 
                                            me->_lexeme_start_p - me->_read_p : 0;
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
    }
    move_distance = QUEX_MIN(move_distance_max, move_distance_nominal);

    return move_distance;
}

QUEX_INLINE void        
QUEX_NAME(Buffer_adapt_pointers_after_move_backward)(QUEX_NAME(Buffer)* me,
                                                     ptrdiff_t          move_distance)
/* Adapt points after content has been moved towards end.
 *
 * ADAPTS: _read_p, _lexeme_start_p, position registers, end_p, 
 *         input.end_lexatom_index                                            */
{
    QUEX_NAME(Buffer_pointers_add_offset)(me, move_distance, 
                                          (QUEX_TYPE_LEXATOM**)0, 0);

    QUEX_BUFFER_ASSERT_pointers_in_range(me);
}

QUEX_INLINE ptrdiff_t
QUEX_NAME(Buffer_move_towards_begin)(QUEX_NAME(Buffer)* me, 
                                     ptrdiff_t          move_distance)
/* Moves the entire (meaningful) content of the buffer by 'move_distance'
 * forward. It does NOT MODIFY any pointers about the buffer content!
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
 * RETURNS: Number of lexatoms that have been moved.                       */
{
    QUEX_TYPE_LEXATOM* BeginP     = &me->_memory._front[1];
    const ptrdiff_t    FilledSize = me->input.end_p - BeginP;
    ptrdiff_t          move_size;

    if( move_distance >= FilledSize ) {
        return 0;
    }

    move_size = FilledSize - move_distance;

    if( move_distance && move_size ) {
        __QUEX_STD_memmove((void*)BeginP, (void*)&BeginP[move_distance],
                           (size_t)move_size * sizeof(QUEX_TYPE_LEXATOM));
    }
    return move_size;
}

QUEX_INLINE ptrdiff_t
QUEX_NAME(Buffer_move_towards_begin_and_adapt_pointers)(QUEX_NAME(Buffer)*  me, 
                                                        ptrdiff_t           MoveDistance,
                                                        QUEX_TYPE_LEXATOM** position_register,
                                                        const size_t        PositionRegisterN)
/* Calls 'Buffer_move_towards_begin' and adapts pointers inside 'me'.
 *
 * CALLS:   callbacks 'on_buffer_change'.
 *
 * RETURNS: free space from 'end_p' to '&back[1]'.                            */
{
    ptrdiff_t move_size;

    if( MoveDistance ) {
        QUEX_NAME(Buffer_call_on_buffer_before_change)(me);

        move_size = QUEX_NAME(Buffer_move_towards_begin)(me, MoveDistance);

        QUEX_NAME(Buffer_pointers_add_offset)(me, - MoveDistance, 
                                              position_register, PositionRegisterN); 
        __quex_assert(me->input.end_p == &me->_memory._front[1 + move_size]);
        (void)move_size;
    }

    return me->_memory._back - me->input.end_p;
}

QUEX_INLINE ptrdiff_t
QUEX_NAME(Buffer_move_towards_end)(QUEX_NAME(Buffer)* me, 
                                   ptrdiff_t          move_distance)
/* Moves content so that previous content may be filled into the buffer.
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
 *
 * RETURNS: Number of lexatom that need to be filled into the gap.
 *                                                                           */
{
    QUEX_TYPE_LEXATOM*  BeginP      = &me->_memory._front[1];
    const ptrdiff_t     ContentSize = (ptrdiff_t)QUEX_NAME(Buffer_content_size)(me);
    ptrdiff_t           move_size;

    if( move_distance > ContentSize ) {
        return ContentSize;
    }

    move_size = ContentSize - move_distance;

    if( move_distance && move_size ) {
        __QUEX_STD_memmove((void*)&BeginP[move_distance], BeginP, 
                           (size_t)move_size * sizeof(QUEX_TYPE_LEXATOM));
    }

    QUEX_IF_ASSERTS_poison(BeginP, &BeginP[move_distance]); 
    return (ptrdiff_t)move_distance;
}

QUEX_INLINE void
QUEX_NAME(Buffer_move_towards_begin_undo)(QUEX_NAME(Buffer)* me,
                                          intmax_t           move_distance,
                                          ptrdiff_t          move_size)
/* Restore the buffer's raw memory to what it was before in the 'FORWARD' case. 
 * It is assumed that the buffer's parameters in
 *
 *                         me->input
 *
 * remained UNTOUCHED during the moving and loading of the caller function.
 * That is, they indicate the situation to be restored.                       */
{
    QUEX_TYPE_LEXATOM* BeginP      = &me->_memory._front[1];
    QUEX_TYPE_LEXATOM* EndP        = me->_memory._back;
    ptrdiff_t            load_request_n;
    ptrdiff_t            loaded_n;
    bool                 end_of_stream_f = false;
    bool                 encoding_error_f = false;

    /* Character with lexatom index 'MinCharacterIndexInBuffer' has
     * not been loaded. => Buffer must be setup as before.                    */
    if( move_size ) {
        /* NOT NECESSARY:
         *
         * QUEX_NAME(Buffer_call_on_buffer_before_change)(me, BeginP);
         *
         * Because, this function is to be called only after 'move_...' which
         * must have called the 'on_buffer_before_change()'
         *                                                                    */
        __QUEX_STD_memmove((void*)&BeginP[move_distance], (void*)BeginP, 
                           (size_t)move_size * sizeof(QUEX_TYPE_LEXATOM));
        load_request_n = (ptrdiff_t)move_distance;
    }
    else {
        load_request_n = (me->input.end_p - BeginP);
    }
    __quex_assert(&BeginP[load_request_n] <= EndP);
    (void)EndP;
    loaded_n = QUEX_NAME(LexatomLoader_load)(me->filler, BeginP, load_request_n,
                                             me->input.lexatom_index_begin,
                                             &end_of_stream_f, &encoding_error_f);

    if( loaded_n != load_request_n ) {
        QUEX_ERROR_EXIT("Buffer filler failed to load content that has been loaded before.!");
    }
    else {
        /* Ensure, that the buffer limit code is restored.                   */
        *(me->input.end_p) = (QUEX_TYPE_LEXATOM)QUEX_SETTING_BUFFER_LIMIT_CODE;
    }
}

QUEX_NAMESPACE_MAIN_CLOSE

#include <quex/code_base/buffer/lexatoms/LexatomLoader.i>
#include <quex/code_base/buffer/BufferMemory.i>

#endif /* __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_MOVE_I */

