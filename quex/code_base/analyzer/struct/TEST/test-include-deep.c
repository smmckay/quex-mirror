/* PURPOSE: Test include-push/pop functions.
 *
 * Include deeply and pop some before reset.
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

quex_TestAnalyzer      lexer;
quex_TestAnalyzer*     lx =&lexer;
#define                MemorySize 7
uint8_t                memory[MemorySize];
int                    self_split_n = 0;
int                    self_total_n = 0;

static void      self_run(ptrdiff_t Depth);
static void      self_test(ptrdiff_t MaxDepth, ptrdiff_t PopN);
static bool      do_action(uint32_t n);
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
    printf("<terminated: buffer-splits: %i/%i; allocate_n: %i; free_n: %i;>\n", 
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
    memory[0]            = QUEX_SETTING_BUFFER_LIMIT_CODE;
    memory[MemorySize-1] = QUEX_SETTING_BUFFER_LIMIT_CODE;

    memset(lx, 0x5A, sizeof(lexer));
    QUEX_NAME(from_file_name)(lx, "file-that-exists.txt", NULL);
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
        if( ! do_action(n) ) {
            /* Too many file descriptors can only occur if i >> 0 */
            hwut_verify(i > 0);
            lx->error_code = E_Error_None;
            break;
        }
    }
    depth = i;
    hwut_verify(self_find_include_depth() == depth);

    for(i=0; i<PopN; ++i) {
        QUEX_NAME(include_pop)(lx);
        if( i < depth ) hwut_verify(lx->error_code == E_Error_None);
        else            hwut_verify(lx->error_code == E_Error_IncludePopOnEmptyStack);
    }

    QUEX_NAME(destruct)(lx);
}

static bool 
do_action(uint32_t n)
{
    QUEX_NAME(ByteLoader)* byte_loader;
    QUEX_NAME(Converter)*  converter;

    /* Setup the pointers, so that the inclusion type varries.
     * => usage of current buffer for the included buffer.                    */
    self_setup_pointers(n);

    switch( n % 3 ) {                             

    case 0:
        n = hwut_random_next(n);
        converter = n % 2 ? QUEX_NAME(Converter_IConv_new)("UTF8", NULL)
                          : (QUEX_NAME(Converter)*)0;
        QUEX_NAME(include_push_file_name)(lx, "file-that-exists.txt", converter);
        self_include_file_name_n += 1;
        break;
    case 1:
        n = hwut_random_next(n);
        byte_loader = n % 2 ? QUEX_NAME(ByteLoader_FILE_new_from_file_name)("file-that-exists.txt")
                            : (QUEX_NAME(ByteLoader)*)0;
        n = hwut_random_next(n);
        converter   = n % 2 ? QUEX_NAME(Converter_IConv_new)("UTF8", NULL)
                            : (QUEX_NAME(Converter)*)0;
        QUEX_NAME(include_push_ByteLoader)(lx, "byte-loader", byte_loader, converter);
        self_include_byte_loader_n += 1;
        break;
    case 2:
        QUEX_NAME(include_push_memory)(lx, "memory", &memory[0], 
                                       MemorySize, &memory[MemorySize-1]);
        self_include_memory_n += 1;
        break;
    }

    if( lx->buffer._memory.ownership == E_Ownership_INCLUDING_BUFFER ) self_split_n += 1;
    self_total_n += 1;

    switch( lx->error_code ) {
    case E_Error_None:                         return true;  /* OK                   */
    case E_Error_Allocation_ByteLoader_Failed: return false; /* Too many file descr. */
    default:                                   hwut_verify(false); return false;
    }
}

static void
self_setup_pointers(uint32_t n)
{
    uint32_t           random0                = hwut_random_next(n);
    uint32_t           random1                = hwut_random_next(random0);
    QUEX_TYPE_LEXATOM* end_p_current          = lx->buffer.input.end_p ? lx->buffer.input.end_p 
                                                                       : &lx->buffer._memory._front[1];
    ptrdiff_t          end_p_max_increment_n  = lx->buffer._memory._back - end_p_current;
    ptrdiff_t          end_p_increment_n      = end_p_max_increment_n ? random0 % end_p_max_increment_n
                                                                      : 0;
    QUEX_TYPE_LEXATOM* end_p_new              = lx->buffer.input.end_p + end_p_increment_n;
    ptrdiff_t          read_p_max_increment_n = end_p_new - lx->buffer._read_p;
    ptrdiff_t          read_p_increment_n     = read_p_max_increment_n ? random1 % read_p_max_increment_n
                                                                       : 0;
    QUEX_TYPE_LEXATOM* read_p_new             = lx->buffer._read_p + read_p_increment_n;

    *(lx->buffer.input.end_p)  = 0x5A;
    lx->buffer.input.end_p     = end_p_new;
    *(lx->buffer.input.end_p)  = QUEX_SETTING_BUFFER_LIMIT_CODE;
    lx->buffer._read_p         = read_p_new;
    lx->buffer._lexeme_start_p = read_p_new;
}

static ptrdiff_t
self_find_include_depth()
{
    ptrdiff_t           depth = -1;
    QUEX_NAME(Memento)* memento_p = lx->_parent_memento;
    for(depth=0; memento_p ; memento_p = memento_p->_parent_memento, ++depth);
    return depth;
}
