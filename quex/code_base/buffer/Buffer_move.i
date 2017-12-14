/* vim:set ft=c: -*- C++ -*- */
#ifndef __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_MOVE_I
#define __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_MOVE_I

#include <quex/code_base/asserts>
#include <quex/code_base/buffer/asserts>
#include <quex/code_base/definitions>
#include <quex/code_base/buffer/Buffer>

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE ptrdiff_t QUEX_NAME(Buffer_move_towards_begin)(QUEX_NAME(Buffer)*  me, 
                                                           ptrdiff_t           move_distance);
QUEX_INLINE void      QUEX_NAME(Buffer_move_towards_begin_undo)(QUEX_NAME(Buffer)* me,
                                                          intmax_t           move_distance,
                                                          ptrdiff_t          move_size);
QUEX_INLINE ptrdiff_t QUEX_NAME(Buffer_move_towards_end)(QUEX_NAME(Buffer)* me, 
                                                      ptrdiff_t          move_distance);
QUEX_INLINE bool      QUEX_NAME(Buffer_is_end_of_stream_inside)(QUEX_NAME(Buffer)* me);

QUEX_INLINE ptrdiff_t QUEX_NAME(Buffer_get_maximum_move_distance_towards_begin)(QUEX_NAME(Buffer)*   me, 
                                                                                QUEX_TYPE_LEXATOM**  move_begin_p);
QUEX_INLINE ptrdiff_t QUEX_NAME(Buffer_get_maximum_move_distance_towards_end)(QUEX_NAME(Buffer)* me);

QUEX_INLINE void      QUEX_NAME(Buffer_adapt_pointers_after_move_forward)(QUEX_NAME(Buffer)*  me,
                                                                          ptrdiff_t           move_distance,
                                                                          QUEX_TYPE_LEXATOM** position_register,
                                                                          const size_t        PositionRegisterN);
QUEX_INLINE void      QUEX_NAME(Buffer_adapt_pointers_after_move_backward)(QUEX_NAME(Buffer)* me,
                                                                           ptrdiff_t          move_distance);

QUEX_INLINE ptrdiff_t
QUEX_NAME(Buffer_get_maximum_move_distance_towards_begin)(QUEX_NAME(Buffer)*   me, 
                                                          QUEX_TYPE_LEXATOM**  move_begin_p)
/* RETURNS: Move Distance
 *
 *  -1,   if the lexeme starts at a position so that it covers so much that 
 *        nothing may be moved.
 *   0,   if nothing can be moved, anyway.
 *   > 1  number of positions that the content may be moved towards the
 *        begin of the buffer.                                                */
{
    QUEX_TYPE_LEXATOM*        BeginP = &me->_memory._front[1];
    const ptrdiff_t           ContentSize = (ptrdiff_t)QUEX_NAME(Buffer_content_size)(me);
    ptrdiff_t                 move_distance;
    const ptrdiff_t           FallBackN = (ptrdiff_t)QUEX_SETTING_BUFFER_MIN_FALLBACK_N;

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);
    __quex_assert(FallBackN >= 0);

    if( me->_read_p - me->_lexeme_start_p >= ContentSize - FallBackN ) { 
        /* OVERFLOW: If stretch from _read_p to _lexeme_start_p 
         * spans the whole buffer, then nothing can be loaded.                */
        return -1;
    }
    else if( QUEX_NAME(Buffer_is_end_of_stream_inside)(me) ) {
        /* Refuse the move, if the end of stream is inside buffer.           */
        return 0;
    }

    /* Determine from where the region-to-be-moved BEGINS, what its size is
     * and how far it is to be moved.                                        */
    *move_begin_p  = me->_read_p;
    if( me->_lexeme_start_p ) {
        *move_begin_p = QUEX_MIN(*move_begin_p, me->_lexeme_start_p);
    }
    if( *move_begin_p - BeginP <= FallBackN ) {
        return 0;
    }
    *move_begin_p  = &((*move_begin_p)[- FallBackN]);
    move_distance = *move_begin_p - BeginP;

    return move_distance;
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
    QUEX_TYPE_LEXATOM*        EndP        = me->_memory._back;
    QUEX_TYPE_LEXATOM*        LastP       = &me->_memory._back[-1];
    const ptrdiff_t           ContentSize = EndP - BeginP;
    ptrdiff_t                 move_distance;
    ptrdiff_t                 move_distance_max;
    ptrdiff_t                 move_distance_nominal;

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);
    __quex_assert(me->_read_p <= LastP);

    if( me->input.lexatom_index_begin == 0 && BeginP == me->_read_p ) {
        return 0;                        /* Begin of stream.                 */
    }
    else if( me->_lexeme_start_p >= LastP ) { 
        /* Overflow. 
         * If _lexeme_start_p at back, then no new content can be loaded.     */
        return -1;
    }

    /* Max. possible move distance: where 'read_p' or 'lexeme_start_p'
     * land on last position in the buffer.                                  */
    move_distance_max = LastP - QUEX_MAX(me->_read_p, me->_lexeme_start_p);
    /* Also, move before lexatom index '0' is impossible.                    */
    move_distance_max = QUEX_MIN(move_distance_max, (ptrdiff_t)me->input.lexatom_index_begin);

    /* Desired move distance: ContentSize / 3                                */
    move_distance_nominal = ContentSize > 3 ?  ContentSize / 3 : ContentSize;

    move_distance = QUEX_MIN(move_distance_max, move_distance_nominal); 

    return move_distance;
}

