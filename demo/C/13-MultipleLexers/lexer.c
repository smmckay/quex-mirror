
#include "moritz/Lexer.h"
#include "moritz/lib/buffer/lexatoms/converter/iconv/Converter_IConv"
#include "moritz/lib/buffer/lexatoms/converter/iconv/Converter_IConv.i"
#include "max/Lexer.h"
#include "max/lib/buffer/lexatoms/converter/iconv/Converter_IConv"
#include "max/lib/buffer/lexatoms/converter/iconv/Converter_IConv.i"
#include "boeck/Lexer.h"

/* When using multiple lexical analyzers, it must be compiled with 
 * QUEX_OPTION_MULTI and 'multi.i' must be included in one single file.      */
#include <boeck/lib/multi.i>
#include <stdio.h> 

int 
main(int argc, char** argv) 
{        
    /* We want to have error outputs in stdout, so that the unit test could 
     * see it.                                                               */
    max_Lexer     max_lex;
    max_Token*    max_token    = 0x0;
    moritz_Lexer  moritz_lex;
    moritz_Token* moritz_token = 0x0;
    boeck_Lexer   boeck_lex;
    boeck_Token*  boeck_token  = 0x0;
    size_t        i, preL, L;
    (void)argc; (void)argv;

    max_Lexer_Converter*    converter_utf16 = max_Lexer_Converter_IConv_new("UTF16", NULL);
    moritz_Lexer_Converter* converter_ucs2  = moritz_Lexer_Converter_IConv_new("UCS-2", NULL);

    max_Lexer_from_file_name(&max_lex,       "example-utf16.txt", converter_utf16);
    moritz_Lexer_from_file_name(&moritz_lex, "example-ucs2.txt",  converter_ucs2);
    boeck_Lexer_from_file_name(&boeck_lex,   "example-utf8.txt",  NULL);

    /* Different lexers produce different interpretations on same lexeme.     */
    printf("                Max:        Moritz:      Boeck:\n");

    do {
        max_lex.receive(&max_lex, &max_token);
        moritz_lex.receive(&moritz_lex, &moritz_token);
        boeck_lex.receive(&boeck_lex, &boeck_token);

        /* Lexeme is same for all three. */
        preL   = (size_t)strlen((const char*)boeck_token->text);
        L      = preL < 10 ? preL : 10;
        printf("%s", boeck_token->text);

        for(i=0; i < 10 - L ; ++i) printf(" ");

        printf("\t");
        printf("%s   %s   %s\n", 
               max_Token_map_id_to_name(max_token->id),
               moritz_Token_map_id_to_name(moritz_token->id),
               boeck_Token_map_id_to_name(boeck_token->id));

    } while( boeck_token->id != TKN_TERMINATION );

    boeck_Lexer_destruct(&boeck_lex);
    max_Lexer_destruct(&max_lex);
    moritz_Lexer_destruct(&moritz_lex);

    return 0;
}

