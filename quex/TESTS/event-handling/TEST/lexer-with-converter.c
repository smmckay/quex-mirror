
#include "EHLexer/EHLexer.h"
#include <EHLexer/lib/buffer/lexatoms/converter/icu/Converter_ICU>
#include <EHLexer/lib/buffer/lexatoms/converter/icu/Converter_ICU.i>         
#include <EHLexer/lib/buffer/lexatoms/converter/iconv/Converter_IConv>
#include <EHLexer/lib/buffer/lexatoms/converter/iconv/Converter_IConv.i>         

#include <stdio.h>    

static bool self_print_token(EHLexer_Token* token_p);

int 
main(int argc, char** argv) 
{        
    EHLexer       qlex;
    char          file_name[256];

    if( strncmp(argv[1], "icu", 3) == 0 ) {
        /* CHOICE 'icu-*' => remove first 4 characters.                       */
        snprintf(file_name, (size_t)256, "./examples/%s.txt", (const char*)&argv[1][4]);
        EHLexer_from_file_name(&qlex, file_name, 
                               EHLexer_Converter_ICU_new("UTF-8", NULL)); 
    }
    else if( strncmp(argv[1], "iconv", 3) == 0 ) {
        /* CHOICE 'iconv-*' => remove first 6 characters.                     */
        snprintf(file_name, (size_t)256, "./examples/%s.txt", (const char*)&argv[1][6]);
        EHLexer_from_file_name(&qlex, file_name, 
                               EHLexer_Converter_IConv_new("UTF-8", NULL)); 
    }
    else {
        printf("<error>\n");
        return 1;
    }

    qlex.run(&qlex, self_print_token, true);

    EHLexer_destruct(&qlex);
    return 0;
}

static bool
self_print_token(EHLexer_Token* token_p)
{
    const size_t    BufferSize = 1024;
    char            buffer[1024];

    switch( token_p->id ) {
    default:
        printf("%s \n", EHLexer_Token_get_string(token_p, buffer, BufferSize));
        break;
    }
    return true;
}
