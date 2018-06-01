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
 * Delete-Ability/V-Table Corruption:
 *
 * Unwise use of 'memset', for example, may alter the V-Table of lexer objects.
 * In such cases, it is likely that the virtual destructor pointer is corrupted.
 *
 * => (1) Placement new to construct lexical analyzers.
 *    (2) Explicit destructor calls to destruct.
 *
 * In case that the v-table is corrupted, this procudure is likely to fail.
 *
 * (C) 2017 Frank-Rene Schaefer                                               */
#include <test_cpp/TestAnalyzer>
#include "ut/lib/quex/MemoryManager"
#include "MemoryManager_UnitTest.i"
#include "ut/lib/buffer/lexatoms/converter/iconv/Converter_IConv"
#include "ut/lib/buffer/lexatoms/converter/iconv/Converter_IConv.i"
#include "ut/lib/buffer/lexatoms/converter/icu/Converter_ICU"
#include "ut/lib/buffer/lexatoms/converter/icu/Converter_ICU.i"
#include <hwut_unit.h>

namespace quex {
MemoryManager_UnitTest_t MemoryManager_UnitTest;
}



static void self_file_name();
static void self_byte_loader();
static void self_memory();
static void self_destruct(size_t N);
static void self_assert(TestAnalyzer* lexer, E_Error ExpectedError);
static void self_byte_loader_core(E_Error ExpectedError);

uint8_t       lexer_memory[sizeof(TestAnalyzer)*128];
TestAnalyzer* lx0 = reinterpret_cast<TestAnalyzer*>(&lexer_memory[0]);
TestAnalyzer* lx = lx0;

int
main(int argc, char** argv)
{
    hwut_info("Constructor;\n"
              "CHOICES: file-name, byte-loader, memory;\n");

    memset(&quex::MemoryManager_UnitTest, 0, sizeof(quex::MemoryManager_UnitTest_t));

    quex::MemoryManager_UnitTest.allocation_addmissible_f = true;
    quex::MemoryManager_UnitTest.forbid_ByteLoader_f      = false;
    quex::MemoryManager_UnitTest.forbid_LexatomLoader_f   = false;
    quex::MemoryManager_UnitTest.forbid_BufferMemory_f    = false;
    quex::MemoryManager_UnitTest.forbid_InputName_f       = false;
    UserConstructor_UnitTest_return_value           = true;
    UserReset_UnitTest_return_value                 = false;
    UserMementoPack_UnitTest_return_value           = false;

    memset(&lexer_memory[0], 0x5A, sizeof(lexer_memory)); /* Poisson all memory. */
    lx = lx0;

    hwut_if_choice("file-name")   self_file_name(); 
    hwut_if_choice("byte-loader") self_byte_loader(); 
    hwut_if_choice("memory")      self_memory(); 

    /* Destruct safely all lexers. */
    self_destruct((size_t)(lx - lx0));

    printf("<terminated: %i>\n", (int)(lx- lx0));

    return 0;
}

