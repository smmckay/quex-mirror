/* vim: ft=c:
 * (C) Frank-Rene Schaefer */
#ifndef  QUEX_INCLUDE_GUARD_$$LEXER_CLASS$$__BUFFER__BYTES__BYTE_LOADER_POSIX_I
#define  QUEX_INCLUDE_GUARD_$$LEXER_CLASS$$__BUFFER__BYTES__BYTE_LOADER_POSIX_I

$$INC: buffer/bytes/ByteLoader_POSIX$$
$$INC: quex/MemoryManager$$

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE void                       QUEX_NAME(ByteLoader_POSIX_construct)(QUEX_NAME(ByteLoader_POSIX)* me, int fd);
QUEX_INLINE QUEX_TYPE_STREAM_POSITION  QUEX_NAME(ByteLoader_POSIX_tell)(QUEX_NAME(ByteLoader)* me);
QUEX_INLINE void                       QUEX_NAME(ByteLoader_POSIX_seek)(QUEX_NAME(ByteLoader)* me, 
                                                                        QUEX_TYPE_STREAM_POSITION Pos);
QUEX_INLINE size_t                     QUEX_NAME(ByteLoader_POSIX_load)(QUEX_NAME(ByteLoader)* me, 
                                                                        void* buffer, const size_t ByteN, 
                                                                        bool*);
QUEX_INLINE void                       QUEX_NAME(ByteLoader_POSIX_delete_self)(QUEX_NAME(ByteLoader)* me);
QUEX_INLINE void                       QUEX_NAME(ByteLoader_POSIX_print_this)(QUEX_NAME(ByteLoader)* me);
QUEX_INLINE bool                       QUEX_NAME(ByteLoader_POSIX_compare_handle)(const QUEX_NAME(ByteLoader)* alter_ego_A, 
                                                                       const QUEX_NAME(ByteLoader)* alter_ego_B);

QUEX_INLINE QUEX_NAME(ByteLoader)*    
QUEX_NAME(ByteLoader_POSIX_new)(int fd)
{
    QUEX_NAME(ByteLoader_POSIX)* me;

    if( fd == -1 ) return (QUEX_NAME(ByteLoader)*)0;
    me = (QUEX_NAME(ByteLoader_POSIX)*)QUEXED(MemoryManager_allocate)(sizeof(QUEX_NAME(ByteLoader_POSIX)),
                                                           E_MemoryObjectType_BYTE_LOADER);
    if( ! me ) return (QUEX_NAME(ByteLoader)*)0;
    QUEX_NAME(ByteLoader_POSIX_construct)(me, fd);
    return &me->base;
}

QUEX_INLINE QUEX_NAME(ByteLoader)*    
QUEX_NAME(ByteLoader_POSIX_new_from_file_name)(const char* FileName)
{
    QUEX_NAME(ByteLoader)*  alter_ego;
    int                     fd = open(FileName, O_RDONLY);

    if( fd == -1 ) {
        return (QUEX_NAME(ByteLoader)*)0;
    }
    alter_ego = QUEX_NAME(ByteLoader_POSIX_new)(fd);
    if( ! alter_ego ) {
        return (QUEX_NAME(ByteLoader)*)0;
    }

    /* ByteLoader from file name *must* be owned by lexical analyzer, 
     * to ensure automatic closure and deletion.                              */
    alter_ego->handle_ownership = E_Ownership_LEXICAL_ANALYZER;
    return alter_ego;
}

QUEX_INLINE void
QUEX_NAME(ByteLoader_POSIX_construct)(QUEX_NAME(ByteLoader_POSIX)* me, int fd)
{
    /* IMPORTANT: fd must be set BEFORE call to constructor!
     *            Constructor does call 'tell()'                             */
    me->fd = fd;

    QUEX_NAME(ByteLoader_construct)(&me->base,
                                    QUEX_NAME(ByteLoader_POSIX_tell),
                                    QUEX_NAME(ByteLoader_POSIX_seek),
                                    QUEX_NAME(ByteLoader_POSIX_load),
                                    QUEX_NAME(ByteLoader_POSIX_delete_self),
                                    QUEX_NAME(ByteLoader_POSIX_print_this),
                                    QUEX_NAME(ByteLoader_POSIX_compare_handle));

    /* A POSIX file handle is always in binary mode.                         */
    me->base.binary_mode_f = true;
}

