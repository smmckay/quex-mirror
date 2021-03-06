#include<cstdio> 
#include<cstdlib> 

// (*) include lexical analyser header
#include "Simple/Simple"
#include <Simple/lib/buffer/lexatoms/converter/iconv/Converter_IConv>
#include <Simple/lib/buffer/lexatoms/converter/iconv/Converter_IConv.i>
#include <Simple/lib/buffer/lexatoms/converter/icu/Converter_ICU>
#include <Simple/lib/buffer/lexatoms/converter/icu/Converter_ICU.i>
#include "Simple/lib/buffer/bytes/ByteLoader_FILE.i"

using namespace std;

int 
main(int argc, char** argv) 
{        

    Simple_Token*   token_p = 0x0;
#   if   defined (QUEX_UT_SETTING_TEST_UTF8)
    const char*    file_name = "example-hindi.utf8";
#   else
    const char*    file_name = "example.txt";
#   endif
#   if defined(QUEX_UT_OPTION_CONVERTER_ICONV)
    Simple_Converter*  converter = Simple_Converter_IConv_new("UTF8", NULL);
#   elif defined(QUEX_UT_OPTION_CONVERTER_ICU)
    Simple_Converter*  converter = Simple_Converter_ICU_new("UTF8", NULL);
#   else
#   define             converter NULL
#   endif
    Simple_ByteLoader* byte_loader = Simple_ByteLoader_FILE_new_from_file_name(file_name);
    Simple             qlex(byte_loader, converter);

    if( argc < 2 ) {
        printf("Command line argument required!\n");
        return 0;
    }
    if( strcmp(argv[1], "--hwut-info") == 0 ) {
#       if   defined(QUEX_UT_OPTION_CONVERTER_ICONV)
        printf("Reset w/ QuexLexatomLoader: Converter_IConv;\n");
#       elif defined(QUEX_UT_OPTION_CONVERTER_ICU)
        printf("Reset w/ QuexLexatomLoader: Converter_ICU;\n");
#       elif defined(QUEX_UT_SETTING_TEST_UTF8)
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
               token_p->id_name(), 
               Simple_lexeme_to_pretty_char(token_p->text).c_str());

    } while( token_p->id != QUEX_TKN_TERMINATION );

    return 0;
}
