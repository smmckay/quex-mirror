/* vim:set ft=c: -*- C++ -*- */
#ifndef __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_NESTING_I
#define __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_NESTING_I

#include <quex/code_base/asserts>
#include <quex/code_base/buffer/asserts>
#include <quex/code_base/definitions>
#include <quex/code_base/buffer/Buffer>
#include <quex/code_base/buffer/Buffer_print.i>
#include <quex/code_base/buffer/lexatoms/LexatomLoader>
#include <quex/code_base/MemoryManager>

QUEX_NAMESPACE_MAIN_OPEN

#if 1 
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
    ptrdiff_t           available_size =   including->_memory._back 
                                         - including->input.end_p;
    QUEX_TYPE_LEXATOM*  memory;
    size_t              memory_size;
    E_Ownership         ownership;
    QUEX_NAME(Buffer)*  including_buffer_p = (QUEX_NAME(Buffer)*)0;

    QUEX_BUFFER_ASSERT_CONSISTENCY(including);

    if( QUEX_NAME(Buffer_resources_absent)(including) ) {
        goto ERROR_0;
    }
    else if( available_size < (ptrdiff_t)(QUEX_SETTING_BUFFER_SIZE_MIN) ) {
        /* (1) AVAILABLE SIZE too SMALL
         *     => Try to move content, so that free space becomes available.  */                    
        available_size = QUEX_NAME(Buffer_load_prepare_forward_tricky)(including);
    }


    if( available_size < (ptrdiff_t)(QUEX_SETTING_BUFFER_SIZE_MIN) ) {
        /* (2) AVAILABLE SIZE still too SMALL
         *     => Allocate new memory for new buffer.                         */                    
        memory_size = (size_t)(QUEX_SETTING_BUFFER_SIZE);
        memory      = (QUEX_TYPE_LEXATOM*)QUEXED(MemoryManager_allocate)(
                                memory_size * sizeof(QUEX_TYPE_LEXATOM), 
                                E_MemoryObjectType_BUFFER_MEMORY);
        if( ! memory ) {
            goto ERROR_0;
        }
        ownership          = E_Ownership_LEXICAL_ANALYZER;
        including_buffer_p = (QUEX_NAME(Buffer)*)0;
    }
    else {
        /* (2) AVAILABLE SIZE in including buffer sufficient
         *     => Use free space for new buffer.                              */                    
        memory      = &including->input.end_p[1];
        memory_size = (size_t)available_size;
        __quex_assert(0           != memory);
        __quex_assert(memory_size == (size_t)(&including->_memory._back[1] - memory));

        including->_memory._back = &including->input.end_p[0];
        ownership          = E_Ownership_INCLUDING_BUFFER;
        including_buffer_p = including;
    }

    QUEX_NAME(Buffer_construct)(included, filler, memory, memory_size, 
                                (QUEX_TYPE_LEXATOM*)0, ownership, 
                                including_buffer_p);
    
    included->event = including->event;               /* Plain copy suffices. */

    QUEX_BUFFER_ASSERT_CONSISTENCY(included);
    QUEX_BUFFER_ASSERT_CONSISTENCY(including);
    return true;

ERROR_0:
    if( filler ) {
        filler->delete_self(filler); 
    }
    QUEX_NAME(Buffer_resources_absent_mark)(included);
    return false;
}

