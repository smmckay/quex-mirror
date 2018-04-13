/* PURPOSE: Construction of a buffer to hold included content.
 *
 * Upon inclusion, new memory must be provided to load included content. Now, it
 * is possible that the 'including' buffer has enough space, so that it may 
 * share memory. In that case the including's buffer is split. 
 *
 * Construction and destruction of included buffer's is triggered by 
 *
 *                   Buffer_nested_construct() and 
 *                   Buffer_destruct_included()
 *
 * CHOICES: allocate    -- MemoryManager allocates a 2nd buffer if split fails.
 *          no-allocate -- MemoryManager does not allocate 2nd buffer.
 *
 * (C) Frank-Rene Schaefer.                                                   */
#define  __QUEX_OPTION_PLAIN_C

#include "minimum-definitions.h"
#include "MemoryManager_UnitTest.i"
#include "ut/lib/definitions"
#include "ut/lib/buffer/Buffer"
#include "ut/lib/MemoryManager"
#include "ut/lib/buffer/Buffer.i"

#include <hwut_unit.h>

MemoryManager_UnitTest_t MemoryManager_UnitTest;

static void
self_check_destruction(QUEX_NAME(Buffer)* including, size_t MemorySize);
static int
self_check_construction(QUEX_NAME(Buffer)* including, QUEX_NAME(Buffer)* included,
                        QUEX_TYPE_LEXATOM* MemoryEnd,
                        ptrdiff_t          DistanceReadToEnd,
                        bool               Verdict);

int
main(int argc, char** argv)
{
    const size_t       MemorySize = QUEX_SETTING_BUFFER_SIZE;
    QUEX_TYPE_LEXATOM* dummy;
    QUEX_TYPE_LEXATOM* memory;
    QUEX_TYPE_LEXATOM* read_p;
    QUEX_TYPE_LEXATOM* end_p;
    QUEX_TYPE_LEXATOM* p;
    bool               verdict;
    QUEX_NAME(Buffer)  including;
    QUEX_NAME(Buffer)  included;
    size_t             split_n = 0, count_n = 0;
    ptrdiff_t          read_i, end_i, i;
    bool               allocation_f;

    hwut_info("Construct/Destruct Included Buffer;"
              "CHOICES: allocate, no-allocate;");

    memset(&MemoryManager_UnitTest, 0, sizeof(MemoryManager_UnitTest));

    hwut_if_choice("allocate")    allocation_f = true;
    hwut_if_choice("no-allocate") allocation_f = false;

    for(read_i = 1; read_i != MemorySize -1 ; ++read_i) {
        for(end_i = read_i + 1; end_i < MemorySize; ++end_i) {
  
            MemoryManager_UnitTest.allocation_addmissible_f = true;
            memory = (QUEX_TYPE_LEXATOM*)QUEXED(MemoryManager_allocate)(
                                MemorySize * sizeof(QUEX_TYPE_LEXATOM), 
                                E_MemoryObjectType_BUFFER_MEMORY);
            /* Dummy allocation to prevent adjacent memories.                */
            dummy = (QUEX_TYPE_LEXATOM*)QUEXED(MemoryManager_allocate)(
                                        4711, E_MemoryObjectType_BUFFER_MEMORY);

            read_p = &memory[read_i];
            end_p  = &memory[end_i];

            /* Construct including ___________________________________________*/
            QUEX_NAME(Buffer_construct)(&including, (QUEX_NAME(LexatomLoader)*)0,
                                        memory, MemorySize, end_p,
                                        E_Ownership_LEXICAL_ANALYZER,
                                        (QUEX_NAME(Buffer)*)0);

            including.input.end_p  = end_p;
            including._read_p = read_p;
            for(p=read_p, i=1; p != end_p; ++p, ++i) {
                *p = i;
            }

            /* Construct Included ____________________________________________*/
            MemoryManager_UnitTest.allocation_addmissible_f = allocation_f;
            including._lexeme_start_p = including._read_p;
            verdict = QUEX_NAME(Buffer_nested_construct)(&included, &including, 
                                                         (QUEX_NAME(LexatomLoader)*)0);

            split_n += self_check_construction(&including, &included, 
                                               &memory[MemorySize], 
                                               end_i - read_i, verdict);

            /* Destruct Included _____________________________________________*/
            QUEX_NAME(Buffer_destruct)(&included);

            self_check_destruction(&including, MemorySize);

            /* Destruct including ____________________________________________*/
            QUEX_NAME(Buffer_destruct)(&including); 

            count_n += 1;

            QUEXED(MemoryManager_free)(dummy, E_MemoryObjectType_BUFFER_MEMORY);
        }
    }

    printf("<terminated: %i; splits: ((%i)); allocated_byte_n: ((%i)); allocate_n: ((%i)); free_n: ((%i));>\n", 
           (int)count_n, (int)split_n,
           (int)MemoryManager_UnitTest.allocated_byte_n, 
           (int)MemoryManager_UnitTest.allocation_n, 
           (int)MemoryManager_UnitTest.free_n); 
}

static int
self_check_construction(QUEX_NAME(Buffer)* including, QUEX_NAME(Buffer)* included, 
                        QUEX_TYPE_LEXATOM* MemoryEnd,
                        ptrdiff_t          DistanceReadToEnd,
                        bool               Verdict)
{
    QUEX_TYPE_LEXATOM* p;
    ptrdiff_t          i;
    /*         front           read_p      end_p
     *           |               |           |
     *          .-------------------------------------------------.
     *          |0|-|-|-|-|-|-|-|a|b|c|d|e|f|0| | | | | | | | | | |
     *          '-------------------------------------------------'
     *
     * may be moved to
     *
     *       front read_p      end_p
     *           | |           |
     *          .-------------------------------------------------.
     *          |0|a|b|c|d|e|f|0| | | | | | | | | | | | | | | | | |
     *          '-------------------------------------------------'
     *
     * From 'front' to 'read_p' everything has been processed. The including
     * buffer only requires 'end_p - read_p + 2'. '+2' for the boarders of the
     * buffer. Additionally, the 'fallback_n' needs to be considered.        */

    if( included->_memory.ownership == E_Ownership_INCLUDING_BUFFER ) {
        /* Intermediate dummy alloction prevents adjacent buffers. 
         * => Only upon 'split' the buffers contents are adjacent!            */
        __quex_assert(&including->_memory._back[1] == &included->_memory._front[0]);
        __quex_assert(&included->_memory._back[1] - &included->_memory._front[0]
                      >= QUEX_SETTING_BUFFER_SIZE_MIN);
        __quex_assert(&included->_memory._back[1] == MemoryEnd);
    }
    else {
        if( Verdict ) {
            /* Intermediate dummy alloction prevents adjacent buffers. 
             * => Only upon 'split' the buffers contents are adjacent!        */
            __quex_assert(&including->_memory._back[1] != &included->_memory._front[0]);
        }
        else {
            __quex_assert(included->_memory._back == (QUEX_TYPE_LEXATOM*)0);
            __quex_assert(included->_memory._front == (QUEX_TYPE_LEXATOM*)0);
        }

        /* Here, construction can only succeed, if allocation is addmissible. */
        __quex_assert(Verdict == MemoryManager_UnitTest.allocation_addmissible_f);
    }

    __quex_assert(including->input.end_p -including->_read_p == DistanceReadToEnd);

    for(p=including->_read_p, i=1; p != including->input.end_p; ++p, ++i) {
        __quex_assert(*p == i);
    }

    return included->_memory.ownership == E_Ownership_INCLUDING_BUFFER;
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
