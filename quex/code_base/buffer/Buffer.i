/* vim:set ft=c: -*- C++ -*- */
#ifndef __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_I
#define __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_I

#include <quex/code_base/asserts>
#include <quex/code_base/buffer/asserts>
#include <quex/code_base/definitions>
#include <quex/code_base/buffer/Buffer>
#include <quex/code_base/buffer/Buffer_print.i>
#include <quex/code_base/buffer/lexatoms/LexatomLoader>
#include <quex/code_base/MemoryManager>

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE void*     QUEX_NAME(Buffer_fill)(QUEX_NAME(Buffer)*  me, 
                                             const void*         ContentBegin,
                                             const void*         ContentEnd);
QUEX_INLINE void      QUEX_NAME(Buffer_fill_prepare)(QUEX_NAME(Buffer)*  me, 
                                                     void**              begin_p, 
                                                     const void**        end_p);
QUEX_INLINE void      QUEX_NAME(Buffer_fill_finish)(QUEX_NAME(Buffer)* me,
                                                    const void*        FilledEndP);
QUEX_INLINE bool      QUEX_NAME(Buffer_is_end_of_stream_inside)(QUEX_NAME(Buffer)* me);
QUEX_INLINE void      QUEX_NAME(Buffer_init_content)(QUEX_NAME(Buffer)* me, 
                                                     QUEX_TYPE_LEXATOM* EndOfFileP);
QUEX_INLINE void      QUEX_NAME(Buffer_init_analyzis)(QUEX_NAME(Buffer)*   me);

QUEX_INLINE void      QUEX_NAME(Buffer_on_overflow_DEFAULT)(void*              aux, 
                                                            QUEX_NAME(Buffer)* buffer, 
                                                            bool               ForwardF);
QUEX_INLINE void      QUEX_NAME(Buffer_on_before_buffer_change_DEFAULT)(void*  aux,
                                                                        const  QUEX_TYPE_LEXATOM*, 
                                                                        const  QUEX_TYPE_LEXATOM*);
QUEX_INLINE ptrdiff_t QUEX_NAME(Buffer_move_to_get_free_space_at_end)(QUEX_NAME(Buffer)* me);

QUEX_INLINE void
QUEX_NAME(Buffer_construct)(QUEX_NAME(Buffer)*        me, 
                            QUEX_NAME(LexatomLoader)* filler,
                            QUEX_TYPE_LEXATOM*        memory,
                            const size_t              MemorySize,
                            QUEX_TYPE_LEXATOM*        EndOfFileP,
                            E_Ownership               Ownership)
{
    /* Ownership of InputMemory is passed to 'me->_memory'.                  */
    QUEX_NAME(BufferMemory_construct)(&me->_memory, memory, MemorySize, 
                                      Ownership); 
    
    /* By setting begin and end to zero, we indicate to the loader that      
     * this is the very first load procedure.                                */
    me->filler       = filler;
    me->fill         = QUEX_NAME(Buffer_fill);
    me->fill_prepare = QUEX_NAME(Buffer_fill_prepare);
    me->fill_finish  = QUEX_NAME(Buffer_fill_finish);

    /* Event handlers.                                                       */
    QUEX_NAME(Buffer_set_event_handlers)(me, 
        (void (*)(void*, const QUEX_TYPE_LEXATOM*, const QUEX_TYPE_LEXATOM*))0,
        (void (*)(void*, QUEX_NAME(Buffer)*, bool))0,
        (void*)0);

    /* Initialize.                                                           */
    QUEX_NAME(Buffer_init)(me, EndOfFileP);

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);
}

QUEX_INLINE void
QUEX_NAME(Buffer_init)(QUEX_NAME(Buffer)* me, QUEX_TYPE_LEXATOM* EndOfFileP)
{
    QUEX_NAME(Buffer_init_content)(me, EndOfFileP);
    QUEX_NAME(Buffer_init_analyzis)(me); 
}

