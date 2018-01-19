/* PURPOSE: Extension and migration of buffer content.
 *
 *                   Buffer_extend_root() and 
 *                   Buffer_migrate_root()
 *
 * With the given functions it is possible to assign new memory to a buffer
 * and to extend it. Since a buffer might be 'living' in an including buffer,
 * the root of all including buffers is extended.
 *
 * CHOICES: plain    -- Buffer exists on its own.
 *          included -- Buffer hots a list of included buffers.
 *
 * (C) Frank-Rene Schaefer.                                                   */
#define  __QUEX_OPTION_PLAIN_C
/* #define  QUEX_OPTION_UNIT_TEST_MEMORY_MANAGER_VERBOSE */

#include <quex/code_base/extra/test_environment/TestAnalyzer-configuration>
#include <quex/code_base/definitions>
#include <quex/code_base/buffer/Buffer>
#include <quex/code_base/MemoryManager>
#include <quex/code_base/buffer/TESTS/MemoryManager_UnitTest.i>
#include <quex/code_base/buffer/Buffer.i>

#include <hwut_unit.h>
#include <stdio.h>
#include <stddef.h>

MemoryManager_UnitTest_t MemoryManager_UnitTest;

static void      self_construct_reference(QUEX_NAME(Buffer)* reference, 
                                          size_t             reference_size);
static void      self_construct_subject(QUEX_NAME(Buffer)* reference, 
                                        QUEX_NAME(Buffer)* subject);
static void      self_verify_offset(QUEX_NAME(Buffer)* reference, 
                                    QUEX_NAME(Buffer)* subject, 
                                    QUEX_TYPE_LEXATOM* reference_p, 
                                    QUEX_TYPE_LEXATOM* subject_p);
static void      self_verify(QUEX_NAME(Buffer)* reference, 
                             QUEX_NAME(Buffer)* subject);
static ptrdiff_t self_play_offsets(QUEX_NAME(Buffer)* reference, 
                                   size_t             NewSize,
                                   ptrdiff_t*         shrink_n);

int
main(int argc, char** argv)
{
    QUEX_NAME(Buffer)  reference;

    size_t    reference_size;
    size_t    new_size;
    ptrdiff_t count;
    ptrdiff_t shrink_n;

    hwut_info("Extend/Migrate Memory: Plain;"
              "CHOICES: 3, 4, 7, 21, 82;");

    reference_size = atoi(argv[1]);

    memset(&MemoryManager_UnitTest, 0, sizeof(MemoryManager_UnitTest));
    MemoryManager_UnitTest.allocation_addmissible_f = true;

    self_construct_reference(&reference, reference_size);

    count = 0;
    for(new_size = QUEX_MAX(3, reference_size - 1); 
        new_size <= reference_size + 2 ; ++new_size) {

        count += self_play_offsets(&reference, new_size, &shrink_n);

    }

    QUEX_NAME(Buffer_destruct)(&reference); 

    printf("<terminated: %i; shrinked: %i; allocated_byte_n: %i; allocate_n: %i; free_n: %i;>\n", 
           (int)count, (int)shrink_n,
           (int)MemoryManager_UnitTest.allocated_byte_n, 
           (int)MemoryManager_UnitTest.allocation_n, 
           (int)MemoryManager_UnitTest.free_n); 
}

static ptrdiff_t
self_play_offsets(QUEX_NAME(Buffer)* reference, size_t NewSize, ptrdiff_t* shrink_n) 
/* 'reference' -- reference buffer to be cloned into the test subject.
 * 'NewSize'   -- size of the memory to which the subject is to be migrated.
 *
 * EXITS:   As soon as an assertion fails.
 *
 * RETURNS: Number of performed experiments.                                  */
{
    size_t              reference_size = reference->_memory._back - reference->_memory._front + 1;
    ptrdiff_t           end_offset;
    ptrdiff_t           offset;
    QUEX_TYPE_LEXATOM   new_memory[256];
    ptrdiff_t           count = 0;
    bool                verdict_f;
    QUEX_NAME(Buffer)   subject_mig; /* subject to migration */
    //QUEX_NAME(Buffer)   subject_ext; /* subject to extension */

    hwut_verify(NewSize < 256);

    /* Varry the offsets of '_read_p', '_lexeme_start_p', and 'input.end_p'.  */
    for(end_offset = 0; end_offset != reference_size; ++end_offset) {
        for(offset = 0; offset <= end_offset ; ++offset) {
            
            /* Prepare                                                        */
            verdict_f = (reference->input.end_p - reference->_memory._front <= NewSize) ? true : false;

            reference->input.end_p     = &reference->_memory._front[end_offset];
            reference->_read_p         = &reference->_memory._front[offset + 1];
            reference->_lexeme_start_p = &reference->_memory._front[offset + 1];

            self_construct_subject(reference, &subject_mig);
            // self_construct_subject(reference, &subject_ext);

            /* Execute                                                        */
            hwut_verify(
                verdict_f == QUEX_NAME(Buffer_migrate_root(&subject_mig, new_memory, NewSize, 
                                                           E_Ownership_EXTERNAL))
            );

            /* Validate                                                       */
            if( verdict_f ) {
                hwut_verify(subject_mig._memory.ownership == E_Ownership_EXTERNAL);
            }
            else {
                hwut_verify(subject_mig._memory.ownership == E_Ownership_LEXICAL_ANALYZER);
            }

            if(   reference->_memory._back  - reference->_memory._front 
                > subject_mig._memory._back - subject_mig._memory._front) {
                *shrink_n += 1;
            }

            self_verify(reference, &subject_mig);

            QUEX_NAME(Buffer_destruct)(&subject_mig); 

            count += 1;
        }
    }
    return count;
}

