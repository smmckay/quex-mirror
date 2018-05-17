#include<cstdio> 
#include<cstdlib> 

// (*) include lexical analyser header
#include "Simple/Simple"

using namespace std;

int 
main(int argc, char** argv) 
{        
    Simple_Token*   token_p;
    Simple   qlex("example.txt", NULL);

    if( argc < 2 ) {
        printf("Command line argument required!\n");
        return 0;
    }
    if( strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("Normal Reset;\n");
        printf("CHOICES:  0, 1, 2, 3, 20, 30, 50, 134, 135, 136, 1000;\n");
        printf("SAME;\n");
        return 0;
    }
    int N = atoi(argv[1]);

    qlex.byte_order_reversion_set(true);
    qlex.push_mode(&Simple_EXTRA);

    /* Read 'N' tokens before doing the reset. */
    for(int i=0; i < N; ++i) {
        (void)qlex.receive(&token_p);
    } 

    // printf("BEFORE Reset:\n");
    // qlex.print_this();
    qlex.reset();

    printf("AFTER Reset:\n");
    qlex.print_this();


    return 0;
}
