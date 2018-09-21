#include <stdio.h>

#include "Simple/Simple.h"

int 
main(int argc, char** argv) 
{        
    Simple  qlex;
    uint8_t buffer[4711];
    size_t  BufferSize = 4711;

    buffer[0] = buffer[4711 - 1] = QUEX_Simple_SETTING_BUFFER_LEXATOM_BUFFER_BORDER;
    Simple_from_memory(&qlex, 
                       &buffer[0], BufferSize, &buffer[1]); 

    printf("EOF-Pointer: %i\n",
           (int)(qlex.buffer.input.end_p - &qlex.buffer._memory._front[1])); 
    printf("Buffer Size: %i\n",
           (int)(qlex.buffer._memory._back - qlex.buffer._memory._front + 1)); 

    Simple_destruct(&qlex);
    printf("<terminated>\n");
    return 0;
}

