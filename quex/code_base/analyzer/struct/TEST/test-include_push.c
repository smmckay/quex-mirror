/* PURPOSE: Test include-push/pop functions.
 *
 * Include-push functions come in three flavors (== CHOICES): 
 *
 *    filen-name:  based on a file name.
 *    byte-loader: based on ByteLoader and Converter objects.
 *    memory:      based on memory chunks.
 *
 * If the including buffer has enough space left, it is used by the included
 * buffer. This may alter the allocation scheme.
 *
 * Include-push may fail, due to memory allocation failure or due to failure
 * of the user constructor. For all three flavors all memory allocations
 * failures are considered and the consequences are checked. 
 *
 * Failure => lexical analyzer remains as it was before, except that an error
 *            code is setup.
 *
 * Include-push operations are performed on four states:
 *    -- lexer has been constructed with loader (and converter)
 *    -- lexer has been constructed on memory
 *
 * The 'PopF' determines whether the destructor is directly called on the 
 * analyzer which included, or whether the 'include_pop()' function is called
 * before.
 *
 * Test is best run inside a 'valgrind' session, so that memory leaks may be
 * properly detected.
 *
 * (C) 2017 Frank-Rene Schaefer                                               */
#include <TestAnalyzer.h>
#include <quex/code_base/MemoryManager>
#include <quex/code_base/buffer/TESTS/MemoryManager_UnitTest.i>
#include <quex/code_base/buffer/lexatoms/converter/iconv/Converter_IConv>
#include <quex/code_base/buffer/lexatoms/converter/iconv/Converter_IConv.i>
#include <quex/code_base/buffer/lexatoms/converter/icu/Converter_ICU>
#include <quex/code_base/buffer/lexatoms/converter/icu/Converter_ICU.i>
#include <hwut_unit.h>

MemoryManager_UnitTest_t MemoryManager_UnitTest;

static void self_include_push_on_loader(int argc, char** argv, bool PopF);
static void self_include_push_on_memory(int argc, char** argv, bool PopF);

/* CHOICES: */
static void self_file_name();
static void self_byte_loader();
static void self_byte_loader_core(E_Error ExpectedError);
static void self_memory();

static void self_pop(quex_TestAnalyzer* lexer, size_t N);
static void self_destruct(quex_TestAnalyzer* lexer, size_t N);
static void self_assert(quex_TestAnalyzer* lexer, E_Error ExpectedError);

quex_TestAnalyzer        lexer[25];
const quex_TestAnalyzer* lexerEnd = &lexer[25];
quex_TestAnalyzer*       lx;
quex_TestAnalyzer        backup;

int
main(int argc, char** argv)
{
    hwut_info("Include Push/Pop;\n"
              "CHOICES: file-name, byte-loader, memory;\n");

    memset(&MemoryManager_UnitTest, 0, sizeof(MemoryManager_UnitTest));

    MemoryManager_UnitTest.allocation_addmissible_f = true;

    self_include_push_on_loader(argc, argv, /* PopF */false);
    hwut_verify(lx <= &lexer[25]);

    self_include_push_on_loader(argc, argv, /* PopF */true);
    hwut_verify(lx <= &lexer[25]);

    self_include_push_on_memory(argc, argv, /* PopF */false);
    hwut_verify(lx <= &lexer[25]);

    self_include_push_on_memory(argc, argv, /* PopF */true);
    hwut_verify(lx <= &lexer[25]);

    return 0;
}

static void
self_include_push_on_loader(int argc, char** argv, bool PopF)
{
    /* Construct: ByteLoader */
    UserConstructor_UnitTest_return_value = true; 
    UserReset_UnitTest_return_value       = false; /* Shall not be called! */

    memset(&lexer[0], 0x5A, sizeof(lexer)); /* Poisson all memory. */
    for(lx=&lexer[0]; lx != lexerEnd; ++lx) {
        QUEX_NAME(from_file_name)(lx, "file-that-exists.txt", NULL);
        assert(lx->error_code == E_Error_None);
    }

    /* Reset */
    UserMementoPack_UnitTest_return_value = true; 
    UserConstructor_UnitTest_return_value = false; /* Shall not be called! */
    UserReset_UnitTest_return_value       = false; /* Shall not be called! */

    lx = &lexer[0];
    hwut_if_choice("file-name")   self_file_name(); 
    hwut_if_choice("byte-loader") self_byte_loader(); 
    hwut_if_choice("memory")      self_memory(); 

    /* Destruct safely all lexers. */
    if( PopF ) self_pop(&lexer[0], lexerEnd - &lexer[0]);
    self_destruct(&lexer[0], lexerEnd - &lexer[0]);
    printf("<terminated 'byte loader': %i>\n", (int)(lx- &lexer[0]));
}

