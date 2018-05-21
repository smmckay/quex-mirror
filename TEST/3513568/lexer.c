#include "Lexer/Lexer.h"
#include <Lexer/lib/multi.i>
#include <Lexer/lib/buffer/lexatoms/converter/icu/Converter_ICU>
#include <Lexer/lib/buffer/lexatoms/converter/icu/Converter_ICU.i>

int 
main(int argc, char** argv) 
{        
    Lexer   x;
    Lexer_Converter*  converter = Lexer_Converter_ICU_new("UCS4", NULL);
    Lexer_from_file_name(&x, "empty.txt", converter);
    Lexer_destruct(&x);

    return 0;
}

