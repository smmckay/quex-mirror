    #include <stdio.h>
    #include "tiny/tiny.h"

    int main(int argc, char** argv)
    {
        quex_Token*      token_p = 0x0;
        quex_tiny        tlex;

        QUEX_NAME(from_file_name)(&tlex, "example.txt", /* Converter */NULL);

        do {
            tlex.receive(&tlex, &token_p);

            printf("%s\n", QUEX_NAME_TOKEN(map_id_to_name)(token_p->id));

        } while(    token_p->id     != QUEX_TKN_TERMINATION
                 && tlex.error_code == E_Error_None );

        return 0;
    }
