/* PURPOSE: Extension and migration of buffer content -- Plain.
 *
 * The test operates on the following functions:
 *
 *    Buffer_nested_extend()     tested in    self_common_single_migration()
 *    Buffer_nested_migrate()    tested in    self_common_single_extension()
 *
 * 'Plain' means, that the initial buffer is not nested in an including
 * buffer. Both functions are checked for the same sample space of setups 
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
 * CHOICES: define the initial size of the buffer before migration/extension.
 *
 * (C) Frank-Rene Schaefer.                                                   */
/* #define  QUEX_OPTION_UNIT_TEST_MEMORY_MANAGER_VERBOSE */

#include <common.h>
#include "TESTS/MemoryManager_UnitTest.i"
$$INC: buffer/asserts$$

MemoryManager_UnitTest_t MemoryManager_UnitTest;

int
main(int argc, char** argv)
{
    QUEX_NAME(Buffer)  reference;
    size_t             reference_size;
    size_t             new_size;
    ptrdiff_t          count;
    ptrdiff_t          shrink_n;

    hwut_info("Extend/Migrate Memory: Plain;"
              "CHOICES: 3, 4, 7, 21, 82;");

    reference_size = atoi(argv[1]);

    memset(&MemoryManager_UnitTest, 0, sizeof(MemoryManager_UnitTest));
    MemoryManager_UnitTest.allocation_addmissible_f = true;

    common_construct_reference_base(&reference, reference_size);

    count = 0;
    for(new_size = QUEX_MAX(3, reference_size - 1); 
        new_size <= reference_size + 2 ; ++new_size) {
        QUEX_BUFFER_ASSERT_CONSISTENCY(&reference);

        count += common_iterate(&reference, new_size, &shrink_n);
    }

    QUEX_NAME(Buffer_destruct)(&reference); 

    printf("<terminated: ((%i)); shrinked: ((%i)); allocated_byte_n: ((%i)); allocate_n: ((%i)); free_n: ((%i));>\n", 
           (int)count, (int)shrink_n,
           (int)MemoryManager_UnitTest.allocated_byte_n, 
           (int)MemoryManager_UnitTest.allocation_n, 
           (int)MemoryManager_UnitTest.free_n); 
}


            
