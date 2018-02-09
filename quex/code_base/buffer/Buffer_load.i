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

QUEX_INLINE bool
QUEX_NAME(Buffer_on_cannot_move_towards_begin)(QUEX_NAME(Buffer)*  me, 
                                               ptrdiff_t*          move_distance);

QUEX_INLINE bool
QUEX_NAME(Buffer_move_and_load)(QUEX_NAME(Buffer)*  me, 
                                QUEX_TYPE_LEXATOM** position_register,
                                size_t              PositionRegisterN,
                                ptrdiff_t           move_distance, 
                                bool*               encoding_error_f, 
                                ptrdiff_t*          loaded_n);
QUEX_INLINE bool
QUEX_NAME(Buffer_move_and_load_backward)(QUEX_NAME(Buffer)*  me, 
                                         ptrdiff_t           move_distance, 
                                         bool*               encoding_error_f, 
                                         ptrdiff_t*          loaded_n);
QUEX_INLINE void
QUEX_NAME(Buffer_backup_lexatom_index_of_read_p)(QUEX_NAME(Buffer)* me,
                                                 ptrdiff_t          move_distance);

QUEX_INLINE E_LoadResult
QUEX_NAME(Buffer_load_forward)(QUEX_NAME(Buffer)*  me,
                               QUEX_TYPE_LEXATOM** position_register,
                               const size_t        PositionRegisterN)
