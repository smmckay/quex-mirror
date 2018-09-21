#include<stdio.h> 

#include "moritz/Lexer"
#include "moritz/lib/buffer/lexatoms/converter/icu/Converter_ICU"
#include "moritz/lib/buffer/lexatoms/converter/icu/Converter_ICU.i"
#include "max/Lexer"
#include "max/lib/buffer/lexatoms/converter/icu/Converter_ICU"
#include "max/lib/buffer/lexatoms/converter/icu/Converter_ICU.i"
#include "boeck/Lexer"
#include "boeck/lib/buffer/lexatoms/converter/icu/Converter_ICU"
#include "boeck/lib/buffer/lexatoms/converter/icu/Converter_ICU.i"

int 
main(int argc, char** argv) 
{        
    using namespace std;

    max::Lexer      max_lex("ucs4.txt", max::Lexer_Converter_ICU_new("UCS4", NULL));
    Common::Token*  max_token    = 0x0;
    moritz::Lexer   moritz_lex("ucs4.txt", moritz::Lexer_Converter_ICU_new("UCS4", NULL));
    Common::Token*  moritz_token = 0x0;
    boeck::Lexer    boeck_lex("ucs4.txt", boeck::Lexer_Converter_ICU_new("UCS4", NULL));
    Common::Token*  boeck_token  = 0x0;
    (void)argc; (void)argv;

    printf("                Max:        Moritz:      Boeck:\n");

    do {
        (void)max_lex.receive(&max_token);
        (void)moritz_lex.receive(&moritz_token);
        (void)boeck_lex.receive(&boeck_token);

        /* Lexeme is same for all three.                                      */
        size_t  L = Global_lexeme_length(max_token->text);

        printf("%s", (char*)Global_lexeme_to_pretty_char(max_token->text).c_str());

        for(size_t i=0; i < (size_t)10 - L ; ++i) printf(" ");
        printf("\t");
        printf("%s   %s   %s\n", 
               max::Lexer_map_token_id_to_name(max_token->id),
               moritz::Lexer_map_token_id_to_name(moritz_token->id),
               boeck::Lexer_map_token_id_to_name(boeck_token->id));

    } while( boeck_token->id != TKN_TERMINATION );

    return 0;
}

