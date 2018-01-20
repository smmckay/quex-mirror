/* PURPOSE: Extension and migration of buffer content -- Nested.
 *
 * The test operates on the following functions:
 *
 *    Buffer_extend_root()     tested in    self_common_single_migration()
 *    Buffer_migrate_root()    tested in    self_common_single_extension()
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
#include <quex/code_base/buffer/TESTS/MemoryManager_UnitTest.i>
#include <quex/code_base/buffer/Buffer>

MemoryManager_UnitTest_t MemoryManager_UnitTest;

QUEX_NAME(Buffer) self_array[1024];

static QUEX_NAME(Buffer)* self_construct_reference(size_t TotalSize, size_t Depth);
static void               self_destruct_reference(size_t Depth);

QUEX_INLINE bool
QUEX_NAME(Buffer_construct_included)(QUEX_NAME(Buffer)*        including,
                                     QUEX_NAME(Buffer)*        included,
                                     QUEX_NAME(LexatomLoader)* filler);

int
main(int argc, char** argv)
{
    QUEX_NAME(Buffer)* reference;
    size_t             new_size;
    ptrdiff_t          count;
    ptrdiff_t          shrink_n;
    size_t             total_size;
    size_t             single_size;
    size_t             depth = atoi(argv[1]);

    hwut_info("Extend/Migrate Memory: Nested;"
              "CHOICES: 2, 3, 997;");

    memset(&MemoryManager_UnitTest, 0, sizeof(MemoryManager_UnitTest));
    MemoryManager_UnitTest.allocation_addmissible_f = true;

    count = 0;

    for(single_size = 4; single_size < 7; ++single_size) {
        total_size = depth * single_size;

        reference = self_construct_reference(total_size, depth);

        for(new_size = QUEX_MAX(3, total_size - 1); 
            new_size <= total_size + 2 ; ++new_size) {

            count += common_iterate(reference, new_size, &shrink_n);
        }

        self_destruct_reference(depth);
    }

    printf("<terminated: ((%i)); shrinked: ((%i)); allocated_byte_n: ((%i)); allocate_n: ((%i)); free_n: ((%i));>\n", 
           (int)count, (int)shrink_n,
           (int)MemoryManager_UnitTest.allocated_byte_n, 
           (int)MemoryManager_UnitTest.allocation_n, 
           (int)MemoryManager_UnitTest.free_n); 
}

static QUEX_NAME(Buffer)*
self_construct_reference(size_t TotalSize, size_t Depth)
{
    ptrdiff_t i=0;
    common_construct_reference_base(&self_array[0], TotalSize);
    for(i=0; i<Depth-1 ; ++i) {
        QUEX_NAME(Buffer_construct_included)(&self_array[i], 
                                             &self_array[i+1], 
                                             (QUEX_NAME(LexatomLoader)*)0);
    }

    return &self_array[Depth-1];
}

static void
self_destruct_reference(size_t Depth)
{
    ptrdiff_t i=0;
    for(i=Depth-1; i>=0 ; --i) {
        QUEX_NAME(Buffer_destruct)(&self_array[i]);
    }
}
            
