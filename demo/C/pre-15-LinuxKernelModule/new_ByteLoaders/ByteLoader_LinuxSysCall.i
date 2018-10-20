/* vim: ft=c:
 * (C) Frank-Rene Schaefer */
#ifndef  QUEX_INCLUDE_GUARD__BUFFER__BYTES__BYTE_LOADER_SYSCALL_I
#define  QUEX_INCLUDE_GUARD__BUFFER__BYTES__BYTE_LOADER_SYSCALL_I

$$INC: buffer/bytes/ByteLoader_LinuxSysCall$$
$$INC: quex/MemoryManager$$
$$INC: definitions$$

#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/module.h>
#include <linux/syscalls.h>
#include <linux/fcntl.h>
#include <asm/uaccess.h>

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE void                       QUEX_NAME(ByteLoader_LinuxSysCall_construct)(QUEX_NAME(ByteLoader_LinuxSysCall)* me, int fd);
QUEX_INLINE QUEX_TYPE_STREAM_POSITION  QUEX_NAME(ByteLoader_LinuxSysCall_tell)(QUEX_NAME(ByteLoader)* me);
QUEX_INLINE void                       QUEX_NAME(ByteLoader_LinuxSysCall_seek)(QUEX_NAME(ByteLoader)* me, 
                                                                               QUEX_TYPE_STREAM_POSITION Pos);
QUEX_INLINE size_t                     QUEX_NAME(ByteLoader_LinuxSysCall_load)(QUEX_NAME(ByteLoader)* me, 
                                                                        void* buffer, const size_t ByteN, 
                                                                        bool*);
QUEX_INLINE void                       QUEX_NAME(ByteLoader_LinuxSysCall_delete_self)(QUEX_NAME(ByteLoader)* me);
QUEX_INLINE void                       QUEX_NAME(ByteLoader_LinuxSysCall_print_this)(QUEX_NAME(ByteLoader)* me);
QUEX_INLINE bool                       QUEX_NAME(ByteLoader_LinuxSysCall_compare_handle)(const QUEX_NAME(ByteLoader)* alter_ego_A, 
                                                                       const QUEX_NAME(ByteLoader)* alter_ego_B);

QUEX_INLINE QUEX_NAME(ByteLoader)*    
QUEX_NAME(ByteLoader_LinuxSysCall_new)(int fd)
{
    QUEX_NAME(ByteLoader_LinuxSysCall)* me;

    if( fd == -1 ) return (QUEX_NAME(ByteLoader)*)0;
    me = (QUEX_NAME(ByteLoader_LinuxSysCall)*)QUEX_GNAME_LIB(MemoryManager_allocate)(sizeof(QUEX_NAME(ByteLoader_LinuxSysCall)),
                                                           E_MemoryObjectType_BYTE_LOADER);
    if( ! me ) return (QUEX_NAME(ByteLoader)*)0;
    QUEX_NAME(ByteLoader_LinuxSysCall_construct)(me, fd);
    return &me->base;
}

QUEX_INLINE QUEX_NAME(ByteLoader)*    
QUEX_NAME(ByteLoader_LinuxSysCall_new_from_file_name)(const char* FileName)
{
    QUEX_NAME(ByteLoader)*  result;
    int                     fd = open(FileName, O_RDONLY);

    old_fs = get_fs(); set_fs(KERNEL_DS); /* Allow reading to kernel buffer.  */

    fd = sys_open(filename, O_RDONLY, 0);
    if (fd <= 0) {
          result = (QUEX_NAME(ByteLoader)*)0;
    }
    else {
        result = QUEX_NAME(ByteLoader_LinuxSysCall_new)(fd);
        if( alter_ego ) {
            /* ByteLoader from file name *must* be owned by lexical analyzer, 
             * to ensure automatic closure and deletion.                      */
            result->handle_ownership = E_Ownership_LEXICAL_ANALYZER;
        }
    }

    set_fs(old_fs); /* Reset previous registers.                              */
    return result;
}

QUEX_INLINE void
QUEX_NAME(ByteLoader_LinuxSysCall_construct)(QUEX_NAME(ByteLoader_LinuxSysCall)* me, int fd)
{
    /* IMPORTANT: fd must be set BEFORE call to constructor!
     *            Constructor does call 'tell()'                             */
    me->fd = fd;

    QUEX_NAME(ByteLoader_construct)(&me->base,
                                    QUEX_NAME(ByteLoader_LinuxSysCall_tell),
                                    QUEX_NAME(ByteLoader_LinuxSysCall_seek),
                                    QUEX_NAME(ByteLoader_LinuxSysCall_load),
                                    QUEX_NAME(ByteLoader_LinuxSysCall_delete_self),
                                    QUEX_NAME(ByteLoader_LinuxSysCall_print_this),
                                    QUEX_NAME(ByteLoader_LinuxSysCall_compare_handle));

    /* A LinuxSysCall file handle is always in binary mode.                         */
    me->base.binary_mode_f = true;
}

