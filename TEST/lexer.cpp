#include<fstream>    
#include<iostream> 
extern "C" {
#include<assert.h> 
}

#ifndef    PRINT_TOKEN_FIRST_NUMBER 
#   define PRINT_TOKEN_FIRST_NUMBER 0
#endif

// (*) include lexical analyser header
#include "Simple/Simple"
#include "Simple/lib/buffer/bytes/ByteLoader_FILE.i"
#include <Simple/lib/buffer/lexatoms/converter/iconv/Converter_IConv>
#include <Simple/lib/buffer/lexatoms/converter/iconv/Converter_IConv.i>
#include <Simple/lib/buffer/lexatoms/converter/icu/Converter_ICU>
#include <Simple/lib/buffer/lexatoms/converter/icu/Converter_ICU.i>

using namespace std;

#ifndef   TEST_EPILOG
#   define TEST_EPILOG \
    printf("| [END] number of token = %li\n", token_n); \
    printf("`------------------------------------------------------------------------------------\n");
#endif

int main(int argc, char** argv) 
{

    assert(argc > 1);

    // (*) create token
    Token*                token_p = 0;
    long                  token_n = 0;
    //
    // (*) create the lexical analyser
#   if defined(QUEX_OPTION_CONVERTER_ICONV)
    QUEX_NAME(Converter)*    converter = QUEX_NAME(Converter_IConv_new)("UTF8", NULL);
#   elif defined(QUEX_OPTION_CONVERTER_ICU)
    QUEX_NAME(Converter)*    converter = QUEX_NAME(Converter_ICU_new)("UTF8", NULL);
#   else
#   define                   converter NULL
#   endif
    Simple*                  qlex = Simple::from_file_name(argv[1], converter); 

    // (*) loop until the 'termination' token arrives
    do {
        // (*) get next token from the token stream
        qlex->receive(&token_p);

        // (*) print out token information
        cerr.flush();
        if( token_p && token_n >= PRINT_TOKEN_FIRST_NUMBER ) {
#           if defined (QUEX_OPTION_CONVERTER_ICU) || defined (QUEX_OPTION_CONVERTER_ICONV)
            cout << *token_p << endl;
#           else
            cout << (const char*)(token_p->type_id_name().c_str());
            cout << " '";
            cout << (const char*)(token_p->get_text());
            cout << "' " << endl;
#           endif
            cout.flush();
        }
        ++token_n;

        // (*) check against 'termination'
    } while( token_p->id != QUEX_TKN_TERMINATION );

    if( qlex->error_code != E_Error_None ) {
        qlex->print_this();
    }

    TEST_EPILOG

    delete qlex;
}
