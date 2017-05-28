#include<fstream>    
#include<iostream> 

#include "EasyLexer"
#include <quex/code_base/buffer/lexatoms/converter/iconv/Converter_IConv>
#include <quex/code_base/buffer/lexatoms/converter/iconv/Converter_IConv.i>

int 
main(int argc, char** argv) 
{        
    using namespace std;
    using namespace quex;

    Token*                 token_p = 0x0;
    FILE*                  fh      = fopen(argc > 1 ? argv[1] : "example.txt", "rb");
    /* The lexer **must** be constructed after the BOM-cut */
    QUEX_NAME(ByteLoader)* byte_loader = QUEX_NAME(ByteLoader_FILE_new)(fh, true);
#   if   defined(QUEX_OPTION_CONVERTER_ICONV)
    QUEX_NAME(Converter)*  converter   = QUEX_NAME(Converter_IConv_new)(NULL, NULL);
#   elif defined(QUEX_OPTION_CONVERTER_ICU)
    QUEX_NAME(Converter)*  converter   = QUEX_NAME(Converter_ICU_new)(NULL, NULL);
#   else
#   define                 converter NULL
#   endif
    QUEX_TYPE_BOM          bom_id      = quex::bom_snap(fh);

    cout << "Found BOM: " << bom_name(bom_id) << endl;

    if( bom_id == QUEX_BOM_NONE ) {
        /* No BOM in data stream => try to interpret data as UTF8 */
        converter->initialize(converter, "UTF8", NULL);
    }
    else if( ! converter->initialize_by_bom_id(converter, bom_id) ) {
        cout << "Cannot treat coding given by BOM.\n";
        fclose(fh);
        converter->delete_self(converter);
        byte_loader->delete_self(byte_loader);
        return 0;
    }
    EasyLexer             qlex(byte_loader, converter);

    cout << ",-----------------------------------------------------------------\n";
    cout << "| [START]\n";

    int number_of_tokens = 0;
    do {
        qlex.receive(&token_p);

        cout << "(" << token_p->line_number() << ", " << token_p->column_number() << ")  \t";
        cout << string(*token_p) << endl;
        ++number_of_tokens;

    } while( token_p->type_id() != QUEX_TKN_TERMINATION );

    cout << "| [END] number of token = " << number_of_tokens << "\n";
    cout << "`-----------------------------------------------------------------\n";

    fclose(fh);
    return 0;
}
