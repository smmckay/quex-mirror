#include "common_token.h"

static int  self_fill_and_empty(QUEX_NAME(TokenQueue)* me, size_t Size, int CPushN);
static int  self_test(int Size, int ContinuousPushN);

static E_UnitTest self_unit_test = E_UNIT_TEST_VOID;

int
main(int argc, char** argv)
{
    int  count_n = 0;

    hwut_info("TokenQueue: Push and Pop;\n"
              "CHOICES: plain, text;");

    hwut_if_choice("plain") self_unit_test = E_UNIT_TEST_PLAIN;
    hwut_if_choice("text")  self_unit_test = E_UNIT_TEST_TEXT;

    count_n += self_test(1, 1); 
    count_n += self_test(2, 2); 
    count_n += self_test(2, 3); 
    count_n += self_test(3, 2); 
    count_n += self_test(3, 3); 
    count_n += self_test(3, 4); 

    printf("<terminated %i>\n", count_n);
}

static int
self_test(int Size, int ContinuousPushN)
{
    QUEX_NAME(TokenQueue) me;
    QUEX_TYPE_ANALYZER    lexer;
    int                   count_n;

    printf("\n---( size: %i; )------------------\n", (int)Size);
    printf("\n");
    QUEX_NAME(TokenQueue_construct)(&me, &lexer, Size);
    hwut_verify(me.end - me.begin == (ptrdiff_t)Size);
    printf("\n");

    count_n = self_fill_and_empty(&me, Size, ContinuousPushN);

    printf("\n");
    hwut_verify(me.end - me.begin == (ptrdiff_t)Size);
    QUEX_NAME(TokenQueue_destruct)(&me);
    printf("\n");

    return count_n;
}

static int
self_fill_and_empty(QUEX_NAME(TokenQueue)* me, size_t Size, int CPushN) 
{
    int              push_n = 1, pop_n = 1, total_n = -1;
    QUEX_TYPE_TOKEN* token_p = (QUEX_TYPE_TOKEN*)0;
    bool             verdict_f;
    char*            example[] = { "adelbert", "berta", "caesar", "dagobert" };
    char*            string;

    hwut_verify(QUEX_NAME(TokenQueue_is_empty)(me));

    for(push_n=1, pop_n=0; push_n<=Size; ++push_n) {

        switch( self_unit_test ) {
        case E_UNIT_TEST_PLAIN:
            QUEX_NAME(TokenQueue_push)(me, 100 * push_n);
            break;
        case E_UNIT_TEST_TEXT:
            string = example[push_n-1];
            QUEX_NAME(TokenQueue_push_text)(me, 100 * push_n, string, &string[strlen(string)+1]);
            break;
        default:
            hwut_verify(false);
        }
        
        common_print_push(me, push_n, &me->write_iterator[-1]);

        if( (push_n+1) % CPushN == 0 ) {
            token_p  = QUEX_NAME(TokenQueue_pop)(me);
            ++pop_n;
            common_print_pop(me, pop_n, token_p);
        }
    }

    total_n = push_n + common_empty_queue(me, pop_n, Size);

    hwut_verify(QUEX_NAME(TokenQueue_is_empty)(me));

    return total_n;
}

