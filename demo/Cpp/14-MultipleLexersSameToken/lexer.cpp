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

/* When using multiple lexical analyzers, it must be compiled with 
 * QUEX_OPTION_MULTI and 'multi.i' must be included in one single file.      */
#include <boeck/lib/multi.i>


int 
main(int argc, char** argv) 
{        
    using namespace std;

    max::Lexer      max_lex("ucs4.txt", max::Lexer_Converter_ICU_new("UCS4", NULL));
    A::B::Token* max_token    = 0x0;
    moritz::Lexer   moritz_lex("ucs4.txt", moritz::Lexer_Converter_ICU_new("UCS4", NULL));
    A::B::Token* moritz_token = 0x0;
    boeck::Lexer    boeck_lex("ucs4.txt", boeck::Lexer_Converter_ICU_new("UCS4", NULL));
    A::B::Token* boeck_token  = 0x0;
    (void)argc; (void)argv;

    printf("                Max:        Moritz:      Boeck:\n");

    do {
        (void)max_lex.receive(&max_token);
        (void)moritz_lex.receive(&moritz_token);
        (void)boeck_lex.receive(&boeck_token);

        /* Lexeme is same for all three.                                      */
        size_t  L = A::B::Token_lexeme_length(max_token->text);

        printf("%s", (char*)A::B::Token_lexeme_to_pretty_char(max_token->text).c_str());

        for(size_t i=0; i < (size_t)10 - L ; ++i) printf(" ");
        printf("\t");
        printf("%s   %s   %s\n", 
               max_token->type_id_name().c_str(), 
               moritz_token->type_id_name().c_str(), 
               boeck_token->type_id_name().c_str());

    } while( boeck_token->id != TKN_TERMINATION );

    return 0;
}

