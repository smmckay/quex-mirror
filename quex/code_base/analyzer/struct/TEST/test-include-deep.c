/* PURPOSE: Test include-push/pop functions.
 *
 * Include deeply and pop some before reset.
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
#include "test_c/lib/quex/MemoryManager_UnitTest.i"
#include <hwut_unit.h>

MemoryManager_UnitTest_t MemoryManager_UnitTest;

TestAnalyzer      lexer;
TestAnalyzer*     lx =&lexer;
#define                MemorySize 65536
uint8_t                memory[MemorySize];
uint8_t*               memory_it = &memory[0];
int                    self_split_n = 0;
int                    self_total_n = 0;

static void      self_run(ptrdiff_t Depth);
static void      self_test(ptrdiff_t MaxDepth, ptrdiff_t PopN);
static bool      self_include_push(uint32_t n);
static void      self_include_pop(TestAnalyzer* lx);
static void      self_setup_pointers(uint32_t n);
static ptrdiff_t self_find_include_depth();

static int  self_include_file_name_n   = 0;
static int  self_include_byte_loader_n = 0;
static int  self_include_memory_n      = 0;

int
main(int argc, char** argv)
{
    hwut_info("Include Push/Pop Deep;\n");

    MemoryManager_UnitTest.allocation_addmissible_f = true;
    MemoryManager_UnitTest.forbid_ByteLoader_f      = false;
    MemoryManager_UnitTest.forbid_LexatomLoader_f   = false;
    MemoryManager_UnitTest.forbid_BufferMemory_f    = false;
    MemoryManager_UnitTest.forbid_InputName_f       = false;
    UserConstructor_UnitTest_return_value           = true;
    UserReset_UnitTest_return_value                 = false;
    UserMementoPack_UnitTest_return_value           = true;

    self_run(2);
    self_run(3);
    /* Max. number of file descripts will hit anyway at about 2053. */
    self_run(2086); 

    printf("<terminated: file_name: %i; byte_loader: %i; memory: %i>\n", 
           self_include_file_name_n, self_include_byte_loader_n, 
           self_include_memory_n);
    printf("<terminated: buffer-splits: %i/%i; allocate_n: ((%i)); free_n: ((%i));>\n", 
           (int)self_split_n, (int)self_total_n,
           (int)MemoryManager_UnitTest.allocation_n, 
           (int)MemoryManager_UnitTest.free_n); 
}

static void
self_run(ptrdiff_t Depth)
{
    self_test(Depth, 0);
    self_test(Depth, 1);
    self_test(Depth, Depth - 2);
    self_test(Depth, Depth - 1);
    self_test(Depth, Depth);
    self_test(Depth, Depth + 1);
    self_test(Depth, Depth + 3);
}


static void
self_test(ptrdiff_t MaxDepth, ptrdiff_t PopN)
{
    ptrdiff_t              i = 0;
    ptrdiff_t              depth = 0;
    uint32_t               n = 57;
    memset(&memory[0], 0x5A, sizeof(memory));

    memset(lx, 0x5A, sizeof(lexer));
    TestAnalyzer_from_file_name(lx, "file-that-exists.txt", NULL);
    hwut_verify(lx->error_code == E_Error_None);

    /* Double check, that global objects are not touched. */
    hwut_verify(MemoryManager_UnitTest.allocation_addmissible_f == true);
    hwut_verify(MemoryManager_UnitTest.forbid_ByteLoader_f      == false);
    hwut_verify(MemoryManager_UnitTest.forbid_LexatomLoader_f   == false);
    hwut_verify(MemoryManager_UnitTest.forbid_BufferMemory_f    == false);
    hwut_verify(MemoryManager_UnitTest.forbid_InputName_f       == false);
    hwut_verify(UserConstructor_UnitTest_return_value           == true);
    hwut_verify(UserReset_UnitTest_return_value                 == false);
    hwut_verify(UserMementoPack_UnitTest_return_value           == true);

    for(i=0; i<MaxDepth; ++i) {
        n = hwut_random_next(n);
        if( ! self_include_push(n) ) {
            /* Too many file descriptors can only occur if i >> 0 */
            hwut_verify(i > 0);
            TestAnalyzer_MF_error_code_clear(lx);
            break;
        }
    }
    depth = i;
    hwut_verify(self_find_include_depth() == depth);

    for(i=0; i<PopN; ++i) {
        self_include_pop(lx);
        if( i < depth ) hwut_verify(lx->error_code == E_Error_None);
        else            hwut_verify(lx->error_code == E_Error_IncludePopOnEmptyStack);
    }

    TestAnalyzer_destruct(lx);
}

