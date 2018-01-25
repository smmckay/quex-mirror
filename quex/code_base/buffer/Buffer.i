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
QUEX_INLINE void      QUEX_NAME(Buffer_init_content_core)(QUEX_NAME(Buffer)*        me, 
                                                          QUEX_TYPE_STREAM_POSITION LI_Begin,
                                                          QUEX_TYPE_STREAM_POSITION LI_EndOfStream,
                                                          QUEX_TYPE_LEXATOM*        EndOfFileP);
QUEX_INLINE void      QUEX_NAME(Buffer_init_analyzis)(QUEX_NAME(Buffer)*   me);
QUEX_INLINE void      QUEX_NAME(Buffer_init_analyzis_core)(QUEX_NAME(Buffer)*        me,
                                                           QUEX_TYPE_LEXATOM*        ReadP,
                                                           QUEX_TYPE_LEXATOM*        LexatomStartP,
                                                           QUEX_TYPE_LEXATOM         LexatomAtLexemeStart,
                                                           QUEX_TYPE_LEXATOM         LexatomBeforeLexemeStart,
                                                           QUEX_TYPE_STREAM_POSITION BackupLexatomIndexOfReadP);

QUEX_INLINE void      QUEX_NAME(Buffer_on_overflow_DEFAULT)(void*              aux, 
                                                            QUEX_NAME(Buffer)* buffer, 
                                                            bool               ForwardF);
QUEX_INLINE void      QUEX_NAME(Buffer_on_before_buffer_change_DEFAULT)(void*  aux,
                                                                        const  QUEX_TYPE_LEXATOM*, 
                                                                        const  QUEX_TYPE_LEXATOM*);
QUEX_INLINE ptrdiff_t QUEX_NAME(Buffer_load_prepare_forward_tricky)(QUEX_NAME(Buffer)* me);
QUEX_INLINE void      QUEX_NAME(Buffer_adapt_to_new_memory_location_root)(QUEX_NAME(Buffer)* me,
                                                                          QUEX_TYPE_LEXATOM* old_memory_root,
                                                                          QUEX_TYPE_LEXATOM* new_memory_root,
                                                                          size_t             NewRootSize);

QUEX_INLINE void
QUEX_NAME(Buffer_construct)(QUEX_NAME(Buffer)*        me, 
                            QUEX_NAME(LexatomLoader)* filler,
                            QUEX_TYPE_LEXATOM*        memory,
                            const size_t              MemorySize,
                            QUEX_TYPE_LEXATOM*        EndOfFileP,
                            E_Ownership               Ownership,
                            QUEX_NAME(Buffer)*        IncludingBuffer)
{
    /* Ownership of InputMemory is passed to 'me->_memory'.                  */
    QUEX_NAME(BufferMemory_construct)(&me->_memory, memory, MemorySize, 
                                      Ownership, IncludingBuffer); 
    
    /* By setting begin and end to zero, we indicate to the loader that      
     * this is the very first load procedure.                                */
    me->filler       = filler;
    me->fill         = QUEX_NAME(Buffer_fill);
    me->fill_prepare = QUEX_NAME(Buffer_fill_prepare);
    me->fill_finish  = QUEX_NAME(Buffer_fill_finish);

    /* Event handlers.                                                       */
    QUEX_NAME(Buffer_set_event_handlers)(me, (void (*)(void*))0,
                                         (void (*)(void*))0, (void*)0);

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
        if( filler ) {
            filler->delete_self(filler); 
        }
        QUEX_NAME(Buffer_resources_absent_mark)(included);
        return false;
    }
    else if( available_size < (ptrdiff_t)(QUEX_SETTING_BUFFER_INCLUDE_MIN_SIZE) ) {
        /* (1) AVAILABLE SIZE too SMALL
         *     => Try to move content, so that free space becomes available.  */                    
        available_size = QUEX_NAME(Buffer_load_prepare_forward_tricky)(including);
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
        ownership          = E_Ownership_LEXICAL_ANALYZER;
        including_buffer_p = (QUEX_NAME(Buffer)*)0;
    }
    else {
        /* (2) AVAILABLE SIZE in including buffer sufficient
         *     => Use free space for new buffer.                              */                    
        memory                   = &including->input.end_p[1];
        memory_size              = (size_t)(&including->_memory._back[1] - memory);
        including->_memory._back = &including->input.end_p[0];
        __quex_assert(0 != memory);
        ownership          = E_Ownership_INCLUDING_BUFFER;
        including_buffer_p = including;
    }

    QUEX_NAME(Buffer_construct)(included, filler, memory, memory_size, 
                                (QUEX_TYPE_LEXATOM*)0, ownership, 
                                including_buffer_p);

    QUEX_BUFFER_ASSERT_CONSISTENCY(included);
    QUEX_BUFFER_ASSERT_CONSISTENCY(including);
    return true;
}

QUEX_INLINE void
QUEX_NAME(Buffer_destruct)(QUEX_NAME(Buffer)* me)
/* Destruct 'me' and mark all resources as absent.                            */
{
    QUEX_NAME(Buffer_call_on_buffer_before_change)(me);

    if( me->filler ) {
        me->filler->delete_self(me->filler); 
    }
    me->filler = (QUEX_NAME(LexatomLoader)*)0;

    QUEX_NAME(BufferMemory_destruct)(&me->_memory);

    QUEX_NAME(Buffer_resources_absent_mark)(me);
}

