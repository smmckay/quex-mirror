#include<stdio.h> 

#include "moritz_Lexer.h"
#include <quex/code_base/buffer/lexatoms/converter/icu/Converter_ICU>
#include <quex/code_base/buffer/lexatoms/converter/icu/Converter_ICU.i>
#include "max_Lexer.h"
#include <quex/code_base/buffer/lexatoms/converter/icu/Converter_ICU>
#include <quex/code_base/buffer/lexatoms/converter/icu/Converter_ICU.i>
#include "boeck_Lexer.h"
#include <quex/code_base/buffer/lexatoms/converter/icu/Converter_ICU>
#include <quex/code_base/buffer/lexatoms/converter/icu/Converter_ICU.i>

/* When using multiple lexical analyzers, it must be compiled with 
 * QUEX_OPTION_MULTI and 'multi.i' must be included in one single file.      */
#include <quex/code_base/multi.i>


int 
main(int argc, char** argv) 
{        
    /* We want to have error outputs in stdout, so that the unit test could 
     * see it.                                                               */
    max_Lexer     max_lex;
    moritz_Lexer  moritz_lex;
    boeck_Lexer   boeck_lex;
    A_B_C_Token*  max_token    = 0x0;
    A_B_C_Token*  moritz_token = 0x0;
    A_B_C_Token*  boeck_token  = 0x0;
    const size_t  BufferSize = 1024;
    char          buffer[1024];
    size_t        i = 0;

    max_Lexer_Converter*    max_converter    = max_Lexer_Converter_ICU_new("UCS4", NULL);
    moritz_Lexer_Converter* moritz_converter = moritz_Lexer_Converter_ICU_new("UCS4", NULL);
    boeck_Lexer_Converter*  boeck_converter  = boeck_Lexer_Converter_ICU_new("UCS4", NULL);

    max_Lexer_from_file_name(&max_lex,       "ucs4.txt", max_converter);
    moritz_Lexer_from_file_name(&moritz_lex, "ucs4.txt", moritz_converter);
    boeck_Lexer_from_file_name(&boeck_lex,   "ucs4.txt", boeck_converter);

    /* Each lexer reads one token, since the grammars are similar the lexeme 
     * is always the same.                                                   */
    printf("                Max:        Moritz:      Boeck:\n");

    do {
        (void)max_Lexer_receive(&max_lex, &max_token);
        (void)moritz_Lexer_receive(&moritz_lex, &moritz_token);
        (void)boeck_Lexer_receive(&boeck_lex, &boeck_token);

        /* Lexeme is same for all three.                                     */
        (void)QUEX_NAME_TOKEN(lexeme_to_pretty_char)(boeck_token->text, buffer, BufferSize);
        printf("%s", &buffer[0]);

        size_t      preL   = (size_t)strlen((const char*)boeck_token->text);
        size_t      L      = preL < 10 ? preL : 10;
        for(i=0; i < 10 - L ; ++i) printf(" ");
        printf("\t");
        printf("%s   %s   %s\n", 
               A_B_C_Token_map_id_to_name(max_token->id),
               A_B_C_Token_map_id_to_name(moritz_token->id),
               A_B_C_Token_map_id_to_name(boeck_token->id));

    } while( boeck_token->id != TKN_TERMINATION );

    boeck_Lexer_destruct(&boeck_lex);
    max_Lexer_destruct(&max_lex);
    moritz_Lexer_destruct(&moritz_lex);

    return 0;
}
