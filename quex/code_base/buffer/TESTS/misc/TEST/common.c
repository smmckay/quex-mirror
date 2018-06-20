#include <common.h>

#include "test_c/lib/buffer/Buffer.i"

int common_recursion_count_n = 0;

ptrdiff_t
common_iterate(QUEX_NAME(Buffer)* reference, size_t NewSize, ptrdiff_t* shrink_n) 
/* 'reference' -- reference buffer to be cloned into the test subject.
 * 'NewSize'   -- size of the memory to which the subject is to be migrated.
 *
 * EXITS:   As soon as an assertion fails.
 *
 * RETURNS: Number of performed experiments.                                  */
{
    size_t     reference_size = reference->_memory._back - reference->_memory._front + 1;
    ptrdiff_t  end_offset;
    ptrdiff_t  offset;
    ptrdiff_t  count = 0;
    QUEX_TYPE_LEXATOM_EXT tmp[3];

    /* Varry the offsets of '_read_p', '_lexeme_start_p', and 'input.end_p'.  */
    for(end_offset = 0; end_offset < reference_size-1; ++end_offset) {
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

            QUEX_BUFFER_ASSERT_CONSISTENCY(reference);
            common_test_single_migration(reference, NewSize, shrink_n);
            QUEX_BUFFER_ASSERT_CONSISTENCY(reference);
            common_test_single_extension(reference, NewSize);

            count += 1;

            reference->input.end_p[0]    = tmp[0];
            reference->_memory._front[0] = tmp[1];
            reference->_memory._back[0]  = tmp[2];
        }
    }
    return count;
}

void
common_clone(QUEX_NAME(Buffer)* reference, QUEX_NAME(Buffer)* subject)
{
    ptrdiff_t reference_size = reference->_memory._back - reference->_memory._front + 1;
    ptrdiff_t end_offset     = reference->input.end_p   - reference->_memory._front;
    ptrdiff_t i;

    __quex_assert(end_offset > 0);

    QUEX_BUFFER_ASSERT_CONSISTENCY(reference);

    QUEX_TYPE_LEXATOM_EXT* memory = (QUEX_TYPE_LEXATOM_EXT*)quex_MemoryManager_allocate(
                                        reference_size * sizeof(QUEX_TYPE_LEXATOM_EXT), 
                                        E_MemoryObjectType_BUFFER_MEMORY);

    QUEX_NAME(Buffer_construct)(subject, (QUEX_NAME(LexatomLoader)*)0,
                                memory, reference_size, &memory[reference_size-1],
                                E_Ownership_LEXICAL_ANALYZER,
                                (QUEX_NAME(Buffer)*)0);

    subject->input.end_p     = &subject->_memory._front[reference->input.end_p     - reference->_memory._front];
    subject->_read_p         = &subject->_memory._front[reference->_read_p         - reference->_memory._front];
    subject->_lexeme_start_p = &subject->_memory._front[reference->_lexeme_start_p - reference->_memory._front];

    /* Set reference content of the buffer.                                   */
    for(i=1; i<=reference_size; ++i) {
        if( i < end_offset ) {
            reference->_memory._front[i] = (QUEX_TYPE_LEXATOM_EXT)('a' + i);
            subject->_memory._front[i]   = (QUEX_TYPE_LEXATOM_EXT)('a' + i);
        }
        else if( i == end_offset ) {
            reference->_memory._front[i] = QUEX_SETTING_BUFFER_LIMIT_CODE;
            subject->_memory._front[i]   = QUEX_SETTING_BUFFER_LIMIT_CODE;
        }
        else {
            reference->_memory._front[i] = (QUEX_TYPE_LEXATOM_EXT)(0xAA);
            subject->_memory._front[i]   = (QUEX_TYPE_LEXATOM_EXT)(0xBB);
        }
    }
    reference->_memory._front[0] = QUEX_SETTING_BUFFER_LIMIT_CODE;
    reference->_memory._back[0]  = QUEX_SETTING_BUFFER_LIMIT_CODE;
    subject->_memory._front[0]   = QUEX_SETTING_BUFFER_LIMIT_CODE;
    subject->_memory._back[0]    = QUEX_SETTING_BUFFER_LIMIT_CODE;
    QUEX_BUFFER_ASSERT_CONSISTENCY(reference);
    QUEX_BUFFER_ASSERT_CONSISTENCY(subject);
}

void
common_test_single_migration(QUEX_NAME(Buffer)* reference, 
                             size_t             NewSize,
                             ptrdiff_t*         shrink_n)
{
    QUEX_NAME(Buffer)   subject; 
    bool                verdict_f = (&reference->input.end_p[1] - reference->_memory._front <= NewSize) ? true : false;
    E_Ownership         ownership = verdict_f ? E_Ownership_EXTERNAL : E_Ownership_LEXICAL_ANALYZER;
    QUEX_TYPE_LEXATOM_EXT   new_memory[256];

    hwut_verify(NewSize < 256);

    common_clone(reference, &subject);

    hwut_verify(
        verdict_f == QUEX_NAME(Buffer_nested_migrate(&subject, new_memory, NewSize, 
                                                     E_Ownership_EXTERNAL))
    );

    hwut_verify(ownership == subject._memory.ownership);

    if( common_verify(reference, &subject) ) { *shrink_n += 1; }

    QUEX_NAME(Buffer_destruct)(&subject); 
}

