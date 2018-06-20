#include "Easy/Easy"
#include <Easy/lib/buffer/lexatoms/converter/iconv/Converter_IConv>
#include <Easy/lib/buffer/lexatoms/converter/iconv/Converter_IConv.i>
#include <Easy/lib/quex/bom.i>
#include <stdio.h>    

static void print_token(Easy_Token* token_p);

int 
main(int argc, char** argv) 
/* 1st arg: input file, default = 'example.txt'
 * 2nd arg: input character encoding name, 0x0 --> no conversion              */
{        


    Easy_Token* token_p          = 0x0;
    int          number_of_tokens = 0;
    FILE*        fh               = fopen(argc > 1 ? argv[1] : "example.txt", "rb");

    /* The lexer must be constructed AFTER the BOM-cut                        */
    Easy_ByteLoader*    byte_loader = Easy_ByteLoader_FILE_new(fh, true);
    Easy_Converter*     converter   = Easy_Converter_IConv_new(NULL, NULL);
    E_ByteOrderMark       bom_id    = quex::bom_snap(fh);

    printf("Found BOM: %s\n", quex::bom_name(bom_id));

    if( bom_id == QUEX_BOM_NONE ) {
        /* No BOM in data stream => try to interpret data as UTF8             */
        converter->initialize(converter, "UTF8", NULL);
    }
    else if( ! converter->initialize_by_bom_id(converter, bom_id) ) {
        printf("Cannot treat encoding given by BOM.\n");
        fclose(fh);
        converter->delete_self(converter);
        byte_loader->delete_self(byte_loader);
        return 0;
    }

    Easy   qlex(byte_loader, converter);
    do {
        qlex.receive(&token_p);

        print_token(token_p);

        ++number_of_tokens;
    } while( token_p->id != QUEX_TKN_TERMINATION );

    std::cout << "| [END] number of token = " << number_of_tokens << std::endl;

    fclose(fh);
    return 0;
}

static void
print_token(Easy_Token* token_p)
{
    std::cout << "(" << token_p->line_number() << ", " << token_p->column_number() << ")  \t";

    switch( token_p->id ) {
    case QUEX_TKN_INDENT: 
    case QUEX_TKN_DEDENT: 
    case QUEX_TKN_NODENT: 
    case QUEX_TKN_TERMINATION: 
        std::cout << token_p->id_name() << std::endl;
        break;
    default:
        std::cout << std::string(*token_p) << std::endl;
        break;
    }
}
