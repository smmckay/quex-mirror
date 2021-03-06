/* PURPOSE: Negotiate a buffer memory extension 
 *
 * The test operates on the following functions:
 *
 *          Buffer_nested_negotiate_extend()
 *
 * Pointer and indice handling is not subject to this test. Subject to test
 * is:
 *
 *    -- Deal with 'no extension possible at all'.
 *    -- Extension possible for 'current_size + 1'
 *    -- Extension possible for 'current_size + 2'
 *    -- Extension possible for 'current_size * factor - 1'
 *    -- Extension possible for 'current_size * factor'
 *    -- Extension possible for 'current_size * factor + 1'
 *    -- Extension possible at first hit.
 *
 * (C) Frank-Rene Schaefer.                                                   */

/* #define  QUEX_OPTION_UNIT_TEST_MEMORY_MANAGER_VERBOSE_EXT */

#include <common.h>
#include "test_c/lib/quex/MemoryManager_UnitTest.i"
#include "test_c/lib/lexeme/converter-from-lexeme.i"
#include "test_c/lib/buffer/Buffer"
#include "test_c/lib/buffer/asserts"

MemoryManager_UnitTest_t MemoryManager_UnitTest;

QUEX_NAME(Buffer) self_reference[1024];
QUEX_NAME(Buffer) self_subject[1024];

static void               self_test(size_t    SizeBefore, 
                                    ptrdiff_t ReallocLimitByteN);
static QUEX_NAME(Buffer)* self_construct_setup(QUEX_NAME(Buffer)* array, 
                                               size_t             TotalSize, 
                                               size_t*            depth);
static void               self_destruct_setup(QUEX_NAME(Buffer)* array,
                                              size_t             Depth);

bool
QUEX_NAME(Buffer_nested_construct)(QUEX_NAME(Buffer)*        me,
                                   QUEX_NAME(Buffer)*        nesting,
                                   QUEX_NAME(LexatomLoader)* filler);

int
main(int argc, char** argv)
{
    ptrdiff_t shrink_n = 0;
    size_t    total_size = 0;
    float     factor = 2.0;

    hwut_info("Extend negotiated amount of memory;");

    memset(&MemoryManager_UnitTest, 0, sizeof(MemoryManager_UnitTest));
    MemoryManager_UnitTest.allocation_addmissible_f = true;

    printf("## COMMENT: The end state of the reallocation is checked via asserts.\n"
           "## COMMENT: The particular sequence of accept/refusal sizes is indifferent.\n"
           "## COMMENT: Important is the final 'verdict'.\n");
    for(total_size = 4; total_size < 21; total_size += 3 ) {
        self_test(total_size, 0);
        self_test(total_size, 1);

        self_test(total_size, total_size - 1);
        self_test(total_size, total_size);
        self_test(total_size, total_size + 1);

        self_test(total_size, factor * total_size - 1);
        self_test(total_size, factor * total_size);
        self_test(total_size, factor * total_size + 1);

        self_test(total_size, PTRDIFF_MAX);
    }

    printf("\nshrinked:              ((%i));\n"
           "allocated_byte_n:      ((%i));\n"
           "allocate_n:            ((%i));\n"
           "free_n:                ((%i));\n"
           "reallocated_byte_n:    ((%i));\n"
           "reallocated_refusal_n: ((%i));\n", 
           (int)shrink_n,
           (int)MemoryManager_UnitTest.allocated_byte_n, 
           (int)MemoryManager_UnitTest.allocation_n, 
           (int)MemoryManager_UnitTest.free_n,
           (int)MemoryManager_UnitTest.reallocated_byte_n,
           (int)MemoryManager_UnitTest.reallocated_refusal_n); 
}

