/* vim:set ft=c: P-*- C++ -*- */
#ifndef __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_I
#define __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_I

#include <quex/code_base/asserts>
#include <quex/code_base/buffer/asserts>
#include <quex/code_base/definitions>
#include <quex/code_base/buffer/Buffer>
#include <quex/code_base/buffer/Buffer_debug.i>
#include <quex/code_base/buffer/filler/BufferFiller>
#include <quex/code_base/MemoryManager>

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE void  QUEX_NAME(BufferMemory_construct)(QUEX_NAME(BufferMemory)*  me, 
                                                    QUEX_TYPE_CHARACTER*      Memory, 
                                                    const size_t              Size,
                                                    E_Ownership               Ownership);
QUEX_INLINE void  QUEX_NAME(BufferMemory_destruct)(QUEX_NAME(BufferMemory)* me);

QUEX_INLINE void
QUEX_NAME(Buffer_construct)(QUEX_NAME(Buffer)*        me, 
                            QUEX_NAME(BufferFiller)*  filler,
                            QUEX_TYPE_CHARACTER*      memory,
                            const size_t              MemorySize,
                            QUEX_TYPE_CHARACTER*      EndOfFileP,
                            E_Ownership               Ownership)
{
    /* Ownership of InputMemory is passed to 'me->_memory'.                  */
    QUEX_NAME(BufferMemory_construct)(&me->_memory, memory, MemorySize, 
                                      Ownership); 
    
    me->on_buffer_content_change = (void (*)(const QUEX_TYPE_CHARACTER*, const QUEX_TYPE_CHARACTER*))0;

    /* Until now, nothing is loaded into the buffer.                         */
                                                                             
    /* By setting begin and end to zero, we indicate to the loader that      
     * this is the very first load procedure.                                */
    me->filler = filler;
    QUEX_NAME(Buffer_init_analyzis)(me, EndOfFileP);
}

QUEX_INLINE void
QUEX_NAME(Buffer_destruct)(QUEX_NAME(Buffer)* me)
{
    QUEX_NAME(BufferFiller_delete)(&me->filler); 
    QUEX_NAME(BufferMemory_destruct)(&me->_memory);
}

QUEX_INLINE void
QUEX_NAME(Buffer_init_analyzis)(QUEX_NAME(Buffer)*   me, 
                                QUEX_TYPE_CHARACTER* EndOfFileP) 
{
    QUEX_TYPE_CHARACTER*      end_p;
    QUEX_TYPE_STREAM_POSITION end_character_index;

    __quex_assert(   ! EndOfFileP 
                  || (EndOfFileP > me->_memory._front && EndOfFileP <= me->_memory._back));
    /* (1) BEFORE LOAD: The pointers must be defined which restrict the 
     *                  fill region. 
     *
     * The first state in the state machine does not increment. Thus, the
     * input pointer is set to the first position, not before.               */
    me->_read_p         = &me->_memory._front[1];                            
    me->_lexeme_start_p = &me->_memory._front[1];                            
                                                                             
    /* No character covered yet -> '\0'.                                     */
    me->_character_at_lexeme_start = '\0';                                   
#   ifdef  __QUEX_OPTION_SUPPORT_BEGIN_OF_LINE_PRE_CONDITION                 
    /* When the buffer is initialized, a line begins. Signalize that.        */
    me->_character_before_lexeme_start = QUEX_SETTING_CHARACTER_NEWLINE_IN_ENGINE_CODEC;
#   endif

    /* (2) Load content, determine character indices of borders, determine
     *     end of file pointer.                                              */
    if( me->filler && me->filler->byte_loader ) {
        __quex_assert(! EndOfFileP);
        end_p               = me->_memory._front;                   /* EMPTY */
        end_character_index = 0;
        QUEX_NAME(Buffer_input_end_set)(me, end_p, end_character_index);
        QUEX_NAME(BufferFiller_load_forward)(me);   
    } 
    else {
        if( EndOfFileP ) {
            end_p               = EndOfFileP;
            end_character_index = EndOfFileP - &me->_memory._front[1];
        }
        else {
            end_p               = me->_memory._front;               /* EMPTY */
            end_character_index = 0;
        }
        QUEX_NAME(Buffer_input_end_set)(me, end_p, end_character_index);
    }

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);
}