#else
QUEX_INLINE bool
QUEX_NAME(Buffer_construct_included)(QUEX_NAME(Buffer)*        me,
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
    ptrdiff_t           available_size = me->_memory._back - me->input.end_p;
    QUEX_TYPE_LEXATOM*  memory;
    size_t              memory_size;
    E_Ownership         ownership;
    QUEX_NAME(Buffer)*  including_buffer_p = (QUEX_NAME(Buffer)*)0;

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    if( QUEX_NAME(Buffer_resources_absent)(me) ) {
        goto ERROR_0;
    }
    else if( available_size > (ptrdiff_t)4 ) {
        ownership          = E_Ownership_INCLUDING_BUFFER;
        including_buffer_p = me;
    }
    else if( QUEX_NAME(Buffer_load_prepare_forward_tricky)(me) > (ptrdiff_t)QUEX_SETTING_BUFFER_SIZE_MIN ) {
        ownership          = E_Ownership_INCLUDING_BUFFER;
        including_buffer_p = me;
    }
    else if( QUEX_NAME(Buffer_negotiate_allocate_memory)((size_t)QUEX_SETTING_BUFFER_SIZE, 
                                                         &memory, &memory_size) ) {
        ownership          = E_Ownership_LEXICAL_ANALYZER;
        including_buffer_p = (QUEX_NAME(Buffer)*)0;
    }
    else {
        goto ERROR_0;
    }

    if( ownership == E_Ownership_INCLUDING_BUFFER ) {
        memory                   = &me->input.end_p[1];
        memory_size              = (size_t)(&me->_memory._back[1] - memory);
        me->_memory._back = &me->input.end_p[0];
    }
    else {
        /* 'memory' and 'memory_size' have been set by called function.       */
    }

    QUEX_NAME(Buffer_construct)(included, filler, memory, memory_size, 
                                (QUEX_TYPE_LEXATOM*)0, ownership, 
                                including_buffer_p);
    
    included->event = me->event;                      /* Plain copy suffices. */

    QUEX_BUFFER_ASSERT_CONSISTENCY(included);
    QUEX_BUFFER_ASSERT_CONSISTENCY(me);
    return true;

ERROR_0:
    if( filler ) {
        filler->delete_self(filler); 
    }
    QUEX_NAME(Buffer_resources_absent_mark)(included);
    return false;
}
#endif
    
QUEX_INLINE bool
QUEX_NAME(Buffer_negotiate_extend_root)(QUEX_NAME(Buffer)*  me, 
                                        float               Factor)
/* Attempt to resize the current buffer to a size 's = Factor * current size'.
 * If that fails, try to access memory that of a sizes in between the 's' and 
 * the current sizes, i.e. 's = (s + current_size) / 2'. This is repeated until
 * either memory can be allocated or 's == current_size'. The latter indicates
 * failure. 
 *
 * RETURNS: true, in case if a chunk of size 's' with 
 *                'current_size < s <= Factor*current sizes'
 *                could be found.
 *          false, else.                                                      */
{
    QUEX_NAME(Buffer)*  root         = QUEX_NAME(Buffer_find_root)(me);
    ptrdiff_t           current_size = &me->_memory._back[1] - root->_memory._front;
    /* Refuse negotiations where the requested amount of memory is greater
     * than the total addressable space divided by 16.
     * Addressable space = PTRDIFF_MAX * 2 => Max. size = PTRDIFF_MAX / 8     */
    const ptrdiff_t     MaxSize      = PTRDIFF_MAX >> 3;
    const ptrdiff_t     MinSize      = 4;
    ptrdiff_t           new_size     = (ptrdiff_t)((float)(QUEX_MAX(MinSize, QUEX_MIN(MaxSize, current_size))) * Factor);

    while( ! QUEX_NAME(Buffer_extend_root)(me, new_size - current_size) ) {
        new_size = (current_size + new_size) >> 1;
        if( new_size <= current_size ) {
            return false;
        }
    }
    return true;
}

QUEX_INLINE bool
QUEX_NAME(Buffer_extend_root)(QUEX_NAME(Buffer)*  me, ptrdiff_t  SizeAdd)
/* Allocates a chunk of memory that is 'SizeAdd' greater than the current size.
 * If 'SizeAdd' is negative a smaller chunk is allocated. However, if the 
 * resulting size is insufficient to hold the buffer's content, the function
 * refuses to operate. 
 *
 * The new chunk is allocated with 'E_Ownership_LEXICAL_ANALYZER', such that 
 * the memory is de-allocated upon destruction.
 *
 * RETURNS: true, in case of success.
 *          false, else.                                                      */
{
    QUEX_TYPE_LEXATOM*  old_memory_root_p;
    QUEX_TYPE_LEXATOM*  new_memory_root_p;
    size_t              required_size;
    size_t              new_size;
    QUEX_NAME(Buffer)*  root = me;
    QUEX_TYPE_LEXATOM*  old_content_end_p = me->input.end_p ? me->input.end_p : me->_memory._back;
    
    /* The 'Buffer_extend()' function cannot be called for an buffer which is
     * currently including, i.e. has dependent buffers! It can only be called
     * for the currently working buffer.                                      */
    root              = QUEX_NAME(Buffer_find_root)(me);
    old_memory_root_p = root->_memory._front;
    required_size     = (size_t)(old_content_end_p - old_memory_root_p);
    new_size          = (size_t)(&me->_memory._back[1] - old_memory_root_p + SizeAdd);

    if( SizeAdd <= 0 ) {
        return false;
    }
    else if( required_size >= new_size ) {
        return false;
    }

    new_memory_root_p = (QUEX_TYPE_LEXATOM*)QUEXED(MemoryManager_reallocate)(
                                                (void*)old_memory_root_p,
                                                sizeof(QUEX_TYPE_LEXATOM) * new_size,
                                                E_MemoryObjectType_BUFFER_MEMORY);

    if( ! new_memory_root_p ) {
        /* Old memory object IS NOT DE-ALLOCATED.                             */
        return false;
    }
    else if( new_memory_root_p == old_memory_root_p ) {
        /* Old memory object IS NOT REPLACED--CONTENT AT SAME ADDRESS.        */
        me->_memory._back = &new_memory_root_p[new_size-1];
        return true;
    }

    QUEX_NAME(Buffer_adapt_to_new_memory_location_root)(me, 
                                                        old_memory_root_p,
                                                        new_memory_root_p, 
                                                        new_size);

    root->_memory.ownership = E_Ownership_LEXICAL_ANALYZER;
    return true;
}

