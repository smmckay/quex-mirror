#include "Simple/Simple.h"
#ifdef  QUEX_OPTION_CONVERTER_ICONV
#   include <Simple/lib/buffer/lexatoms/converter/iconv/Converter_IConv>
#   include <Simple/lib/buffer/lexatoms/converter/iconv/Converter_IConv.i>
#endif
#ifdef  QUEX_OPTION_CONVERTER_ICU
#   include <Simple/lib/buffer/lexatoms/converter/icu/Converter_ICU>
#   include <Simple/lib/buffer/lexatoms/converter/icu/Converter_ICU.i>
#endif

#ifndef    PRINT_TOKEN_FIRST_NUMBER 
#   define PRINT_TOKEN_FIRST_NUMBER 0
#endif
#ifndef    TEST_PROLOG
#   define TEST_PROLOG \
    printf(",------------------------------------------------------------------------------------\n"); \
    printf("| [START]\n");
#endif
#ifndef    TEST_EPILOG
#   define TEST_EPILOG \
    printf("| [END] number of token = %li\n", token_n); \
    printf("`------------------------------------------------------------------------------------\n");
#endif

#ifdef HWUT_INFO_MESSAGE
#include <support/C/hwut_unit.h>
#endif

int 
main(int argc, char** argv) 
{        
#   ifdef PRINT_TOKEN
    const size_t  BufferSize = 1024;
    char          buffer[1024];
#   endif
    quex_Token*   token_p = 0x0;
    long          token_n = 0;
    quex_Simple   qlex;
    const char*   file_name = argc > 1 ? argv[1] : "example.txt";

    QUEX_NAME(ByteLoader)*   byte_loader = QUEX_NAME(ByteLoader_FILE_new_from_file_name)(file_name);

#   if   defined(QUEX_OPTION_CONVERTER_ICONV)
    QUEX_NAME(Converter)*    converter = QUEX_NAME(Converter_IConv_new)("UTF8", NULL);
#   elif defined(QUEX_OPTION_CONVERTER_ICU)
    QUEX_NAME(Converter)*    converter = QUEX_NAME(Converter_ICU_new)("UTF8", NULL);
#   else
#   define                   converter NULL
#   endif
    QUEX_NAME(from_ByteLoader)(&qlex, byte_loader, converter);

#   ifdef HWUT_INFO_MESSAGE
	hwut_info(HWUT_INFO_MESSAGE);
#   endif

    TEST_PROLOG
    fflush(stdout);
    fflush(stderr);

    /* Loop until the 'termination' token arrives */
    token_n = 0;

    do {
        /* Get next token from the token stream   */
        qlex.receive(&qlex, &token_p);

#       ifdef PRINT_LINE_COLUMN_NUMBER
        printf("(%i, %i)  \t", (int)token_p->_line_n, (int)token_p->_column_n);
#       endif
        /* Print out token information            */
        fflush(stderr);
#       ifdef PRINT_TOKEN
        if( token_n >= PRINT_TOKEN_FIRST_NUMBER ) {
            printf("%s", QUEX_NAME_TOKEN(get_string)(token_p, buffer, BufferSize));
            printf("\n");
        }
#       else
        printf("%s", QUEX_NAME_TOKEN(map_id_to_name)(token_p->id));
        printf("\n");
#       endif
        fflush(stdout);

        ++token_n;
        /* Check against 'termination'            */
    } while( token_p->id != QUEX_TKN_TERMINATION );

    if( qlex.error_code != E_Error_None ) {
        qlex.print_this(&qlex);
    }
    TEST_EPILOG

    QUEX_NAME(destruct)(&qlex);
    return 0;
}