QUEX_INLINE void
QUEX_NAME(Buffer_input_end_set)(QUEX_NAME(Buffer)*        me,
                                QUEX_TYPE_CHARACTER*      EndOfInputP,
                                QUEX_TYPE_STREAM_POSITION EndCharacterIndex)
/* Determines the two parameters concerned with the end of input. Sets both
 * elements and makes sure that buffer limit codes are setup properly.
 *
 * input.end_p != 0, if the input stream's end has not been reached yet and the
 *                   buffer is fully filled.
 *             == 0, if the input stream's end has been reached and the buffer 
 *                   is no longer fully filled, due to lack of more incoming
 *                   data. Then, 'input.end_p' points to the first position 
 *                   behind the last filled character.
 *
 * input.end_character_index: character index of the last character in the
 *                            the buffer PLUS ONE. It is the index of the next
 *                            character that would be loaded upon the call to
 *                            'load_forward'.                                */
{
    if( EndOfInputP ) {
        __quex_assert(EndOfInputP <= me->_memory._back);
        /* EndOfInputP == me->_memory._front indicates 'EMPTY'               */
        __quex_assert(EndOfInputP >=  me->_memory._front);
        *EndOfInputP = QUEX_SETTING_BUFFER_LIMIT_CODE;
        QUEX_IF_ASSERTS_poison(&EndOfInputP[1], me->_memory._back);
    }
    me->input.end_p               = EndOfInputP;
    me->input.end_character_index = EndCharacterIndex;

    /* NOT: assert(QUEX_NAME(Buffer_input_begin_character_index)(me) >= 0);
     * This function may be called before content is setup/loaded propperly. */ 
}

QUEX_INLINE bool
QUEX_NAME(Buffer_is_empty)(QUEX_NAME(Buffer)* me)
/* Setting the input.end_p = front meanse: buffer is empty.                  */
{ return me->input.end_p == me->_memory._front; }

QUEX_INLINE QUEX_TYPE_STREAM_POSITION  
QUEX_NAME(Buffer_input_begin_character_index)(QUEX_NAME(Buffer)* me)
/* Determine character index of first character in the buffer.               */
{
    const ptrdiff_t            fill_level =   QUEX_NAME(Buffer_text_end)(me) 
                                            - &me->_memory._front[1];
    QUEX_TYPE_STREAM_POSITION  result     =   me->input.end_character_index 
                                            - fill_level;
    /* NOT: assert(result >= 0); 
     * This function may be called before content is setup/loaded propperly. */ 
    return result;
}

QUEX_INLINE void
QUEX_NAME(Buffer_read_p_add_offset)(QUEX_NAME(Buffer)* buffer, const size_t Offset)
{ 
    QUEX_BUFFER_ASSERT_pointers_in_range(buffer);
    buffer->_read_p += Offset; 
    QUEX_BUFFER_ASSERT_pointers_in_range(buffer);
}

QUEX_INLINE QUEX_TYPE_CHARACTER
QUEX_NAME(Buffer_input_get_offset)(QUEX_NAME(Buffer)* me, const ptrdiff_t Offset)
{
    QUEX_BUFFER_ASSERT_pointers_in_range(me);
    __quex_assert( me->_read_p + Offset > me->_memory._front );
    __quex_assert( me->_read_p + Offset <= me->_memory._back );
    return *(me->_read_p + Offset); 
}

QUEX_INLINE QUEX_TYPE_CHARACTER*
QUEX_NAME(Buffer_content_front)(QUEX_NAME(Buffer)* me)
{
    return me->_memory._front + 1;
}

QUEX_INLINE QUEX_TYPE_CHARACTER*
QUEX_NAME(Buffer_content_back)(QUEX_NAME(Buffer)* me)
{
    return me->_memory._back - 1;
}

QUEX_INLINE size_t
QUEX_NAME(Buffer_content_size)(QUEX_NAME(Buffer)* me)
{
    return QUEX_NAME(BufferMemory_size)(&(me->_memory)) - 2;
}

