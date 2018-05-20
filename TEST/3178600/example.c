#include <stdio.h>    

#include "EasyLexer/EasyLexer.h"


int 
main(int argc, char** argv) 
{        
    EasyLexer           qlex;
    EasyLexer_Token*    token_p = 0x0;
    const size_t   BufferSize = 1024;
    char           buffer[1024];
    const char*    FileName = "example.txt";

    EasyLexer_from_file_name(&qlex, FileName, (void*)0);

    do {
        qlex.receive(&qlex, &token_p);

        printf("%s \n", EasyLexer_Token_get_string(token_p, buffer, BufferSize));

    } while( token_p->id != QUEX_TKN_TERMINATION );

    EasyLexer_destruct(&qlex);

    return 0;
}