QUEX_INLINE bool
QUEX_NAME(Buffer_migrate_root)(QUEX_NAME(Buffer)*  me,
                               QUEX_TYPE_LEXATOM*  memory,
                               const size_t        MemoryLexatomN,
                               E_Ownership         Ownership) 
/* Migrate the content of the current buffer to a new memory space. In case
 * that the buffer is nested in an including buffer, the root of all included
 * buffers is moved. 
 *
 * The new memory *might* be smaller than the current memory, as long as the
 * content itself is less or equal the size of the newly provided memory.
 *
 * If this function fails, the caller is responsible for the de-allocation of
 * the memory.
 *
 * RETURNS: true, if migration was successful.
 *          false, if newly allocated memory is too small.                    */
{
    size_t             required_size;
    QUEX_NAME(Buffer)* root;
    QUEX_TYPE_LEXATOM* old_memory_root_p;
    QUEX_TYPE_LEXATOM* old_content_end_p = me->input.end_p ? me->input.end_p : me->_memory._back;
    size_t             copy_size;

    __quex_assert(old_content_end_p >= me->_memory._front);
    __quex_assert(old_content_end_p <= me->_memory._back);

    root              = QUEX_NAME(Buffer_find_root)(me);
    old_memory_root_p = root->_memory._front;
    required_size     = (size_t)(old_content_end_p - old_memory_root_p);

    if( required_size > MemoryLexatomN ) {
        return false;
    }

    /* Copy content to the new habitat.                                       */
    copy_size = old_content_end_p <= old_memory_root_p ? 
                (size_t)0 : (size_t)(old_content_end_p - &old_memory_root_p[1]);
    __QUEX_STD_memcpy((void*)&memory[1], 
                      (void*)&old_memory_root_p[1],
                      copy_size * sizeof(QUEX_TYPE_LEXATOM));

    /* Adapt this and all nesting buffers to new memory location.             */
    QUEX_NAME(Buffer_adapt_to_new_memory_location_root)(me, old_memory_root_p,
                                                        &memory[0], MemoryLexatomN);

    if( root->_memory.ownership == E_Ownership_LEXICAL_ANALYZER ) {
        QUEXED(MemoryManager_free)(old_memory_root_p, E_MemoryObjectType_BUFFER_MEMORY);
    }
    root->_memory.ownership = Ownership;

    return true;
}

QUEX_INLINE QUEX_NAME(Buffer)*
QUEX_NAME(Buffer_find_root)(QUEX_NAME(Buffer)* me)
/* A buffer may be nested in an including buffer. This function walks down
 * the path of nesting until the root of all including buffers is found.
 *
 * RETURNS: Pointer to root buffer object.                                */
{
    QUEX_NAME(Buffer)* focus = me;
    for(; focus->_memory.including_buffer; 
        focus = focus->_memory.including_buffer) {
        __quex_assert(focus->_memory.ownership == E_Ownership_INCLUDING_BUFFER);
    }
    __quex_assert(focus->_memory.ownership != E_Ownership_INCLUDING_BUFFER);
    return focus;
}

