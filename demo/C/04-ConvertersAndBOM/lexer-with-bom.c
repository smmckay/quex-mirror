#include "Easy/Easy.h"
#include <Easy/lib/buffer/lexatoms/converter/iconv/Converter_IConv>
#include <Easy/lib/buffer/lexatoms/converter/iconv/Converter_IConv.i>
/* #include <Easy/lib/buffer/lexatoms/converter/icu/Converter_ICU>
 * #include <Easy/lib/buffer/lexatoms/converter/icu/Converter_ICU.i>          */

#include <Easy/lib/bom>
#include <stdio.h>    

static void print_token(quex_Token* token_p);

int 
main(int argc, char** argv) 
/* 1st arg: input file, default = 'example.txt'
 * 2nd arg: input character encoding name, 0x0 --> no conversion              */
{        
    quex_Easy   qlex;
    quex_Token* token_p = 0x0;
    int         number_of_tokens = 0;
    FILE*       fh = fopen(argc > 1 ? argv[1] : "example.txt", "rb");

    /* The lexer must be constructed AFTER the BOM-cut                        */
    QUEX_NAME(ByteLoader)*    byte_loader = QUEX_NAME(ByteLoader_FILE_new)(fh, true);
    QUEX_NAME(Converter)*     converter   = QUEX_NAME(Converter_IConv_new)(NULL, NULL);
    /* QUEX_NAME(Converter)*  converter   = QUEX_NAME(Converter_ICU_new)(NULL, NULL); */
    QUEX_TYPE_BOM             bom_id      = quex_bom_snap(fh);

    printf("Found BOM: %s\n", quex_bom_name(bom_id));

    if( bom_id == QUEX_BOM_NONE ) {
        /* No BOM in data stream => try to interpret data as UTF8             */
        converter->initialize(converter, "UTF8", NULL);
    }
    else if( ! converter->initialize_by_bom_id(converter, bom_id) ) {
        printf("Cannot treat coding given by BOM.\n");
        fclose(fh);
        converter->delete_self(converter);
        byte_loader->delete_self(byte_loader);
        return 0;
    }
    quex_Easy_from_ByteLoader(&qlex, byte_loader, converter);

    do {
        qlex.receive(&qlex, &token_p);

        print_token(token_p);

        ++number_of_tokens;
    } while( token_p->id != QUEX_TKN_TERMINATION );

    printf("| [END] number of token = %i\n", number_of_tokens);

    quex_Easy_destruct(&qlex);

    fclose(fh);
    return 0;
}

static void
print_token(quex_Token* token_p)
{
    const size_t    BufferSize = 1024;
    char            buffer[1024];

    printf("(%i, %i)  \t", (int)token_p->_line_n, (int)token_p->_column_n);

    switch( token_p->id ) {
    case QUEX_TKN_INDENT: 
    case QUEX_TKN_DEDENT: 
    case QUEX_TKN_NODENT: 
    case QUEX_TKN_TERMINATION: 
        printf("%s\n", QUEX_NAME_TOKEN(map_id_to_name)(token_p->id));
        break;
    default:
        printf("%s \n", QUEX_NAME_TOKEN(get_string)(token_p, buffer, BufferSize));
        break;
    }
}
