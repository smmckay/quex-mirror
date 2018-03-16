#include "approach-2/Easy"
#include "approach-2/Easy-token_ids"
#include <stdio.h>

static void  space(size_t N);
static void  print_token(QUEX_TYPE_ANALYZER* qlex, QUEX_TYPE_TOKEN* token_p); 

int 
main(int argc, char** argv) 
{        
    quex::Easy   qlex(argc == 1 ? "example-shallow.txt" : argv[1], NULL);
    quex::Token* token_p = NULL;
    int          number_of_tokens = 0;

    do {
        qlex.receive(&token_p);
        if( ! token_p ) break;

        print_token(&qlex, token_p);

        ++number_of_tokens;

    } while( token_p->id != QUEX_TKN_TERMINATION );

    printf("[END] number of tokens = %i\n", number_of_tokens);
    if( qlex.error_code != E_Error_None ) qlex.print_this(); 

    return 0;
}

static void  
space(size_t N)
{ size_t i = 0; for(i=0; i<N; ++i) printf("    "); }

static void  
print_token(QUEX_TYPE_ANALYZER* qlex, QUEX_TYPE_TOKEN* token_p)
{ 
    using namespace quex;
    space(qlex->include_depth);
    printf("(%02i, %02i) ", (int)token_p->line_number(), (int)token_p->column_number());

    switch( token_p->id ) {
    case QUEX_TKN_TERMINATION: 
        std::cout << token_p->type_id_name() << std::endl;
        break;
    case QUEX_TKN_NUMBER: 
        std::cout << token_p->type_id_name() << ": " << token_p->number << std::endl;
        break;
    default:
        std::cout << std::string(*token_p) << std::endl;
        break;
    }
}

void 
my_print(QUEX_TYPE_ANALYZER* qlex, const char* Str1, 
         const char* Str2 /* = 0x0 */, const char* Str3 /* = 0x0*/)
{
    space(qlex->include_depth);
    if( Str1 ) printf("%s", Str1);
    if( Str2 ) printf("%s", Str2);
    if( Str3 ) printf("%s", Str3);
    printf("\n");
}
