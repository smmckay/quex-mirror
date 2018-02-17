/* vim: set ft=c:
 * (C) Frank-Rene Schaefer */
#ifndef  __QUEX_INCLUDE_GUARD__BUFFER__BYTES__BYTE_LOADER_LEXATOM_PIPE_I
#define  __QUEX_INCLUDE_GUARD__BUFFER__BYTES__BYTE_LOADER_LEXATOM_PIPE_I

#include <quex/code_base/MemoryManager>

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE void                       QUEX_NAME(ByteLoader_LexatomPipe_construct)(QUEX_NAME(ByteLoader_LexatomPipe)* me, 
                                                                                   __QUEX_STD_LexatomPipe*            fh);
QUEX_INLINE QUEX_TYPE_STREAM_POSITION  QUEX_NAME(ByteLoader_LexatomPipe_tell)(QUEX_NAME(ByteLoader)* me);
QUEX_INLINE void                       QUEX_NAME(ByteLoader_LexatomPipe_seek)(QUEX_NAME(ByteLoader)*    me, 
                                                                              QUEX_TYPE_STREAM_POSITION Pos);
QUEX_INLINE size_t                     QUEX_NAME(ByteLoader_LexatomPipe_load)(QUEX_NAME(ByteLoader)* me, 
                                                                              void*                  buffer, 
                                                                              const size_t           ByteN, 
                                                                              bool*);
QUEX_INLINE void                       QUEX_NAME(ByteLoader_LexatomPipe_delete_self)(QUEX_NAME(ByteLoader)* me);
QUEX_INLINE void                       QUEX_NAME(ByteLoader_LexatomPipe_print_this)(QUEX_NAME(ByteLoader)* me);
QUEX_INLINE bool                       QUEX_NAME(ByteLoader_LexatomPipe_compare_handle)(const QUEX_NAME(ByteLoader)* alter_ego_A, 
                                                                                        const QUEX_NAME(ByteLoader)* alter_ego_B);

QUEX_INLINE QUEX_NAME(ByteLoader)*    
QUEX_NAME(ByteLoader_LexatomPipe_new)(QUEX_NAME(LexatomLoader)* filler)
{
    QUEX_NAME(ByteLoader_LexatomPipe)* me;
   
    if( ! filler ) return (QUEX_NAME(ByteLoader)*)0;

    me = (QUEX_NAME(ByteLoader_LexatomPipe)*)QUEXED(MemoryManager_allocate)(sizeof(QUEX_NAME(ByteLoader_LexatomPipe)),
                                                                     E_MemoryObjectType_BYTE_LOADER);
    if( ! me ) return (QUEX_NAME(ByteLoader)*)0;

    QUEX_NAME(ByteLoader_LexatomPipe_construct)(me, filler);

    return &me->base;
}

QUEX_INLINE void
QUEX_NAME(ByteLoader_LexatomPipe_construct)(QUEX_NAME(ByteLoader_LexatomPipe)* me, 
                                            QUEX_NAME(LexatomLoader)*          filler)
{
    /* IMPORTANT: lexatom_loader must be set BEFORE call to base constructor!
     *            Constructor does call 'tell()'                             */
    me->lexatom_loader = filler;

    QUEX_NAME(ByteLoader_construct)(&me->base,
                         QUEX_NAME(ByteLoader_LexatomPipe_tell),
                         QUEX_NAME(ByteLoader_LexatomPipe_seek),
                         QUEX_NAME(ByteLoader_LexatomPipe_load),
                         QUEX_NAME(ByteLoader_LexatomPipe_delete_self),
                         QUEX_NAME(ByteLoader_LexatomPipe_print_this),
                         QUEX_NAME(ByteLoader_LexatomPipe_compare_handle));
}

