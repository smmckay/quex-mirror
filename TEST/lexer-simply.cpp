#include<fstream>    
#include<iostream> 

#include <./Simple>
#include "quex/code_base/buffer/bytes/ByteLoader_FILE.i"

#if   defined(QUEX_OPTION_CONVERTER_ICONV)
#   define QUEX_SETTING_UT_CONVERTER_NEW QUEX_NAME(Converter_IConv_new)
#elif defined(QUEX_OPTION_CONVERTER_ICU)
#   define QUEX_SETTING_UT_CONVERTER_NEW QUEX_NAME(Converter_ICU_new)
#elif defined(QUEX_SETTING_UT_CONVERTER_NEW)
#   undef  QUEX_SETTING_UT_CONVERTER_NEW
#endif

using namespace std;

int 
main(int argc, char** argv) 
{        
    using namespace quex;
    // we want to have error outputs in stdout, so that the unit test could see it.
    Token*      token_p;
#   ifdef STRANGE_STREAM
    ifstream                 istr("example.txt");
    StrangeStream<ifstream>  strange_stream(&istr);
    Simple                   qlex(&strange_stream);
#   elif defined (QUEX_SETTING_UT_CONVERTER_NEW)
    QUEX_NAME(ByteLoader)* byte_loader = QUEX_NAME(ByteLoader_FILE_new_from_file_name)(argv[1]);
    Simple  qlex(byte_loader, QUEX_SETTING_UT_CONVERTER_NEW, 
                 CONVERTER_ENCODING);
#   else
    Simple  qlex(argc == 1 ? "example.txt" : argv[1]);
#   endif

    cout << "## An Assert-Abortion might be an intended element of the experiment.\n";
#   ifdef QUEX_OPTION_TOKEN_POLICY_SINGLE
    token_p = qlex.token_p();
#   endif
    do {
#       ifdef QUEX_OPTION_TOKEN_POLICY_SINGLE
        qlex.receive();
#       else
        qlex.receive(&token_p);
#       endif
        if( token_p->type_id() == QUEX_TKN_TERMINATION ) {
            token_p->text = (QUEX_TYPE_LEXATOM*)"";
        }
#       ifdef PRINT_LINE_COLUMN
        cout << "(" << qlex.line_number() << ", " << qlex.column_number() << ")  \t";
#       endif
        if( token_p->type_id() != QUEX_TKN_TERMINATION )
            cout << string(*token_p) << endl;
        else
            cout << "<TERMINATION>\n";
        cout.flush();
    } while( token_p->type_id() != QUEX_TKN_TERMINATION );

    return 0;
}

