#include <stdio.h> 

#include "iso8859-7/ISO8859_7_Lex.h"

int 
main(int argc, char** argv) 
{        
    ISO8859_7_Lex_Token*  token_p;
    ISO8859_7_Lex         qlex;
    size_t                BufferSize = 1024;
    char                  buffer[1024];
    (void)argc; (void)argv;
    
    ISO8859_7_Lex_from_file_name(&qlex, "example-iso8859-7.txt", NULL);

    // (*) loop until the 'termination' token arrives
    do {
        // (*) get next token from the token stream
        qlex.receive(&qlex, &token_p);

        /* (*) print out token information
         *     'get_string' automagically converts codec bytes into utf8 */
        printf("%s \n", QUEX_NAME_TOKEN(get_string)(token_p, buffer, BufferSize));
#       if 0
        cout << "\t\t plain bytes: ";
        for(QUEX_TYPE_LEXATOM* iterator = (uint8_t*)tmp.c_str(); *iterator ; ++iterator) {
            printf("%02X.", (int)*iterator);
        }
#       endif

        // (*) check against 'termination'
    } while( token_p->id != TKN_TERMINATION );

    ISO8859_7_Lex_destruct(&qlex);
    return 0;
}