QUEX_INLINE void
QUEX_NAME(Buffer_adapt_pointers_after_move_forward)(QUEX_NAME(Buffer)*  me,
                                                    ptrdiff_t           move_distance,
                                                    QUEX_TYPE_LEXATOM** position_register,
                                                    const size_t        PositionRegisterN)
/* Adapt points after content has been moved towards begin.
 *
 * ADAPTS: _read_p, _lexeme_start_p, position registers, end_p, 
 *         input.end_lexatom_index                                            */
{ 
    QUEX_TYPE_LEXATOM*   BeginP = &me->_memory._front[1];
    QUEX_TYPE_LEXATOM**  pr_it     = 0x0;

    me->_read_p                                   -= move_distance;
    if( me->_lexeme_start_p ) me->_lexeme_start_p -= move_distance;
   
    if( position_register ) {
        /* All position registers MUST point behind '_lexeme_start_p'.       */
        for(pr_it = position_register; pr_it != &position_register[PositionRegisterN]; ++pr_it) {
            if( ! *pr_it ) continue;
            *pr_it = (*pr_it - BeginP) >= move_distance ? *pr_it - move_distance : 0;
        }
    }

    /* input.end_p/end_lexatom_index: End lexatom index remains the SAME, 
     * since no new content has been loaded into the buffer.                 */
    __quex_assert(me->input.end_p - BeginP >= move_distance);

    QUEX_NAME(Buffer_register_content)(me, &me->input.end_p[- move_distance], 
                                       me->input.lexatom_index_begin + move_distance);
}

QUEX_INLINE void        
QUEX_NAME(Buffer_adapt_pointers_after_move_backward)(QUEX_NAME(Buffer)* me,
                                                     ptrdiff_t          move_distance)
/* Adapt points after content has been moved towards end.
 *
 * ADAPTS: _read_p, _lexeme_start_p, position registers, end_p, 
 *         input.end_lexatom_index                                            */
{
    QUEX_TYPE_LEXATOM*  EndP   = me->_memory._back;
    QUEX_TYPE_LEXATOM*  end_p;

    /* Pointer Adaption: _read_p, _lexeme_start_p.                           */
    me->_read_p += move_distance;
    if( me->_lexeme_start_p ) me->_lexeme_start_p += move_distance;

    /* Adapt and of content pointer and new lexatom index at begin.          */
    end_p = EndP - me->input.end_p < move_distance ? EndP
                                                   : &me->input.end_p[move_distance];

    QUEX_NAME(Buffer_register_content)(me, end_p, 
                                       me->input.lexatom_index_begin - move_distance);
}

QUEX_INLINE ptrdiff_t
QUEX_NAME(Buffer_move_to_get_free_space_at_end)(QUEX_NAME(Buffer)* me)
/* Circumvent restriction of 'Buffer_load_prepare_forward()' which 
 * refuses to move if end of stream is inside buffer. 
 *
 * => Trick: Backup & restore 'lexatom_index_end_of_stream'               
 *
 * RETURNS: Available elements at end of buffer.                              */
{
    QUEX_TYPE_STREAM_POSITION backup_ios;

    backup_ios                            = me->input.lexatom_index_end_of_stream;
    me->input.lexatom_index_end_of_stream = (QUEX_TYPE_STREAM_POSITION)-1;
    /* Position registers are only relevant during lexical analyzis.
     * Inclusion happens in a 'terminal' or external to the lexer step.   
     * => Position registers = empty set.                                     */
    (void)QUEX_NAME(Buffer_load_prepare_forward)(me, (QUEX_TYPE_LEXATOM**)0, 0);

    me->input.lexatom_index_end_of_stream = backup_ios;

    /* After 'move away' possibly:
     *
     *   size(me's buffer) < 'QUEX_SETTING_BUFFER_INCLUDE_MIN_SIZE'
     *
     * However, 'me' buffer is NOT used before 'included' terminates.
     * => included is pasted back at the end of me.                           */
    return me->_memory._back - me->input.end_p;
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

