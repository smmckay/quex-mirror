/* PURPOSE: Test reset functions.
 *
 * Reset functions come in three flavors (== CHOICES): 
 *
 *    filen-name:  based on a file name.
 *    byte-loader: based on ByteLoader and Converter objects.
 *    memory:      based on memory chunks.
 *    plain:       based on current state of objects.
 *
 * Important:
 *              RESET != DESTRUCTOR + CONSTRUCTOR
 *
 * because DESTRUCTOR and CONSTRUCTOR may involve resource de-allocation and
 * resource re-allocation. Reset, instead may work on existing resources.
 *
 * Reset may fail, due to memory allocation failure or due to failure
 * of the user constructor. For all three flavors all memory allocations
 * failures are considered and the consequences are checked. 
 *
 * Resets are performed on four states:
 *    -- lexer has been constructed with loader (and converter)
 *    -- lexer has been constructed on memory
 *    -- lexer construction failure (resources marked absent)
 *
 * Test is best run inside a 'valgrind' session, so that memory leaks may be
 * properly detected.
 *
 * (C) 2017 Frank-Rene Schaefer                                               */
#include <test_c/TestAnalyzer.h>
#include "test_c/lib/quex/MemoryManager"
#include "test_c/lib/buffer/lexatoms/converter/iconv/Converter_IConv"
#include "test_c/lib/buffer/lexatoms/converter/iconv/Converter_IConv.i"
#include "test_c/lib/buffer/lexatoms/converter/icu/Converter_ICU"
#include "test_c/lib/buffer/lexatoms/converter/icu/Converter_ICU.i"
#include "MemoryManager_UnitTest.i"
#include <hwut_unit.h>
#include <common.h>

MemoryManager_UnitTest_t MemoryManager_UnitTest;

static void self_reset_on_loader(int argc, char** argv);
static void self_reset_on_memory(int argc, char** argv);

/* CHOICES: */
static void self_file_name();
static void self_byte_loader();
static void self_byte_loader_core(E_Error ExpectedError);
static void self_memory();
static void self_plain();

static void self_destruct(TestAnalyzer* lexer, size_t N);
static void self_assert(TestAnalyzer* lexer, E_Error ExpectedError);

TestAnalyzer        lexer[24];
const TestAnalyzer* lexerEnd = &lexer[24];
TestAnalyzer*       lx;

int
main(int argc, char** argv)
{
    hwut_info("Reset;\n"
              "CHOICES: file-name, byte-loader, memory, plain;\n");

    memset(&MemoryManager_UnitTest, 0, sizeof(MemoryManager_UnitTest));

    MemoryManager_UnitTest.allocation_addmissible_f = true;

    self_reset_on_loader(argc, argv);
    hwut_verify(lx <= &lexer[24]);

    self_reset_on_memory(argc, argv);
    hwut_verify(lx <= &lexer[24]);

    return 0;
}

static void
self_reset_on_loader(int argc, char** argv)
{
    /* Construct: ByteLoader */
    UserConstructor_UnitTest_return_value = true; 
    UserReset_UnitTest_return_value       = false; /* Shall not be called! */

    memset(&lexer[0], 0x5A, sizeof(lexer)); /* Poisson all memory. */
    for(lx=&lexer[0]; lx != lexerEnd; ++lx) {
        TestAnalyzer_from_file_name(lx, "file-that-exists.txt", NULL);
        common_token_queue_dummy_setup(lx);
        assert(lx->error_code == E_Error_None);
    }

    /* Reset */
    UserConstructor_UnitTest_return_value = false; /* Shall not be called! */
    UserReset_UnitTest_return_value       = true;
    UserMementoPack_UnitTest_return_value = false;

    lx = &lexer[0];
    hwut_if_choice("file-name")   self_file_name(); 
    hwut_if_choice("byte-loader") self_byte_loader(); 
    hwut_if_choice("memory")      self_memory(); 
    hwut_if_choice("plain")       self_plain(); 

    /* Destruct safely all lexers. */
    self_destruct(&lexer[0], lexerEnd - &lexer[0]);
    printf("<terminated 'byte loader': %i>\n", (int)(lx- &lexer[0]));
}