/* Load as much new content into the buffer as possible--from what lies ahead
 * in the input stream. Maintains '_read_p', '_lexeme_start_p' inside the
 * buffer (if possible also fallback region). The 'input.end_p' pointer and
 * 'input.end_lexatom_index' are adapted according to the newly loaded
 * content, i.e. the point to exactly the same lexatom as before the load.
 *
 * BEHAVIOR: BLOCKING wait for incoming stream content. 
 *           No return without content--except at end of stream.
 *
 *           Buffer and pointers are adapted are adapted IN ANY CASE!
 *
 *           (i) Content present:
 *               => return 'true'.
 *
 *           (ii) No content:
 *               => pointers are 'disabled' because 'end_p = _read_p'.
 *                  return 'false'.
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
 *
 * The case of 'end-of-stream' may be true in both cases. When 'end-of-stream' 
 * is detected, the lexatom index of the 'end-of-stream' is registered. This 
 * prevents future attemps to load beyond that index. Again, even if 
 * 'end-of-stream' has been detected, there might be lexatoms for the lexer 
 * to chew on.                                                               */
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
QUEX_NAME(Buffer_move_and_load)(QUEX_NAME(Buffer)*  me, 
                                QUEX_TYPE_LEXATOM** position_register,
                                size_t              PositionRegisterN,
                                ptrdiff_t           move_distance, 
                                bool*               encoding_error_f, 
                                ptrdiff_t*          loaded_n)
{
    QUEX_TYPE_STREAM_POSITION   load_lexatom_index;
    ptrdiff_t                   move_size;
    ptrdiff_t                   free_space;
    bool                        end_of_stream_f  = false;

    if( move_distance ) {
        QUEX_NAME(Buffer_call_on_buffer_before_change)(me);

        move_size = QUEX_NAME(Buffer_move_towards_begin)(me, move_distance);

        QUEX_NAME(Buffer_pointers_add_offset)(me, - move_distance, 
                                              position_register, PositionRegisterN); 
        __quex_assert(me->input.end_p == &me->_memory._front[1 + move_size]);
        (void)move_size;
    }
    free_space = me->_memory._back - me->input.end_p;

    if( free_space == 0 ) {
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

QUEX_INLINE bool
QUEX_NAME(Buffer_load_forward_to_contain)(QUEX_NAME(Buffer)*        me, 
                                          QUEX_TYPE_STREAM_POSITION LexatomIndexToBeContained)
/* RETURNS:  true -- if the the buffer could be filled starting from 
 *                   NewCharacterIndexBegin.
 *           false, else.
 *
 * In case, that the loading fails, the buffer is setup as it was BEFORE the call
 * to this function.
 *
 * EXPLANATION:
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
 * Moves the region of size 'Size' from the end of the buffer to the beginning
 * of the buffer and tries to load as many lexatoms as possible behind it. */
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

    /* Move existing content in the buffer to appropriate position.          */
    move_distance = QUEX_NAME(Buffer_get_move_distance_forward_to_contain)(me, 
                                             &lexatom_index_to_be_contained);

    verdict_f = QUEX_NAME(Buffer_move_and_load)(me, (QUEX_TYPE_LEXATOM**)0, 0,
                                                move_distance, &encoding_error_f, &loaded_n);
    if(    verdict_f
        && LexatomIndexToBeContained < me->input.lexatom_index_begin + 
                                       (me->input.end_p - &me->_memory._front[1]) ) {
        return true;
    }
    load_request_n = QUEX_NAME(Buffer_move_towards_begin_undo)(me, &bi, move_distance);

    loaded_n       = QUEX_NAME(LexatomLoader_load)(me->filler, &me->_memory._front[1], load_request_n,
                                                   me->input.lexatom_index_begin,
                                                   &end_of_stream_f, &encoding_error_f);
    if( loaded_n != load_request_n ) {
        QUEX_ERROR_EXIT("Buffer filler failed to load content that has been loaded before.!");
    }
    else {
        /* Ensure, that the buffer limit code is restored.                   */
        *(me->input.end_p) = (QUEX_TYPE_LEXATOM)QUEX_SETTING_BUFFER_LIMIT_CODE;
    }
    return false;
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
    bool                end_of_stream_f  = false;
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
    QUEX_NAME(Buffer_backup_lexatom_index_of_read_p)(me, move_distance);
    
    (void)QUEX_NAME(Buffer_move_towards_end)(me, move_distance);
    QUEX_NAME(Buffer_pointers_add_offset)(me, move_distance, (QUEX_TYPE_LEXATOM**)0, 0);

    /* Load new content.                                                     */
    loaded_n = QUEX_NAME(LexatomLoader_load)(me->filler, &me->_memory._front[1], move_distance,
                                             me->input.lexatom_index_begin, 
                                             &end_of_stream_f, &encoding_error_f);
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
    QUEX_TYPE_LEXATOM*         begin_p  = &me->_memory._front[1];
    QUEX_TYPE_LEXATOM*         end_p    = me->_memory._back;
    QUEX_TYPE_STREAM_POSITION  ci_begin = QUEX_NAME(Buffer_input_lexatom_index_begin)(me);
    ptrdiff_t                  load_request_n;
    ptrdiff_t                  loaded_n;
    ptrdiff_t                  move_distance;
    bool                       end_of_stream_f  = false;
    bool                       encoding_error_f = false;

    __quex_assert(NewCharacterIndexBegin >= 0);
    __quex_assert(ci_begin  >= NewCharacterIndexBegin);

    /* (1) Move away content, so that previous content can be reloaded.      */
    move_distance  = (ptrdiff_t)(ci_begin - NewCharacterIndexBegin);

    QUEX_NAME(Buffer_call_on_buffer_before_change)(me);
    load_request_n = QUEX_NAME(Buffer_move_towards_end)(me, (ptrdiff_t)move_distance);

    /* Assign 'begin_p/end_p' lately to capture adaptions in preparation etc. */
    begin_p = &me->_memory._front[1];
    end_p   = me->_memory._back;                                    (void)end_p;

    __quex_assert(&begin_p[load_request_n] <= end_p);

    /* (2) Move away content, so that previous content can be reloaded.       */
    loaded_n = QUEX_NAME(LexatomLoader_load)(me->filler, begin_p, load_request_n,
                                             NewCharacterIndexBegin,
                                             &end_of_stream_f, &encoding_error_f);
                           
    /* (3) In case of error, the stream must have been corrupted. Previously
     *     present content is not longer available. Continuation impossible.  */
    if( loaded_n != load_request_n ) {
        return false;
    }

    end_p = end_p - me->input.end_p < move_distance ? 
            end_p : &me->input.end_p[move_distance];

    QUEX_NAME(Buffer_register_content)(me, end_p, NewCharacterIndexBegin);
    return true;
}

QUEX_INLINE void
QUEX_NAME(Buffer_backup_lexatom_index_of_read_p)(QUEX_NAME(Buffer)* me,
                                                 ptrdiff_t          move_distance)
{
    if( me->_backup_lexatom_index_of_read_p == (QUEX_TYPE_STREAM_POSITION)-1 ) {
        QUEX_NAME(Buffer_call_on_buffer_before_change)(me);
    }
    else {
        /* Content has already been completely moved. No notification.        */
    }

    if(    me->_lexeme_start_p
           && me->_lexeme_start_p + move_distance >= me->_memory._back
           && me->_backup_lexatom_index_of_read_p == (QUEX_TYPE_STREAM_POSITION)-1 ) {
        /* Lexeme start will be out of buffer. Store the position to be
         * reloaded when lexing forward restarts.                             */
        me->_backup_lexatom_index_of_read_p =   QUEX_NAME(Buffer_tell)(me)
            + (me->_lexeme_start_p - me->_read_p);
    }
}

QUEX_INLINE ptrdiff_t
QUEX_NAME(Buffer_free_back)(QUEX_NAME(Buffer)*  me,
                            QUEX_TYPE_LEXATOM** position_register,
                            const size_t        PositionRegisterN)
/*    ..    WARNING: 
 *   /  \   Pointers to the '_memory' object may change!
 *  /    \  References to pointers from prior a call to this function
 *  '----'  become INVALID!
 *
 * Free some space AHEAD so that new content can be loaded. Content that 
 * is still used, or expected to be used shall remain inside the buffer.
 * Following things need to be respected:
 *
 *    _lexeme_start_p  --> points to the lexeme that is currently treated.
 *                         MUST BE INSIDE BUFFER!
 *    _read_p          --> points to the lexatom that is currently used
 *                         for triggering. MUST BE INSIDE BUFFER!
 *    fall back region --> A used defined buffer backwards from the lexeme
 *                         start. Shall help to avoid extensive backward
 *                         loading.
 *
 * RETURNS: Free space at end of buffer to fill new data.
 *          0, if there is none.                                              */
{ 
    ptrdiff_t  free_space;
    ptrdiff_t  move_distance;
    ptrdiff_t  move_size;
    (void)move_size;

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    move_distance = QUEX_NAME(Buffer_get_move_distance_max_towards_begin)(me); 

    if( 0 == move_distance ) {
        if( ! QUEX_NAME(Buffer_on_cannot_move_towards_begin)(me, &move_distance) ) {
            return 0;
        }
    }

    if( move_distance ) {
        QUEX_NAME(Buffer_call_on_buffer_before_change)(me);

        move_size = QUEX_NAME(Buffer_move_towards_begin)(me, move_distance);

        QUEX_NAME(Buffer_pointers_add_offset)(me, - move_distance, 
                                              position_register, PositionRegisterN); 
        __quex_assert(me->input.end_p == &me->_memory._front[1 + move_size]);
        (void)move_size;
    }

    free_space = me->_memory._back - me->input.end_p;

    /*________________________________________________________________________*/
    QUEX_IF_ASSERTS_poison(&me->_memory._back[- move_distance + 1], 
                           me->_memory._back);

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    return free_space;
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

QUEX_INLINE ptrdiff_t
QUEX_NAME(Buffer_nested_free_front)(QUEX_NAME(Buffer)* me)
/* Shrink all nesting buffers to a minimum and reset all pointers accordingly.
 *
 * RETURNS: Free space at the end of 'me'.                                    */
{
    QUEX_NAME(Buffer)* it;
    QUEX_NAME(Buffer)* previous = (QUEX_NAME(Buffer)*)0;
    ptrdiff_t          move_distance = 0;
    ptrdiff_t          nesting_freed = 0;

    /* Iterate over all nesting buffers starting from root up to 'me'.
     * Shrink each buffer, adapt its 'back pointer' and the 'front pointer'
     * of the included buffer.                                                */
    for(it = QUEX_NAME(Buffer_nested_find_root)(me); true ; 
        it = QUEX_NAME(Buffer_get_nested)(it, me)) {
        move_distance = QUEX_NAME(Buffer_get_move_distance_max_towards_begin)(it);

        if( previous ) {
            previous->_memory._back   -= nesting_freed;
            it->_memory._front        -= nesting_freed;
            previous->_memory._back[0] = (QUEX_TYPE_LEXATOM)(QUEX_SETTING_BUFFER_LIMIT_CODE);
            it->_memory._front[0]      = (QUEX_TYPE_LEXATOM)(QUEX_SETTING_BUFFER_LIMIT_CODE);
        }

        (void)QUEX_NAME(Buffer_move_towards_begin_and_adapt_pointers)(it, 
                          move_distance + nesting_freed,
                          (QUEX_TYPE_LEXATOM**)0, 0);

        /* Adapt pointers added 'move_distance + nesting_freed' to lexatom
         * index. Must subtract 'nesting_freed'.                              */
        __quex_assert(it->input.lexatom_index_begin >= nesting_freed);
        it->input.lexatom_index_begin -= nesting_freed;

        if( it == me ) {
            break;
        }

        nesting_freed = it->_memory._back - it->input.end_p;
        previous      = it;
    } 

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);
    return me->_memory._back - me->input.end_p;
}
    
QUEX_INLINE ptrdiff_t        
QUEX_NAME(Buffer_free_front)(QUEX_NAME(Buffer)* me)
/* Free some space in the REAR so that previous content can be re-loaded. Some 
 * content is to be left in front, so that no immediate reload is necessary
 * once the analysis goes forward again. Following things need to be respected:
 *
 *    _lexeme_start_p  --> points to the lexeme that is currently treated.
 *                         MUST BE INSIDE BUFFER!
 *    _read_p          --> points to the lexatom that is currently used
 *                         for triggering. MUST BE INSIDE BUFFER!
 *
 * RETURNS: Moved distance >  0: OK.
 *                         == 0: Nothing has been moved.                     
 *                         <  0: Overflow. Nothing has been moved. 
 *                               Lexeme fills complete buffer.                */
{
    const QUEX_TYPE_LEXATOM*  last_p = (QUEX_TYPE_LEXATOM*)0;
    ptrdiff_t                 move_distance;

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    if( 0 == me->input.lexatom_index_begin ) {
        return 0;
    }
    
    move_distance = QUEX_NAME(Buffer_get_maximum_move_distance_towards_end)(me);

    if( 0 == move_distance ) {
        return 0;
    }
    else if( me->_backup_lexatom_index_of_read_p == (QUEX_TYPE_STREAM_POSITION)-1 ) {
        QUEX_NAME(Buffer_call_on_buffer_before_change)(me);
    }
    else {
        /* Content has already been completely moved. No notification.        */
    }

    /* Assign 'last_p' lately to capture adaptions in preparation etc.        */
    last_p = &me->_memory._back[-1];

    if(    me->_lexeme_start_p
        && me->_lexeme_start_p + move_distance > last_p 
        && me->_backup_lexatom_index_of_read_p == (QUEX_TYPE_STREAM_POSITION)-1 ) {
        /* Lexeme start will be out of buffer. Store the position to be
         * reloaded when lexing forward restarts.                             */
        me->_backup_lexatom_index_of_read_p =   QUEX_NAME(Buffer_tell)(me)
                                              + (me->_lexeme_start_p - me->_read_p);
    }
    
    (void)QUEX_NAME(Buffer_move_towards_end)(me, move_distance);
    QUEX_NAME(Buffer_pointers_add_offset)(me, move_distance, (QUEX_TYPE_LEXATOM**)0, 0);

    /*________________________________________________________________________*/
    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    return move_distance;
}

QUEX_NAMESPACE_MAIN_CLOSE

#include <quex/code_base/buffer/lexatoms/LexatomLoader.i>
#include <quex/code_base/buffer/BufferMemory.i>

#endif /* __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_LOAD_I */

