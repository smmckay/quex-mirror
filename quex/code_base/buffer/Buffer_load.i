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

/* Moving buffer content. */
QUEX_INLINE ptrdiff_t QUEX_NAME(Buffer_move_towards_begin)(QUEX_NAME(Buffer)*  me, 
                                                           ptrdiff_t           move_distance);
QUEX_INLINE void      QUEX_NAME(Buffer_move_towards_begin_undo)(QUEX_NAME(Buffer)* me,
                                                          intmax_t           move_distance,
                                                          ptrdiff_t          move_size);
QUEX_INLINE ptrdiff_t QUEX_NAME(Buffer_move_towards_end)(QUEX_NAME(Buffer)* me, 
                                                         ptrdiff_t          move_distance);

QUEX_INLINE void      QUEX_NAME(Buffer_call_on_buffer_before_change)(QUEX_NAME(Buffer)* me);
QUEX_INLINE void      QUEX_NAME(Buffer_call_on_buffer_overflow)(QUEX_NAME(Buffer)* me,
                                                                bool               ForwardF);
QUEX_INLINE ptrdiff_t QUEX_NAME(Buffer_get_maximum_move_distance_towards_begin)(QUEX_NAME(Buffer)*   me, 
                                                                                QUEX_TYPE_LEXATOM**  move_begin_p);
QUEX_INLINE ptrdiff_t QUEX_NAME(Buffer_get_maximum_move_distance_towards_end)(QUEX_NAME(Buffer)* me);
QUEX_INLINE void      QUEX_NAME(Buffer_adapt_pointers_after_move_forward)(QUEX_NAME(Buffer)*  me,
                                                                          ptrdiff_t           move_distance,
                                                                          QUEX_TYPE_LEXATOM** position_register,
                                                                          const size_t        PositionRegisterN);
QUEX_INLINE void      QUEX_NAME(Buffer_adapt_pointers_after_move_backward)(QUEX_NAME(Buffer)* me,
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
    QUEX_TYPE_LEXATOM*          BeginP      = &me->_memory._front[1];
    QUEX_TYPE_LEXATOM*          EndP        = me->_memory._back;
    const ptrdiff_t             ContentSize = (ptrdiff_t)QUEX_NAME(Buffer_content_size)(me);
    QUEX_TYPE_STREAM_POSITION   ci_begin    = QUEX_NAME(Buffer_input_lexatom_index_begin)(me);
    QUEX_TYPE_STREAM_POSITION   ci_load_begin;
    ptrdiff_t                   move_distance;
    ptrdiff_t                   load_request_n;
    ptrdiff_t                   loaded_n;
    bool                        end_of_stream_f  = false;
    bool                        encoding_error_f = false;

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    if( me->_read_p != me->input.end_p) {
        /* If the read pointer does not stand on the end of input pointer, then
         * the 'buffer limit code' at the read pointer is a bad lexatom.    
         * Buffer limit codes cannot be possibly be part of buffer content.  */
        return E_LoadResult_BAD_LEXATOM;
    }
    else if( ! me->filler || ! me->filler->byte_loader ) {
        QUEX_NAME(Buffer_register_eos)(me, ci_begin + (me->input.end_p - BeginP));
        return E_LoadResult_NO_MORE_DATA;  /* No filler/loader => no load!   */
    }

    /* Move remaining content.
     * Maintain lexeme and fallback.                 
     * Adapt pointers.                                                       */
    move_distance = QUEX_NAME(Buffer_load_prepare_forward)(me, position_register, 
                                                               PositionRegisterN);

    if( ! move_distance && me->input.end_p == EndP ) {
        /* The 'on_buffer_overflow()' callback has been called already.      */
        return E_LoadResult_FAILURE; 
    }

    /* Load new content.                                                     */
    ci_load_begin  = me->input.lexatom_index_begin + (me->input.end_p - BeginP);
    load_request_n = ContentSize                   - (me->input.end_p - BeginP);
    loaded_n       = QUEX_NAME(LexatomLoader_load)(me->filler, 
                                                   me->input.end_p, load_request_n,
                                                   ci_load_begin, 
                                                   &end_of_stream_f,
                                                   &encoding_error_f);
    QUEX_NAME(Buffer_register_content)(me, &me->input.end_p[loaded_n], -1);

    if( ! loaded_n ) {
        /* If filler returned, then either some lexatoms have been filled, 
         * or it indicates 'end-of-stream' by 'load_n = 0'.                  */
        end_of_stream_f = true; 
    }
    if( end_of_stream_f ) {
        QUEX_NAME(Buffer_register_eos)(me, ci_load_begin + loaded_n); 
    }

    __quex_debug_buffer_load(me, "LOAD FORWARD(exit)\n");
    QUEX_BUFFER_ASSERT_CONSISTENCY(me);
    if     ( encoding_error_f ) return E_LoadResult_BAD_LEXATOM;
    else if( loaded_n )         return E_LoadResult_DONE;
    else                        return E_LoadResult_NO_MORE_DATA;
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
    QUEX_TYPE_LEXATOM*  BeginP = &me->_memory._front[1];
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
        return E_LoadResult_BAD_LEXATOM;
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

    move_distance = QUEX_NAME(Buffer_load_prepare_backward)(me);

    if( ! move_distance ) {
        return E_LoadResult_FAILURE;
    }

    /* Load new content.                                                     */
    loaded_n = QUEX_NAME(LexatomLoader_load)(me->filler, 
                                             BeginP, move_distance,
                                             me->input.lexatom_index_begin, 
                                             &end_of_stream_f, &encoding_error_f);
    if( encoding_error_f ) {
        return E_LoadResult_BAD_LEXATOM;
    }

    if( loaded_n  != move_distance ) {
        /* Serious: previously loaded content could not be loaded again!     
         * => Buffer has now hole: 
         *    from BeginP[loaded_n] to Begin[move_distance]                 
         * The analysis can continue in forward direction, but not backwards.*/
        return E_LoadResult_FAILURE;     
    }

    __quex_debug_buffer_load(me, "BACKWARD(exit)\n");
    QUEX_BUFFER_ASSERT_CONSISTENCY(me);
    return E_LoadResult_DONE;     
}