static void
self_reset_on_memory(int argc, char** argv)
{
    uint8_t memory[65536];

    memset(&memory[0], 0x5A, sizeof(memory));
    memory[0]       = QUEX_SETTING_BUFFER_LIMIT_CODE;
    memory[65536-1] = QUEX_SETTING_BUFFER_LIMIT_CODE;

    UserConstructor_UnitTest_return_value = true; 
    UserReset_UnitTest_return_value       = false; /* Shall not be called! */
    UserMementoPack_UnitTest_return_value = false;

    /* Construct: Memory */
    memset(&lexer[0], 0x5A, sizeof(lexer)); /* Poisson all memory. */
    for(lx=&lexer[0]; lx != lexerEnd; ++lx) {
        TestAnalyzer_from_memory(lx, &memory[0], 65536, &memory[65536-1]);
        common_token_queue_dummy_setup(lx);
        assert(lx->error_code == E_Error_None);
    }

    /* Reset */
    UserConstructor_UnitTest_return_value = false; /* Shall not be called! */
    UserReset_UnitTest_return_value       = true;

    lx = &lexer[0];
    hwut_if_choice("file-name")   self_file_name(); 
    hwut_if_choice("byte-loader") self_byte_loader(); 
    hwut_if_choice("memory")      self_memory(); 
    hwut_if_choice("plain")       self_plain(); 

    /* Destruct safely all lexers. */
    self_destruct(&lexer[0], lexerEnd - &lexer[0]);

    printf("<terminated 'memory': %i>\n", (int)(lx- &lexer[0]));
}

