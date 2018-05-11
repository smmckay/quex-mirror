#include <stdio.h>
#include <support/C/hwut_unit.h>
#include HEADER_FILE // "tiny.h"

int main(int argc, char** argv)
{
    Token*  token_p = 0x0;
    LEXER_TYPE   tlex;
    const char*  file_name = (const char*)0;
#   define       BufferSize 1024
    char         buffer[BufferSize];

    hwut_info(TITLE ";\n" \
              "CHOICES: bos-and-eos.txt, bos-eos.txt, bos-x-x-eos.txt, not-bos-eos.txt;");

    file_name = argv[1];

    QUEX_NAME(from_file_name)(&tlex, file_name, /* Converter */NULL);

    do {
        tlex.receive(&tlex, &token_p);

        printf("%s;\n", QUEX_NAME_TOKEN(get_string)(token_p, buffer, BufferSize));

    } while(    token_p->id     != QUEX_TKN_TERMINATION
             && tlex.error_code == E_Error_None );

    return 0;
}
