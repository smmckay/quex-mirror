#include <TestAnalyzer.h>
#include <quex/code_base/MemoryManager>
#include <quex/code_base/buffer/TESTS/MemoryManager_UnitTest.i>
#include <hwut_unit.h>

MemoryManager_UnitTest_t MemoryManager_UnitTest;

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

    hwut_if_choice("file-name")   self_file_name(); 
    hwut_if_choice("byte-loader") self_byte_loader(); 
    hwut_if_choice("memory")      self_memory(); 

    return 0;
}

static void 
self_file_name()
{
    quex_TestAnalyzer lexer[2];

    QUEX_NAME(from_file_name)(&lexer[0], "file-that-does-not-exists.txt", NULL);
    hwut_verify(  QUEX_NAME(resources_absent)(&lexer[0]));

    QUEX_NAME(from_file_name)(&lexer[1], "file-that-exists.txt", NULL);
    hwut_verify(! QUEX_NAME(resources_absent)(&lexer[1]));

    self_destruct(lexer, 2);
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

