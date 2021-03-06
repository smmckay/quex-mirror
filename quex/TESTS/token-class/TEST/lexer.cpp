#include<fstream>    
#include<iostream> 

// (*) include lexical analyser header
#include "Simple/Simple"

using namespace std;
using namespace europa::deutschland::baden_wuertemberg;

int 
main(int argc, char** argv) 
{        
    if( argc > 1 && strcmp("--hwut-info", argv[1]) == 0 ) {
        printf("With token policy 'queue'.\n");
        return 0;
    }
    Simple           qlex("example.txt");
    ispringen::MeinToken*  token_p = qlex.token_p();

    // (*) Access the '__nonsense__' member to ensure it has been generated
    token_p->__nonsense__ = 0;

    cout << "[START]\n";

    int number_of_tokens = 0;
    // (*) loop until the 'termination' token arrives
    do {
        qlex.receive(&token_p);
        cout << Simple_map_token_id_to_name(token_p->id) << " ";

        switch( token_p->id ) {
        case QUEX_TKN_N1a: 
        case QUEX_TKN_N2a: 
        case QUEX_TKN_N3a: 
            cout << std::string((char*)token_p->get_name().c_str()) << endl; 
            break;
        case QUEX_TKN_N1b: 
        case QUEX_TKN_N2b: 
        case QUEX_TKN_N3b: 
            cout << (int)token_p->get_mini_x() << ", " << (int)token_p->get_mini_y() << endl;
            break;
        case QUEX_TKN_N1c: 
        case QUEX_TKN_N2c: 
        case QUEX_TKN_N3c: 
            cout << (int)token_p->get_big_x() << ", " << (int)token_p->get_big_y() << endl;
            break;
        case QUEX_TKN_WHO: 
            cout << (int)token_p->get_who_is_that() << endl; 
            break;
        }

        ++number_of_tokens;
        if( number_of_tokens > 100 ) {
            QUEX_ERROR_EXIT("Loop beyond border.\n");
        }

    } while( token_p->id != QUEX_TKN_TERMINATION );

    cout << "\n[END] number of token = " << number_of_tokens << "\n";

    return 0;
}
