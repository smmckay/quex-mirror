/* vim:set ft=c: -*- C++ -*- */
#ifndef __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_LOAD_I
#define __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_LOAD_I

#include <quex/code_base/asserts>
#include <quex/code_base/buffer/asserts>
#include <quex/code_base/definitions>
#include <quex/code_base/buffer/Buffer>
#include <quex/code_base/buffer/Buffer_print.i>
#include <quex/code_base/buffer/lexatoms/LexatomLoader>
#include <quex/code_base/MemoryManager>

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE E_LoadResult
QUEX_NAME(Buffer_load_forward)(QUEX_NAME(Buffer)*  me,
                               QUEX_TYPE_LEXATOM** position_register,
                               const size_t        PositionRegisterN)
/* Load a maximum amount of new content into the buffer from input stream. 
 * Pointers and indices are adapted, so that they relate to the same content 
 * in the input stream as before the call. 
 *
 *        .-----------------------------------------------------.
 *        |     BLOCKING wait for incoming stream content.      |
 *        | No return without content--except at end of stream. |
 *        '-----------------------------------------------------'
 *
 * RETURNS: 
 *          
 *     DONE              => Something has been loaded   (analysis MAY CONTINUE)
 *     FAILURE           => General load failure.       (analysis MUST STOP)
 *     NO_SPACE_FOR_LOAD => Lexeme exceeds buffer size. (analysis MUST STOP)
 *     ENCODING_ERROR    => Failed. conversion error    (analysis MUST STOP)
 *     NO_MORE_DATA      => No more data available.     (analysis MUST STOP)
 *     BAD_LEXATOM       => Read pointer on buffer limit code,
 *                          but it was not a buffer limit.
 *                                                                            */
{
    QUEX_TYPE_LEXATOM*          begin_p = &me->_memory._front[1];
    QUEX_TYPE_STREAM_POSITION   ci_begin = QUEX_NAME(Buffer_input_lexatom_index_begin)(me);
    ptrdiff_t                   move_distance;
    ptrdiff_t                   loaded_n;
    bool                        encoding_error_f = false;

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    if( me->_read_p != me->input.end_p) {
        /* If the read pointer does not stand on the end of input pointer, then
         * the 'buffer limit code' at the read pointer is a bad lexatom.    
         * Buffer limit codes cannot be possibly be part of buffer content.  */
        return E_LoadResult_ENCODING_ERROR;
    }
    else if( ! me->filler || ! me->filler->byte_loader ) {
        QUEX_NAME(Buffer_register_eos)(me, ci_begin + (me->input.end_p - begin_p));
        return E_LoadResult_NO_MORE_DATA;  /* No filler/loader => no load!   */
    }

    /* Move remaining content.
     * Maintain lexeme and fallback.                 
     * Adapt pointers.                                                       */
    move_distance = QUEX_NAME(Buffer_get_move_distance_max_towards_begin)(me); 

    if(    0 == move_distance 
        && ! QUEX_NAME(Buffer_on_cannot_move_towards_begin)(me, &move_distance) ) {
        return E_LoadResult_FAILURE; 
    }

    if( ! QUEX_NAME(Buffer_move_and_load)(me, position_register, PositionRegisterN, 
                                          move_distance, &encoding_error_f, &loaded_n) ) {
        return E_LoadResult_FAILURE;
    }
    __quex_debug_buffer_load(me, "LOAD FORWARD(exit)\n");
    QUEX_BUFFER_ASSERT_CONSISTENCY(me);
    if     ( encoding_error_f ) return E_LoadResult_ENCODING_ERROR;
    else if( loaded_n )         return E_LoadResult_DONE;
    else                        return E_LoadResult_NO_MORE_DATA;
}

QUEX_INLINE bool
QUEX_NAME(Buffer_load_forward_to_contain)(QUEX_NAME(Buffer)*        me, 
                                          QUEX_TYPE_STREAM_POSITION LexatomIndexToBeContained)