QUEX_INLINE void
QUEX_NAME(Buffer_destruct)(QUEX_NAME(Buffer)* me)
/* Destruct 'me' and mark all resources as absent.                            */
{
    if( me->filler ) {
        me->filler->delete_self(me->filler); 
    }
    me->filler = (QUEX_NAME(LexatomLoader)*)0;
    QUEX_NAME(BufferMemory_destruct)(&me->_memory);

    QUEX_NAME(Buffer_resources_absent_mark)(me);
}

QUEX_INLINE void  
QUEX_NAME(Buffer_set_event_handlers)(QUEX_NAME(Buffer)* me,
                                     void   (*on_before_change)(void* aux,
                                                                const QUEX_TYPE_LEXATOM*  BeginP,
                                                                const QUEX_TYPE_LEXATOM*  EndP),
                                     void   (*on_overflow)(void*  aux,
                                                           struct QUEX_NAME(Buffer_tag)*, 
                                                           bool   ForwardF),
                                     void*  aux)
{
    me->event.on_buffer_before_change = on_before_change;
    me->event.on_buffer_overflow      = on_overflow;
    me->event.aux                     = aux;
}

QUEX_INLINE bool
QUEX_NAME(Buffer_construct_included)(QUEX_NAME(Buffer)*        including,
                                     QUEX_NAME(Buffer)*        included,
                                     QUEX_NAME(LexatomLoader)* filler)
/* Construct 'included' buffer (-> memory split):
 *
 * Constructor takes over ownership over 'filler'. If construction fails,
 * the 'filler' is immediatedly deleted.
 *
 * To optimize memory usage and minimize the generation of new buffers in 
 * situations of extensive file inclusions, the current buffer's memory may
 * be split to generate the included buffer's memory.
 *
 *                 including  .---------------------.
 *                 buffer     |0|a|b|c|d|0| | | | | |
 *                            '---------------------'
 *                   read_p -------'     |
 *                   end_p  -------------'
 *
 *                              /    split      \
 *                             /                 \
 *                                  
 *        including  .-----------.     included .---------.
 *        buffer     |0|a|b|c|d|0|  +  buffer   | | | | | |
 *                   '-----------'              '---------'
 *          read_p -------'     |
 *          end_p  -------------'
 *
 * NOTE: Loaded content is NEVER overwritten or split. This is a precaution
 *       for situations where byte loaders may not be able to reload content
 *       that has already been loaded (for example 'TCP socket' byte loaders).
 *
 * RETURNS: true,  if memory has been allocated and the 'included' buffer is
 *                 ready to rumble.
 *          false, if memory allocation failed. 'included' buffer is not 
 *                 functional.
 *                                                                            */
{
    /*         front           read_p      end_p                 back
     *           |               |           |                   |
     *          .-------------------------------------------------.
     *          |0|-|-|-|-|-|-|-|a|b|c|d|e|f|0| | | | | | | | | | |
     *          '-------------------------------------------------'
     *                                         :                 :
     *                                         '--- available ---'
     *                                                                        */
    ptrdiff_t                 available_size =   including->_memory._back 
                                               - including->input.end_p;
    QUEX_TYPE_LEXATOM*        memory;
    size_t                    memory_size;
    E_Ownership               ownership;

    if( QUEX_NAME(Buffer_resources_absent)(including) ) {
        if( filler ) {
            filler->delete_self(filler); 
        }
        QUEX_NAME(Buffer_resources_absent_mark)(included);
        return false;
    }
    else if( available_size < (ptrdiff_t)(QUEX_SETTING_BUFFER_INCLUDE_MIN_SIZE) ) {
        /* (1) AVAILABLE SIZE too SMALL
         *     => Try to move content, so that free space becomes available.  */                    
        available_size = QUEX_NAME(Buffer_move_to_get_free_space_at_end)(including);
    }

    if( available_size < (ptrdiff_t)(QUEX_SETTING_BUFFER_INCLUDE_MIN_SIZE) ) {
        /* (2) AVAILABLE SIZE still too SMALL
         *     => Allocate new memory for new buffer.                         */                    
        memory_size = (size_t)(QUEX_SETTING_BUFFER_SIZE);
        memory      = (QUEX_TYPE_LEXATOM*)QUEXED(MemoryManager_allocate)(
                                memory_size * sizeof(QUEX_TYPE_LEXATOM), 
                                E_MemoryObjectType_BUFFER_MEMORY);
        if( ! memory ) {
            if( filler ) {
                filler->delete_self(filler); 
            }
            QUEX_NAME(Buffer_resources_absent_mark)(included);
            return false;
        }
        ownership = E_Ownership_LEXICAL_ANALYZER;
    }
    else {
        /* (2) AVAILABLE SIZE in including buffer sufficient
         *     => Use free space for new buffer.                              */                    
        memory                   = &including->input.end_p[1];
        memory_size              = (size_t)(&including->_memory._back[1] - memory);
        including->_memory._back = &including->input.end_p[0];
        __quex_assert(memory);
        ownership = E_Ownership_INCLUDING_BUFFER;
    }

    QUEX_NAME(Buffer_construct)(included, filler, memory, memory_size, 
                                (QUEX_TYPE_LEXATOM*)0, ownership);
    QUEX_BUFFER_ASSERT_CONSISTENCY(included);
    QUEX_BUFFER_ASSERT_CONSISTENCY(including);
    return true;
}

