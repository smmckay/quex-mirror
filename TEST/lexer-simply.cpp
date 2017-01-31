#include<fstream>    
#include<iostream> 

#include <Simple>
#include "quex/code_base/buffer/bytes/ByteLoader_FILE.i"

#ifndef    CONVERTER
#   define CONVERTER 0
#endif

using namespace std;

int 
main(int argc, char** argv) 
{        
    using namespace quex;
    // we want to have error outputs in stdout, so that the unit test could see it.
    Token*                   token_p;
    const char*              file_name = argc < 2 ? "example.txt" : argv[1];

#   ifdef STRANGE_STREAM
    ifstream                 istr(file_name);
    StrangeStream<ifstream>  strange_stream(&istr);
    QUEX_NAME(ByteLoader)*   byte_loader = QUEX_NAME(ByteLoader_stream_new)(&strange_stream);
#   else
    QUEX_NAME(ByteLoader)*   byte_loader = QUEX_NAME(ByteLoader_FILE_new_from_file_name)(file_name);
#   endif

#   if   defined(QUEX_OPTION_CONVERTER_ICONV)
    QUEX_NAME(Converter)*    converter = QUEX_NAME(Converter_IConv_new)("UTF8", NULL);
#   elif defined(QUEX_OPTION_CONVERTER_ICU)
    QUEX_NAME(Converter)*    converter = QUEX_NAME(Converter_ICU_new)("UTF8", NULL);
#   else
#   define                   converter NULL
#   endif
    Simple                   qlex(byte_loader, converter); 

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

