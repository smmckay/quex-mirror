#include "Easy/Easy"
#include <Easy/lib/buffer/lexatoms/converter/icu/Converter_ICU>
#include <Easy/lib/buffer/lexatoms/converter/icu/Converter_ICU.i>         

#include <stdio.h>    

static bool self_print_token(Easy_Token* token_p);
static int  self_number_of_tokens = 0;

int 
main(int argc, char** argv) 
{        


    const char*      FileName  = (argc < 2) ? "example.txt" : argv[1];
    Easy_Converter*  converter = Easy_Converter_ICU_new("UTF8", NULL); 
    Easy             qlex(FileName, converter);

    qlex.run(self_print_token, true);

    printf("[END] number of tokens = %i\n", self_number_of_tokens);

    return 0;
}

static bool
self_print_token(Easy_Token* token_p)
{
    std::cout << "(" << token_p->line_number() << ", " << token_p->column_number() << ")  \t";

    switch( token_p->id ) {
    case QUEX_TKN_INDENT: 
    case QUEX_TKN_DEDENT: 
    case QUEX_TKN_NODENT: 
    case QUEX_TKN_TERMINATION: 
        std::cout << token_p->id_name() << std::endl;
        break;
    default:
        std::cout << std::string(*token_p) << std::endl;
        break;
    }

    ++self_number_of_tokens;
    return true;
}