QUEX_INLINE void
QUEX_NAME(Buffer_shallow_copy)(QUEX_NAME(Buffer)* drain, const QUEX_NAME(Buffer)* source)
/*    ,.
 *   /  \   DANGER: Do not use this function, except that you totally 
 *  /    \                understand its implications!
 *  '----'
 * Copy indices and references *as is*. The purpose of this function is solely
 * to copy the setup of a buffer to a safe place and restore it. 
 *
 *           NOT TO BE USED AS A REPLACEMENT FOR COPYING/CLONING!
 *
 * At the time of this writing, the only propper application is when a backup 
 * is generated in a memento. When it is restored in the 'real' buffer object 
 * the pointers point to the right places and the ownership is handled propperly.
 *
 * The caller of this function MUST determine whether 'drain' or 'source'
 * maintains ownership.                                                       */
{
    *drain = *source;
}

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
    ptrdiff_t           new_size     = (ptrdiff_t)((float)(QUEX_MIN(current_size, MaxSize)) * Factor);

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
 *              _lexatom_before_lexeme_start                                  */
{
    QUEX_TYPE_LEXATOM*  BeginP = &me->_memory._front[1];

    if( ! me->_memory._front ) {
        /* No memory => FSM is put into a non-functional state.               */
        QUEX_NAME(Buffer_init_analyzis_core)(me, 
        /* ReadP                          */ (QUEX_TYPE_LEXATOM*)0,
        /* LexatomStartP                  */ (QUEX_TYPE_LEXATOM*)0,
        /* LexatomAtLexemeStart           */ (QUEX_TYPE_LEXATOM)0,                                   
        /* LexatomBeforeLexemeStart       */ (QUEX_TYPE_LEXATOM)0,
        /* BackupLexatomIndexOfReadP      */ (QUEX_TYPE_STREAM_POSITION)-1);
    }
    else {
        /* The first state in the state machine does not increment. 
         * => input pointer is set to the first position, not before.         */
        QUEX_NAME(Buffer_init_analyzis_core)(me, 
        /* ReadP                          */ BeginP,
        /* LexatomStartP                  */ BeginP,
        /* LexatomAtLexemeStart           */ (QUEX_TYPE_LEXATOM)0,
        /* LexatomBeforeLexemeStart       */ QUEX_SETTING_CHARACTER_NEWLINE_IN_ENGINE_CODEC,
        /* BackupLexatomIndexOfReadP      */ (QUEX_TYPE_STREAM_POSITION)-1);
    }
}

QUEX_INLINE void
QUEX_NAME(Buffer_init_analyzis_core)(QUEX_NAME(Buffer)*        me,
                                     QUEX_TYPE_LEXATOM*        ReadP,
                                     QUEX_TYPE_LEXATOM*        LexatomStartP,
                                     QUEX_TYPE_LEXATOM         LexatomAtLexemeStart,
                                     QUEX_TYPE_LEXATOM         LexatomBeforeLexemeStart,
                                     QUEX_TYPE_STREAM_POSITION BackupLexatomIndexOfReadP) 
{
    (void)LexatomBeforeLexemeStart;

    me->_read_p                         = ReadP;
    me->_lexeme_start_p                 = LexatomStartP;
    me->_lexatom_at_lexeme_start        = LexatomAtLexemeStart;                                   
#   ifdef  __QUEX_OPTION_SUPPORT_BEGIN_OF_LINE_PRE_CONDITION                 
    me->_lexatom_before_lexeme_start    = LexatomBeforeLexemeStart;
#   endif
    me->_backup_lexatom_index_of_read_p = BackupLexatomIndexOfReadP;
}

QUEX_INLINE void
QUEX_NAME(Buffer_init_content)(QUEX_NAME(Buffer)* me, QUEX_TYPE_LEXATOM* EndOfFileP)
/*  Initialize: input.lexatom_index_begin
 *              input.lexatom_index_end_of_stream                         
 *              input.end_p                                                   */
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
        __quex_assert(0 == EndOfFileP);

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
        __quex_assert(0 != me->_memory._front);           /* See first condition. */
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

    QUEX_NAME(Buffer_init_content_core)(me, ci_begin, ci_end_of_stream, end_p);
}

QUEX_INLINE void
QUEX_NAME(Buffer_init_content_core)(QUEX_NAME(Buffer)* me, 
                                    QUEX_TYPE_STREAM_POSITION LI_Begin,
                                    QUEX_TYPE_STREAM_POSITION LI_EndOfStream,
                                    QUEX_TYPE_LEXATOM*        EndOfFileP)
{
    me->input.lexatom_index_begin         = LI_Begin;
    me->input.lexatom_index_end_of_stream = LI_EndOfStream;
    me->input.end_p                       = EndOfFileP;
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

QUEX_INLINE void  
QUEX_NAME(Buffer_set_event_handlers)(QUEX_NAME(Buffer)* me,
                                     void   (*on_before_change)(void* aux),
                                     void   (*on_overflow)(void*  aux),
                                     void*  aux)
{
    me->event.on_buffer_before_change = on_before_change;
    me->event.on_buffer_overflow      = on_overflow;
    me->event.aux                     = aux;
}

QUEX_INLINE void
QUEX_NAME(Buffer_call_on_buffer_before_change)(QUEX_NAME(Buffer)* me)
{
    if( me->event.on_buffer_before_change ) {
        me->event.on_buffer_before_change(me->event.aux); 
    }
}

QUEX_INLINE void
QUEX_NAME(Buffer_call_on_buffer_overflow)(QUEX_NAME(Buffer)* me)
{
    if( me->event.on_buffer_overflow ) {
        me->event.on_buffer_overflow(me->event.aux);
    }
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
