#include "approach-1/Easy.h"
#include "approach-1/Easy-token_ids.h"
#include <stdio.h>

static void  space(size_t N);
static void  print_token(QUEX_TYPE_ANALYZER* qlex, QUEX_TYPE_TOKEN* token_p); 
static void  my_print(QUEX_TYPE_ANALYZER* qlex, const char* Str1, 
                      const char* Str2 /* = 0x0 */, const char* Str3 /* = 0x0*/);

int 
main(int argc, char** argv) 
{        
    int                   number_of_tokens = 0;
    bool                  continue_lexing_f = true;
    const char*           included_file_name = 0x0;
    QUEX_TYPE_ANALYZER    qlex;
    QUEX_TYPE_TOKEN*      token_p;
    
    QUEX_NAME(from_file_name)(&qlex, argc == 1 ? "example-shallow.txt" : argv[1], 0x0);

    /* Loop until TERMINATION                                                 */
    do {
        qlex.receive(&qlex, &token_p);

        print_token(&qlex, token_p);

        if( token_p->id == QUEX_TKN_INCLUDE ) { 
            qlex.receive(&qlex, &token_p);

            print_token(&qlex, token_p);

            if( token_p->id != QUEX_TKN_IDENTIFIER ) {
                continue_lexing_f = false;
                my_print(&qlex, "Found 'include' without a subsequent filename: '%s' hm?\n",
                         (char*)QUEX_NAME_TOKEN(map_id_to_name)(token_p->id), 0x0);
                break;
            }
            my_print(&qlex, ">> including: ", (const char*)token_p->text, 0x0);
            included_file_name = ((const char*)token_p->text);
            qlex.include_push_file_name(&qlex, included_file_name, 0x0);
        }
        else if( token_p->id == QUEX_TKN_TERMINATION ) {
            space(qlex.include_depth);
            printf("Per File Letter Count = %i\n", (int)qlex.letter_count);
            if( qlex.include_pop(&qlex) == false ) 
                continue_lexing_f = false;
            else {
                my_print(&qlex, "<< return from include", 0x0, 0x0);
            }
        }

        ++number_of_tokens;

    } while( continue_lexing_f );

    printf("| [END] number of tokens = %i\n", (int)number_of_tokens);

    QUEX_NAME(destruct)(&qlex);
    return 0;
}

static void  
space(size_t N)
{ size_t i = 0; for(i=0; i<N; ++i) printf("    "); }

static void  
print_token(QUEX_TYPE_ANALYZER* qlex, QUEX_TYPE_TOKEN* token_p)
{ 
    const size_t    BufferSize = 1024;
    char            buffer[1024];
    space(qlex->include_depth);
    printf("(%02i, %02i) ", (int)token_p->_line_n, (int)token_p->_column_n);

    switch( token_p->id ) {
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

static void 
my_print(QUEX_TYPE_ANALYZER* qlex, const char* Str1, 
         const char* Str2 /* = 0x0 */, const char* Str3 /* = 0x0*/)
{
    space(qlex->include_depth);
    if( Str1 ) printf("%s", Str1);
    if( Str2 ) printf("%s", Str2);
    if( Str3 ) printf("%s", Str3);
    printf("\n");
}