static void
self_include_push_on_memory(int argc, char** argv, bool PopF)
{
    uint8_t memory[65536];

    memset(&memory[0], 0x5A, sizeof(memory));
    memory[0]       = QUEX_SETTING_BUFFER_LIMIT_CODE;
    memory[65536-1] = QUEX_SETTING_BUFFER_LIMIT_CODE;

    UserConstructor_UnitTest_return_value = true; /* Shall not be called! */

    /* Construct: Memory */
    memset(&lexer[0], 0x5A, sizeof(lexer)); /* Poisson all memory. */
    for(lx=&lexer[0]; lx != lexerEnd; ++lx) {
        QUEX_NAME(from_memory)(lx, &memory[0], 65536, &memory[65536-1]);
        assert(lx->error_code == E_Error_None);
    }

    /* Include Push */
    UserMementoPack_UnitTest_return_value = true; 
    UserReset_UnitTest_return_value       = false; /* Shall not be called! */
    UserConstructor_UnitTest_return_value = false; /* Shall not be called! */

    lx = &lexer[0];
    hwut_if_choice("file-name")   self_file_name(); 
    hwut_if_choice("byte-loader") self_byte_loader(); 
    hwut_if_choice("memory")      self_memory(); 

    /* Destruct safely all lexers. */
    if( PopF ) self_pop(&lexer[0], lexerEnd - &lexer[0]);
    self_destruct(&lexer[0], lexerEnd - &lexer[0]);

    printf("<terminated 'memory': %i>\n", (int)(lx- &lexer[0]));
}

static void 
self_file_name()
{
    /* Good case                                                              */
    backup = *lx;
    {
        QUEX_NAME(include_push_file_name)(lx, "file-that-exists.txt", NULL);
        self_assert(lx, E_Error_None);
    }

    /* Bad cases                                                              */
    ++lx;
    backup = *lx;
    {
        QUEX_NAME(include_push_file_name)(lx, "file-that-does-not-exists.txt", NULL);
        self_assert(lx, E_Error_Allocation_ByteLoader_Failed);
    }
    ++lx;
    backup = *lx;
    {
        MemoryManager_UnitTest.forbid_ByteLoader_f = true;
        QUEX_NAME(include_push_file_name)(lx, "file-that-exists.txt", NULL);
        self_assert(lx, E_Error_Allocation_ByteLoader_Failed); 
        MemoryManager_UnitTest.forbid_ByteLoader_f = false;
    }
    ++lx;
    backup = *lx;
    {
        MemoryManager_UnitTest.forbid_LexatomLoader_f = true;
        QUEX_NAME(include_push_file_name)(lx, "file-that-exists.txt", NULL);
        self_assert(lx, E_Error_Allocation_LexatomLoader_Failed); 
        MemoryManager_UnitTest.forbid_LexatomLoader_f = false;
    }
    ++lx;
    backup = *lx;
    {   /* Buffer Memory allocation is not required => No Error!              */
        MemoryManager_UnitTest.forbid_BufferMemory_f = true;
        QUEX_NAME(include_push_file_name)(lx, "file-that-exists.txt", NULL);
        self_assert(lx, E_Error_None); 
        MemoryManager_UnitTest.forbid_BufferMemory_f = false;
    }
    ++lx;
    backup = *lx;
    {
        UserMementoPack_UnitTest_return_value = false;
        QUEX_NAME(include_push_file_name)(lx, "file-that-exists.txt", NULL);
        self_assert(lx, E_Error_UserMementoPack_Failed); 
        UserMementoPack_UnitTest_return_value = true;
    }
    ++lx;
    backup = *lx;
    {
        MemoryManager_UnitTest.forbid_InputName_f = true;
        QUEX_NAME(include_push_file_name)(lx, "file-that-exists.txt", NULL);
        self_assert(lx, E_Error_InputName_Set_Failed); 
        MemoryManager_UnitTest.forbid_InputName_f = false;
    }
    ++lx;
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
    self_byte_loader_core(E_Error_UserMementoPack_Failed);
}

