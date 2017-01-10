/* -*- C++ -*- vim: set syntax=cpp: 
 *
 * PURPOSE: Implementation of the MemoryManager for Unit Tests.
 *          
 * Some information about allocation and freeing of memory is collected in 
 * 'MemoryManager_UnitTest_t'.                                                        
 *
 * (C) Frank-Rene Schaefer                                                    */

#ifndef __QUEX_INCLUDE_GUARD__MEMORY_MANAGER_UNIT_TEST_I
#define __QUEX_INCLUDE_GUARD__MEMORY_MANAGER_UNIT_TEST_I

#include <quex/code_base/definitions>
#include <quex/code_base/MemoryManager>

QUEX_NAMESPACE_QUEX_OPEN

typedef struct {
    int allocation_n;
    int allocated_byte_n;
    int free_n;
} MemoryManager_UnitTest_t;

/* Object must be defined in unit test!                                       */
extern MemoryManager_UnitTest_t MemoryManager_UnitTest;

uint8_t*
QUEXED_DEF(MemoryManager_allocate)(const size_t       ByteN, 
                                   E_MemoryObjectType Type)
{
    uint8_t*  me = (uint8_t*)__QUEX_STD_malloc((size_t)ByteN);

    (void)Type;
#   ifdef QUEX_OPTION_ASSERTS
    __QUEX_STD_memset((void*)me, 0xFF, ByteN);
#   endif

    MemoryManager_UnitTest.allocation_n     += 1;
    MemoryManager_UnitTest.allocated_byte_n += ByteN;
    return me;
}
       
void 
QUEXED_DEF(MemoryManager_free)(void*              alter_ego, 
                               E_MemoryObjectType Type)  
{ 
    void* me = (void*)alter_ego;
    (void)Type;
    /* The de-allocator shall never be called for LexemeNull object.         */
    if( me ) {
        __QUEX_STD_free(me); 
    }
    MemoryManager_UnitTest.free_n       += 1;
}

size_t
QUEXED_DEF(MemoryManager_insert)(uint8_t* drain_begin_p,  uint8_t* drain_end_p,
                                 uint8_t* source_begin_p, uint8_t* source_end_p)
/* Inserts as many bytes as possible into the array from 'drain_begin_p'
 * to 'drain_end_p'. The source of bytes starts at 'source_begin_p' and
 * ends at 'source_end_p'.
 *
 * RETURNS: Number of bytes that have been copied.                           */
{
    /* Determine the insertion size.                                         */
    const size_t DrainSize = (size_t)(drain_end_p  - drain_begin_p);
    size_t       size      = (size_t)(source_end_p - source_begin_p);
    __quex_assert(drain_end_p  >= drain_begin_p);
    __quex_assert(source_end_p >= source_begin_p);

    if( DrainSize < size ) size = DrainSize;

    /* memcpy() might fail if the source and drain domain overlap! */
#   ifdef QUEX_OPTION_ASSERTS 
    if( drain_begin_p > source_begin_p ) __quex_assert(drain_begin_p >= source_begin_p + size);
    else                                 __quex_assert(drain_begin_p <= source_begin_p - size);
#   endif
    __QUEX_STD_memcpy(drain_begin_p, source_begin_p, size);

    return size;
}

bool 
QUEXED_DEF(system_is_little_endian)(void)
{
    union {
        long int multi_bytes;
        char     c[sizeof (long int)];
    } u;
    u.multi_bytes = 1;
    return u.c[sizeof(long int)-1] != 1;
}


QUEX_NAMESPACE_QUEX_CLOSE
 
#endif /*  __QUEX_INCLUDE_GUARD__MEMORY_MANAGER_I */


