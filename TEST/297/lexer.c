#include "TestAnalyzer.h"

int 
main(int argc, char** argv) 
{        
    quex_TestAnalyzer  qlex;
    
    QUEX_NAME(from_file_name)(&qlex, "example.txt", NULL);

    uint8_t  hello[] = "auxiliary/hallo.txt";
    QUEX_NAME_TOKEN(take_text)(qlex.token, &qlex, &hello[0], &hello[sizeof(hello)]);

    QUEX_NAME(destruct)(&qlex);
    return 0;
}

