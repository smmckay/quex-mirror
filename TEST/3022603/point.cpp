#include <string.h>
#include<fstream>    
#include<iostream> 

#include "Simple/Simple"

int 
main(int argc, char** argv) 
{        
    using namespace std;
    const static size_t BUFFER_SIZE = 10000;
    uint8_t             BUFFER[BUFFER_SIZE];
    Simple_Token*   token_p;
    Simple*  qlex;
        
    // -- Call the low lever driver to fill the fill region
    const char* str  = "bye";
    size_t      receive_n = strlen(str);
    memcpy(&BUFFER[1], str, receive_n*sizeof(char));

    qlex = new Simple(&BUFFER[0], BUFFER_SIZE, &BUFFER[receive_n + 1]);
    
    // -- Loop until the 'termination' token_p arrives
    do {
        qlex->receive(&token_p);

        cout << token_p->get_string() << endl;

    } while( token_p->id != QUEX_TKN_TERMINATION );

    delete qlex;
    return 0;
}


 	  	 
