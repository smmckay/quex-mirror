#include<cstdio> 

// (*) include lexical analyser header
#include "utf8/UTF8Lex"
#include "utf8/lib/lexeme_converter/from-utf8"
#include "utf8/lib/lexeme_converter/from-utf8.i"

using namespace std;

int 
main(int argc, char** argv) 
{        
    using namespace quex;

    Token*   token;
    UTF8Lex  qlex("example-utf8.txt");
    (void)argc; (void)argv;
    

    do {
        qlex.receive(&token);

        printf("%s\n", (char*)(string(*token).c_str()));

    } while( token->type_id() != TKN_TERMINATION );

    return 0;
}
