#include "post-categorizer-common.h"
#include "test_cpp/lib/quex/MemoryManager.i"
#include "test_cpp/converter-from-lexeme.i"


void post_categorizer_setup(QUEX_NAME(Dictionary)* me, int Seed)
{
    (void)QUEX_NAME(PostCategorizer_construct)(me);
    /* The 'Seed' value tells where it starts. */
    for(int i=0; i<7; ++i) {
        if     ( (i + Seed) % 7 == 0 ) me->enter("Ab", 1);
        else if( (i + Seed) % 7 == 1 ) me->enter("Ad", 2);
        else if( (i + Seed) % 7 == 2 ) me->enter("Af", 3);
        else if( (i + Seed) % 7 == 3 ) me->enter("Ah", 4);
        else if( (i + Seed) % 7 == 4 ) me->enter("Bb", 5);
        else if( (i + Seed) % 7 == 5 ) me->enter("Bd", 6);
        else if( (i + Seed) % 7 == 6 ) me->enter("Bf", 7);
    }
}
