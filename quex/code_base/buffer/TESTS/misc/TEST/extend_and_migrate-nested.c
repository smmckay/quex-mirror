/* PURPOSE: Extension and migration of buffer content -- Nested.
 *
 * The test operates on the following functions:
 *
 *    Buffer_nested_extend()     tested in    self_common_single_migration()
 *    Buffer_nested_migrate()    tested in    self_common_single_extension()
 *
 * 'Nested' means, that the initial buffer IS NESTED IN AN INCLUDING BUFFER.
 * Both functions are checked for the same sample space of setups 
 * which is defined by the following parameters:
 *
 *  -- reference_size: initial size of the buffer before migration 
 *                     or extension shall be applied.
 *
 *  -- new_size:       size of the memory to which the buffer shall
 *                     migrate or extend.
 *
 *  -- '._read_p', '._lexeme_start_p', '.input.end_p' which limit the
 *                     ability to move or extend memory.
 *
 * Additionally, some content is written into the buffer, so that it can be
 * verified whether the content is maintained. This test also checks whether
 * the migration fails, if the new size is too small to hold the current
 * content.
 *
 * CHOICES: define the DEPTH of nesting. '1' is done in 'Plain', so it is
 *          not repeated here.
 *
 * (C) Frank-Rene Schaefer.                                                   */
/* #define  QUEX_OPTION_UNIT_TEST_MEMORY_MANAGER_VERBOSE */

#include <common.h>
#include "MemoryManager_UnitTest.i"
#include "test_c/lib/buffer/Buffer"

MemoryManager_UnitTest_t MemoryManager_UnitTest;

QUEX_NAME(Buffer) self_reference[1024];
QUEX_NAME(Buffer) self_subject[1024];

static QUEX_NAME(Buffer)* self_construct_setup(QUEX_NAME(Buffer)* array, 
                                               size_t TotalSize, size_t Depth);
static void               self_destruct_setup(QUEX_NAME(Buffer)* array,
                                              size_t Depth);
static void               self_test_single_migration(QUEX_NAME(Buffer)* reference, 
                                                     QUEX_NAME(Buffer)* subject, 
                                                     size_t             NewSize,
                                                     ptrdiff_t*         shrink_n);

bool
QUEX_NAME(Buffer_nested_construct)(QUEX_NAME(Buffer)*        me,
                                   QUEX_NAME(Buffer)*        nesting,
                                   QUEX_NAME(LexatomLoader)* filler);

int
main(int argc, char** argv)
{
    QUEX_NAME(Buffer)* reference;
    QUEX_NAME(Buffer)* subject;
    size_t             new_size;
    ptrdiff_t          count = 0;
    ptrdiff_t          shrink_n = 0;
    ptrdiff_t          end_offset;
    ptrdiff_t          offset;
    size_t             total_size = 0;
    size_t             single_size = 0;
    size_t             depth = atoi(argv[1]);
    QUEX_TYPE_LEXATOM_EXT  tmp[3];

    hwut_info("Extend/Migrate Memory: Nested;"
              "CHOICES: 2, 3, 51;");

    memset(&MemoryManager_UnitTest, 0, sizeof(MemoryManager_UnitTest));
    MemoryManager_UnitTest.allocation_addmissible_f = true;

    for(single_size = 4; single_size < 7; ++single_size) {
        total_size = depth * single_size;

        reference = self_construct_setup(&self_reference[0], total_size, depth);

        __quex_assert(single_size <= &reference->_memory._back[1] - reference->_memory._front);

        for(new_size = QUEX_MAX(3, total_size - 1); 
            new_size <= total_size + 2 ; ++new_size) {
            /* Varry the offsets of '_read_p', '_lexeme_start_p', and 'input.end_p'.  */
            for(end_offset = 0; end_offset != single_size-1; ++end_offset) {
                for(offset = 0; offset <= end_offset ; ++offset) {

                    /* Prepare                                                        */
                    reference->input.end_p       = &reference->_memory._front[end_offset + 1];
                    reference->_read_p           = &reference->_memory._front[offset + 1];
                    reference->_lexeme_start_p   = &reference->_memory._front[offset + 1];
                    tmp[0] = reference->input.end_p[0];
                    tmp[1] = reference->_memory._front[0];
                    tmp[2] = reference->_memory._back[0];
                    reference->input.end_p[0]    = (QUEX_TYPE_LEXATOM_EXT)0;
                    reference->_memory._front[0] = (QUEX_TYPE_LEXATOM_EXT)0;
                    reference->_memory._back[0]  = (QUEX_TYPE_LEXATOM_EXT)0;

                    subject = self_construct_setup(&self_subject[0], total_size, depth);
                    subject->input.end_p       = &subject->_memory._front[end_offset + 1];
                    subject->_read_p           = &subject->_memory._front[offset + 1];
                    subject->_lexeme_start_p   = &subject->_memory._front[offset + 1];
                    subject->input.end_p[0]    = (QUEX_TYPE_LEXATOM_EXT)0;
                    subject->_memory._front[0] = (QUEX_TYPE_LEXATOM_EXT)0;
                    subject->_memory._back[0]  = (QUEX_TYPE_LEXATOM_EXT)0;

                    self_test_single_migration(reference, subject, new_size, &shrink_n);
                    self_destruct_setup(&self_subject[0], depth);

                    reference->input.end_p[0]    = tmp[0];
                    reference->_memory._front[0] = tmp[1];
                    reference->_memory._back[0]  = tmp[2];
#if 0
                    self_destruct_setup(&self_subject, depth);

                    subject = self_construct_setup(&self_subject, total_size, depth);
                    subject->input.end_p       = &subject->_memory._front[end_offset];
                    subject->_read_p           = &subject->_memory._front[offset + 1];
                    subject->_lexeme_start_p   = &subject->_memory._front[offset + 1];

                    self_test_single_extension(subject, NewSize);

                    self_destruct_setup(&self_subject, depth);
#endif

                    count += 1;
                }
            }
        }

        self_destruct_setup(&self_reference[0], depth);
    }

    printf("<terminated: ((%i)); shrinked: ((%i)); allocated_byte_n: ((%i)); allocate_n: ((%i)); free_n: ((%i)); recursion_n: ((%i))>\n", 
           (int)count, (int)shrink_n,
           (int)MemoryManager_UnitTest.allocated_byte_n, 
           (int)MemoryManager_UnitTest.allocation_n, 
           (int)MemoryManager_UnitTest.free_n,
           (int)common_recursion_count_n); 
}