/* Load new content into the buffer, so that a specific lexatom index is 
 * contained inside the buffer.
 * 
 * Before:    .-------------------------------------- prev lexatom_index_begin             
 *            :                 
 *            | . . . . . . . . .x.x.x.x.x.x.x.x.x.x.x| 
 *                              |<---- move size ---->|
 * After:     |<- move distance |
 *            .-------------------------------------- new lexatom_index_begin
 *            :                     .---------------- prev lexatom index begin
 *            :                     :  
 *            |x.x.x.x.x.x.x.x.x.x.x|N.N.N.N.N.N.N. . | 
 *            |- move_size -------->|- loaded_n ->|
 *                                                             
 *
 * RETURNS:  true, in case of success.
 *           false, in case of FAILURE.
 *
 * FAILURE:  If it was not possible to restore the previous content of the 
 *           buffer the buffer is *disabled*. That is, in case of 'return false',
 *           the function 'QUEX_NAME(Buffer_dysfunctional)(me)' must be checked.*/
{
    QUEX_TYPE_STREAM_POSITION lexatom_index_to_be_contained = LexatomIndexToBeContained;
    bool                      verdict_f;
    ptrdiff_t                 load_request_n;
    ptrdiff_t                 loaded_n;
    intmax_t                  move_distance;
    bool                      end_of_stream_f  = false;
    bool                      encoding_error_f = false;
    QUEX_NAME(BufferInvariance)  bi;

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    QUEX_NAME(BufferInvariance_construct)(&bi, me);

    /* Move existing content in the buffer to appropriate position.           */
    move_distance = QUEX_NAME(Buffer_get_move_distance_forward_to_contain)(me, 
                                             &lexatom_index_to_be_contained);

    verdict_f = QUEX_NAME(Buffer_move_and_load)(me, (QUEX_TYPE_LEXATOM**)0, 0,
                                                move_distance, &encoding_error_f, 
                                                &loaded_n);
    if(    verdict_f
        && LexatomIndexToBeContained < me->input.lexatom_index_begin + 
                                       (me->input.end_p - &me->_memory._front[1]) ) {
        return true;
    }
    else {
        load_request_n = QUEX_NAME(Buffer_move_towards_begin_undo)(me, &bi, move_distance);

        loaded_n       = QUEX_NAME(LexatomLoader_load)(me->filler, &me->_memory._front[1], 
                                                       load_request_n, me->input.lexatom_index_begin,
                                                       &end_of_stream_f, &encoding_error_f);
        if( loaded_n != load_request_n ) {
            /* Error: buffer is dysfunctional.                                    */
            QUEX_NAME(Buffer_dysfunctional_set)(me);
        }
        else {
            /* Ensure, that the buffer limit code is restored.                    */
            *(me->input.end_p) = (QUEX_TYPE_LEXATOM)QUEX_SETTING_BUFFER_LIMIT_CODE;
        }
        return false;
    }
}