static bool 
self_include_push(uint32_t n)
{
    TestAnalyzer_ByteLoader* byte_loader;
    TestAnalyzer_Converter*  converter;
    TestAnalyzer_Buffer_event_callbacks backup_callbacks = lx->buffer.event; 
    TestAnalyzer_lexatom_t*     new_memory = (TestAnalyzer_lexatom_t*)0;
    TestAnalyzer_lexatom_t*     new_memory_end = (TestAnalyzer_lexatom_t*)0;
    TestAnalyzer_lexatom_t*     new_memory_eos_p = (TestAnalyzer_lexatom_t*)0;
    ptrdiff_t              new_memory_size;

    /* Setup the pointers, so that the inclusion type varries.
     * => usage of current buffer for the included buffer.                    */
    self_setup_pointers(n);

    switch( n % 3 ) {                             

    case 0:
        n = hwut_random_next(n);
        converter = n % 2 ? TestAnalyzer_Converter_IConv_new("UTF8", NULL)
                          : (TestAnalyzer_Converter*)0;
        lx->include_push_file_name(lx, "file-that-exists.txt", converter);
        self_include_file_name_n += 1;
        break;
    case 1:
        n = hwut_random_next(n);
        byte_loader = n % 2 ? TestAnalyzer_ByteLoader_FILE_new_from_file_name("file-that-exists.txt")
                            : (TestAnalyzer_ByteLoader*)0;
        n = hwut_random_next(n);
        converter   = n % 2 ? TestAnalyzer_Converter_IConv_new("UTF8", NULL)
                            : (TestAnalyzer_Converter*)0;
        lx->include_push_ByteLoader(lx, "byte-loader", byte_loader, converter);
        self_include_byte_loader_n += 1;
        break;
    case 2:
        new_memory_size  = (n % 8) + 4;
        new_memory       = memory_it;
        new_memory_end   = &new_memory[new_memory_size];
        new_memory_eos_p = &new_memory[(n % (new_memory_size-1)) + 1];

        memory_it        = new_memory_end;
        assert(&memory[MemorySize] >= memory_it);

        new_memory[0]       = QUEX_TestAnalyzer_SETTING_BUFFER_LEXATOM_BUFFER_BORDER;
        new_memory_end[-1]  = QUEX_TestAnalyzer_SETTING_BUFFER_LEXATOM_BUFFER_BORDER;
        new_memory_eos_p[0] = QUEX_TestAnalyzer_SETTING_BUFFER_LEXATOM_BUFFER_BORDER;

        lx->include_push_memory(lx, "memory", new_memory, (size_t)(new_memory_size), 
                                new_memory_eos_p);
        self_include_memory_n += 1;
        break;
    }

    /* Ensure, that event handlers are copied around propperly.                      */
    hwut_verify(memcmp((void*)&backup_callbacks, (void*)&lx->buffer.event, sizeof(backup_callbacks)) == 0);

    if( lx->buffer._memory.ownership == E_Ownership_INCLUDING_BUFFER ) self_split_n += 1;
    self_total_n += 1;

    switch( lx->error_code ) {
    case E_Error_None:                         return true;  /* OK                   */
    case E_Error_File_OpenFailed:              return false; /* Too many file descr. */
    case E_Error_Allocation_ByteLoader_Failed: return false; /* Too many file descr. */
    default:                                   hwut_verify(false); return false;
    }
}


static void      
self_include_pop(TestAnalyzer* lx)
{
    TestAnalyzer_Buffer_event_callbacks  backup_callbacks = lx->buffer.event;

    lx->include_pop(lx);

    /* Ensure, that event handlers are copied around propperly.                      */
    hwut_verify(memcmp((void*)&backup_callbacks, (void*)&lx->buffer.event, sizeof(backup_callbacks)) == 0);
}

static void
self_setup_pointers(uint32_t n)
{
    uint32_t           random0                = hwut_random_next(n);
    uint32_t           random1                = hwut_random_next(random0);
    TestAnalyzer_lexatom_t* end_p_current          = lx->buffer.input.end_p ? lx->buffer.input.end_p 
                                                                       : &lx->buffer._memory._front[1];
    ptrdiff_t          end_p_max_increment_n  = lx->buffer._memory._back - end_p_current;
    ptrdiff_t          end_p_increment_n      = end_p_max_increment_n ? random0 % end_p_max_increment_n
                                                                      : 0;
    TestAnalyzer_lexatom_t* end_p_new              = lx->buffer.input.end_p + end_p_increment_n;
    ptrdiff_t          read_p_max_increment_n = end_p_new - lx->buffer._read_p;
    ptrdiff_t          read_p_increment_n     = read_p_max_increment_n ? random1 % read_p_max_increment_n
                                                                       : 0;
    TestAnalyzer_lexatom_t* read_p_new             = lx->buffer._read_p + read_p_increment_n;

    *(lx->buffer.input.end_p)  = 0x5A;
    lx->buffer.input.end_p     = end_p_new;
    *(lx->buffer.input.end_p)  = QUEX_TestAnalyzer_SETTING_BUFFER_LEXATOM_BUFFER_BORDER;
    lx->buffer._read_p         = read_p_new;
    lx->buffer._lexeme_start_p = read_p_new;
}

static ptrdiff_t
self_find_include_depth()
{
    ptrdiff_t           depth = -1;
    TestAnalyzer_Memento* memento_p = lx->_parent_memento;
    for(depth=0; memento_p ; memento_p = memento_p->_parent_memento, ++depth);
    return depth;
}
