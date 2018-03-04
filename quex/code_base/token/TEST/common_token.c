#include "common_token.h"
#include <quex/code_base/token/TokenQueue.i>
#include <quex/code_base/MemoryManager.i>

void
common_print_push(QUEX_NAME(TokenQueue)* me, int count, QUEX_TYPE_TOKEN* token_p)
{
    int         id   = token_p->id;
    const char* text = token_p->text ? token_p->text : "";

    printf("(%i)  %3i %s-->\n", count, id, text);
}

void
common_print_pop(QUEX_NAME(TokenQueue)* me, int count, QUEX_TYPE_TOKEN* token_p)
{
    int         id   = token_p ? token_p->id : -1;
    const char* text = (token_p && token_p->text) ? token_p->text : "";
    printf("(%i)      <-- %3i %s\n", count, id, text);
}

int
common_empty_queue(QUEX_NAME(TokenQueue)* me, int pop_n, int Size)
{
    bool             verdict_f;
    QUEX_TYPE_TOKEN* token_p;

    hwut_verify(QUEX_NAME(TokenQueue_is_full)(me));

    while( false == QUEX_NAME(TokenQueue_is_empty)(me) ) {
        token_p = QUEX_NAME(TokenQueue_pop)(me);
        hwut_verify(token_p != (QUEX_TYPE_TOKEN*)0);
        ++pop_n;
        common_print_pop(me, pop_n, token_p);
    }

    token_p = QUEX_NAME(TokenQueue_pop)(me);
    hwut_verify(token_p == (QUEX_TYPE_TOKEN*)0);
    ++pop_n;
    common_print_pop(me, pop_n, token_p);

    hwut_verify(QUEX_NAME(TokenQueue_is_empty)(me));

    return pop_n;
}

QUEX_INLINE void QUEX_NAME_TOKEN(construct)(QUEX_TYPE_TOKEN* me) 
{ 
    printf("construct: ((%p))\n", (void*)me);
    me->id   = 4711; 
    me->text = 0; 
}

QUEX_INLINE void QUEX_NAME_TOKEN(destruct)(QUEX_TYPE_TOKEN* me) 
{ 
    printf("destruct: ((%p))\n", (void*)me);
    if( me->text ) free(me->text);
}

QUEX_INLINE bool QUEX_NAME_TOKEN(take_text)(QUEX_TYPE_TOKEN* me, 
                                            const char*      BeginP,
                                            const char*      EndP) 
{ 
    printf("         take_text: ((%p)) '%s'\n", (void*)me, BeginP);
    me->text = (char*)malloc(sizeof(char) * (EndP - BeginP));
    memcpy(me->text, BeginP, sizeof(char) * (EndP - BeginP));
    return false;
}

QUEX_INLINE void
QUEX_NAME_TOKEN(repetition_n_set)(QUEX_TYPE_TOKEN* me, size_t RepetitionN)
{
    me->repetition_n = RepetitionN;
}

QUEX_INLINE size_t 
QUEX_NAME_TOKEN(repetition_n_get)(QUEX_TYPE_TOKEN* me)
{
    return me->repetition_n;
} 