QUEX_INLINE QUEX_TYPE_CHARACTER*  
QUEX_NAME(Buffer_text_end)(QUEX_NAME(Buffer)* me)
/* Returns a pointer to the position after the last text content inside 
 * the buffer.                                                               */
{
    return me->input.end_p ? me->input.end_p : me->_memory._back;   
}

QUEX_INLINE ptrdiff_t
QUEX_NAME(Buffer_distance_input_to_text_end)(QUEX_NAME(Buffer)* me)
{
    QUEX_BUFFER_ASSERT_pointers_in_range(me);
    return QUEX_NAME(Buffer_text_end)(me) - me->_read_p;
}

QUEX_INLINE bool 
QUEX_NAME(Buffer_is_end_of_file)(QUEX_NAME(Buffer)* buffer)
{ 
    QUEX_BUFFER_ASSERT_CONSISTENCY(buffer);
    return buffer->_read_p == buffer->input.end_p;
}

QUEX_INLINE bool                  
QUEX_NAME(Buffer_is_begin_of_file)(QUEX_NAME(Buffer)* buffer)
{ 
    QUEX_BUFFER_ASSERT_CONSISTENCY(buffer);
    if     ( buffer->_read_p != buffer->_memory._front )                  return false;
    else if( QUEX_NAME(Buffer_input_begin_character_index)(buffer) != 0 ) return false;
    return true;
}

QUEX_INLINE QUEX_TYPE_CHARACTER*
QUEX_NAME(Buffer_move_away_passed_content)(QUEX_NAME(Buffer)* me)
/* Free some space AHEAD so that new content can be loaded. Content that 
 * is still used, or expected to be used shall remain inside the buffer.
 * Following things need to be respected:
 *
 *    _lexeme_start_p  --> points to the lexeme that is currently treated.
 *                         MUST BE INSIDE BUFFER!
 *    _read_p          --> points to the character that is currently used
 *                         for triggering. MUST BE INSIDE BUFFER!
 *    fall back region --> A used defined buffer backwards from the lexeme
 *                         start. Shall help to avoid extensive backward
 *                         loading.
 *
 * RETURNS: Pointer to the end of the maintained content.                    */
{ 
    QUEX_TYPE_CHARACTER*        FrontP      = &me->_memory._front[1];
    const QUEX_TYPE_CHARACTER*  BackP       = &me->_memory._back[-1];
    const QUEX_TYPE_CHARACTER*  ContentEndP = me->input.end_p ? me->input.end_p 
                                                              : me->_memory._back;
    QUEX_TYPE_CHARACTER*        end_p;
    QUEX_TYPE_CHARACTER*        move_begin_p;
    size_t                      move_size;
    ptrdiff_t                   move_distance;
    const ptrdiff_t             FallBackN   = (ptrdiff_t)QUEX_SETTING_BUFFER_MIN_FALLBACK_N;

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    /* Determine from where the region-to-be-moved BEGINS, what its size is
     * and how far it is to be moved.                                        */
    move_begin_p  = me->_read_p;
    move_begin_p  = me->_lexeme_start_p ? 
                      QUEX_MIN(move_begin_p, me->_lexeme_start_p)
                    : move_begin_p;
    /* Plain math: move_begin_p = max(FrontP, move_begin_p - FallBackN); 
     * BUT: Consider case where 'move_begin_p - FallBackN < 0'! CAREFUL!     */
    move_begin_p  = &FrontP[FallBackN] > move_begin_p ? FrontP 
                                                      : &move_begin_p[- FallBackN];
    move_size     = (ptrdiff_t)(ContentEndP - move_begin_p);
    move_distance = move_begin_p - FrontP;

    if( ! move_distance ) return (QUEX_TYPE_CHARACTER*)0;

    else if( move_size ) {
        /* Move.                                                             */
        __QUEX_STD_memmove((void*)FrontP, (void*)move_begin_p,
                           move_size * sizeof(QUEX_TYPE_CHARACTER));
    }

    /* Pointer Adaption: _read_p, _lexeme_start_p, 
     *                   input.end_p, input.end_character_index              */
    me->_read_p -= move_distance;
    if( me->_lexeme_start_p ) {
        me->_lexeme_start_p -= move_distance;
    }

    /* input.end_p/end_character_index: End character index remains the SAME, 
     * since no new content has been loaded into the buffer.                 */
    if( ! me->input.end_p ) {
        end_p = (QUEX_TYPE_CHARACTER*)0;
    }
    else if( &me->input.end_p[- move_distance] < FrontP ) {
        __quex_assert(false);
    }
    else {
        end_p = &me->input.end_p[- move_distance];
    }

    QUEX_NAME(Buffer_input_end_set)(me, end_p, me->input.end_character_index);

    /*_______________________________________________________________________*/
    QUEX_IF_ASSERTS_poison(&BackP[- move_distance + 1], &BackP[1]);
    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    return &move_begin_p[move_size - move_distance];
}