QUEX_INLINE void
QUEX_NAME(Buffer_destruct_included)(QUEX_NAME(Buffer)* including,
                                    QUEX_NAME(Buffer)* included)
{
    if( included->_memory.ownership == E_Ownership_INCLUDING_BUFFER ) {
        __quex_assert(&included->_memory._front[0] == &including->_memory._back[1]);
        including->_memory._back = included->_memory._back;
    }
    /* Destructor only frees memory, if ownership is 'LEXICAL_ANALYZER'.      */
    QUEX_NAME(Buffer_destruct)(included);
}

QUEX_INLINE void
QUEX_NAME(Buffer_resources_absent_mark)(QUEX_NAME(Buffer)* me)
{
    __QUEX_STD_memset((void*)me, 0, sizeof(QUEX_NAME(Buffer)));
}

QUEX_INLINE bool    
QUEX_NAME(Buffer_resources_absent)(QUEX_NAME(Buffer)* me)
{
    return    me->filler == (QUEX_NAME(LexatomLoader)*)0 
           && QUEX_NAME(BufferMemory_resources_absent)(&me->_memory);
}

QUEX_INLINE void
QUEX_NAME(Buffer_init_analyzis)(QUEX_NAME(Buffer)*   me) 
/* Initialize:  _read_p                          
 *              _lexeme_start_p                 
 *              _lexatom_at_lexeme_start     
 *              _lexatom_before_lexeme_start                                 */
{
    QUEX_TYPE_LEXATOM*  BeginP = &me->_memory._front[1];

    if( ! me->_memory._front ) {
        /* No memory => FSM is put into a non-functional state.         */
        me->_read_p                      = (QUEX_TYPE_LEXATOM*)0;
        me->_lexeme_start_p              = (QUEX_TYPE_LEXATOM*)0;
        me->_lexatom_at_lexeme_start     = (QUEX_TYPE_LEXATOM)0;                                   
#       ifdef  __QUEX_OPTION_SUPPORT_BEGIN_OF_LINE_PRE_CONDITION                 
        me->_lexatom_before_lexeme_start = (QUEX_TYPE_LEXATOM)0;
#       endif
    }
    else {
        /* The first state in the state machine does not increment. 
         * => input pointer is set to the first position, not before.        */
        me->_read_p                      = BeginP;                                
        me->_lexeme_start_p              = BeginP;                                
        me->_lexatom_at_lexeme_start     = '\0';  /* Nothing covered. */
#       ifdef  __QUEX_OPTION_SUPPORT_BEGIN_OF_LINE_PRE_CONDITION                     
        /* When the buffer is initialized, a line begins. Set 'newline'.     */
        me->_lexatom_before_lexeme_start = QUEX_SETTING_CHARACTER_NEWLINE_IN_ENGINE_CODEC;
#       endif
    }
}

