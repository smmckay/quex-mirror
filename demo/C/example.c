#include <stdio.h>    

#include "EasyLexer.h"
#include <quex/code_base/buffer/lexatoms/converter/iconv/Converter_IConv>
#include <quex/code_base/buffer/lexatoms/converter/iconv/Converter_IConv.i>


static void print_token(quex_Token* token_p);

int 
main(int argc, char** argv) 
{        
    quex_Token*     token_p = NULL;
    size_t          number_of_tokens = 0;
    quex_EasyLexer  qlex;
    const char*     FileName = (argc == 1) ? "example.txt" : argv[1];
#   if   defined(QUEX_OPTION_CONVERTER_ICONV)
    QUEX_NAME(Converter)*    converter = QUEX_NAME(Converter_IConv_new)("UTF8", NULL);
#   elif defined(QUEX_OPTION_CONVERTER_ICU)
    QUEX_NAME(Converter)*    converter = QUEX_NAME(Converter_ICU_new)("UTF8", NULL);
#   else
#   define                   converter NULL
#   endif
    quex_EasyLexer_from_file_name(&qlex, FileName, converter); 

    printf(",-----------------------------------------------------------------\n");
    printf("| [START]\n");

    do {
        quex_EasyLexer_receive(&qlex, &token_p);
        if( ! token_p ) break;

        print_token(token_p);

        ++number_of_tokens;

    } while( token_p->_id != QUEX_TKN_TERMINATION );

    printf("| [END] number of token = %i\n", (int)number_of_tokens);
    printf("`-----------------------------------------------------------------\n");

    if( qlex.error_code != E_Error_None ) {
        QUEX_NAME(print_this)(&qlex);
    }
    quex_EasyLexer_destruct(&qlex);

    return 0;
}

static void
print_token(quex_Token* token_p)
{
#   ifdef PRINT_TOKEN
    const size_t    BufferSize = 1024;
    char            buffer[1024];
#   endif

#   ifdef PRINT_LINE_COLUMN_NUMBER
    printf("(%i, %i)  \t", (int)token_p->_line_n, (int)token_p->_column_n);
#   endif

#   ifdef PRINT_TOKEN
    switch( token_p->_id ) {
    case QUEX_TKN_INDENT: 
    case QUEX_TKN_DEDENT: 
    case QUEX_TKN_NODENT: 
    case QUEX_TKN_TERMINATION: 
        /* In this case, the token still carries an old lexeme; Printing it
         * would be confusing.                                               */
        printf("%s\n", QUEX_NAME_TOKEN(map_id_to_name)(token_p->_id));
        break;
    default:
        printf("%s \n", QUEX_NAME_TOKEN(get_string)(token_p, buffer, BufferSize));
        break;
    }
#   else
    printf("%s\n", QUEX_NAME_TOKEN(map_id_to_name)(token_p->_id));
#   endif
}