QUEX_INLINE ptrdiff_t        
QUEX_NAME(Buffer_move_away_upfront_content)(QUEX_NAME(Buffer)* me)
/* Free some space in the REAR so that previous content can be re-loaded. Some 
 * content is to be left in front, so that no immediate reload is necessary
 * once the analysis goes forward again. Following things need to be respected:
 *
 *    _lexeme_start_p  --> points to the lexeme that is currently treated.
 *                         MUST BE INSIDE BUFFER!
 *    _read_p          --> points to the character that is currently used
 *                         for triggering. MUST BE INSIDE BUFFER!
 *
 * RETURNS: Distance the the buffer content has been freed to be filled.     */
{
    const QUEX_TYPE_CHARACTER*       FrontP      = &me->_memory._front[1];
    const QUEX_TYPE_CHARACTER*       BackP       = &me->_memory._back[-1];
    const ptrdiff_t                  ContentSize = BackP - FrontP + 1;
    const QUEX_TYPE_CHARACTER*       ContentEndP = me->input.end_p ? me->input.end_p 
                                                                   : me->_memory._back;
    const QUEX_TYPE_CHARACTER*       move_end_p;
    ptrdiff_t                        move_distance;
    ptrdiff_t                        move_size;
    QUEX_TYPE_CHARACTER*             end_p;
    QUEX_TYPE_STREAM_POSITION        begin_character_index;
    QUEX_TYPE_STREAM_POSITION        end_character_index;

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    begin_character_index = QUEX_NAME(Buffer_input_begin_character_index)(me);
    /* The begin character index should never be negative--one cannot read
     * before the first byte of a stream. 
     * --> move_distance      <= begin_character_index                       */
    __quex_assert(begin_character_index >= 0);

    /* Determine where the region-to-be-moved ENDS, what its size is and how
     * far it is to be moved.                                                */
    move_distance = &BackP[1] - ContentEndP;
    move_distance = QUEX_MAX(move_distance, (ptrdiff_t)(ContentSize/3));
    move_distance = QUEX_MIN(move_distance, begin_character_index);
    move_distance = QUEX_MIN(move_distance, BackP - me->_read_p);
    if( me->_lexeme_start_p ) {
        move_distance = QUEX_MIN(move_distance, BackP - me->_lexeme_start_p);
    }
    move_end_p    = &BackP[1] - move_distance;
    move_size     = (ptrdiff_t)(move_end_p - FrontP);

    if( ! move_distance ) return 0;

    if( move_size ) {
        /* Move.                                                             */
        __QUEX_STD_memmove((void*)&FrontP[move_distance], (void*)FrontP, 
                           move_size * sizeof(QUEX_TYPE_CHARACTER));
    }

    /* Pointer Adaption: _read_p, _lexeme_start_p.                           */
    me->_read_p += move_distance;
    if( me->_lexeme_start_p ) {
        me->_lexeme_start_p += move_distance;
    }

    /* input.end_p/end_character_index: End character index may CHANGE, since 
     * some of the loaded content is thrown away.                            */
    if( ! me->input.end_p ) {
        end_character_index = me->input.end_character_index - move_distance;
        end_p               = (QUEX_TYPE_CHARACTER*)0;
    }
    else if( &me->input.end_p[move_distance] > &BackP[1] ) {
        end_character_index = me->input.end_character_index 
                              - (&me->input.end_p[move_distance] - &BackP[1]);
        end_p               = (QUEX_TYPE_CHARACTER*)0;
    }
    else {
        end_p               = &me->input.end_p[move_distance];
        end_character_index = me->input.end_character_index;
    }

    QUEX_NAME(Buffer_input_end_set)(me, end_p, end_character_index);

    /*_______________________________________________________________________*/
    QUEX_IF_ASSERTS_poison(FrontP, &FrontP[move_distance]); 
    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    return move_distance;
}