QUEX_INLINE bool
QUEX_NAME(Buffer_move_and_load_forward)(QUEX_NAME(Buffer)*        me, 
                                        QUEX_TYPE_STREAM_POSITION NewCharacterIndexBegin,
                                        QUEX_TYPE_STREAM_POSITION MinCharacterIndexInBuffer)
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
    QUEX_TYPE_LEXATOM*        BeginP      = &me->_memory._front[1];
    QUEX_TYPE_LEXATOM*        EndP        = me->_memory._back;
    const ptrdiff_t           ContentSize = (ptrdiff_t)QUEX_NAME(Buffer_content_size)(me);
    QUEX_TYPE_STREAM_POSITION load_lexatom_index;
    ptrdiff_t                 load_request_n;
    QUEX_TYPE_LEXATOM*        load_p;
    ptrdiff_t                 loaded_n;
    intmax_t                  move_distance;
    ptrdiff_t                 move_size;
    bool                      end_of_stream_f  = false;
    bool                      encoding_error_f = false;

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);
    __quex_assert(me->input.lexatom_index_begin        <= NewCharacterIndexBegin);
    __quex_assert(NewCharacterIndexBegin               <= MinCharacterIndexInBuffer);
    __quex_assert(NewCharacterIndexBegin + ContentSize >= MinCharacterIndexInBuffer );

    if(    me->input.lexatom_index_end_of_stream != -1
        && MinCharacterIndexInBuffer >= me->input.lexatom_index_end_of_stream ) {
        /* If the end of the stream is INSIDE the buffer already, then there
         * is no need, no chance, of loading more content.                   */
        return false;
    }

    /* Move existing content in the buffer to appropriate position.          */
    move_distance      = NewCharacterIndexBegin - me->input.lexatom_index_begin;

    QUEX_NAME(Buffer_call_on_buffer_before_change)(me);
    move_size          = QUEX_NAME(Buffer_move_towards_begin)(me, (ptrdiff_t)move_distance);
    load_lexatom_index = NewCharacterIndexBegin + move_size;
    load_request_n     = ContentSize - move_size; 
    load_p             = &BeginP[move_size];

    __quex_assert(load_lexatom_index == NewCharacterIndexBegin + (load_p - BeginP));
    __quex_assert(load_p >= BeginP);
    __quex_assert(&load_p[load_request_n] <= EndP);
    (void)EndP;
    loaded_n = QUEX_NAME(LexatomLoader_load)(me->filler, load_p, load_request_n,
                                             load_lexatom_index,
                                             &end_of_stream_f, &encoding_error_f);

    if( (! loaded_n) || end_of_stream_f ) { /* End of stream detected.       */
        QUEX_NAME(Buffer_register_eos)(me, load_lexatom_index + loaded_n);
    }

    /* (3) In case of failure, restore previous buffer content.              */
    if( MinCharacterIndexInBuffer >= load_lexatom_index + loaded_n ) {
        QUEX_NAME(Buffer_move_towards_begin_undo)(me, move_distance, move_size);
        return false;
    }

    QUEX_NAME(Buffer_register_content)(me, &load_p[loaded_n], NewCharacterIndexBegin);
    return true;
}

