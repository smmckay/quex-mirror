#include <stdio.h> 

// (*) include lexical analyser header
#include "utf8/UTF8Lex.h"

int 
main(int argc, char** argv) 
{        
    quex_Token*   token_p = 0x0;
    size_t        BufferSize = 1024;
    char          buffer[1024];
    quex_UTF8Lex  qlex;
    (void)argc; (void)argv;

    QUEX_NAME(from_file_name)(&qlex, "example-utf8.txt", NULL);

    // (*) loop until the 'termination' token arrives
    do {
        // (*) get next token from the token stream
        qlex.receive(&qlex, &token_p);

        /* (*) print out token information
         *     'get_string' automagically converts codec bytes into utf8 */
        printf("%s \n", QUEX_NAME_TOKEN(get_string)(token_p, buffer, BufferSize));

        // (*) check against 'termination'
    } while( token_p->id != TKN_TERMINATION );

    QUEX_NAME(destruct)(&qlex);
    return 0;
}