QUEX_INLINE void    
QUEX_NAME(ByteLoader_LexatomPipe_delete_self)(QUEX_NAME(ByteLoader)* alter_ego)
{
    QUEX_NAME(ByteLoader_LexatomPipe)* me = (QUEX_NAME(ByteLoader_LexatomPipe)*)(alter_ego);

    if( me->lexatom_loader && me->base.handle_ownership == E_Ownership_LEXICAL_ANALYZER ) {
        me->lexatom_loader->delete_self(me->lexatom_loader);
    }
    QUEXED(MemoryManager_free)(me, E_MemoryObjectType_BYTE_LOADER);
}

QUEX_INLINE QUEX_TYPE_STREAM_POSITION    
QUEX_NAME(ByteLoader_LexatomPipe_tell)(QUEX_NAME(ByteLoader)* alter_ego)            
{ 
    QUEX_NAME(ByteLoader_LexatomPipe)* me = (QUEX_NAME(ByteLoader_LexatomPipe)*)(alter_ego);

    return (QUEX_TYPE_STREAM_POSITION)me->lexatom_loader->tell(me->lexatom_loader); 
}

QUEX_INLINE void    
QUEX_NAME(ByteLoader_LexatomPipe_seek)(QUEX_NAME(ByteLoader)* alter_ego, QUEX_TYPE_STREAM_POSITION Pos) 
{ 
    QUEX_NAME(ByteLoader_LexatomPipe)* me = (QUEX_NAME(ByteLoader_LexatomPipe)*)(alter_ego);
#   if 0
    printf("#seek from: %i to: %i;\n", (int)ftell(me->lexatom_loader), (int)Pos);
#   endif
    me->lexatom_loader->seek(me->lexatom_loader, (long)Pos); 
}

QUEX_INLINE size_t  
QUEX_NAME(ByteLoader_LexatomPipe_load)(QUEX_NAME(ByteLoader)* alter_ego, 
                                void*                  buffer, 
                                const size_t           ByteN, 
                                bool*                  end_of_stream_f) 
{ 
    QUEX_NAME(ByteLoader_LexatomPipe)* me = (QUEX_NAME(ByteLoader_LexatomPipe)*)(alter_ego);
    size_t                             load_request_n;
    size_t                             loaded_n;

    load_request_n = ByteN / sizeof(QUEX_TYPE_LEXATOM);

    loaded_n = QUEX_NAME(LexatomLoader_load)(me->filler, me->input.end_p, 
                                             load_request_n,
                                             load_lexatom_index, &end_of_stream_f,
                                             encoding_error_f);

    return loaded_n * sizeof(QUEX_TYPE_LEXATOM);
}

QUEX_INLINE bool  
QUEX_NAME(ByteLoader_LexatomPipe_compare_handle)(const QUEX_NAME(ByteLoader)* alter_ego_A, 
                                          const QUEX_NAME(ByteLoader)* alter_ego_B) 
/* RETURNS: true  -- if A and B point to the same LexatomPipe object.
 *          false -- else.                                                   */
{ 
    const QUEX_NAME(ByteLoader_LexatomPipe)* A = (QUEX_NAME(ByteLoader_LexatomPipe)*)(alter_ego_A);
    const QUEX_NAME(ByteLoader_LexatomPipe)* B = (QUEX_NAME(ByteLoader_LexatomPipe)*)(alter_ego_B);

    return A->lexatom_loader == B->lexatom_loader;
}

QUEX_INLINE void                       
QUEX_NAME(ByteLoader_LexatomPipe_print_this)(QUEX_NAME(ByteLoader)* alter_ego)
{
    QUEX_NAME(ByteLoader_LexatomPipe)* me = (QUEX_NAME(ByteLoader_LexatomPipe)*)(alter_ego);

    __QUEX_STD_printf("        type:             LexatomPipe;\n");
    __QUEX_STD_printf("        lexatom_loader:   ((%p));\n", (const void*)me->lexatom_loader);
    if( me->lexatom_loader ) {
        __QUEX_STD_printf("        end_of_stream:    %s;\n", E_Boolean_NAME(feof(me->lexatom_loader)));
    }
}

QUEX_NAMESPACE_MAIN_CLOSE

#endif /*    __QUEX_INCLUDE_GUARD__BUFFER__BYTES__BYTE_LOADER_LEXATOM_PIPE_I */
