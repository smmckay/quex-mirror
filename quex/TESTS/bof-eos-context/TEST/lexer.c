#include <stdio.h>
#include <support/C/hwut_unit.h>
#include HEADER_FILE // "tiny.h"

int main(int argc, char** argv)
{
    quex_Token*      token_p = 0x0;
    LEXER_TYPE       tlex;

    hwut_info(TITLE ";\n" \
              "CHOICES: 1, 2;");

    hwut_if_choice("1") {
        QUEX_NAME(from_file_name)(&tlex, "1.txt", /* Converter */NULL);
    }
    hwut_if_choice("2") {
        QUEX_NAME(from_file_name)(&tlex, "2.txt", /* Converter */NULL);
    }

    do {
        QUEX_NAME(receive)(&tlex, &token_p);

        printf("%s: %s;\n", QUEX_NAME_TOKEN(map_id_to_name)(token_p->id), token_p->text);

    } while(    token_p->id     != QUEX_TKN_TERMINATION
             && tlex.error_code == E_Error_None );

    return 0;
}