static void 
self_file_name()
{
    /* Good case                                                              */
    {
        new (lx) TestAnalyzer("file-that-exists.txt", NULL);
        self_assert(lx, E_Error_None);
        lx->TestAnalyzer::~TestAnalyzer();
    }

    /* Bad cases                                                              */
    ++lx;
    {
        new (lx) TestAnalyzer("file-that-does-not-exists.txt", NULL);
        self_assert(lx, E_Error_File_OpenFailed);
        lx->TestAnalyzer::~TestAnalyzer();
    }

    ++lx;
    {
        quex::MemoryManager_UnitTest.forbid_ByteLoader_f = true;
        new (lx) TestAnalyzer("file-that-exists.txt", NULL);
        self_assert(lx, E_Error_File_OpenFailed); 
        lx->TestAnalyzer::~TestAnalyzer();
        quex::MemoryManager_UnitTest.forbid_ByteLoader_f    = false;
    }

    ++lx;
    {
        quex::MemoryManager_UnitTest.forbid_LexatomLoader_f = true;
        new (lx) TestAnalyzer("file-that-exists.txt", NULL);
        self_assert(lx, E_Error_Allocation_LexatomLoader_Failed); 
        lx->TestAnalyzer::~TestAnalyzer();
        quex::MemoryManager_UnitTest.forbid_LexatomLoader_f = false;
    }

    ++lx;
    {
        quex::MemoryManager_UnitTest.forbid_BufferMemory_f = true;
        new (lx) TestAnalyzer("file-that-exists.txt", NULL);
        self_assert(lx, E_Error_Allocation_BufferMemory_Failed); 
        lx->TestAnalyzer::~TestAnalyzer();
        quex::MemoryManager_UnitTest.forbid_BufferMemory_f = false;
    }

    ++lx;
    {
        UserConstructor_UnitTest_return_value = false;
        new (lx) TestAnalyzer("file-that-exists.txt", NULL);
        self_assert(lx, E_Error_UserConstructor_Failed); 
        lx->TestAnalyzer::~TestAnalyzer();
        UserConstructor_UnitTest_return_value = true;
    }

    ++lx;
    {
        quex::MemoryManager_UnitTest.forbid_InputName_f = true;
        new (lx) TestAnalyzer("file-that-exists.txt", NULL);
        self_assert(lx, E_Error_InputName_Set_Failed); 
        lx->TestAnalyzer::~TestAnalyzer();
        quex::MemoryManager_UnitTest.forbid_InputName_f = false;
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
    TestAnalyzer_ByteLoader* byte_loader;
    TestAnalyzer_Converter*  converter;

    switch( ExpectedError ) {
    case E_Error_Allocation_ByteLoader_Failed:
        assert(false); /* Not subject to test, here. */
        break;
    case E_Error_Allocation_LexatomLoader_Failed:
        quex::MemoryManager_UnitTest.forbid_LexatomLoader_f = true;
        break;
    case E_Error_Allocation_BufferMemory_Failed:
        quex::MemoryManager_UnitTest.forbid_BufferMemory_f = true;
        break;
    case E_Error_InputName_Set_Failed:
        quex::MemoryManager_UnitTest.forbid_InputName_f = true;
        ExpectedError = E_Error_None;
        break;
    case E_Error_UserConstructor_Failed:
        UserConstructor_UnitTest_return_value = false;
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
        new (lx) TestAnalyzer(byte_loader, converter);
        self_assert(lx, ExpectedError);
        lx->TestAnalyzer::~TestAnalyzer();
    }
    ++lx;
    {
        byte_loader = TestAnalyzer_ByteLoader_FILE_new_from_file_name("file-that-exists.txt");
        converter   = NULL;
        new (lx) TestAnalyzer(byte_loader, converter);
        self_assert(lx, ExpectedError);
        lx->TestAnalyzer::~TestAnalyzer();
    }
    ++lx;
    {
        byte_loader = NULL;
        converter   = TestAnalyzer_Converter_IConv_new("UTF8", NULL);
        new (lx) TestAnalyzer(byte_loader, converter);
        self_assert(lx, ExpectedError);
        lx->TestAnalyzer::~TestAnalyzer();
    }
    ++lx;
    {
        byte_loader = NULL;
        converter   = NULL;
        new (lx) TestAnalyzer(byte_loader, converter);
        self_assert(lx, ExpectedError);
        lx->TestAnalyzer::~TestAnalyzer();
    }
    ++lx;

    quex::MemoryManager_UnitTest.forbid_ByteLoader_f    = false;
    quex::MemoryManager_UnitTest.forbid_LexatomLoader_f = false;
    quex::MemoryManager_UnitTest.forbid_BufferMemory_f  = false;
    quex::MemoryManager_UnitTest.forbid_InputName_f     = false;
    UserConstructor_UnitTest_return_value         = true;
}

static void 
self_memory()
{
    uint8_t memory[65536];

    memset(&memory[0], 0x5A, sizeof(memory));
    memory[0]       = QUEX_SETTING_BUFFER_LIMIT_CODE;
    memory[65536-1] = QUEX_SETTING_BUFFER_LIMIT_CODE;

    {
        new (lx) TestAnalyzer(&memory[0], 65536, &memory[65536-1]);
        self_assert(lx, E_Error_None);
        lx->TestAnalyzer::~TestAnalyzer();
    }
    ++lx;
    {
        /* Forbidding Allocation: ByteLoader, LexatomLoader, Memory
         * => No Error!                                                       */
        quex::MemoryManager_UnitTest.forbid_ByteLoader_f    = false;
        quex::MemoryManager_UnitTest.forbid_LexatomLoader_f = false;
        quex::MemoryManager_UnitTest.forbid_BufferMemory_f  = false;

        new (lx) TestAnalyzer(&memory[0], 65536, &memory[65536-1]);
        self_assert(lx, E_Error_None);
        lx->TestAnalyzer::~TestAnalyzer();
    }
    ++lx;
    {
        UserConstructor_UnitTest_return_value = false;
        new (lx) TestAnalyzer(&memory[0], 65536, &memory[65536-1]);
        self_assert(lx, E_Error_UserConstructor_Failed);
        lx->TestAnalyzer::~TestAnalyzer();
        UserConstructor_UnitTest_return_value = true;
    }
    ++lx;
    {
        quex::MemoryManager_UnitTest.forbid_InputName_f = true;
        new (lx) TestAnalyzer(&memory[0], 65536, &memory[65536-1]);
        /* Input name is not set upon construction from memory. */
        hwut_verify(lx->__input_name == (char*)0);
        self_assert(lx, E_Error_None);
        lx->TestAnalyzer::~TestAnalyzer();

        quex::MemoryManager_UnitTest.forbid_InputName_f = false;
    }
    ++lx;

}

static void
self_destruct(size_t N)
{
    TestAnalyzer* End = &lx0[N];

    for(TestAnalyzer* it = lx0; it != End; ++it) {
        it->~TestAnalyzer();
        hwut_verify(TestAnalyzer_MF_resources_absent(it));
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
}
