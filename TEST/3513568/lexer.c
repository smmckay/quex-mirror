#include "boeck_Lexer.h"
#include <quex/code_base/multi.i>
#include <quex/code_base/buffer/lexatoms/converter/icu/Converter_ICU>
#include <quex/code_base/buffer/lexatoms/converter/icu/Converter_ICU.i>

int 
main(int argc, char** argv) 
{        
    boeck_Lexer   x;
    QUEX_NAME(Converter)*  converter = QUEX_NAME(Converter_ICU_new)("UCS4", NULL);
    boeck_Lexer_from_file_name(&x, "empty.txt", converter);
    boeck_Lexer_destruct(&x);

    return 0;
}

