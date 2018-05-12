#include <stdio.h>
#include "simple/simple.h"
#include "simple/simple-token_ids.h"
#define BUFFER_SIZE 1024
char file_buffer[BUFFER_SIZE];

#ifndef     ENCODING_NAME
#    define ENCODING_NAME (0x0)
#endif

int main(int argc, char** argv) {
    simple qlex;
    Token* token_p;
    char*  file_name = argc    ==   1    ?   "example.txt"    :   argv[1];

	simple_from_file_name(&qlex, file_name, ENCODING_NAME);
	do {
		qlex.receive(&qlex, &token_p);
		/* Print out token information            */
#       ifdef PRINT_LINE_COLUMN_NUMBER
		printf("(%i, %i)  \t", (int)token_p._line_n, (int)token_p._column_n);
#       endif
#       ifdef PRINT_TOKEN
		printf("%s \n", QUEX_NAME_TOKEN(get_string)(&token_p, buffer, BufferSize));
#       else
		printf("%s\n", QUEX_NAME_TOKEN(map_id_to_name)(token_p->id));
#       endif
	} while(token_p->id != QUEX_TKN_TERMINATION);

	simple_destruct(&qlex);
	return 0;
}

