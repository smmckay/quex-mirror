#include <hwut_unit.h>
#include <basic_functionality.h>
#include "test_cpp/lib/buffer/Buffer.i"
// #include "test_cpp/lib/MemoryManager.i"


#include <sstream>

using namespace std;

QUEX_NAMESPACE_MAIN_OPEN
static void test(bool BinaryF, size_t BPC);
QUEX_NAMESPACE_MAIN_CLOSE

int
main(int argc, char** argv)
{
    const size_t   BPC = sizeof(QUEX_TYPE_LEXATOM_EXT);
    if( argc > 1 && strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("Buffer Tell&Seek: LexatomLoader_Plain wiostream (BPC=%i, FALLBACK=%i);\n", 
               (int)BPC, (int)QUEX_UT_SETTING_BUFFER_FALLBACK_N_EXT);
        printf("CHOICES: linear, stepping;\n"
               "SAME;\n");
        return 0;
    }
    hwut_if_choice("linear")   QUEX_NAMESPACE_MAIN::test(true, BPC);
    hwut_if_choice("stepping") QUEX_NAMESPACE_MAIN::test(false, BPC);

    return 0;
}

QUEX_NAMESPACE_MAIN_OPEN
static void
test(bool BinaryF, size_t BPC)
{
    QUEX_NAME(Buffer)         buffer;
    std::wstringstream        sh;
    QUEX_NAME(ByteLoader)*    byte_loader;
    QUEX_NAME(LexatomLoader*) filler;
    const size_t              MemorySize  = true ? 5 : 16;
    QUEX_TYPE_LEXATOM_EXT     memory[MemorySize];

    sh << L"Fest gemauert in der Erden\n";
    sh.seekg(0);
    byte_loader = QUEX_NAME(ByteLoader_stream_new)(&sh);
    hwut_verify(byte_loader);

    byte_loader->binary_mode_f = BinaryF;
    filler = QUEX_NAME(LexatomLoader_Plain_new)(byte_loader);
    hwut_verify(filler);

    QUEX_NAME(Buffer_construct)(&buffer, filler, &memory[0], MemorySize, 0, 
                                QUEX_UT_SETTING_BUFFER_FALLBACK_N_EXT, 
                                E_Ownership_EXTERNAL, (QUEX_NAME(Buffer)*)0);
    buffer._fallback_n = QUEX_UT_SETTING_BUFFER_FALLBACK_N_EXT;

    /* REFERENCE file and INPUT file are the SAME.                           */
    hwut_verify(basic_functionality(&buffer, find_reference("examples/festgemauert")));

    filler->delete_self(filler);
}

QUEX_NAMESPACE_MAIN_CLOSE