void
common_test_single_extension(QUEX_NAME(Buffer)* reference, size_t NewSize)
{
    QUEX_NAME(Buffer)   subject; 
    ptrdiff_t           reference_size = reference->_memory._back - reference->_memory._front + 1;

    common_clone(reference, &subject);

    QUEX_NAME(Buffer_nested_extend)(&subject, NewSize - reference_size); 

    hwut_verify(E_Ownership_LEXICAL_ANALYZER == subject._memory.ownership);

    common_verify(reference, &subject);

    QUEX_NAME(Buffer_destruct)(&subject); 
}

bool
common_verify(QUEX_NAME(Buffer)* reference, QUEX_NAME(Buffer)* subject)
/* RETURNS: 'true' if the buffer has been shrunk.                             */
{ 
    ptrdiff_t end_offset = reference->input.end_p - reference->_memory._front;
    ptrdiff_t i;
    QUEX_BUFFER_ASSERT_CONSISTENCY(reference);
    QUEX_BUFFER_ASSERT_CONSISTENCY(subject);
    QUEX_NAME(Buffer)*  root;

    common_verify_offset(reference, subject, reference->_read_p,         subject->_read_p);
    common_verify_offset(reference, subject, reference->_lexeme_start_p, subject->_lexeme_start_p);
    common_verify_offset(reference, subject, reference->input.end_p,     subject->input.end_p);

    hwut_verify(   reference->input.lexatom_index_begin 
                == subject->input.lexatom_index_begin);

    hwut_verify(   reference->input.lexatom_index_end_of_stream 
                == subject->input.lexatom_index_end_of_stream);
#   ifdef  QUEX_OPTION_SUPPORT_BEGIN_OF_LINE_PRE_CONDITION                 
    hwut_verify(   reference->_lexatom_reference_lexeme_start
                == subject->_lexatom_reference_lexeme_start);
#   endif
    hwut_verify(   reference->_backup_lexatom_index_of_lexeme_start_p
                == subject->_backup_lexatom_index_of_lexeme_start_p);

    if( memcmp((void*)reference->_memory._front, (void*)subject->_memory._front,
               (size_t)end_offset * sizeof(QUEX_TYPE_LEXATOM_EXT)) != 0 ) {

        root = QUEX_NAME(Buffer_nested_find_root)(reference);
        printf("reference.root: ((%p))\n", root->_memory._front);
        for(i=0; i<reference->input.end_p - reference->_memory._front + 1; ++i) 
        { printf("[%i]%02x.", 
                 (int)(reference->_memory._front - root->_memory._front + i), 
                 (int)reference->_memory._front[i]); }
        printf("\n");
        root = QUEX_NAME(Buffer_nested_find_root)(subject);
        printf("subject.root:   ((%p))\n", root->_memory._front);
        for(i=0; i<subject->input.end_p - subject->_memory._front + 1; ++i) 
        { printf("[%i]%02x.", 
                 (int)(subject->_memory._front - root->_memory._front + i), 
                 (int)subject->_memory._front[i]); }
        printf("\n");
        abort();
    }

    /* Recursion, if buffer is nested in including buffer. */
    if( reference->_memory.including_buffer ) {
        common_recursion_count_n += 1;

        hwut_verify(E_Ownership_INCLUDING_BUFFER == reference->_memory.ownership);

        hwut_verify(E_Ownership_INCLUDING_BUFFER == subject->_memory.ownership);
        hwut_verify(0                            != subject->_memory.including_buffer);

        /* The buffer size of including buffers shall not change at all! */
        hwut_verify(   reference->_memory.including_buffer->_memory._back - reference->_memory.including_buffer->_memory._front 
                    == subject->_memory.including_buffer->_memory._back   - subject->_memory.including_buffer->_memory._front);

        common_verify(reference->_memory.including_buffer, 
                      subject->_memory.including_buffer);

    }
    else {
        hwut_verify(0                            == subject->_memory.including_buffer);
        hwut_verify(E_Ownership_INCLUDING_BUFFER != subject->_memory.ownership);
    }

    /* Determine whether buffer has been shrunk. */
    return   reference->_memory._back  - reference->_memory._front 
           > subject->_memory._back    - subject->_memory._front;
}

void
common_verify_offset(QUEX_NAME(Buffer)* reference, QUEX_NAME(Buffer)* subject, 
                     QUEX_TYPE_LEXATOM_EXT* reference_p, QUEX_TYPE_LEXATOM_EXT* subject_p)
{
    ptrdiff_t offset_0 = reference_p - reference->_memory._front;
    ptrdiff_t offset_1 = subject_p   - subject->_memory._front;
       
    if( offset_0 == offset_1 ) { return; }

    printf("reference offset 0: %i; subject offset 1: %i;\n", 
           (int)offset_0, (int)offset_1);
    abort();

}


void
common_construct_reference_base(QUEX_NAME(Buffer)* reference, 
                                size_t             reference_size)
{
    QUEX_TYPE_LEXATOM_EXT* memory = (QUEX_TYPE_LEXATOM_EXT*)quex_MemoryManager_allocate(
                                      reference_size * sizeof(QUEX_TYPE_LEXATOM_EXT), 
                                      E_MemoryObjectType_BUFFER_MEMORY);

    QUEX_NAME(Buffer_construct)(reference, (QUEX_NAME(LexatomLoader)*)0,
                                memory, reference_size, &memory[reference_size-1],
                                E_Ownership_LEXICAL_ANALYZER,
                                (QUEX_NAME(Buffer)*)0);
    QUEX_BUFFER_ASSERT_CONSISTENCY(reference);
}