QUEX_INLINE E_LoadResult   
QUEX_NAME(Buffer_load_backward)(QUEX_NAME(Buffer)* me)
/* Load *previous* content into the buffer so that the analyzer can continue
 * seeminglessly (in backward direction).
 *
 * BEHAVIOR: BLOCKING wait for incoming stream content. 
 *           No return without content--except at end of stream.
 *
 *           Buffer and pointers are adapted are adapted IN ANY CASE!
 *
 * RETURNS: 
 *          
 *     DONE              => Something has been loaded   (analysis MAY CONTINUE)
 *     FAILURE           => General load failure.       (analysis MUST STOP)
 *     NO_SPACE_FOR_LOAD => Lexeme exceeds buffer size. (analysis MUST STOP)
 *     ENCODING_ERROR    => Failed. Conversion error.   (analysis MUST STOP)
 *     NO_MORE_DATA      => Begin of stream reached.    (analysis MUST STOP)
 *
 *  __________________________________________________________________________
 * ! In the false case, the range from 'Begin' to '_lexeme_start_p' may       !
 * ! have ARBITRARY CONTENT. Then the '_read_p' MUST be reset IMMEDIATELY and !
 * ! only forward analysis may work.                                          !
 * '--------------------------------------------------------------------------'
 *
 *_____________________________________________________________________________
 * NO ADAPTIONS OF POST-CONTEXT POSITIONS. Reason: Backward analysis appears
 * only in the following two cases.
 *  
 *  (1) When checking for a pre-condition. This does not involve pre-contexts.
 * 
 *  (2) When tracing back along a 'pseudo-ambigous post context'. However,
 *      the stretch from 'end-of-core' pattern to 'end-of-post context' lies
 *      completely in between 'lexeme start' to 'read '. Thus, one never has
 *      to go farther back then the buffer's begin.                          */
{
    ptrdiff_t           move_distance;
    ptrdiff_t           loaded_n;
    ptrdiff_t           load_request_n;
    bool                encoding_error_f = false;

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    __quex_debug_buffer_load(me, "BACKWARD(entry)\n");
    if( me->_read_p != me->_memory._front ) {
        /* If the read pointer does not stand on 'front', then the buffer limit
         * code is a bad character, Buffer limit codes are not supposed to     
         * appear in buffer content.                                         */
        return E_LoadResult_ENCODING_ERROR;
    }
    else if( me->input.lexatom_index_begin == 0 ) {
        return E_LoadResult_NO_MORE_DATA; /* Begin of stream.                */
    }
    else if( ! me->filler || ! me->filler->byte_loader ) {
        return E_LoadResult_NO_MORE_DATA; /* No filler/loader => no loading! */
    }
    else if( ! QUEX_NAME(ByteLoader_seek_is_enabled)(me->filler->byte_loader) ) {
        return E_LoadResult_NO_MORE_DATA; /* Stream cannot go backwards.     */
    }

    move_distance = QUEX_NAME(Buffer_get_maximum_move_distance_towards_end)(me);

    if( 0 == move_distance ) {
        return E_LoadResult_FAILURE;
    }
    loaded_n = QUEX_NAME(Buffer_move_and_load_backward)(me, move_distance, &encoding_error_f, &load_request_n);

    if( encoding_error_f ) {
        return E_LoadResult_ENCODING_ERROR;
    }
    else if( loaded_n != move_distance ) {
        /* Serious: previously loaded content could not be loaded again!     
         * => Buffer has now hole: 
         *    from _front[1+loaded_n] to Begin[move_distance]                 
         * The analysis can continue in forward direction, but not backwards.*/
        return E_LoadResult_FAILURE;     
    }

    __quex_debug_buffer_load(me, "BACKWARD(exit)\n");
    QUEX_BUFFER_ASSERT_CONSISTENCY(me);
    return E_LoadResult_DONE;     
}

QUEX_INLINE bool
QUEX_NAME(Buffer_load_backward_to_contain)(QUEX_NAME(Buffer)*        me, 
                                           QUEX_TYPE_STREAM_POSITION NewCharacterIndexBegin)
/* Before:                     
 *            .------------------------------------- prev lexatom index begin
 *            :
 *            |x.x.x.x.x.x.x.x.x.x. . . . . . . . . . . . . |
 *            |<--- move size---->|                         
 * After:                                             
 *            .------------------------------------- new lexatom index begin
 *            :                     .--------------- prev lexatom index begin
 *            :                     :
 *            :--- move distance--->|                 
 *            |N.N.N.N.N.N.N.N.N.N.N.x.x.x.x.x.x.x.x.x.x. . | 
 *                               
 * Moves the region of size 'Size' from the beginning of the buffer to the end
 * and tries to load as many lexatoms as possible behind it. 
 *
 * RETURN: true, in case of success.
 *         false, if the region could not be be filled.
 *                => something is seriously wrong.                            */
{
    /* QUEX_TYPE_LEXATOM* end_p    = me->_memory._back; */
    ptrdiff_t loaded_n;
    ptrdiff_t load_request_n;
    ptrdiff_t move_distance;
    bool      encoding_error_f = false;

    __quex_assert(NewCharacterIndexBegin >= 0);
    __quex_assert(me->input.lexatom_index_begin >= NewCharacterIndexBegin);

    /* (1) Move away content, so that previous content can be reloaded.      */
    move_distance  = (ptrdiff_t)(me->input.lexatom_index_begin - NewCharacterIndexBegin);

    loaded_n = QUEX_NAME(Buffer_move_and_load_backward)(me, move_distance, 
                                                        &encoding_error_f, 
                                                        &load_request_n);
                           
    /* (3) In case of error, the stream must have been corrupted. Previously
     *     present content is not longer available. Continuation impossible.  */
    if( loaded_n != load_request_n ) {
        return false;
    }
    return true;
}

