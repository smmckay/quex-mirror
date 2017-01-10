/* PURPOSE: Construction of a buffer to hold included content.
 *
 * Upon inclusion, new memory must be provided to load included content. Now, it
 * is possible that the 'including' buffer has enough space, so that it may 
 * share memory. In that case the including's buffer is split. 
 *
 * Construction and destruction of included buffer's is triggered by 
 *
 *                   Buffer_construct_included() and 
 *                   Buffer_destruct_included()
 *
 * Those are the functions to be tested in this file.
 *
 * (C) Frank-Rene Schaefer.                                                   */
#define  __QUEX_OPTION_PLAIN_C

#include <quex/code_base/test_environment/TestAnalyzer-configuration>
#include <quex/code_base/buffer/TESTS/MemoryManager_UnitTest.i>
#include <quex/code_base/definitions>
#include <quex/code_base/buffer/Buffer>
#include <quex/code_base/MemoryManager>
#include <quex/code_base/buffer/Buffer.i>

#include <hwut_unit.h>

MemoryManager_UnitTest_t MemoryManager_UnitTest;

static void
self_check_destruction(QUEX_NAME(Buffer)* including, size_t MemorySize);
static int
self_check_construction(QUEX_NAME(Buffer)* including, QUEX_NAME(Buffer)* included,
                        QUEX_TYPE_LEXATOM* MemoryBack,
                        ptrdiff_t          DistanceReadToEnd);

int
main(int argc, char** argv)
{
    const size_t       MemorySize = QUEX_SETTING_BUFFER_SIZE;
    QUEX_TYPE_LEXATOM* memory;
    QUEX_TYPE_LEXATOM* read_p;
    QUEX_TYPE_LEXATOM* end_p;
    QUEX_TYPE_LEXATOM* p;

    hwut_info("Construct/Destruct Included Buffer;");

    QUEX_NAME(Buffer) including;
    QUEX_NAME(Buffer) included;
    size_t            split_n = 0, count_n = 0;
    ptrdiff_t         read_i, end_i, i;

    for(read_i = 0; read_i != MemorySize; ++read_i) {
        for(end_i = read_i; end_i != MemorySize; ++end_i) {
  
            memory = (QUEX_TYPE_LEXATOM*)QUEXED(MemoryManager_allocate)(
                                MemorySize * sizeof(QUEX_TYPE_LEXATOM), 
                                E_MemoryObjectType_BUFFER_MEMORY);

            read_p = &memory[read_i];
            end_p  = &memory[end_i];

            /* Construct including ___________________________________________*/
            QUEX_NAME(Buffer_construct)(&including, (QUEX_NAME(LexatomLoader)*)0,
                                        memory, MemorySize, end_p,
                                        E_Ownership_LEXICAL_ANALYZER);

            including.input.end_p  = end_p;
            including._read_p = read_p;
            for(p=read_p, i=1; p != end_p; ++p, ++i) {
                *p = i;
            }

            /* Construct Included ____________________________________________*/
            QUEX_NAME(Buffer_construct_included)(&including, &included, 
                                                 (QUEX_NAME(LexatomLoader)*)0);

            split_n += self_check_construction(&including, &included, 
                                               &memory[MemorySize-1], end_i - read_i);

            /* Destruct Included _____________________________________________*/
            QUEX_NAME(Buffer_destruct_included)(&including, &included);

            self_check_destruction(&including, MemorySize);

            /* Destruct including ____________________________________________*/
            QUEX_NAME(Buffer_destruct)(&including); 

            count_n += 1;
        }
    }

    printf("<terminated: %i; splits: %i; allocate_n: %i; allocated_byte_n: %i; free_n: %i;>\n", 
           (int)count_n, (int)split_n,
           (int)MemoryManager_UnitTest.allocation_n, 
           (int)MemoryManager_UnitTest.allocated_byte_n, 
           (int)MemoryManager_UnitTest.free_n); 
}

static int
self_check_construction(QUEX_NAME(Buffer)* including, QUEX_NAME(Buffer)* included, 
                        QUEX_TYPE_LEXATOM* MemoryBack,
                        ptrdiff_t          DistanceReadToEnd)
{
    QUEX_TYPE_LEXATOM* p;
    bool               split_f;
    ptrdiff_t          i;

    __quex_assert(&including->_memory._back[1] - &included->_memory._front[0]
                  >= QUEX_SETTING_BUFFER_INCLUDE_MIN_SIZE);

    split_f = (&including->_memory._back[1] == &included->_memory._front[0]) ? true : false;

    if( split_f ) {
        __quex_assert(included->_memory._back == MemoryBack);
    }

    __quex_assert(   including->input.end_p -including->_read_p == DistanceReadToEnd);

    for(p=including->_read_p, i=1; p != including->input.end_p; ++p, ++i) {
        __quex_assert(*p == i);
    }

    return split_f ? 1 : 0;
}

static void
self_check_destruction(QUEX_NAME(Buffer)* including, size_t MemorySize)
{
    QUEX_TYPE_LEXATOM* p;
    ptrdiff_t          i;

    __quex_assert(&including->_memory._back[1] - &including->_memory._front[0] 
                  == MemorySize);
    for(p=including->_read_p, i=1; p != including->input.end_p; ++p, ++i) {
        __quex_assert(*p == i);
    }
}
