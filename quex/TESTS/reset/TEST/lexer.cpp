#include<cstdio> 
#include<cstdlib> 

// (*) include lexical analyser header
#include "Simple"
#include <quex/code_base/buffer/lexatoms/converter/iconv/Converter_IConv>
#include <quex/code_base/buffer/lexatoms/converter/iconv/Converter_IConv.i>
#include <quex/code_base/buffer/lexatoms/converter/icu/Converter_ICU>
#include <quex/code_base/buffer/lexatoms/converter/icu/Converter_ICU.i>
#include "quex/code_base/buffer/bytes/ByteLoader_FILE.i"

using namespace std;

int 
main(int argc, char** argv) 
{        
    using namespace quex;
    Token*   token_p = 0x0;
#   if   defined (__QUEX_SETTING_TEST_UTF8)
    const char*    file_name = "example-hindi.utf8";
#   else
    const char*    file_name = "example.txt";
#   endif
#   if defined(QUEX_OPTION_CONVERTER_ICONV)
    QUEX_NAME(Converter)*    converter = QUEX_NAME(Converter_IConv_new)("UTF8", NULL);
#   elif defined(QUEX_OPTION_CONVERTER_ICU)
    QUEX_NAME(Converter)*    converter = QUEX_NAME(Converter_ICU_new)("UTF8", NULL);
#   else
#   define                   converter NULL
#   endif
    QUEX_NAME(ByteLoader)* byte_loader = QUEX_NAME(ByteLoader_FILE_new_from_file_name)(file_name);
    Simple   qlex(byte_loader, converter);

    if( argc < 2 ) {
        printf("Command line argument required!\n");
        return 0;
    }
    if( strcmp(argv[1], "--hwut-info") == 0 ) {
#       if   defined(QUEX_OPTION_ENABLED_ICONV)
        printf("Reset w/ QuexLexatomLoader: Converter_IConv;\n");
#       elif defined(QUEX_OPTION_ENABLED_ICU)
        printf("Reset w/ QuexLexatomLoader: Converter_ICU;\n");
#       elif defined(__QUEX_SETTING_TEST_UTF8)
        printf("Reset w/ QuexLexatomLoader: Plain w/ Engine Codec;\n");
#       else
        printf("Reset w/ QuexLexatomLoader: Plain;\n");
#       endif
        printf("CHOICES:  0, 1, 2, 3, 20, 30, 50, 134, 135, 136, 1000;\n");
        printf("SAME;\n");
        return 0;
    }
    int N = atoi(argv[1]);

    /* Read 'N' tokens before doing the reset. */
    for(int i=0; i < N; ++i) {
        assert(qlex.buffer.filler);
        (void)qlex.receive(&token_p);
    } 

    assert(qlex.buffer.filler);
    qlex.reset();

    printf("## repeated: %i\n", N);

    do {
        assert(qlex.buffer.filler);
        (void)qlex.receive(&token_p);

        printf("(%2i, %2i)   \t%s '%s' \n", (int)qlex.line_number(), (int)qlex.column_number(),
               token_p->type_id_name().c_str(), 
               QUEX_NAME(lexeme_to_pretty_char)(token_p->text).c_str());

    } while( token_p->type_id() != QUEX_TKN_TERMINATION );

    return 0;
}
