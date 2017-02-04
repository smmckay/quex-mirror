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

static void self_file_name();
static void self_byte_loader();
static void self_memory();
static void self_destruct(quex_TestAnalyzer* lexer, size_t N);
static void self_assert(quex_TestAnalyzer* lexer, E_Error ExpectedError);
static void self_byte_loader_core(E_Error ExpectedError);

quex_TestAnalyzer  lexer[128];
quex_TestAnalyzer* lx;

int
main(int argc, char** argv)
{
    hwut_info("Constructor;\n"
              "CHOICES: file-name, byte-loader, memory;\n");

    memset(&MemoryManager_UnitTest, 0, sizeof(MemoryManager_UnitTest));

    MemoryManager_UnitTest.allocation_addmissible_f = true;
    UserConstructor_UnitTest_return_value           = true;


    memset(&lexer[0], 0x5A, sizeof(lexer));            /* Poisson all memory. */
    lx = &lexer[0];

    hwut_if_choice("file-name")   self_file_name(); 
    hwut_if_choice("byte-loader") self_byte_loader(); 
    hwut_if_choice("memory")      self_memory(); 

    /* Destruct safely all lexers. */
    self_destruct(&lexer[0], lx - &lexer[0]);

    printf("<terminated: %i>\n", (int)(lx- &lexer[0]));

    return 0;
}

static void 
self_file_name()
{
    /* Good case                                                              */
    {
        QUEX_NAME(from_file_name)(lx, "file-that-exists.txt", NULL);
        self_assert(lx, E_Error_None);
    }

    /* Bad cases                                                              */
    ++lx;
    {
        QUEX_NAME(from_file_name)(lx, "file-that-does-not-exists.txt", NULL);
        self_assert(lx, E_Error_Allocation_ByteLoader_Failed);
    }

    ++lx;
    {
        MemoryManager_UnitTest.forbid_ByteLoader_f = true;
        QUEX_NAME(from_file_name)(lx, "file-that-exists.txt", NULL);
        self_assert(lx, E_Error_Allocation_ByteLoader_Failed); 
        MemoryManager_UnitTest.forbid_ByteLoader_f    = false;
    }

    ++lx;
    {
        MemoryManager_UnitTest.forbid_LexatomLoader_f = true;
        QUEX_NAME(from_file_name)(lx, "file-that-exists.txt", NULL);
        self_assert(lx, E_Error_Allocation_LexatomLoader_Failed); 
        MemoryManager_UnitTest.forbid_LexatomLoader_f = false;
    }

    ++lx;
    {
        MemoryManager_UnitTest.forbid_BufferMemory_f = true;
        QUEX_NAME(from_file_name)(lx, "file-that-exists.txt", NULL);
        self_assert(lx, E_Error_Allocation_BufferMemory_Failed); 
        MemoryManager_UnitTest.forbid_BufferMemory_f = false;
    }

    ++lx;
    {
        UserConstructor_UnitTest_return_value = false;
        QUEX_NAME(from_file_name)(lx, "file-that-exists.txt", NULL);
        self_assert(lx, E_Error_UserConstructor_Failed); 
        UserConstructor_UnitTest_return_value = true;
    }

    ++lx;
    {
        MemoryManager_UnitTest.forbid_InputName_f = true;
        QUEX_NAME(from_file_name)(lx, "file-that-exists.txt", NULL);
        self_assert(lx, E_Error_InputName_Set_Failed); 
        MemoryManager_UnitTest.forbid_InputName_f = false;
    }
}

static void 
self_byte_loader()
{
    /* Good cases                                                             */
    self_byte_loader_core(E_Error_None);

    /* Bad cases                                                              */
    self_byte_loader_core(E_Error_Allocation_LexatomLoader_Failed);
    self_byte_loader_core(E_Error_Allocation_BufferMemory_Failed);
    self_byte_loader_core(E_Error_InputName_Set_Failed);
    self_byte_loader_core(E_Error_UserConstructor_Failed);
}