QUEX_INLINE void    
QUEX_NAME(ByteLoader_POSIX_delete_self)(QUEX_NAME(ByteLoader)* alter_ego)
{
    QUEX_NAME(ByteLoader_POSIX)* me = (QUEX_NAME(ByteLoader_POSIX)*)(alter_ego);

    if( me->fd && me->base.handle_ownership == E_Ownership_LEXICAL_ANALYZER ) {
        close(me->fd);
    }
    QUEXED(MemoryManager_free)(me, E_MemoryObjectType_BYTE_LOADER);
}

QUEX_INLINE QUEX_TYPE_STREAM_POSITION    
QUEX_NAME(ByteLoader_POSIX_tell)(QUEX_NAME(ByteLoader)* alter_ego)            
{ 
    QUEX_NAME(ByteLoader_POSIX)* me = (QUEX_NAME(ByteLoader_POSIX)*)(alter_ego);
    /* Use 'lseek(current position + 0)' to get the current position.        */
    return (QUEX_TYPE_STREAM_POSITION)lseek(me->fd, 0, SEEK_CUR); 
}

QUEX_INLINE void    
QUEX_NAME(ByteLoader_POSIX_seek)(QUEX_NAME(ByteLoader)*    alter_ego, 
                                 QUEX_TYPE_STREAM_POSITION Pos) 
{ 
    QUEX_NAME(ByteLoader_POSIX)* me = (QUEX_NAME(ByteLoader_POSIX)*)(alter_ego);
    lseek(me->fd, (long)Pos, SEEK_SET); 
}

QUEX_INLINE size_t  
QUEX_NAME(ByteLoader_POSIX_load)(QUEX_NAME(ByteLoader)* alter_ego, 
                                 void*                  buffer, 
                                 const size_t           ByteN, 
                                 bool*                  end_of_stream_f) 
/* The POSIX interface does not allow to detect end of file upon reading.
 * The caller will realize end of stream by a return of zero bytes.          */
{ 
    QUEX_NAME(ByteLoader_POSIX)* me = (QUEX_NAME(ByteLoader_POSIX)*)(alter_ego);
    ssize_t                      n  = read(me->fd, buffer, ByteN); 
    /* Theoretically, a last 'terminating zero' might be send over socket 
     * connections. Make sure, that this does not appear in the stream.      */
    if( n && ((uint8_t*)buffer)[n-1] == 0x0 ) {
        --n;
    }
    *end_of_stream_f = false;
    return (size_t)n;
}

QUEX_INLINE bool  
QUEX_NAME(ByteLoader_POSIX_compare_handle)(const QUEX_NAME(ByteLoader)* alter_ego_A, 
                                           const QUEX_NAME(ByteLoader)* alter_ego_B) 
/* RETURNS: true  -- if A and B point to the same POSIX object.
 *          false -- else.                                                   */
{ 
    const QUEX_NAME(ByteLoader_POSIX)* A = (QUEX_NAME(ByteLoader_POSIX)*)(alter_ego_A);
    const QUEX_NAME(ByteLoader_POSIX)* B = (QUEX_NAME(ByteLoader_POSIX)*)(alter_ego_B);

    return A->fd == B->fd;
}

QUEX_INLINE void                       
QUEX_NAME(ByteLoader_POSIX_print_this)(QUEX_NAME(ByteLoader)* alter_ego)
{
    QUEX_NAME(ByteLoader_POSIX)* me = (QUEX_NAME(ByteLoader_POSIX)*)(alter_ego);

    __QUEX_STD_printf("        type:             POSIX;\n");
    __QUEX_STD_printf("        file_descriptor:  ((%i));\n", (int)me->fd);
    __QUEX_STD_printf("        end_of_stream_f:  <no means to detect>;\n");
}

QUEX_NAMESPACE_MAIN_CLOSE

#endif /*  QUEX_INCLUDE_GUARD_$$LEXER_CLASS$$__BUFFER__BYTES__BYTE_LOADER_POSIX_I */