QUEX_INLINE bool
QUEX_NAME(Buffer_move_and_load)(QUEX_NAME(Buffer)*  me, 
                                QUEX_TYPE_LEXATOM** position_register,
                                size_t              PositionRegisterN,
                                ptrdiff_t           move_distance, 
                                bool*               encoding_error_f, 
                                ptrdiff_t*          loaded_n)
{
    QUEX_TYPE_STREAM_POSITION   load_lexatom_index;
    ptrdiff_t                   free_space;
    bool                        end_of_stream_f  = false;

    if( move_distance ) {
        QUEX_NAME(Buffer_move_towards_begin)(me, move_distance,
                                             position_register, PositionRegisterN); 
    }
    free_space = me->_memory._back - me->input.end_p;

    if( 0 == free_space ) {
        return false; 
    }

    load_lexatom_index  =   me->input.lexatom_index_begin 
                          + (me->input.end_p - &me->_memory._front[1]);

    *loaded_n = QUEX_NAME(LexatomLoader_load)(me->filler, me->input.end_p, free_space,
                                              load_lexatom_index, &end_of_stream_f,
                                              encoding_error_f);

    if( (! *loaded_n) || end_of_stream_f ) { /* End of stream detected.       */
        me->input.lexatom_index_end_of_stream = load_lexatom_index + *loaded_n;
    }

    me->input.end_p    = &me->input.end_p[*loaded_n];
    *(me->input.end_p) = QUEX_SETTING_BUFFER_LIMIT_CODE;
    return true;
}

QUEX_INLINE ptrdiff_t
QUEX_NAME(Buffer_move_and_load_backward)(QUEX_NAME(Buffer)* me, 
                                         ptrdiff_t          move_distance,
                                         bool*              encoding_error_f, 
                                         ptrdiff_t*         load_request_n)
{
    bool end_of_stream_f  = false;

    if( move_distance ) {
        if( me->_backup_lexatom_index_of_read_p == (QUEX_TYPE_STREAM_POSITION)-1 ) {
            /* If content has not been moved already, notify change!          */
            QUEX_NAME(Buffer_call_on_buffer_before_change)(me);
        }
        (void)QUEX_NAME(Buffer_move_towards_end)(me, (ptrdiff_t)move_distance);
    }

    *load_request_n = QUEX_MIN(me->_memory._back - &me->_memory._front[1], 
                               move_distance);

    /* (2) Move away content, so that previous content can be reloaded.       */
    return QUEX_NAME(LexatomLoader_load)(me->filler, &me->_memory._front[1], *load_request_n,
                                         me->input.lexatom_index_begin,
                                         &end_of_stream_f, encoding_error_f);
}

QUEX_INLINE void
QUEX_NAME(Buffer_backup_lexatom_index_of_read_p)(QUEX_NAME(Buffer)* me,
                                                 ptrdiff_t          move_distance)
{
    if(    me->_lexeme_start_p
        && me->_lexeme_start_p + move_distance >= me->_memory._back
        && me->_backup_lexatom_index_of_read_p == (QUEX_TYPE_STREAM_POSITION)-1 ) {
        /* Lexeme start will be out of buffer. Store the position to be
         * reloaded when lexing forward restarts.                             */
        me->_backup_lexatom_index_of_read_p =   QUEX_NAME(Buffer_tell)(me)
            + (me->_lexeme_start_p - me->_read_p);
    }
}

QUEX_INLINE bool
QUEX_NAME(Buffer_on_cannot_move_towards_begin)(QUEX_NAME(Buffer)*  me, 
                                               ptrdiff_t*          move_distance)
{
    if( me->input.end_p >= me->_memory._back && me->input.end_p == me->_read_p ) {
        /* No free space can be provided for loading new content. This is 
         * a buffer overflow situation. The lexeme spans complete buffer.     */
        QUEX_NAME(Buffer_call_on_buffer_overflow)(me);

        /* 'on_buffer_overflow' may have extended the buffer's memory.
         * => second chance!                                                  */
        *move_distance = QUEX_NAME(Buffer_get_move_distance_max_towards_begin)(me);
        if( me->input.end_p >= me->_memory._back ) {
            return false;                                         /* Give up! */
        }
    }
    return true;
}


QUEX_NAMESPACE_MAIN_CLOSE

#include <quex/code_base/buffer/lexatoms/LexatomLoader.i>
#include <quex/code_base/buffer/BufferMemory.i>

#endif /* __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_LOAD_I */

