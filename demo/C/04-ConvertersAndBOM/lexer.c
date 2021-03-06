
#include "Easy/Easy.h"
#include <Easy/lib/buffer/lexatoms/converter/iconv/Converter_IConv>
#include <Easy/lib/buffer/lexatoms/converter/iconv/Converter_IConv.i>

#include <stdio.h>    

static bool self_print_token(Easy_Token* token_p);
static int  self_number_of_tokens = 0;

int 
main(int argc, char** argv) 
{        
    Easy             qlex;
    const char*      FileName  = (argc < 2) ? "example.txt" : argv[1];
    Easy_Converter*  converter = Easy_Converter_IConv_new("UTF8", NULL);

    Easy_from_file_name(&qlex, FileName, converter); 

    qlex.run(&qlex, self_print_token, true);

    printf("[END] number of tokens = %i\n", self_number_of_tokens);

    Easy_destruct(&qlex);
    return 0;
}

static bool
self_print_token(Easy_Token* token_p)
{
    const size_t    BufferSize = 1024;
    char            buffer[1024];

    printf("(%i, %i)  \t", (int)token_p->_line_n, (int)token_p->_column_n);

    switch( token_p->id ) {
    case QUEX_TKN_INDENT: 
    case QUEX_TKN_DEDENT: 
    case QUEX_TKN_NODENT: 
    case QUEX_TKN_TERMINATION: 
        printf("%s\n", Easy_map_token_id_to_name(token_p->id));
        break;
    default:
        printf("%s \n", Easy_Token_get_string(token_p, buffer, BufferSize));
        break;
    }

    ++self_number_of_tokens;
    return true;
}