static QUEX_NAME(Buffer)*
self_construct_setup(QUEX_NAME(Buffer)* array, size_t TotalSize, size_t Depth)
{
    ptrdiff_t          i           = 0;
    bool               success_f   = false;
    ptrdiff_t          single_size = TotalSize / Depth;
    QUEX_TYPE_LEXATOM_EXT* p;

    QUEX_TYPE_LEXATOM_EXT* memory = (QUEX_TYPE_LEXATOM_EXT*)quex_MemoryManager_allocate(
                                      TotalSize * sizeof(QUEX_TYPE_LEXATOM_EXT), 
                                      E_MemoryObjectType_BUFFER_MEMORY);

    QUEX_NAME(Buffer_construct)(&array[0], (QUEX_NAME(LexatomLoader)*)0,
                                memory, TotalSize, 
                                &memory[single_size-1],
                                E_Ownership_LEXICAL_ANALYZER,
                                (QUEX_NAME(Buffer)*)0);

    for(p =  &array[0]._memory._front[1]; p != array[0].input.end_p; ++p) {
        *p = (QUEX_TYPE_LEXATOM_EXT)('a' + i);
    }

    /* Ensure, that all buffers are split from the root buffer. */
    MemoryManager_UnitTest.allocation_addmissible_f = false;

    for(i=0; i<Depth-1 ; ++i) {
        success_f = QUEX_NAME(Buffer_nested_construct)(&array[i+1], &array[i], 
                                                       (QUEX_NAME(LexatomLoader)*)0);
        hwut_verify(success_f);

        array[i+1].input.end_p    = &array[i+1]._memory._front[single_size-1];
        array[i+1].input.end_p[0] = QUEX_SETTING_BUFFER_LIMIT_CODE;

        for(p =  &array[i+1]._memory._front[1]; p != array[i+1].input.end_p; ++p) {
            *p = (QUEX_TYPE_LEXATOM_EXT)('a' + i);
        }
    }

    MemoryManager_UnitTest.allocation_addmissible_f = true;

    return &array[Depth-1];
}

static void
self_destruct_setup(QUEX_NAME(Buffer)* array, size_t Depth)
{
    ptrdiff_t i=0;
    for(i=Depth-1; i>=0 ; --i) {
        QUEX_NAME(Buffer_destruct)(&array[i]);
    }
}

static void
self_test_single_migration(QUEX_NAME(Buffer)* reference, 
                           QUEX_NAME(Buffer)* subject, 
                           size_t             NewSize,
                           ptrdiff_t*         shrink_n)
{
    //  QUEX_NAME(Buffer)*  root      = &self_reference[0];
    // bool                verdict_f = (subject->input.end_p - root->_memory._front <= NewSize) ? true : false;
    // E_Ownership         ownership = verdict_f ? E_Ownership_EXTERNAL : E_Ownership_LEXICAL_ANALYZER;
    QUEX_TYPE_LEXATOM_EXT   new_memory[8192];

    hwut_verify(NewSize < 8192);

    MemoryManager_UnitTest.allocation_addmissible_f = false;

    __quex_assert(subject->input.end_p >= subject->_memory._front);
    __quex_assert(subject->input.end_p <= subject->_memory._back);

    QUEX_NAME(Buffer_nested_migrate)(subject, new_memory, NewSize, 
                                     E_Ownership_EXTERNAL);

    MemoryManager_UnitTest.allocation_addmissible_f = true;

    /* hwut_verify(ownership == subject->_memory.ownership); */

    if( common_verify(reference, subject) ) { *shrink_n += 1; }
}

