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

#include <quex/code_base/extra/test_environment/TestAnalyzer-configuration>
#include <quex/code_base/buffer/TESTS/MemoryManager_UnitTest.i>
#include <quex/code_base/definitions>
#include <quex/code_base/buffer/Buffer>
#include <quex/code_base/MemoryManager>
#include <quex/code_base/buffer/Buffer.i>

#include <hwut_unit.h>

static void
self_verify_offset(QUEX_NAME(Buffer)* before, QUEX_TYPE_LEXATOM* before_p, 
                   QUEX_NAME(Buffer)* after, QUEX_TYPE_LEXATOM* after_p);
static void
self_verify(QUEX_NAME(Buffer)* before, QUEX_NAME(Buffer)* after);
static void
self_play_offsets(QUEX_NAME(Buffer)* before, QUEX_NAME(Buffer)* after);

int
main(int argc, char** argv)
{
    const size_t       MemorySize = QUEX_SETTING_BUFFER_SIZE;
    QUEX_TYPE_LEXATOM* memory0;
    QUEX_TYPE_LEXATOM* memory1;
    QUEX_NAME(Buffer)  before;
    QUEX_NAME(Buffer)  after;

    hwut_info("Extend/Migrate Memory;"
              "CHOICES: 0, included;");

    QUEX_NAME(Buffer_construct)(before, 
                                (QUEX_NAME(LexatomLoader)*)0,
                                memory0, before_size, &memory[before_size+1],
                                E_Ownership_EXTERNAL);

    for(size = before_size - 1 ; size <= before_size + 1 ; ++ size) {
        memory1 = (QUEX_TYPE_LEXATOM*)QUEXED(MemoryManager_allocate)(
                            size * sizeof(QUEX_TYPE_LEXATOM), 
                            E_MemoryObjectType_BUFFER_MEMORY);

        QUEX_NAME(Buffer_construct)(after, 
                                    (QUEX_NAME(LexatomLoader)*)0,
                                    memory1, size, &memory[size+1],
                                    E_Ownership_EXTERNAL);

        self_play_offsets(before, after);
    }
}

static void
self_play_offsets(QUEX_NAME(Buffer)* before, QUEX_NAME(Buffer)* after) 
{
    ptrdiff_t end_offset;
    ptrdiff_t offset;

    for(end_offset = 0; 
        end_offset != buffer._memory._back - buffer._memory._front; 
        ++end_offset) {

        before.input.end_p = &buffer._memory._front[end_offset + 1];

        for(offset = 0; offset <= end_offset ; ++offset) {
            before._read_p         = &buffer._memory._front[offset + 1];
            before._lexeme_start_p = &buffer._memory._front[offset + 1];
            
            buffer._read_p         = before._read_p;
            buffer._lexeme_start_p = before._lexeme_start_p;

            QUEX_NAME(Buffer_migrate(&buffer, new_memory, E_Ownership_EXTERNAL));

            hwut_verify(buffer._memory.ownership = ownership);

            self_verify(before, after);
        }
    }
}

static void
self_verify(QUEX_NAME(Buffer)* before, QUEX_NAME(Buffer)* after)
{ 
    self_verify_offset(before, after, before._read_p,         after._read_p);
    self_verify_offset(before, after, before._lexeme_start_p, after._lexeme_start_p);
    self_verify_offset(before, after, before.input.end_p,     after.input.end_p);

    self_verify_offset(   before->input.lexatom_index_begin 
                       == after->input.lexatom_index_begin);
    self_verify_offset(   before->input.lexatom_index_end_of_stream 
                       == after->input.lexatom_index_end_of_stream);
#   ifdef  __QUEX_OPTION_SUPPORT_BEGIN_OF_LINE_PRE_CONDITION                 
    self_verify_offset(   before->_lexatom_before_lexeme_start
                       == after->_lexatom_before_lexeme_start);
#   endif
    self_verify_offset(   before->_backup_lexatom_index_of_read_p
                       == after->_backup_lexatom_index_of_read_p);
}

static void
self_verify_offset(QUEX_NAME(Buffer)* before, QUEX_TYPE_LEXATOM* before_p, 
                   QUEX_NAME(Buffer)* after, QUEX_TYPE_LEXATOM* after_p)
{
    hwut_verify(   before_p - before->_memory._front
                == after_p  - after->_memory._front);
}
