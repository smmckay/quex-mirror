#include<fstream>    
#include<iostream> 

// (*) include lexical analyser header
#include "EasyLexer"
#include "EasyLexer-token_ids"

using namespace std;

static void  space(size_t N);
static void  print_token(QUEX_TYPE_ANALYZER* qlex, QUEX_TYPE_TOKEN* token_p, 
                         bool TextF /* = false */);
static void  print(QUEX_TYPE_ANALYZER* qlex, const char* Str1, 
                   const char* Str2 = 0, const char* Str3 = 0);

int 
main(int argc, char** argv) 
{        
    using namespace quex;
    QUEX_TYPE_TOKEN*      token_p;
    int                   number_of_tokens = 0;
    bool                  continue_lexing_f = true;
    char                  included_file_name[256];
    EasyLexer  qlex(argc == 1 ? "example.txt" : argv[1], NULL);

    cout << ",------------------------------------------------------------------------------------\n";
    cout << "| [START]\n";

    // (*) loop until the 'termination' token arrives
    do {
        // (*) get next token from the token stream
        qlex.receive(&token_p);

        // (*) print out token information
        print_token(&qlex, token_p, true);

        if( token_p->_id == QUEX_TKN_INCLUDE ) { 
            qlex.receive(&token_p);

            print_token(&qlex, token_p, true);

            /* The token queue *must* be empty, otherwise, the remaining tokens
             * get lost upon the event of 'include_push'.                     */
            __quex_assert(QUEX_NAME(TokenQueue_is_empty(&qlex._token_queue)));

            if( token_p->_id != QUEX_TKN_IDENTIFIER ) {
                continue_lexing_f = false;
                print(&qlex, "Found 'include' without a subsequent filename: '%s' hm?\n",
                      (char*)QUEX_NAME_TOKEN(map_id_to_name)(token_p->_id));
                break;
            }
            if( token_p->get_text().copy((uint8_t*)&included_file_name[0], (size_t)255) == token_p->get_text().length() ) {
                included_file_name[token_p->get_text().length()] = (char)0;
                print(&qlex, ">> including: ", (const char*)&included_file_name[0]);
                qlex.include_push(&included_file_name[0], NULL);
            }
        }
        else if( token_p->_id == QUEX_TKN_TERMINATION ) {
            space(qlex.include_depth);
            printf("Per File Letter Count = %i\n", (int)qlex.letter_count);
            if( qlex.include_pop() == false ) 
                continue_lexing_f = false;
            else {
                print(&qlex, "<< return from include");
            }
        }

        ++number_of_tokens;

        // (*) check against 'termination'
    } while( continue_lexing_f );

    cout << "| [END] number of token = " << number_of_tokens << "\n";
    cout << "`------------------------------------------------------------------------------------\n";

    return 0;
}

static void  
space(size_t N)
{ size_t i = 0; for(i=0; i<N; ++i) printf("    "); }

static void  
print_token(QUEX_TYPE_ANALYZER* qlex, QUEX_TYPE_TOKEN* token_p, bool TextF /* = false */)
{ 
    space(qlex->include_depth);
    printf("%i: (%i)", (int)token_p->line_number(), (int)token_p->column_number());
    printf("%s", token_p->type_id_name().c_str());
    if( TextF ) printf("\t'%s'", (char*)token_p->text.c_str());
    printf("\n");
}

static void 
print(QUEX_TYPE_ANALYZER* qlex, const char* Str1, 
      const char* Str2 /* = 0x0 */, const char* Str3 /* = 0x0*/)
{
    space(qlex->include_depth);
    if( Str1 ) printf("%s", Str1);
    if( Str2 ) printf("%s", Str2);
    if( Str3 ) printf("%s", Str3);
    printf("\n");
}
