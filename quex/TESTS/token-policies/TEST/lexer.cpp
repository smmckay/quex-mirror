#include<cstdio> 
#include<cstring>

#include "TPLex"
#if ! defined(__QUEX_OPTION_PLAIN_C)
using namespace std;
using namespace quex;
#endif

__QUEX_TYPE_ANALYZER_RETURN_VALUE  pseudo_analysis(QUEX_TYPE_ANALYZER* me);
QUEX_TYPE_TOKEN_ID  test_core(TPLex&, const char*);

#define UMM_NAME ""
#if defined(UNIT_TEST_PSEUDO_ANALYSIS)
#   define NAME "Pseudo Analysis;\n"
#else
#   define NAME "Real Analysis;\n"
#endif
#define POLICY_NAME "queue"

int 
main(int argc, char** argv) 
{
    if( argc > 1 && strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("Token Policy '" POLICY_NAME "': " UMM_NAME NAME ";\n");
        printf("HAPPY: :[0-9]+;\n");
        return 0;
    }
    printf("NOTE: The production of an assertion error might be part of the test.\n");
    printf("---------------------------------------------------------------------\n");
    stderr = stdout;

    /* Allocating on 'heap' allows for easier memory violation detection via 'efence' */
    TPLex*     qlex = new TPLex("real.txt");  /* In case of pseudo_analysis the file  *
                                               * does not matter.                     */
#   if defined(UNIT_TEST_PSEUDO_ANALYSIS)
    printf("Pseudo Analysis: Replace analysis pointer with own function.\n");
    printf("Queue Size: %i\n", QUEX_SETTING_TOKEN_QUEUE_SIZE);
    qlex->current_analyzer_function = pseudo_analysis;
#   endif

    while( test_core(*qlex, argv[1]) != QUEX_TKN_TERMINATION );

    delete qlex;
}

QUEX_TYPE_TOKEN_ID test_core(TPLex& qlex, const char* Choice)
{
    QUEX_TYPE_TOKEN*  token_p;

    qlex.receive(&token_p);

    printf("received: %s\n", token_p->type_id_name().c_str());
    QUEX_TYPE_TOKEN_ID token_id = token_p->type_id();

    return token_id;
}

#if defined(UNIT_TEST_PSEUDO_ANALYSIS)
__QUEX_TYPE_ANALYZER_RETURN_VALUE  pseudo_analysis(QUEX_TYPE_ANALYZER* me)
{
    TPLex&     self = *((TPLex*)me);
    static int i = 0;

    switch( i++ ) {
    default: self_send(QUEX_TKN_TERMINATION); break;
    case 0:  self_send(QUEX_TKN_ONE);         break;
    case 1:  self_send(QUEX_TKN_TWO);         break;
    case 2:  self_send(QUEX_TKN_THREE);       break;
    case 3:  self_send(QUEX_TKN_FOUR);        break;
    case 4:  self_send(QUEX_TKN_FIVE);        break;
    case 5:  self_send(QUEX_TKN______NEXT_____); break;
    case 6:  self_send(QUEX_TKN______NEXT_____); break;
    case 7:  self_send(QUEX_TKN______NEXT_____); break;
    case 8:  
             self_send(QUEX_TKN_ONE);
             self_send(QUEX_TKN______NEXT_____);
             break;
    case 9:
             self_send(QUEX_TKN_ONE);
             self_send(QUEX_TKN_TWO);
             self_send(QUEX_TKN______NEXT_____);
             break;
    case 10:
             self_send(QUEX_TKN_ONE);
             self_send(QUEX_TKN_TWO);
             self_send(QUEX_TKN_THREE);
             self_send(QUEX_TKN______NEXT_____);
             break;
    case 11:
             self_send(QUEX_TKN_ONE);
             self_send(QUEX_TKN_TWO);
             self_send(QUEX_TKN_THREE); 
             self_send(QUEX_TKN_FOUR);   
             self_send(QUEX_TKN______NEXT_____);
             break;
    case 12:
             self_send(QUEX_TKN_ONE);
             self_send(QUEX_TKN_TWO);
             self_send(QUEX_TKN_THREE); 
             self_send(QUEX_TKN_FOUR); 
             self_send(QUEX_TKN_FIVE); 
             self_send(QUEX_TKN______NEXT_____);
             break;
    }
}
#endif