static void
self_construct_reference(QUEX_NAME(Buffer)* reference, size_t reference_size)
{
    QUEX_TYPE_LEXATOM* memory = (QUEX_TYPE_LEXATOM*)QUEXED(MemoryManager_allocate)(
                                      reference_size * sizeof(QUEX_TYPE_LEXATOM), 
                                      E_MemoryObjectType_BUFFER_MEMORY);

    QUEX_NAME(Buffer_construct)(reference, (QUEX_NAME(LexatomLoader)*)0,
                                memory, reference_size, &memory[reference_size-1],
                                E_Ownership_LEXICAL_ANALYZER,
                                (QUEX_NAME(Buffer)*)0);

}

static void
self_construct_subject(QUEX_NAME(Buffer)* reference, QUEX_NAME(Buffer)* subject)
{
    ptrdiff_t reference_size = reference->_memory._back - reference->_memory._front + 1;
    ptrdiff_t end_offset     = reference->input.end_p   - reference->_memory._front;
    ptrdiff_t i;

    QUEX_TYPE_LEXATOM* memory = (QUEX_TYPE_LEXATOM*)QUEXED(MemoryManager_allocate)(
                                        reference_size * sizeof(QUEX_TYPE_LEXATOM), 
                                        E_MemoryObjectType_BUFFER_MEMORY);

    QUEX_NAME(Buffer_construct)(subject, (QUEX_NAME(LexatomLoader)*)0,
                                memory, reference_size, &memory[reference_size-1],
                                E_Ownership_LEXICAL_ANALYZER,
                                (QUEX_NAME(Buffer)*)0);

    memset((void*)&subject->_memory._front[end_offset], 
           0x5A, 
           (reference_size - end_offset) * sizeof(QUEX_TYPE_LEXATOM));

    subject->input.end_p     = &subject->_memory._front[reference->input.end_p     - reference->_memory._front];
    subject->_read_p         = &subject->_memory._front[reference->_read_p         - reference->_memory._front];
    subject->_lexeme_start_p = &subject->_memory._front[reference->_lexeme_start_p - reference->_memory._front];

    for(i=1; i<=reference_size; ++i) {
        if( i < end_offset ) {
            reference->_memory._front[i] = (QUEX_TYPE_LEXATOM)('a' + i);
            subject->_memory._front[i]   = (QUEX_TYPE_LEXATOM)('a' + i);
        }
        else if( i == end_offset ) {
            reference->_memory._front[i] = (QUEX_TYPE_LEXATOM)(0);
            subject->_memory._front[i]   = (QUEX_TYPE_LEXATOM)(0);
        }
        else {
            reference->_memory._front[i] = (QUEX_TYPE_LEXATOM)(0xAA);
            subject->_memory._front[i]   = (QUEX_TYPE_LEXATOM)(0xBB);
        }
    }
}

            
static void
self_verify(QUEX_NAME(Buffer)* reference, QUEX_NAME(Buffer)* subject)
{ 
    ptrdiff_t end_offset = reference->input.end_p - reference->_memory._front;
    ptrdiff_t i;

    self_verify_offset(reference, subject, reference->_read_p,         subject->_read_p);
    self_verify_offset(reference, subject, reference->_lexeme_start_p, subject->_lexeme_start_p);
    self_verify_offset(reference, subject, reference->input.end_p,     subject->input.end_p);

    hwut_verify(   reference->input.lexatom_index_begin 
                == subject->input.lexatom_index_begin);
    hwut_verify(   reference->input.lexatom_index_end_of_stream 
                == subject->input.lexatom_index_end_of_stream);
#   ifdef  __QUEX_OPTION_SUPPORT_BEGIN_OF_LINE_PRE_CONDITION                 
    hwut_verify(   reference->_lexatom_reference_lexeme_start
                == subject->_lexatom_reference_lexeme_start);
#   endif
    hwut_verify(   reference->_backup_lexatom_index_of_read_p
                == subject->_backup_lexatom_index_of_read_p);

    if( memcmp((void*)reference->_memory._front, (void*)subject->_memory._front,
               (size_t)end_offset * sizeof(QUEX_TYPE_LEXATOM)) != 0 ) {
        for(i=0; i<end_offset; ++i) 
        { printf("%02x.", (int)reference->_memory._front[i]); }
        printf("\n");
        for(i=0; i<end_offset; ++i) 
        { printf("%02x.", (int)subject->_memory._front[i]); }
        printf("\n");
        abort();
    }
}

static void
self_verify_offset(QUEX_NAME(Buffer)* reference, QUEX_NAME(Buffer)* subject, 
                   QUEX_TYPE_LEXATOM* reference_p, QUEX_TYPE_LEXATOM* subject_p)
{
    ptrdiff_t offset_0 = reference_p - reference->_memory._front;
    ptrdiff_t offset_1 = subject_p   - subject->_memory._front;
       
    if( offset_0 == offset_1 ) { return; }

    printf("reference offset 0: %i; subject offset 1: %i;\n", 
           (int)offset_0, (int)offset_1);
    abort();

}
