#include "Simple/Simple.h"
#include "support/C/hwut_unit.h"

#ifndef    CHARACTER_ENCODING_NAME 
#   define CHARACTER_ENCODING_NAME 0x0
#endif

int 
main(int argc, char** argv) 
{        
#   ifdef PRINT_TOKEN
    const size_t BufferSize = 1024;
    char         buffer[1024];
#   endif
    Simple_Token*      token_p = 0x0;
    int                token_n = 0;
    Simple             qlex;
    const char*        file_name = argc > 1 ? argv[1] : "example.txt";

    QUEX_NAME(from_file_name)(&qlex, file_name, CHARACTER_ENCODING_NAME);

    printf(",------------------------------------------------------------------------------------\n");
    printf("| [START]\n");
    fflush(stdout);
    fflush(stderr);

    /* Loop until the 'termination' token arrives */
    token_n = 0;

    do {
        /* Get next token from the token stream   */
        qlex.receive(&qlex, &token_p);
        printf("(%i, %i)  \t", (int)token_p->_line_n, (int)token_p->_column_n);
        /* Print out token information            */
        fflush(stderr);
        printf("%s: ", QUEX_NAME_TOKEN(map_id_to_name)(token_p->id));
        switch( token_p->id ) {
        case QUEX_TKN_ON_AFTER_MATCH:
        case QUEX_TKN_ON_MATCH______:
            printf("%i\n", (int)token_p->number); 
            break;
        default:
            hwut_verify(QUEX_NAME(lexeme_to_pretty_char)(token_p->text, buffer, &buffer[BufferSize]));
            printf("%s\n", &buffer[0]); 
            break;
        }
        fflush(stdout);

        ++token_n;
        /* Check against 'termination'            */
    } while( token_p->id != QUEX_TKN_TERMINATION );

    printf("| [END] number of token = %i\n", token_n);
    printf("`------------------------------------------------------------------------------------\n");

    return 0;
}
