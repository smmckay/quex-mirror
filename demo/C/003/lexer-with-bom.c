#include "EasyLexer.h"
#include <quex/code_base/bom>
#include <stdio.h>    

int 
main(int argc, char** argv) 
/* 1st arg: input file, default = 'example.txt'
 * 2nd arg: input character encoding name, 0x0 --> no conversion             */
{        
    quex_Token*     token_p = 0x0;
    const size_t    BufferSize = 1024;
    char            buffer[1024];
    int             number_of_tokens = 0;
    FILE*           fh = fopen(argc > 1 ? argv[1] : "example.txt", "rb");
    quex_EasyLexer  qlex;

    /* The lexer **must** be constructed after the BOM-cut */
    QUEX_NAME(ByteLoader)* byte_loader = QUEX_NAME(ByteLoader_FILE_new)(fh, true);
#   if   defined(QUEX_OPTION_CONVERTER_ICONV)
    QUEX_NAME(Converter)*  converter   = QUEX_NAME(Converter_IConv_new)(NULL, NULL);
#   elif defined(QUEX_OPTION_CONVERTER_ICU)
    QUEX_NAME(Converter)*  converter   = QUEX_NAME(Converter_ICU_new)(NULL, NULL);
#   else
#   define                 converter NULL
#   endif
    QUEX_TYPE_BOM          bom_id      = quex_bom_snap(fh);

    printf("Found BOM: %s\n", quex_bom_name(bom_id));

    if( bom_id == QUEX_BOM_NONE ) {
        /* No BOM in data stream => try to interpret data as UTF8 */
        converter->initialize(converter, "UTF8", NULL);
    }
    else if( ! converter->initialize_by_bom_id(converter, bom_id) ) {
        printf("Cannot treat coding given by BOM.\n");
        fclose(fh);
        converter->delete_self(converter);
        byte_loader->delete_self(byte_loader);
        return 0;
    }
    QUEX_NAME(from_ByteLoader)(&qlex, byte_loader, converter);

    printf(",-----------------------------------------------------------------\n");
    printf("| [START]\n");

    do {
        QUEX_NAME(receive)(&qlex, &token_p);

        printf("(%i, %i)  \t", (int)token_p->_line_n, (int)token_p->_column_n);
        printf("%s \n", QUEX_NAME_TOKEN(get_string)(token_p, buffer, BufferSize));

        ++number_of_tokens;
    } while( token_p->_id != QUEX_TKN_TERMINATION );

    printf("| [END] number of token = %i\n", number_of_tokens);
    printf("`-----------------------------------------------------------------\n");

    QUEX_NAME(destruct)(&qlex);

    fclose(fh);
    return 0;
}
