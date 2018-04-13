#include "common.h"
#include <hwut_unit.h>

void 
common_token_queue_dummy_setup(quex_TestAnalyzer* me)
{
    TestAnalyzer_token_id_t token_id;
    int                     token_n = 0;
    for(token_id = 3; token_n < 5 ; ++token_n) {
        QUEX_NAME(TokenQueue_push)(&me->_token_queue, token_id);
        token_id = (token_id * 571) % 513 + 1;
    }
}

void 
common_token_queue_verify(const quex_TestAnalyzer* me)
{
    TestAnalyzer_token_id_t token_id;
    QUEX_TYPE_TOKEN*        token_p = me->_token_queue.read_iterator;
    int                     token_n = 0;
    for(token_id = 3; token_p != me->_token_queue.write_iterator; ++token_p, ++token_n) {
        hwut_verify(token_p);
        hwut_verify(token_p->id == token_id);
        token_id = (token_id * 571) % 513 + 1;
    }
    hwut_verify(token_n == 5);
}
