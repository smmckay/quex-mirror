#include "Lexer/Lexer.h"

#include <stdlib.h>

int main(int argc, char* argv[])
{
    Lexer lex;
    Lexer_from_file_name(&lex, argv[1], 0x0);

    while (1) {
        Lexer_Token* t = NULL;
        lex.receive(&lex, &t);

        if (QUEX_TKN_TERMINATION == t->id)
            break;

        printf("id=%s text=[%s]\n",
               Lexer_map_token_id_to_name(t->id),
               t->text);
    }

    Lexer_destruct(&lex);

    return 0;
}
