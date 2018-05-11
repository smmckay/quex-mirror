#include <stdio.h> 

// (*) include lexical analyser header
#include "utf8/UTF8Lex.h"

int 
main(int argc, char** argv) 
{        
    Token*        token_p = 0x0;
    size_t        BufferSize = 1024;
    char          buffer[1024];
    UTF8Lex       qlex;
    (void)argc; (void)argv;

    UTF8Lex_from_file_name(&qlex, "example-utf8.txt", NULL);

    // (*) loop until the 'termination' token arrives
    do {
        // (*) get next token from the token stream
        qlex.receive(&qlex, &token_p);

        /* (*) print out token information
         *     'get_string' automagically converts codec bytes into utf8 */
        printf("%s \n", QUEX_NAME_TOKEN(get_string)(token_p, buffer, BufferSize));

        // (*) check against 'termination'
    } while( token_p->id != TKN_TERMINATION );

    UTF8Lex_destruct(&qlex);
    return 0;
}