QUEX_INLINE void
QUEX_NAME(Buffer_init_content)(QUEX_NAME(Buffer)* me, QUEX_TYPE_LEXATOM* EndOfFileP)
/*  Initialize: input.lexatom_index_begin
 *              input.lexatom_index_end_of_stream                         
 *              input.end_p                                                  */
{
    QUEX_TYPE_LEXATOM*        BeginP           = &me->_memory._front[1];
    QUEX_TYPE_LEXATOM*        EndP             = me->_memory._back;
    QUEX_TYPE_STREAM_POSITION ci_begin         = (QUEX_TYPE_STREAM_POSITION)0;
    QUEX_TYPE_STREAM_POSITION ci_end_of_stream = (QUEX_TYPE_STREAM_POSITION)-1;
    QUEX_TYPE_LEXATOM*        end_p            = (QUEX_TYPE_LEXATOM*)0;
    (void)EndP;

    if( ! me->_memory._front ) {
        ci_end_of_stream = (QUEX_TYPE_STREAM_POSITION)-1;
        end_p            = (QUEX_TYPE_LEXATOM*)0;
        ci_begin         = (QUEX_TYPE_STREAM_POSITION)-1;
    }
    else if( me->filler && me->filler->byte_loader ) {
        __quex_assert(! EndOfFileP);

#       if 0
        loaded_n         = QUEX_NAME(LexatomLoader_load)(me->filler, BeginP, ContentSize,
                                                         0, &end_of_stream_f, &encoding_error_f);
        ci_end_of_stream = ((! loaded_n) || end_of_stream_f) ? loaded_n 
                                                             : (QUEX_TYPE_STREAM_POSITION)-1;
        end_p            = &BeginP[loaded_n];
#       endif
        /* Setup condition to initiate immediate load when the state machine
         * is entered: 'read pointer hits buffer limit code'.                */
        ci_begin         = (QUEX_TYPE_STREAM_POSITION)0;
        ci_end_of_stream = (QUEX_TYPE_STREAM_POSITION)-1;
        end_p            = &BeginP[0];
    } 
    else {
        __quex_assert(me->_memory._front);           /* See first condition. */
        __quex_assert(! EndOfFileP || (EndOfFileP >= BeginP && EndOfFileP <= EndP));

        if( EndOfFileP ) {
            ci_end_of_stream = EndOfFileP - BeginP;
            end_p            = EndOfFileP;   
        }
        else {
            ci_end_of_stream = (QUEX_TYPE_STREAM_POSITION)-1;
            end_p            = BeginP;   
        }
    }
    me->input.lexatom_index_begin         = ci_begin;
    me->input.lexatom_index_end_of_stream = ci_end_of_stream;
    me->input.end_p                       = end_p;
    if( me->input.end_p ) {
        *(me->input.end_p)                = QUEX_SETTING_BUFFER_LIMIT_CODE;
    }

    QUEX_IF_ASSERTS_poison(&me->input.end_p[1], me->_memory._back);
}

QUEX_INLINE void
QUEX_NAME(Buffer_register_content)(QUEX_NAME(Buffer)*        me,
                                   QUEX_TYPE_LEXATOM*        EndOfInputP,
                                   QUEX_TYPE_STREAM_POSITION CharacterIndexBegin)
/* Registers information about the stream that fills the buffer and its
 * relation to the buffer. 
 *  
 *  EndOfInputP --> Position behind the last lexatom in the buffer that has
 *                  been streamed.
 *          '0' --> No change.
 *  
 *  CharacterIndexBegin --> Character index of the first lexatom in the 
 *                          buffer.
 *                 '-1' --> No change.                                       */
{
    if( EndOfInputP ) {
        __quex_assert(EndOfInputP <= me->_memory._back);
        __quex_assert(EndOfInputP >  me->_memory._front);

        me->input.end_p    = EndOfInputP;
        *(me->input.end_p) = QUEX_SETTING_BUFFER_LIMIT_CODE;
    }

    if( CharacterIndexBegin != (QUEX_TYPE_STREAM_POSITION)-1 ) {
        me->input.lexatom_index_begin = CharacterIndexBegin;
    }

    QUEX_IF_ASSERTS_poison(&me->input.end_p[1], me->_memory._back);
    /* NOT: assert(QUEX_NAME(Buffer_input_lexatom_index_begin)(me) >= 0);
     * This function may be called before content is setup/loaded propperly. */ 
}