QUEX_INLINE void
QUEX_NAME(Buffer_adapt_to_new_memory_location_root)(QUEX_NAME(Buffer)* me,
                                                    QUEX_TYPE_LEXATOM* old_memory_root,
                                                    QUEX_TYPE_LEXATOM* new_memory_root,
                                                    size_t             NewRootSize)
{
    QUEX_NAME(Buffer)* focus;
    QUEX_TYPE_LEXATOM* new_memory;
    size_t             new_size;

    /* Adapt this and all nesting buffers to new memory location.             */
    for(focus = me; focus ; focus = focus->_memory.including_buffer) {

        QUEX_NAME(Buffer_call_on_buffer_before_change)(focus);

        new_memory = &new_memory_root[focus->_memory._front - old_memory_root];
        new_size   = (size_t)(&focus->_memory._back[1]      - focus->_memory._front);
        QUEX_NAME(Buffer_adapt_to_new_memory_location)(focus, new_memory, new_size);
    }

    me->_memory._back = &new_memory_root[NewRootSize - 1];
}

QUEX_INLINE void
QUEX_NAME(Buffer_adapt_to_new_memory_location)(QUEX_NAME(Buffer)* me,
                                               QUEX_TYPE_LEXATOM* new_memory_base,
                                               size_t             NewSize)
/* Adapt all content to a new memory base and ownership. 
 *
 * -- This function is not concerned with memory management, etc. everything is
 *    supposed to be setup/destructed previously.
 *
 * -- This function does not consider the buffer nesting. It solely treats 
 *    the memory of 'me' itself.
 *
 * -- It is assumed, that new memory has the SAME size as the current.
 *                                                                            */
{
    ptrdiff_t  offset_end_p          = me->input.end_p     - me->_memory._front;
    ptrdiff_t  offset_read_p         = me->_read_p         - me->_memory._front;
    ptrdiff_t  offset_lexeme_start_p = me->_lexeme_start_p - me->_memory._front;

    __quex_assert(   (0                            != me->_memory.including_buffer) 
                  == (E_Ownership_INCLUDING_BUFFER == me->_memory.ownership));

    QUEX_NAME(BufferMemory_construct)(&me->_memory, new_memory_base, NewSize,
                                      me->_memory.ownership, me->_memory.including_buffer); 

    QUEX_NAME(Buffer_init_content_core)(me, 
                                        me->input.lexatom_index_begin,
                                        me->input.lexatom_index_end_of_stream,
                                        &new_memory_base[offset_end_p]);
    QUEX_NAME(Buffer_init_analyzis_core)(me, 
    /* ReadP                          */ &new_memory_base[offset_read_p],
    /* LexatomStartP                  */ &new_memory_base[offset_lexeme_start_p],
    /* LexatomAtLexemeStart           */ me->_lexatom_at_lexeme_start,
#   ifdef  __QUEX_OPTION_SUPPORT_BEGIN_OF_LINE_PRE_CONDITION                 
    /* LexatomBeforeLexemeStart       */ me->_lexatom_before_lexeme_start,
#   else
    /* LexatomBeforeLexemeStart       */ (QUEX_TYPE_LEXATOM)0, /* ignored */
#   endif
    /* BackupLexatomIndexOfReadP      */ me->_backup_lexatom_index_of_read_p);
}

QUEX_INLINE QUEX_NAME(Buffer)* 
QUEX_NAME(Buffer_get_nested)(QUEX_NAME(Buffer)* me, 
                             QUEX_NAME(Buffer)* tail)
/* RETURNS: Buffer which is included by 'me'.
 *          'tail' in case 'me' does not inculude a buffer. 
 *
 * The 'tail' must be provided because only the including buffer is 
 * provided. Finding the nested buffer means going backward until the 
 * buffer's included buffer is equal to 'me'                              */
{
    QUEX_NAME(Buffer)* focus;

    for(focus = tail; focus->_memory.including_buffer != me; 
        focus = focus->_memory.including_buffer) {
        if( ! focus->_memory.including_buffer ) {
            return tail;
        }
    }
    
    /* HERE: 'focus' is directly included by 'me', or 'focus' == tail, 
     *       if it fails.                                                 */
    return focus;
}

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_NESTING_I */
