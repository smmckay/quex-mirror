#include<string.h>
#include<stdio.h>

#include "Simple/Simple.h"

int 
main(int argc, char** argv) 
{        
    const size_t        BufferSize = 1024;
    char                buffer[1024];
    Simple_Token*       token_p = 0x0;
    Simple_token_id_t   token_id = 0;
    Simple              qlex;
    Simple_Mode*        mode;

    const char*         mode_name = argv[1];
    const char*         file_name = argv[2];

    if     ( 0 == strcmp(mode_name, "PRE_X") )          mode = &Simple_PRE_X;
    else if( 0 == strcmp(mode_name, "PRE_X_PC") )       mode = &Simple_PRE_X_PC;
    else if( 0 == strcmp(mode_name, "PRE_X_DTC") )      mode = &Simple_PRE_X_DTC;
    else if( 0 == strcmp(mode_name, "PRE_LONG_X") )     mode = &Simple_PRE_LONG_X;
    else if( 0 == strcmp(mode_name, "PRE_LONG_X_PC") )  mode = &Simple_PRE_LONG_X_PC;
    else if( 0 == strcmp(mode_name, "PRE_LONG_X_DTC") ) mode = &Simple_PRE_LONG_X_DTC;


    Simple_from_file_name(&qlex, file_name, NULL); 
    qlex.set_mode_brutally(&qlex, mode);

    printf("START: initial buffer size: %i\n", 
            (int)(&qlex.buffer._memory._back[1] - qlex.buffer._memory._front));

    do {
        qlex.receive(&qlex, &token_p);
        token_id = token_p->id;
        printf("       %s\n", Simple_Token_get_string(token_p, buffer, BufferSize));
    } while( token_id != QUEX_TKN_TERMINATION );

    if( qlex.error_code != E_Error_None ) {
        qlex.print_this(&qlex);
    }

    printf("END: final buffer size: %i\n", 
            (int)(&qlex.buffer._memory._back[1] - qlex.buffer._memory._front));

    Simple_destruct(&qlex);

    return 0;
}
