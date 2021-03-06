#include "post-categorizer-common.h"

void post_categorizer_setup(QUEX_NAME(Dictionary)* me, int Seed);
void test(QUEX_NAME(Dictionary)* pc, const char* Name);

int
main(int argc, char** argv)
{

    if( argc < 2 ) return -1;

    if( strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("Post Categorizer: Remove Existent Node;\n");
        printf("CHOICES: Ab, Ad, Af, Ah, Bb, Bd, Bf;\n");
        return 0;
    }
    QUEX_NAME(Dictionary)  pc;

    post_categorizer_setup(&pc, 4);
    
    pc.remove(argv[1]);

    QUEX_NAME(PostCategorizer_print_this)(&pc);
}