static void
self_byte_loader_core(E_Error ExpectedError)
{
    QUEX_NAME(ByteLoader)* byte_loader;
    QUEX_NAME(Converter)*  converter;
    bool                   success_f = false;

    switch( ExpectedError ) {
    case E_Error_Allocation_ByteLoader_Failed:
        assert(false); /* Not subject to test, here. */
        break;
    case E_Error_Allocation_LexatomLoader_Failed:
        MemoryManager_UnitTest.forbid_LexatomLoader_f = true;
        break;
    case E_Error_Allocation_BufferMemory_Failed:
        MemoryManager_UnitTest.forbid_BufferMemory_f = true;
        break;
    case E_Error_InputName_Set_Failed:
        MemoryManager_UnitTest.forbid_InputName_f = true;
        break;
    case E_Error_UserConstructor_Failed:
        UserConstructor_UnitTest_return_value = false;
        break;
    case E_Error_None:
        success_f = true;
        break;
    }
    {
        byte_loader = QUEX_NAME(ByteLoader_FILE_new_from_file_name)("file-that-exists.txt");
        converter   = QUEX_NAME(Converter_IConv_new)("UTF8", NULL);
        QUEX_NAME(from_ByteLoader)(lx, byte_loader, converter);
        self_assert(lx, ExpectedError);
    }
    ++lx;
    {
        byte_loader = QUEX_NAME(ByteLoader_FILE_new_from_file_name)("file-that-exists.txt");
        converter   = NULL;
        QUEX_NAME(from_ByteLoader)(lx, byte_loader, converter);
        self_assert(lx, ExpectedError);
    }
    ++lx;
    {
        byte_loader = NULL;
        converter   = QUEX_NAME(Converter_IConv_new)("UTF8", NULL);
        QUEX_NAME(from_ByteLoader)(lx, byte_loader, converter);
        self_assert(lx, ExpectedError);
    }
    ++lx;
    {
        byte_loader = NULL;
        converter   = NULL;
        QUEX_NAME(from_ByteLoader)(lx, byte_loader, converter);
        self_assert(lx, ExpectedError);
    }
    ++lx;

    MemoryManager_UnitTest.forbid_ByteLoader_f    = false;
    MemoryManager_UnitTest.forbid_LexatomLoader_f = false;
    MemoryManager_UnitTest.forbid_BufferMemory_f  = false;
    MemoryManager_UnitTest.forbid_InputName_f     = false;
    UserConstructor_UnitTest_return_value         = true;
}

static void 
self_memory()
{
    uint8_t memory[65536];

    MemoryManager_UnitTest.forbid_ByteLoader_f    = false;
    MemoryManager_UnitTest.forbid_LexatomLoader_f = false;
    MemoryManager_UnitTest.forbid_BufferMemory_f  = false;
    MemoryManager_UnitTest.forbid_InputName_f     = false;

    memset(&memory[0], 0x5A, sizeof(memory));
    memory[0]       = QUEX_SETTING_BUFFER_LIMIT_CODE;
    memory[65536-1] = QUEX_SETTING_BUFFER_LIMIT_CODE;

    {
        QUEX_NAME(from_memory)(lx, &memory[0], 65536, &memory[65536-1]);
        self_assert(lx, E_Error_None);
    }
    ++lx;
    {
        /* No alloaction of byte loader, lexatom loader or memory needed. */
        MemoryManager_UnitTest.forbid_ByteLoader_f    = false;
        MemoryManager_UnitTest.forbid_LexatomLoader_f = false;
        MemoryManager_UnitTest.forbid_BufferMemory_f  = false;

        QUEX_NAME(from_memory)(lx, &memory[0], 65536, &memory[65536-1]);
        self_assert(lx, E_Error_None);
    }
    ++lx;
    {
        UserConstructor_UnitTest_return_value = false;
        QUEX_NAME(from_memory)(lx, &memory[0], 65536, &memory[65536-1]);
        self_assert(lx, E_Error_UserConstructor_Failed);
        UserConstructor_UnitTest_return_value = true;
    }
    ++lx;
    {
        MemoryManager_UnitTest.forbid_InputName_f = true;
        QUEX_NAME(from_memory)(lx, &memory[0], 65536, &memory[65536-1]);
        self_assert(lx, E_Error_InputName_Set_Failed);

        MemoryManager_UnitTest.forbid_InputName_f = false;
    }
    ++lx;

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

static void 
self_assert(quex_TestAnalyzer* lexer, E_Error ExpectedError)
{
    hwut_verify(lx->error_code == ExpectedError);

    if( ExpectedError != E_Error_None ) {
        hwut_verify(QUEX_NAME(resources_absent)(lx));
    }
    else {
        hwut_verify(! QUEX_NAME(resources_absent)(lx));
    }
}
