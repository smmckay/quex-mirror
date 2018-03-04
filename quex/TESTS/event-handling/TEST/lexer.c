#include<string.h>
#include<stdio.h>

#include "EHLexer.h"
#ifdef      UNIT_TEST_DEFINE_MEMORY_MANAGER_IMPLEMENTATION
#   include "quex/code_base/buffer/TESTS/MemoryManager_UnitTest.i"
MemoryManager_UnitTest_t MemoryManager_UnitTest;
#endif


#define FLUSH() do { fflush(stdout); fflush(stderr); } while(0)

int 
main(int argc, char** argv) 
{        
    const size_t        BufferSize = 1024;
    char                buffer[1024];
    QUEX_TYPE_TOKEN*    token_p = 0x0;
    QUEX_TYPE_TOKEN_ID  token_id = 0;
    char                file_name[256];
    quex_EHLexer        qlex;

#   ifdef UNIT_TEST_DEFINE_MEMORY_MANAGER_IMPLEMENTATION
    memset((void*)&MemoryManager_UnitTest, 0, sizeof(MemoryManager_UnitTest_t));
    MemoryManager_UnitTest.allocation_addmissible_f = 1;
#   endif

    snprintf(file_name, (size_t)256, "./examples/%s.txt", (const char*)argv[1]);
    /* printf("%s\n", file_name); */
    QUEX_NAME(from_file_name)(&qlex, file_name, NULL); 
    FLUSH();

    fprintf(stderr, "| [START]\n");
    FLUSH();

#   ifdef UNIT_TEST_DEFINE_MEMORY_MANAGER_IMPLEMENTATION
    MemoryManager_UnitTest.allocation_addmissible_f = 0;
    MemoryManager_UnitTest.reallocate_limit_byte_n  = 0;
#   endif

    do {
        qlex.receive(&qlex, &token_p);
        token_id = token_p->id;
        FLUSH();
        printf("TOKEN: %s\n", QUEX_NAME_TOKEN(get_string)(token_p, buffer, BufferSize));
        FLUSH();
    } while( token_id != TK_TERMINATION );

    fprintf(stderr, "| [END]\n");
    FLUSH();

    if( qlex.error_code != E_Error_None ) {
        QUEX_NAME(print_this)(&qlex);
    }

    QUEX_NAME(destruct)(&qlex);

    return 0;
}
