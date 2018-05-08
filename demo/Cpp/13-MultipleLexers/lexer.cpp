#include<cstdio> 

#include "moritz/Lexer"
#include "moritz/lib/buffer/lexatoms/converter/iconv/Converter_IConv"
#include "moritz/lib/buffer/lexatoms/converter/iconv/Converter_IConv.i"
#include "max/Lexer"
#include "max/lib/buffer/lexatoms/converter/iconv/Converter_IConv"
#include "max/lib/buffer/lexatoms/converter/iconv/Converter_IConv.i"
#include "boeck/Lexer"

/* When using multiple lexical analyzers, it must be compiled with 
 * QUEX_OPTION_MULTI and 'multi.i' must be included in one single file.      */
#include <boeck/lib/multi.i>

using namespace std;


int 
main(int argc, char** argv) 
{        
    // we want to have error outputs in stdout, so that the unit test could see it.
    max::Lexer      max_lex("example-utf16.txt", max::Lexer_Converter_IConv_new("UTF16", NULL));
    moritz::Lexer   moritz_lex("example-ucs2.txt", moritz::Lexer_Converter_IConv_new("UCS-2", NULL));
    boeck::Lexer    boeck_lex("example-utf8.txt");
    max::Token*     max_token    = 0x0;
    moritz::Token*  moritz_token = 0x0;
    boeck::Token*   boeck_token  = 0x0;
    (void)argc; (void)argv;

    // Different lexers produce different interpretations on same lexeme.
    printf("                Max:        Moritz:      Boeck:\n");

    do {
        max_lex.receive(&max_token);
        moritz_lex.receive(&moritz_token);
        boeck_lex.receive(&boeck_token);

        /* Lexeme is same for all three. */
        size_t   L = max::Lexer_lexeme_length(max_token->text);

        printf("%s", (char*)max::Lexer_lexeme_to_pretty_char(max_token->text).c_str());

        for(size_t i=0; i < 10 - L ; ++i) printf(" ");
        printf("\t");
        printf("%s   %s   %s\n", 
               max_token->type_id_name().c_str(), 
               moritz_token->type_id_name().c_str(), 
               boeck_token->type_id_name().c_str());

    } while( boeck_token->type_id() != TKN_TERMINATION );

    return 0;
}