QUEX_INLINE void    
QUEX_NAME(ByteLoader_LinuxSysCall_delete_self)(QUEX_NAME(ByteLoader)* alter_ego)
{
    QUEX_NAME(ByteLoader_LinuxSysCall)* me = (QUEX_NAME(ByteLoader_LinuxSysCall)*)(alter_ego);

    if( me->fd && me->base.handle_ownership == E_Ownership_LEXICAL_ANALYZER ) {
        old_fs = get_fs(); set_fs(KERNEL_DS); /* Allow reading to kernel buffer*/
        sys_close(me->fd);
        set_fs(old_fs); /* Reset previous registers.                           */
    }
    QUEX_GNAME_LIB(MemoryManager_free)(me, E_MemoryObjectType_BYTE_LOADER);
}

QUEX_INLINE QUEX_TYPE_STREAM_POSITION    
QUEX_NAME(ByteLoader_LinuxSysCall_tell)(QUEX_NAME(ByteLoader)* alter_ego)            
{ 
    QUEX_NAME(ByteLoader_LinuxSysCall)* me = (QUEX_NAME(ByteLoader_LinuxSysCall)*)(alter_ego);
    /* Use 'sys_lseek(current position + 0)' to get the current position.     */
    return (QUEX_TYPE_STREAM_POSITION)sys_lseek(me->fd, 0, SEEK_CUR); 
}

QUEX_INLINE void    
QUEX_NAME(ByteLoader_LinuxSysCall_seek)(QUEX_NAME(ByteLoader)*    alter_ego, 
                                        QUEX_TYPE_STREAM_POSITION Pos) 
{ 
    QUEX_NAME(ByteLoader_LinuxSysCall)* me = (QUEX_NAME(ByteLoader_LinuxSysCall)*)(alter_ego);
    sys_lseek(me->fd, (long)Pos, SEEK_SET); 
}

QUEX_INLINE size_t  
QUEX_NAME(ByteLoader_LinuxSysCall_load)(QUEX_NAME(ByteLoader)* alter_ego, 
                                 void*                  buffer, 
                                 const size_t           ByteN, 
                                 bool*                  end_of_stream_f) 
/* The LinuxSysCall interface does not allow to detect end of file upon reading.
 * The caller will realize end of stream by a return of zero bytes.          */
{ 
    QUEX_NAME(ByteLoader_LinuxSysCall)* me = (QUEX_NAME(ByteLoader_LinuxSysCall)*)(alter_ego);
    ssize_t                        n  = sys_read(me->fd, buffer, ByteN); 
    /* Theoretically, a last 'terminating zero' might be send over socket 
     * connections. Make sure, that this does not appear in the stream.      */
    if( n && ((uint8_t*)buffer)[n-1] == 0x0 ) {
        --n;
    }
    *end_of_stream_f = false;
    return (size_t)n;
}

QUEX_INLINE bool  
QUEX_NAME(ByteLoader_LinuxSysCall_compare_handle)(const QUEX_NAME(ByteLoader)* alter_ego_A, 
                                           const QUEX_NAME(ByteLoader)* alter_ego_B) 
/* RETURNS: true  -- if A and B point to the same LinuxSysCall object.
 *          false -- else.                                                   */
{ 
    const QUEX_NAME(ByteLoader_LinuxSysCall)* A = (QUEX_NAME(ByteLoader_LinuxSysCall)*)(alter_ego_A);
    const QUEX_NAME(ByteLoader_LinuxSysCall)* B = (QUEX_NAME(ByteLoader_LinuxSysCall)*)(alter_ego_B);

    return A->fd == B->fd;
}

QUEX_INLINE void                       
QUEX_NAME(ByteLoader_LinuxSysCall_print_this)(QUEX_NAME(ByteLoader)* alter_ego)
{
    QUEX_NAME(ByteLoader_LinuxSysCall)* me = (QUEX_NAME(ByteLoader_LinuxSysCall)*)(alter_ego);

    QUEX_DEBUG_PRINT("        type:             LinuxSysCall;\n");
    QUEX_DEBUG_PRINT1("        file_descriptor:  ((%i));\n", (int)me->fd);
    QUEX_DEBUG_PRINT("        end_of_stream_f:  <no means to detect>;\n");
}

QUEX_NAMESPACE_MAIN_CLOSE

#endif /*  QUEX_INCLUDE_GUARD__BUFFER__BYTES__BYTE_LOADER_SYSCALL_I */

