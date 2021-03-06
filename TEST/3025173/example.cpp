#include "br_scan/br_scan"
#include "iostream"

int 
main(int argc, char** argv) 
{        
    blackray::Token*  token_p = 0x0;
    br_scan     qlex("example.txt");

    do {
        qlex.receive(&token_p);
        std::cout << "token.id: " << token_p->id << "; token.number: ";
        std::cout << token_p->number_ << ";" << std::endl;
    } while( token_p->id != BR_TKN_TERMINATION);

    return 0;
}
