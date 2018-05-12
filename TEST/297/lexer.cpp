#include "TestAnalyzer"

int 
main(int argc, char** argv) 
{        
    TestAnalyzer  qlex("example.txt", NULL);

    uint8_t  hello[] = "auxiliary/hallo.txt";
    QUEX_NAME_TOKEN(take_text)(qlex.token_p(), &hello[0], &hello[sizeof(hello)]);

    return 0;
}

