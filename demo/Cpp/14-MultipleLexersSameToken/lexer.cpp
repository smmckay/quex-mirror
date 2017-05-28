#include<cstdio> 

#include "moritz_Lexer"
#include <quex/code_base/buffer/lexatoms/converter/icu/Converter_ICU>
#include <quex/code_base/buffer/lexatoms/converter/icu/Converter_ICU.i>
#include "max_Lexer"
#include <quex/code_base/buffer/lexatoms/converter/icu/Converter_ICU>
#include <quex/code_base/buffer/lexatoms/converter/icu/Converter_ICU.i>
#include "boeck_Lexer"
#include <quex/code_base/buffer/lexatoms/converter/icu/Converter_ICU>
#include <quex/code_base/buffer/lexatoms/converter/icu/Converter_ICU.i>

/* When using multiple lexical analyzers, it must be compiled with 
 * QUEX_OPTION_MULTI and 'multi.i' must be included in one single file.      */
#include <quex/code_base/multi.i>


int 
main(int argc, char** argv) 
{        
    using namespace std;

    // we want to have error outputs in stdout, so that the unit test could see it.
    max::Lexer      max_lex("ucs4.txt", max::Lexer_Converter_ICU_new("UCS4", NULL));
    A::B::C::Token* max_token    = 0x0;
    moritz::Lexer   moritz_lex("ucs4.txt", moritz::Lexer_Converter_ICU_new("UCS4", NULL));
    A::B::C::Token* moritz_token = 0x0;
    boeck::Lexer    boeck_lex("ucs4.txt", boeck::Lexer_Converter_ICU_new("UCS4", NULL));
    A::B::C::Token* boeck_token  = 0x0;

    // Each lexer reads one token, since the grammars are similar the lexeme 
    // is always the same.                                                    
    printf("                Max:        Moritz:      Boeck:\n");

    do {
        (void)max_lex.receive(&max_token);
        (void)moritz_lex.receive(&moritz_token);
        (void)boeck_lex.receive(&boeck_token);

        /* Lexeme is same for all three. */
        int  L = A::B::C::Token_lexeme_length(max_token->text);

        printf("%s", (char*)A::B::C::Token_lexeme_to_pretty_char(max_token->text).c_str());

        for(int i=0; i < 10 - L ; ++i) printf(" ");
        printf("\t");
        printf("%s   %s   %s\n", 
               max_token->type_id_name().c_str(), 
               moritz_token->type_id_name().c_str(), 
               boeck_token->type_id_name().c_str());

    } while( boeck_token->type_id() != TKN_TERMINATION );

    return 0;
}