static void 
self_file_name()
{
    /* Good case                                                              */
    {
        lx->reset_file_name(lx, "file-that-exists.txt", NULL);
        self_assert(lx, E_Error_None);
    }

    /* Bad cases                                                              */
    ++lx;
    {
        lx->reset_file_name(lx, "file-that-does-not-exists.txt", NULL);
        self_assert(lx, E_Error_File_OpenFailed);
    }
    ++lx;
    {
        MemoryManager_UnitTest.forbid_ByteLoader_f = true;
        lx->reset_file_name(lx, "file-that-exists.txt", NULL);
        self_assert(lx, E_Error_File_OpenFailed); 
        MemoryManager_UnitTest.forbid_ByteLoader_f    = false;
    }
    ++lx;
    {
        MemoryManager_UnitTest.forbid_LexatomLoader_f = true;
        lx->reset_file_name(lx, "file-that-exists.txt", NULL);
        self_assert(lx, E_Error_Allocation_LexatomLoader_Failed); 
        MemoryManager_UnitTest.forbid_LexatomLoader_f = false;
    }
    ++lx;
    {   /* Buffer Memory allocation is not required => No Error!              */
        MemoryManager_UnitTest.forbid_BufferMemory_f = true;
        lx->reset_file_name(lx, "file-that-exists.txt", NULL);
        self_assert(lx, E_Error_None); 
        MemoryManager_UnitTest.forbid_BufferMemory_f = false;
    }
    ++lx;
    {
        UserReset_UnitTest_return_value = false;
        lx->reset_file_name(lx, "file-that-exists.txt", NULL);
        self_assert(lx, E_Error_UserReset_Failed); 
        UserReset_UnitTest_return_value = true;
    }
    ++lx;
    {
        MemoryManager_UnitTest.forbid_InputName_f = true;
        lx->reset_file_name(lx, "file-that-exists.txt", NULL);
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
    self_byte_loader_core(E_Error_Allocation_ByteLoader_Failed);
    self_byte_loader_core(E_Error_Allocation_LexatomLoader_Failed);
    self_byte_loader_core(E_Error_Allocation_BufferMemory_Failed);
    self_byte_loader_core(E_Error_InputName_Set_Failed);
    self_byte_loader_core(E_Error_UserReset_Failed);
}

static void
self_byte_loader_core(E_Error ExpectedError)
{
    TestAnalyzer_ByteLoader* byte_loader;
    TestAnalyzer_Converter*  converter;

    switch( ExpectedError ) {
    case E_Error_Allocation_ByteLoader_Failed:
        ExpectedError = E_Error_None;
        break;
    case E_Error_Allocation_LexatomLoader_Failed:
        MemoryManager_UnitTest.forbid_LexatomLoader_f = true;
        break;
    case E_Error_Allocation_BufferMemory_Failed:
        MemoryManager_UnitTest.forbid_BufferMemory_f = true;
        ExpectedError = E_Error_None;
        break;
    case E_Error_InputName_Set_Failed:
        MemoryManager_UnitTest.forbid_InputName_f = true;
        ExpectedError = E_Error_None;
        break;
    case E_Error_UserReset_Failed:
        UserReset_UnitTest_return_value = false;
        break;
    case E_Error_None:
        break;
    default:
        assert(false);
        break;
    }

    {
        byte_loader = TestAnalyzer_ByteLoader_FILE_new_from_file_name("file-that-exists.txt");
        converter   = TestAnalyzer_Converter_IConv_new("UTF8", NULL);
        lx->reset_ByteLoader(lx, byte_loader, converter);
        self_assert(lx, ExpectedError);
    }
    ++lx;
    {
        byte_loader = TestAnalyzer_ByteLoader_FILE_new_from_file_name("file-that-exists.txt");
        converter   = NULL;
        lx->reset_ByteLoader(lx, byte_loader, converter);
        self_assert(lx, ExpectedError);
    }
    ++lx;
    {
        byte_loader = NULL;
        converter   = TestAnalyzer_Converter_IConv_new("UTF8", NULL);
        lx->reset_ByteLoader(lx, byte_loader, converter);
        self_assert(lx, ExpectedError);
    }
    ++lx;
    {
        byte_loader = NULL;
        converter   = NULL;
        lx->reset_ByteLoader(lx, byte_loader, converter);
        self_assert(lx, ExpectedError);
    }
    ++lx;

    MemoryManager_UnitTest.forbid_ByteLoader_f    = false;
    MemoryManager_UnitTest.forbid_LexatomLoader_f = false;
    MemoryManager_UnitTest.forbid_BufferMemory_f  = false;
    MemoryManager_UnitTest.forbid_InputName_f     = false;
    UserReset_UnitTest_return_value               = true;
}

static void 
self_memory()
{
    uint8_t memory[65536];

    memset(&memory[0], 0x5A, sizeof(memory));
    memory[0]       = QUEX_SETTING_BUFFER_LIMIT_CODE;
    memory[65536-1] = QUEX_SETTING_BUFFER_LIMIT_CODE;

    {
        lx->reset_memory(lx, &memory[0], 65536, &memory[65536-1]);
        self_assert(lx, E_Error_None);
    }
    ++lx;
    {
        /* No alloaction of byte loader, lexatom loader or memory needed. */
        MemoryManager_UnitTest.forbid_ByteLoader_f    = true;
        MemoryManager_UnitTest.forbid_LexatomLoader_f = true;
        MemoryManager_UnitTest.forbid_BufferMemory_f  = true;

        lx->reset_memory(lx, &memory[0], 65536, &memory[65536-1]);
        self_assert(lx, E_Error_None);
    }
    ++lx;
    {
        UserReset_UnitTest_return_value = false;
        lx->reset_memory(lx, &memory[0], 65536, &memory[65536-1]);
        self_assert(lx, E_Error_UserReset_Failed);
        UserReset_UnitTest_return_value = true;
    }
    ++lx;
    {
        MemoryManager_UnitTest.forbid_InputName_f = true;
        lx->reset_memory(lx, &memory[0], 65536, &memory[65536-1]);
        self_assert(lx, E_Error_None);

        MemoryManager_UnitTest.forbid_InputName_f = false;
    }
    ++lx;
}

static void 
self_plain()
{
    /* Good case (no allocation required) */
    MemoryManager_UnitTest.allocation_addmissible_f = true;  /* Allow 'TEXT' */
    MemoryManager_UnitTest.forbid_ByteLoader_f      = false;
    MemoryManager_UnitTest.forbid_LexatomLoader_f   = false;
    MemoryManager_UnitTest.forbid_BufferMemory_f    = false;
    MemoryManager_UnitTest.forbid_InputName_f       = false;
    UserConstructor_UnitTest_return_value           = false; /* Shall not be called! */
    UserReset_UnitTest_return_value                 = true;
    {
        lx->reset(lx);
        self_assert(lx, E_Error_None);
        hwut_verify(! TestAnalyzer_MF_resources_absent(lx));
    }
    ++lx;

    /* Bad case (User reset fails) */
    UserConstructor_UnitTest_return_value           = false; /* Shall not be called! */
    UserReset_UnitTest_return_value                 = false;
    {
        lx->reset(lx);
        self_assert(lx, E_Error_UserReset_Failed);
        hwut_verify(TestAnalyzer_MF_resources_absent(lx));
    }
    ++lx;
}

static void
self_destruct(TestAnalyzer* lexer, size_t N)
{
    int i;

    for(i=0; i<N; ++i) {
        TestAnalyzer_destruct(&lexer[i]);
        hwut_verify(TestAnalyzer_MF_resources_absent(&lexer[i]));
    }
}

static void 
self_assert(TestAnalyzer* lexer, E_Error ExpectedError)
{
    hwut_verify(lx->error_code == ExpectedError);

    if( ExpectedError != E_Error_None ) {
        hwut_verify(TestAnalyzer_MF_resources_absent(lx));
    }
    else {
        hwut_verify(! TestAnalyzer_MF_resources_absent(lx));
    }
    hwut_verify(TestAnalyzer_TokenQueue_is_empty(&lx->_token_queue));
}
