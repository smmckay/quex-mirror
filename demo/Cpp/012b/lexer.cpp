#include<cstdio> 

#include "moritz_Lexer"
#include "max_Lexer"
#include "boeck_Lexer"

/* When using multiple lexical analyzers, it must be compiled with 
 * QUEX_OPTION_MULTI and 'multi.i' must be included in one single file.      */
#include <quex/code_base/multi.i>


int 
main(int argc, char** argv) 
{        
    using namespace std;

    // we want to have error outputs in stdout, so that the unit test could see it.
    max::Lexer     max_lex("ucs4.txt", "UCS4");
    A::B::C::Token* max_token    = 0x0;
    moritz::Lexer  moritz_lex("ucs4.txt", "UCS4");
    A::B::C::Token* moritz_token = 0x0;
    boeck::Lexer   boeck_lex("ucs4.txt", "UCS4");
    A::B::C::Token* boeck_token  = 0x0;


    // Each lexer reads one token, since the grammars are similar the lexeme 
    // is always the same.                                                    
    printf("                Max:        Moritz:      Boeck:\n");

    max_token    = max_lex.token_p();
    moritz_token = moritz_lex.token_p();
    boeck_token  = boeck_lex.token_p();
    do {
        (void)max_lex.receive();
        (void)moritz_lex.receive();
        (void)boeck_lex.receive();

        /* Lexeme is same for all three. */
        int  L = (int)max_token->text.length();

        printf("%s", max_token->pretty_char_text().c_str());

        for(int i=0; i < 10 - L ; ++i) printf(" ");
        printf("\t");
        printf("%s   %s   %s\n", 
               max_token->type_id_name().c_str(), 
               moritz_token->type_id_name().c_str(), 
               boeck_token->type_id_name().c_str());

    } while( boeck_token->type_id() != TKN_TERMINATION );

    return 0;
}

