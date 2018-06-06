#include<string.h>
#include<stdio.h>

#if defined(UNIT_TEST_IN_UT)
#   include "ut/EHLexer.h"
#else
#   include "EHLexer/EHLexer.h"
#endif
#ifdef      QUEX_OPTION_USER_DEFINED_MEMORY_MANAGER
#   include "../../../code_base/TESTS/MemoryManager_UnitTest.i"
MemoryManager_UnitTest_t MemoryManager_UnitTest;
#endif


#define FLUSH() do { fflush(stdout); fflush(stderr); } while(0)

int 
main(int argc, char** argv) 
{        
    const size_t        BufferSize = 1024;
    char                buffer[1024];
    EHLexer_Token*      token_p = 0x0;
    EHLexer_token_id_t  token_id = 0;
    char                file_name[256];
    EHLexer             qlex;

#   ifdef QUEX_OPTION_USER_DEFINED_MEMORY_MANAGER
    memset((void*)&MemoryManager_UnitTest, 0, sizeof(MemoryManager_UnitTest_t));
    MemoryManager_UnitTest.allocation_addmissible_f = 1;
#   endif

    snprintf(file_name, (size_t)256, "./examples/%s.txt", (const char*)argv[1]);
    /* printf("%s\n", file_name); */
    EHLexer_from_file_name(&qlex, file_name, NULL); 
    FLUSH();

    fprintf(stderr, "| [START]\n");
    FLUSH();

#   ifdef QUEX_OPTION_USER_DEFINED_MEMORY_MANAGER
    MemoryManager_UnitTest.allocation_addmissible_f = 0;
    MemoryManager_UnitTest.reallocate_limit_byte_n  = 0;
#   endif

    do {
        qlex.receive(&qlex, &token_p);
        token_id = token_p->id;
        FLUSH();
        printf("TOKEN: %s\n", EHLexer_Token_get_string(token_p, buffer, BufferSize));
        FLUSH();
    } while( token_id != TK_TERMINATION );

    fprintf(stderr, "| [END]\n");
    FLUSH();

    if( qlex.error_code != E_Error_None ) {
        qlex.print_this(&qlex);
    }

    EHLexer_destruct(&qlex);

    return 0;
}