static void
self_byte_loader_core(E_Error ExpectedError)
{
    QUEX_NAME(ByteLoader)* byte_loader;
    QUEX_NAME(Converter)*  converter;

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
        break;
    case E_Error_UserMementoPack_Failed:
        UserMementoPack_UnitTest_return_value = false;
        break;
    case E_Error_None:
        break;
    default:
        assert(false);
        return;
    }

    backup = *lx;
    {
        byte_loader = QUEX_NAME(ByteLoader_FILE_new_from_file_name)("file-that-exists.txt");
        converter   = QUEX_NAME(Converter_IConv_new)("UTF8", NULL);
        QUEX_NAME(include_push_ByteLoader)(lx, "UT Input0", byte_loader, converter);
        self_assert(lx, ExpectedError);
    }
    ++lx;
    backup = *lx;
    {
        byte_loader = QUEX_NAME(ByteLoader_FILE_new_from_file_name)("file-that-exists.txt");
        converter   = NULL;
        QUEX_NAME(include_push_ByteLoader)(lx, "UT Input1", byte_loader, converter);
        self_assert(lx, ExpectedError);
    }
    ++lx;
    backup = *lx;
    {
        byte_loader = NULL;
        converter   = QUEX_NAME(Converter_IConv_new)("UTF8", NULL);
        QUEX_NAME(include_push_ByteLoader)(lx, "UT Input2", byte_loader, converter);
        self_assert(lx, ExpectedError);
    }
    ++lx;
    backup = *lx;
    {
        byte_loader = NULL;
        converter   = NULL;
        QUEX_NAME(include_push_ByteLoader)(lx, "UT Input2", byte_loader, converter);
        self_assert(lx, ExpectedError);
    }
    ++lx;

    MemoryManager_UnitTest.forbid_ByteLoader_f    = false;
    MemoryManager_UnitTest.forbid_LexatomLoader_f = false;
    MemoryManager_UnitTest.forbid_BufferMemory_f  = false;
    MemoryManager_UnitTest.forbid_InputName_f     = false;
    UserMementoPack_UnitTest_return_value         = true;
}

static void 
self_memory()
{
    uint8_t memory[65536];

    memset(&memory[0], 0x5A, sizeof(memory));
    memory[0]       = QUEX_SETTING_BUFFER_LIMIT_CODE;
    memory[65536-1] = QUEX_SETTING_BUFFER_LIMIT_CODE;

    backup = *lx;
    {
        QUEX_NAME(include_push_memory)(lx, "InputMemory", &memory[0], 65536, &memory[65536-1]);
        self_assert(lx, E_Error_None);
    }
    ++lx;
    backup = *lx;
    {
        /* No alloaction of byte loader, lexatom loader or memory needed. */
        MemoryManager_UnitTest.forbid_ByteLoader_f    = false;
        MemoryManager_UnitTest.forbid_LexatomLoader_f = false;
        MemoryManager_UnitTest.forbid_BufferMemory_f  = false;

        QUEX_NAME(include_push_memory)(lx, "InputMemory", &memory[0], 65536, &memory[65536-1]);
        self_assert(lx, E_Error_None);
    }
    ++lx;
    backup = *lx;
    {
        UserMementoPack_UnitTest_return_value = false;
        QUEX_NAME(include_push_memory)(lx, "InputMemory", &memory[0], 65536, &memory[65536-1]);
        self_assert(lx, E_Error_UserMementoPack_Failed);
        UserMementoPack_UnitTest_return_value = true;
    }
    ++lx;
    backup = *lx;
    {
        MemoryManager_UnitTest.forbid_InputName_f = true;
        QUEX_NAME(include_push_memory)(lx, "InputMemory", &memory[0], 65536, &memory[65536-1]);
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
self_pop(quex_TestAnalyzer* lexer, size_t N)
{
    int i;

    for(i=0; i<N; ++i) {
        if( lexer[i].error_code == E_Error_None ) {
            QUEX_NAME(include_pop)(&lexer[i]);
        }
        hwut_verify(! QUEX_NAME(resources_absent)(&lexer[i]));
    }
}

static void 
self_assert(quex_TestAnalyzer* lexer, E_Error ExpectedError)
{
    hwut_verify(lx->error_code == ExpectedError);

    /* Resources are *never* absent.                                          */
    hwut_verify(! QUEX_NAME(resources_absent)(lx));

    if( ExpectedError == E_Error_None ) return;

    /* Error => lexical analyzer as in the exact state as before.
     *          --except that the error code may have been set.               */
    backup.error_code = lexer->error_code;
    hwut_verify(memcmp((void*)lexer, (void*)&backup, sizeof(backup)) == 0);
}
