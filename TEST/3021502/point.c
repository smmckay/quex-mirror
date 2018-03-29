#include <stdio.h>

#include "Simple/Simple.h"

int 
main(int argc, char** argv) 
{        
    quex_Simple  qlex;
    uint8_t      buffer[4711];
    size_t       BufferSize = 4711;

    buffer[0] = buffer[4711 - 1] = QUEX_SETTING_BUFFER_LIMIT_CODE;
    QUEX_NAME(from_memory)(&qlex, 
                           &buffer[0], BufferSize, &buffer[1]); 

    printf("EOF-Pointer: %i\n",
           (int)(qlex.buffer.input.end_p - &qlex.buffer._memory._front[1])); 
    printf("Buffer Size: %i\n",
           (int)(qlex.buffer._memory._back - qlex.buffer._memory._front + 1)); 

    QUEX_NAME(destruct)(&qlex);
    printf("<terminated>\n");
    return 0;
}