QUEX_INLINE bool
QUEX_NAME(Buffer_move_and_load_backward)(QUEX_NAME(Buffer)*        me, 
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
    QUEX_TYPE_LEXATOM*         BeginP   = &me->_memory._front[1];
    QUEX_TYPE_LEXATOM*         EndP     = me->_memory._back;
    QUEX_TYPE_STREAM_POSITION  ci_begin = QUEX_NAME(Buffer_input_lexatom_index_begin)(me);
    ptrdiff_t                  load_request_n;
    ptrdiff_t                  loaded_n;
    ptrdiff_t                  move_distance;
    QUEX_TYPE_LEXATOM*         end_p;
    bool                       end_of_stream_f = false;
    bool                       encoding_error_f = false;

    __quex_assert(NewCharacterIndexBegin >= 0);
    __quex_assert(ci_begin  >= NewCharacterIndexBegin);

    /* (1) Move away content, so that previous content can be reloaded.      */
    move_distance  = (ptrdiff_t)(ci_begin - NewCharacterIndexBegin);

    QUEX_NAME(Buffer_call_on_buffer_before_change)(me);
    load_request_n = QUEX_NAME(Buffer_move_towards_end)(me, (ptrdiff_t)move_distance);

    __quex_assert(&BeginP[load_request_n] <= EndP);

    /* (2) Move away content, so that previous content can be reloaded.      */
    loaded_n = QUEX_NAME(LexatomLoader_load)(me->filler, BeginP, load_request_n,
                                             NewCharacterIndexBegin,
                                             &end_of_stream_f, &encoding_error_f);
                           
    /* (3) In case of error, the stream must have been corrupted. Previously
     *     present content is not longer available. Continuation impossible. */
    if( loaded_n != load_request_n ) {
        return false;
    }

    end_p = EndP - me->input.end_p < move_distance ? 
            EndP : &me->input.end_p[move_distance];

    QUEX_NAME(Buffer_register_content)(me, end_p, NewCharacterIndexBegin);
    return true;
}

QUEX_INLINE ptrdiff_t
QUEX_NAME(Buffer_load_prepare_forward)(QUEX_NAME(Buffer)*  me,
                                       QUEX_TYPE_LEXATOM** position_register,
                                       const size_t        PositionRegisterN)
/* Free some space AHEAD so that new content can be loaded. Content that 
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
 * RETURNS: Moved distance >  0: OK.
 *                         == 0: Nothing has been moved.                     
 *                         <  0: Overflow. Nothing has been moved. 
 *                               Lexeme fills complete buffer.                */
{ 
    const QUEX_TYPE_LEXATOM*  EndP   = me->_memory._back;
    QUEX_TYPE_LEXATOM*        move_begin_p;
    ptrdiff_t                 move_size;
    ptrdiff_t                 move_distance;

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    move_distance = QUEX_NAME(Buffer_get_maximum_move_distance_towards_begin)(me, &move_begin_p);

    if( move_distance < 0 ) {
        QUEX_NAME(Buffer_call_on_buffer_overflow)(me, /* ForwardF */ true);
        return 0;
    }
    else if( ! move_distance ) {
        return 0;
    }
    else {
        QUEX_NAME(Buffer_call_on_buffer_before_change)(me);
    }

    move_size = QUEX_NAME(Buffer_move_towards_begin)(me, move_distance);

    QUEX_NAME(Buffer_adapt_pointers_after_move_forward)(me, move_distance, 
                                                        position_register,
                                                        PositionRegisterN);

    /*_______________________________________________________________________*/
    __quex_assert(me->input.end_p == &move_begin_p[move_size - move_distance]);
    (void)move_size;
    QUEX_IF_ASSERTS_poison(&EndP[- move_distance + 1], EndP);
    QUEX_BUFFER_ASSERT_CONSISTENCY(me);
    (void)EndP;

    return move_distance;
}

QUEX_INLINE ptrdiff_t        
QUEX_NAME(Buffer_load_prepare_backward)(QUEX_NAME(Buffer)* me)
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
    const QUEX_TYPE_LEXATOM*  BeginP = &me->_memory._front[1];
    ptrdiff_t                 move_distance;
    (void)BeginP;

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    move_distance = QUEX_NAME(Buffer_get_maximum_move_distance_towards_end)(me);

    if( move_distance < 0 ) {
        QUEX_NAME(Buffer_call_on_buffer_overflow)(me, /* ForwardF */ false);
        return 0;
    }
    else if( ! move_distance ) {
        return 0;
    }
    else {
        QUEX_NAME(Buffer_call_on_buffer_before_change)(me);
    }

    (void)QUEX_NAME(Buffer_move_towards_end)(me, move_distance);
    QUEX_NAME(Buffer_adapt_pointers_after_move_backward)(me, move_distance);
    /*________________________________________________________________________*/
    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    return move_distance;
}

QUEX_INLINE void
QUEX_NAME(Buffer_call_on_buffer_before_change)(QUEX_NAME(Buffer)* me)
{
    if( ! me->event.on_buffer_before_change ) return;

    me->event.on_buffer_before_change(me->event.aux, 
                                      &me->_memory._front[1], 
                                      me->input.end_p);
}

QUEX_INLINE void
QUEX_NAME(Buffer_call_on_buffer_overflow)(QUEX_NAME(Buffer)* me,
                                          bool               ForwardF)
{
    if( me->event.on_buffer_overflow ) {
        me->event.on_buffer_overflow(me->event.aux, me, ForwardF);
    }
}

QUEX_NAMESPACE_MAIN_CLOSE

#include <quex/code_base/buffer/lexatoms/LexatomLoader.i>
#include <quex/code_base/buffer/BufferMemory.i>

#endif /* __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_LOAD_I */

