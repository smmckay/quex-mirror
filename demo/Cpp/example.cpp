#include<fstream>    
#include<iostream> 

#include "Easy"
#include <quex/code_base/buffer/lexatoms/converter/iconv/Converter_IConv>
#include <quex/code_base/buffer/lexatoms/converter/iconv/Converter_IConv.i>

static void print_token(quex::Token* token_p);

int 
main(int argc, char** argv) 
{        
    using namespace std;
    using namespace quex;

#   if   defined(QUEX_OPTION_CONVERTER_ICONV)
    QUEX_NAME(Converter)*    converter = QUEX_NAME(Converter_IConv_new)("UTF8", NULL);
#   elif defined(QUEX_OPTION_CONVERTER_ICU)
    QUEX_NAME(Converter)*    converter = QUEX_NAME(Converter_ICU_new)("UTF8", NULL);
#   else
#   define                   converter NULL
#   endif
    Easy    qlex(argc == 1 ? "example.txt" : argv[1], converter);
    Token*  token_p = 0;

    cout << ",-----------------------------------------------------------------\n";
    cout << "| [START]\n";

    int number_of_tokens = 0;
    while( qlex.error_code == E_Error_None ) {
        qlex.receive(&token_p);
        if( ! token_p ) break;

        print_token(token_p);

        ++number_of_tokens;

        if( token_p->type_id() == QUEX_TKN_TERMINATION ) break;
    }

    cout << "| [END] number of token = " << number_of_tokens << "\n";
    cout << "`-----------------------------------------------------------------\n";

    if( qlex.error_code != E_Error_None ) qlex.print_this(); 
    return 0;
}

static void
print_token(quex::Token* token_p)
{
    using namespace std;

#   ifdef PRINT_LINE_COLUMN_NUMBER
    cout << "(" << token_p->line_number() << ", " << token_p->column_number() << ")  \t";
#   endif
#   ifdef PRINT_TOKEN
    switch( token_p->id ) {
    case QUEX_TKN_INDENT: 
    case QUEX_TKN_DEDENT: 
    case QUEX_TKN_NODENT: 
    case QUEX_TKN_TERMINATION: 
        /* In this case, the token still carries an old lexeme; Printing it
         * would be confusing.                                               */
        cout << token_p->type_id_name() << endl;
        break;
    default:
        cout << string(*token_p) << endl;
        break;
    }
#   else
    cout << token_p->type_id_name() << endl;
#   endif
}