QUEX_INLINE void       
QUEX_NAME(Buffer_register_eos)(QUEX_NAME(Buffer)*        me,
                               QUEX_TYPE_STREAM_POSITION CharacterIndexEndOfStream)
{
    me->input.lexatom_index_end_of_stream = CharacterIndexEndOfStream;
}

QUEX_INLINE bool
QUEX_NAME(Buffer_is_empty)(QUEX_NAME(Buffer)* me)
/* RETURNS: true, if buffer does not contain anything.
 *          false, else.                                                     */
{ 
    return    me->input.end_p == &me->_memory._front[1] 
           && me->input.lexatom_index_begin == 0; 
}

QUEX_INLINE QUEX_TYPE_STREAM_POSITION  
QUEX_NAME(Buffer_input_lexatom_index_end)(QUEX_NAME(Buffer)* me)
/* RETURNS: Character index of the lexatom to which '.input.end_p' points.
 *                                                                           */
{
    __quex_assert(me->input.lexatom_index_begin >= 0);
    QUEX_BUFFER_ASSERT_pointers_in_range(me);

    return   me->input.lexatom_index_begin 
           + (me->input.end_p - &me->_memory._front[1]);
}

QUEX_INLINE void
QUEX_NAME(Buffer_read_p_add_offset)(QUEX_NAME(Buffer)* buffer, const size_t Offset)
/* Add offset to '._read_p'. No check applies whether this is admissible.
 *                                                                           */
{ 
    QUEX_BUFFER_ASSERT_pointers_in_range(buffer);
    buffer->_read_p += Offset; 
    QUEX_BUFFER_ASSERT_pointers_in_range(buffer);
}

QUEX_INLINE size_t
QUEX_NAME(Buffer_content_size)(QUEX_NAME(Buffer)* me)
{
    return QUEX_NAME(BufferMemory_size)(&(me->_memory)) - 2;
}

QUEX_INLINE bool 
QUEX_NAME(Buffer_is_end_of_stream_inside)(QUEX_NAME(Buffer)* me)
{ 
    const ptrdiff_t ContentSize = (ptrdiff_t)QUEX_NAME(Buffer_content_size)(me);

    if( me->input.lexatom_index_end_of_stream == (QUEX_TYPE_STREAM_POSITION)-1 ) {
        return false;
    }
    else if( me->input.lexatom_index_end_of_stream < me->input.lexatom_index_begin ) {
        return false;
    }
    
    return me->input.lexatom_index_end_of_stream - me->input.lexatom_index_begin < ContentSize;
}

QUEX_INLINE bool 
QUEX_NAME(Buffer_is_end_of_stream)(QUEX_NAME(Buffer)* me)
{ 
    QUEX_BUFFER_ASSERT_CONSISTENCY(me);
    if( me->input.lexatom_index_end_of_stream == (QUEX_TYPE_STREAM_POSITION)-1 ) {
        return false;
    }
    else if( me->_read_p != me->input.end_p ) {
        return false;
    }

    return    QUEX_NAME(Buffer_input_lexatom_index_end)(me) 
           == me->input.lexatom_index_end_of_stream;
}

QUEX_INLINE bool                  
QUEX_NAME(Buffer_is_begin_of_stream)(QUEX_NAME(Buffer)* buffer)
{ 
    QUEX_BUFFER_ASSERT_CONSISTENCY(buffer);
    if     ( buffer->_lexeme_start_p != &buffer->_memory._front[1] ) return false;
    else if( QUEX_NAME(Buffer_input_lexatom_index_begin)(buffer) )   return false;
    else                                                             return true;
}

QUEX_NAMESPACE_MAIN_CLOSE

#include <quex/code_base/buffer/lexatoms/LexatomLoader.i>
#include <quex/code_base/buffer/Buffer_print.i>
#include <quex/code_base/buffer/Buffer_navigation.i>
#include <quex/code_base/buffer/Buffer_fill.i>
#include <quex/code_base/buffer/Buffer_load.i>
#include <quex/code_base/buffer/Buffer_move.i>
#include <quex/code_base/buffer/BufferMemory.i>

#endif /* __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_I */
