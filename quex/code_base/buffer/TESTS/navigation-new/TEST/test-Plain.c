#include <hwut_unit.h>
#include <basic_functionality.h>
#include <quex/code_base/buffer/Buffer.i>
#include <quex/code_base/MemoryManager.i>

QUEX_NAMESPACE_MAIN_OPEN
static void test(bool BinaryF, size_t BPC);
static void test_file(bool BinaryF, const char* FileStem);
QUEX_NAMESPACE_MAIN_CLOSE

int
main(int argc, char** argv)
{
    const size_t              BPC         = sizeof(QUEX_TYPE_CHARACTER);
    if( argc > 1 && strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("Buffer Tell&Seek: BufferFiller_Plain (BPC=%i, FALLBACK=%i);\n", 
               BPC, QUEX_SETTING_BUFFER_MIN_FALLBACK_N);
        printf("CHOICES: linear, stepping;\n"
               "SAME;\n");
        return 0;
    }
    hwut_if_choice("linear")   test(true, BPC);
    hwut_if_choice("stepping") test(false, BPC);

    return 0;
}

QUEX_NAMESPACE_MAIN_OPEN
static void
test(bool BinaryF, size_t BPC)
{
    switch( BPC ) {
    case 4:  test_file(BinaryF, "examples/languages");      /* only with UCS4         */
    case 2:  test_file(BinaryF, "examples/small");          /* only with UCS4, UCS2   */
    case 1:  test_file(BinaryF, "examples/festgemauert");   /* with UCS4, UCS2, ASCII */
             break;
    default: hwut_verify(false);
    }
}

static void
test_file(bool BinaryF, const char* FileStem)
{
    QUEX_NAME(Buffer)         buffer;
    /* With 'BufferFiller_Plain()' no conversion takes place. Thus, the file
     * containing the REFERENCE data and the INPUT file are the SAME.        */
    const char*               file_name   = find_reference(FileStem); 
    FILE*                     fh          = fopen(file_name, "rb"); 
    ByteLoader*               byte_loader = ByteLoader_FILE_new(fh);
    QUEX_NAME(BufferFiller)*  filler;
    const size_t              MemorySize  = true ? 5 : 16;
    QUEX_TYPE_CHARACTER       memory[MemorySize];

    if( ! fh ) {
        printf("Failed to open '%s'.", file_name);
        hwut_verify(false);
    }

    byte_loader->binary_mode_f = BinaryF;
    filler = QUEX_NAME(BufferFiller_Plain_new)(byte_loader);

    QUEX_NAME(Buffer_construct)(&buffer, filler, &memory[0], MemorySize, 0, E_Ownership_EXTERNAL);

    /* REFERENCE file and INPUT file are the SAME.                           */
    hwut_verify(basic_functionality(&buffer, file_name));

    filler->delete_self(filler);
}

QUEX_NAMESPACE_MAIN_CLOSE