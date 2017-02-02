/* PURPOSE: Test constructor and destructor functions.
 *
 * Constructors come in three flavors (== CHOICES): 
 *
 *    filen-name:  based on a file name.
 *    byte-loader: based on ByteLoader and Converter objects.
 *    memory:      based on memory chunks.
 *
 * Construction may fail, due to memory allocation failure or due to failure
 * of the user constructor. For all three flavors all memory allocations
 * failures are considered and the consequences are checked. 
 *
 * The destruction must be possible in any case. Thus it is performed for
 * each an every lexer that is subject to a construction try.
 *
 * Test is best run inside a 'valgrind' session, so that memory leaks may be
 * properly detected.
 *
 * (C) 2017 Frank-Rene Schaefer                                               */
#include <TestAnalyzer.h>
#include <quex/code_base/MemoryManager>
#include <quex/code_base/buffer/TESTS/MemoryManager_UnitTest.i>
#include <hwut_unit.h>

MemoryManager_UnitTest_t MemoryManager_UnitTest;
bool                     UserConstructor_UnitTest_return_value;

static void self_file_name();
static void self_byte_loader();
static void self_memory();
static void self_destruct(quex_TestAnalyzer* lexer, size_t N);

int
main(int argc, char** argv)
{
    hwut_info("Constructor;\n"
              "CHOICES: file-name, byte-loader, memory;");

    memset(&MemoryManager_UnitTest, 0, sizeof(MemoryManager_UnitTest));

    MemoryManager_UnitTest.allocation_addmissible_f = true;
    UserConstructor_UnitTest_return_value           = true;

    hwut_if_choice("file-name")   self_file_name(); 
    hwut_if_choice("byte-loader") self_byte_loader(); 
    hwut_if_choice("memory")      self_memory(); 

    return 0;
}

static void 
self_file_name()
{
    quex_TestAnalyzer  lexer[3];
    quex_TestAnalyzer* lx = &lexer[0];

    {
        QUEX_NAME(from_file_name)(lx, "file-that-does-not-exists.txt", NULL);
        hwut_verify(  QUEX_NAME(resources_absent)(lx));
    }

    ++lx;
    {
        QUEX_NAME(from_file_name)(lx, "file-that-exists.txt", NULL);
        hwut_verify(! QUEX_NAME(resources_absent)(lx));
    }

    ++lx;
    {
        MemoryManager_UnitTest.forbid_ByteLoader_f = true;
        QUEX_NAME(from_file_name)(lx, "file-that-exists.txt", NULL);
        hwut_verify(lx->error_code = E_Error_Allocation_ByteLoader_Failed); 
        hwut_verify(QUEX_NAME(resources_absent)(lx));
        MemoryManager_UnitTest.forbid_ByteLoader_f    = false;
    }

    ++lx;
    {
        MemoryManager_UnitTest.forbid_LexatomLoader_f = true;
        QUEX_NAME(from_file_name)(lx, "file-that-exists.txt", NULL);
        hwut_verify(lx->error_code = E_Error_Allocation_LexatomLoader_Failed); 
        hwut_verify(QUEX_NAME(resources_absent)(lx));
        MemoryManager_UnitTest.forbid_LexatomLoader_f = false;
    }

    ++lx;
    {
        MemoryManager_UnitTest.forbid_BufferMemory_f = true;
        QUEX_NAME(from_file_name)(lx, "file-that-exists.txt", NULL);
        hwut_verify(lx->error_code = E_Error_Allocation_BufferMemory_Failed); 
        hwut_verify(QUEX_NAME(resources_absent)(lx));
        MemoryManager_UnitTest.forbid_BufferMemory_f = false;
    }

    ++lx;
    {
        UserConstructor_UnitTest_return_value = false;
        QUEX_NAME(from_file_name)(lx, "file-that-exists.txt", NULL);
        hwut_verify(lx->error_code = E_Error_UserConstructor_Failed); 
        hwut_verify(QUEX_NAME(resources_absent)(lx));
        UserConstructor_UnitTest_return_value = true;
    }

    ++lx;
    {
        MemoryManager_UnitTest.forbid_InputName_f = true;
        QUEX_NAME(from_file_name)(lx, "file-that-exists.txt", NULL);
        hwut_verify(lx->error_code = E_Error_InputName_Set_Failed); 
        hwut_verify(QUEX_NAME(resources_absent)(lx));
        MemoryManager_UnitTest.forbid_InputName_f = false;
    }

    /* Destruct safely all lexers. */
    self_destruct(&lexer[0], lx - &lexer[0]);
}

static void 
self_byte_loader()
{
    quex_TestAnalyzer lexer[2];
    QUEX_NAME(ByteLoader)*   byte_loader;
    QUEX_NAME(Converter)*    converter;
    QUEX_NAME(from_ByteLoader)(&lexer[0], byte_loader, converter);
}

static void 
self_memory()
{
    quex_TestAnalyzer lexer[2];
    uint8_t   memory[65536];
    QUEX_NAME(from_memory)(&lexer[0], &memory[0], 65536, NULL);
}

static void
self_destruct(quex_TestAnalyzer* lexer, size_t N)
{
    int i;

    for(i=0; i<N; ++i) {
        QUEX_NAME(destruct)(&lexer[i]);
        hwut_verify(QUEX_NAME(resources_absent)(&lexer[i]));
    }
}