QUEX_INLINE size_t          
QUEX_NAME(BufferMemory_size)(QUEX_NAME(BufferMemory)* me)
{ return (size_t)(me->_back - me->_front + 1); }

QUEX_INLINE void
QUEX_NAME(Buffer_reverse_byte_order)(QUEX_TYPE_CHARACTER*       Begin, 
                                     const QUEX_TYPE_CHARACTER* End)
{
    uint8_t              tmp = 0xFF;
    QUEX_TYPE_CHARACTER* iterator = 0x0;

    switch( sizeof(QUEX_TYPE_CHARACTER) ) {
    default:
        __quex_assert(false);
        break;
    case 1:
        /* Nothing to be done */
        break;
    case 2:
        for(iterator=Begin; iterator != End; ++iterator) {
            tmp = *(((uint8_t*)iterator) + 0);
            *(((uint8_t*)iterator) + 0) = *(((uint8_t*)iterator) + 1);
            *(((uint8_t*)iterator) + 1) = tmp;
        }
        break;
    case 4:
        for(iterator=Begin; iterator != End; ++iterator) {
            tmp = *(((uint8_t*)iterator) + 0);
            *(((uint8_t*)iterator) + 0) = *(((uint8_t*)iterator) + 3);
            *(((uint8_t*)iterator) + 3) = tmp;
            tmp = *(((uint8_t*)iterator) + 1);
            *(((uint8_t*)iterator) + 1) = *(((uint8_t*)iterator) + 2);
            *(((uint8_t*)iterator) + 2) = tmp;
        }
        break;
    }
}

QUEX_INLINE void 
QUEX_NAME(BufferMemory_construct)(QUEX_NAME(BufferMemory)*  me, 
                                  QUEX_TYPE_CHARACTER*      Memory, 
                                  const size_t              Size,
                                  E_Ownership               Ownership) 
{
    __quex_assert(Memory);
    /* "Memory size > QUEX_SETTING_BUFFER_MIN_FALLBACK_N + 2" is reqired.
     * Maybe, define '-DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0' for 
     * compilation (assumed no pre-contexts.)                            */
    __quex_assert(Size > QUEX_SETTING_BUFFER_MIN_FALLBACK_N + 2);

    me->_front    = Memory;
    me->_back     = &Memory[Size-1];
    me->ownership = Ownership;
    *(me->_front) = QUEX_SETTING_BUFFER_LIMIT_CODE;
    *(me->_back)  = QUEX_SETTING_BUFFER_LIMIT_CODE;
}

QUEX_INLINE void 
QUEX_NAME(BufferMemory_destruct)(QUEX_NAME(BufferMemory)* me) 
/* Does not set 'me->_front' to zero, if it is not deleted. Thus, the user
 * may detect wether it needs to be deleted or not.                      */
{
    if( me->_front && me->ownership == E_Ownership_LEXICAL_ANALYZER ) {
        QUEXED(MemoryManager_free)((void*)me->_front, 
                                   E_MemoryObjectType_BUFFER_MEMORY);
        /* Protect against double-destruction.                           */
        me->_front = me->_back = (QUEX_TYPE_CHARACTER*)0x0;
    }
}

QUEX_NAMESPACE_MAIN_CLOSE

#include <quex/code_base/buffer/Buffer_debug.i>
#include <quex/code_base/buffer/Buffer_navigation.i>

#endif /* __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_I */