static void
self_test(size_t SizeBefore, ptrdiff_t ReallocLimitByteN)
{
    QUEX_NAME(Buffer)*   me;
    bool                 verdict_f = false;
    ptrdiff_t            size;
    QUEX_NAME(Buffer)*   root = &self_reference[0];
    QUEX_TYPE_LEXATOM_EXT*   content_before = (QUEX_TYPE_LEXATOM_EXT*)malloc(
                                            sizeof(QUEX_TYPE_LEXATOM_EXT) * SizeBefore);
    size_t               content_before_size;
    QUEX_TYPE_LEXATOM_EXT*   root_memory_p = 0;
    size_t               depth = 5;            

    if( ReallocLimitByteN < 0) return; 

    printf("\n---( initial size: %i; target size: %i; reallocation limit: ",
           (int)SizeBefore, (int)(SizeBefore * 2.0)); 

    if( ReallocLimitByteN == PTRDIFF_MAX ) printf("PTRDIFF_MAX");
    else                                   printf("%i", (int)ReallocLimitByteN);
    printf(" [byte]; )---\n");

    me = self_construct_setup(&self_reference[0], SizeBefore, &depth);
    hwut_verify(SizeBefore == me->end(me) - self_reference[0].begin(&self_reference[0]));

    /* depth may have been adapted. */

    content_before_size = (size_t)(me->content_end(me) - self_reference[0].begin(&self_reference[0]));

    /* Backup the initial content for later check. */
    root_memory_p = &self_reference[0]._memory._front[0];
    memcpy((void*)content_before, (void*)root_memory_p, content_before_size);

    MemoryManager_UnitTest.reallocate_limit_byte_n = ReallocLimitByteN;
    MemoryManager_UnitTest.reallocate_verbose_f    = 1;

    verdict_f   = QUEX_NAME(Buffer_nested_negotiate_extend)(me, 2.0);
    printf("verdict: %s;\n", verdict_f ? "true" : "false");

    size        = me->end(me) - root->_memory._front;

    /* Verify content before/after is the same. */
    root_memory_p = &self_reference[0]._memory._front[0];
    hwut_verify(
        0 == memcmp((void*)content_before, (void*)root_memory_p,
                    content_before_size)
    );
    hwut_verify(verdict_f   == (size > SizeBefore));
    hwut_verify(! verdict_f == (size == SizeBefore));

    self_destruct_setup(&self_reference[0], depth);

    free(content_before);
}

static QUEX_NAME(Buffer)*
self_construct_setup(QUEX_NAME(Buffer)* array, size_t TotalSize, size_t* depth)
{
    ptrdiff_t          i           = 0;
    bool               success_f   = false;
    ptrdiff_t          single_size;
    QUEX_TYPE_LEXATOM_EXT* p;

    *depth      = QUEX_MIN(TotalSize / 4, *depth);
    single_size = TotalSize / *depth;

    QUEX_TYPE_LEXATOM_EXT* memory = (QUEX_TYPE_LEXATOM_EXT*)quex_MemoryManager_allocate(
                                      TotalSize * sizeof(QUEX_TYPE_LEXATOM_EXT), 
                                      E_MemoryObjectType_BUFFER_MEMORY);

    QUEX_NAME(Buffer_construct)(&array[0], (QUEX_NAME(LexatomLoader)*)0,
                                memory, TotalSize, 
                                &memory[single_size-1],
                                QUEX_UT_SETTING_BUFFER_FALLBACK_N_EXT, 
                                E_Ownership_LEXICAL_ANALYZER,
                                (QUEX_NAME(Buffer)*)0);

    for(p =  &array[0]._memory._front[1]; p != array[0].input.end_p; ++p) {
        *p = (QUEX_TYPE_LEXATOM_EXT)('a' + i);
    }

    /* Ensure, that all buffers are split from the root buffer. */
    MemoryManager_UnitTest.allocation_addmissible_f = false;

    for(i=0; i<*depth-1 ; ++i) {
        success_f = QUEX_NAME(Buffer_nested_construct)(&array[i+1], &array[i], 
                                                       (QUEX_NAME(LexatomLoader)*)0);
        hwut_verify(success_f);

        array[i+1].input.end_p    = &array[i+1]._memory._front[single_size-1];
        *(array[i+1].input.end_p) = (QUEX_TYPE_LEXATOM_EXT)0;

        for(p =  &array[i+1]._memory._front[1]; p != array[i+1].input.end_p; ++p) {
            *p = (QUEX_TYPE_LEXATOM_EXT)('a' + i);
        }

        QUEX_NAME(Buffer_assert_consistency)(&array[i+1]);
    }

    MemoryManager_UnitTest.allocation_addmissible_f = true;

    return &array[*depth-1];
}

static void
self_destruct_setup(QUEX_NAME(Buffer)* array, size_t Depth)
{
    ptrdiff_t i=0;
    for(i=Depth-1; i>=0 ; --i) {
        QUEX_NAME(Buffer_destruct)(&array[i]);
    }
}

