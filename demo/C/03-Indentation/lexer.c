#ifndef LEXER2
#   include "Easy/Easy.h"
typedef Easy  Lexer;
typedef Token Token;
#define CONSTRUCT Easy_from_file_name
#define DESTRUCT  Easy_destruct
#else
#   include "Easy2/Easy2.h"
typedef Easy2  Lexer;
typedef Token  Token;
#define CONSTRUCT Easy2_from_file_name
#define DESTRUCT  Easy2_destruct
#endif

#include<stdio.h>    

static void print_token(Token* token_p);

int 
main(int argc, char** argv) 
{        
    Lexer   qlex;
    Token*  token_p = 0;

    CONSTRUCT(&qlex, argc == 1 ? "example.txt" : argv[1], NULL); 

    int number_of_tokens = 0;
    do {
        qlex.receive(&qlex, &token_p);
        if( ! token_p ) break;

        print_token(token_p);

        ++number_of_tokens;

    } while( token_p->id != QUEX_TKN_TERMINATION );

    printf("[END] number of tokens = %i\n", number_of_tokens);
    if( qlex.error_code != E_Error_None ) qlex.print_this(&qlex); 

    DESTRUCT(&qlex);

    return 0;
}

static void
print_token(Token* token_p)
{
    const size_t    BufferSize = 1024;
    char            buffer[1024];
    printf("(%i, %i)  \t", (int)token_p->_line_n, (int)token_p->_column_n);

    switch( token_p->id ) {
    case QUEX_TKN_INDENT:
    case QUEX_TKN_DEDENT:
    case QUEX_TKN_NODENT:
    case QUEX_TKN_BRACKET_O:
    case QUEX_TKN_BRACKET_C:
    case QUEX_TKN_CURLY_BRACKET_O:
    case QUEX_TKN_CURLY_BRACKET_C:
    case QUEX_TKN_OP_EQUAL:
    case QUEX_TKN_IF:
    case QUEX_TKN_ELSE:
    case QUEX_TKN_AND:
    case QUEX_TKN_OR:
    case QUEX_TKN_COLON:
    case QUEX_TKN_FOR:
    case QUEX_TKN_IN:
    case QUEX_TKN_INDENTATION:
    case QUEX_TKN_STRUCT:
    case QUEX_TKN_SEMICOLON:
    case QUEX_TKN_ERROR_MISALIGNED_INDENTATION:
    case QUEX_TKN_DOTS:
    case QUEX_TKN_FAILURE:
    case QUEX_TKN_TERMINATION: 
        /* In this case, the token still might carry an old lexeme. 
         * Printing it would be confusing.                                    */
        printf("%s\n", QUEX_NAME_TOKEN(map_id_to_name)(token_p->id));
        break;
    case QUEX_TKN_NUMBER: 
        /* In this case, the token still might carry an old lexeme. 
         * Printing it would be confusing.                                    */
        printf("%s: %i\n", QUEX_NAME_TOKEN(map_id_to_name)(token_p->id), (int)token_p->number);
        break;
    default:
        printf("%s \n", QUEX_NAME_TOKEN(get_string)(token_p, buffer, BufferSize));
        break;
    }
}
