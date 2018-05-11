#include <stdio.h>
#include "tiny/tiny.h"

int main(int argc, char** argv)
{
    Token*      token_p = 0x0;
    tiny        tlex;

    tiny_from_file_name(&tlex, "example.txt", /* Converter */NULL);

    do {
        tlex.receive(&tlex, &token_p);

        printf("%s\n", Token_map_id_to_name(token_p->id));

    } while(    token_p->id     != QUEX_TKN_TERMINATION
             && tlex.error_code == E_Error_None );

    tiny_destruct(&tlex);
    return 0;
}
