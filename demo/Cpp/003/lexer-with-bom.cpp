#include<fstream>    
#include<iostream> 

// (*) include lexical analyser header
#include "EasyLexer"
#include <quex/code_base/bom>

int 
main(int argc, char** argv) 
{        
    using namespace std;
    using namespace quex;

    Token*                token_p = 0x0;
    FILE*                 fh = fopen(argc > 1 ? argv[1] : "example.txt", "rb");
    QUEX_TYPE_BOM         bom_type = quex::bom_snap(fh);

    cout << "Found BOM: " << bom_name(bom_type) << endl;

    /* Either there is no BOM, or if there is one, then it must be UTF8 */
    if( (bom_type & (QUEX_BOM_UTF_8 | QUEX_BOM_NONE)) == 0 ) {
        cout << "Found a non-UTF8 BOM. Exit\n";
        fclose(fh);
        return 0;
    }

    /* The lexer **must** be constructed after the BOM-cut */
    QUEX_NAME(ByteLoader)* byte_loader = QUEX_NAME(ByteLoader_FILE_new)(fh, true);
#   if   defined(QUEX_OPTION_CONVERTER_ICONV)
    QUEX_NAME(Converter)* converter = QUEX_NAME(Converter_IConv_new)("UTF8", NULL);
#   elif defined(QUEX_OPTION_CONVERTER_ICU)
    QUEX_NAME(Converter)* converter = QUEX_NAME(Converter_ICU_new)("UTF8", NULL);
#   else
#   define                converter NULL
#   endif
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
