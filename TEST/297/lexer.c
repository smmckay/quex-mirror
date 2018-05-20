#include "TestAnalyzer.h"

int 
main(int argc, char** argv) 
{        
    TestAnalyzer  qlex;
    
    TestAnalyzer_from_file_name(&qlex, "example.txt", NULL);

    uint8_t  hello[] = "auxiliary/hallo.txt";
    TestAnalyzer_Token_take_text(qlex.token_p(&qlex), &hello[0], &hello[sizeof(hello)]);

    TestAnalyzer_destruct(&qlex);
    return 0;
}

