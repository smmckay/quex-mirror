#include<string.h>
#include<stdio.h>

#include "EHLexer.h"
#include "quex/code_base/buffer/bytes/ByteLoader_Probe"
#include "quex/code_base/buffer/bytes/ByteLoader_Memory"

#define FLUSH() do { fflush(stdout); fflush(stderr); } while(0)

static size_t self_on_after_load_forward(struct QUEX_NAME(ByteLoader_Probe_tag)*, 
                                         void*        buffer, 
                                         const size_t LoadedN, 
                                         bool*        end_of_stream_f);
static QUEX_TYPE_STREAM_POSITION 
              self_on_seek_backward(struct QUEX_NAME(ByteLoader_Probe_tag)* me, 
                                    QUEX_TYPE_STREAM_POSITION               Pos);
static size_t self_on_after_load_backward(struct QUEX_NAME(ByteLoader_Probe_tag)*, 
                                          void*        buffer, 
                                          const size_t LoadedN, 
                                          bool*        end_of_stream_f);

int 
main(int argc, char** argv) 
{        
    const size_t        BufferSize = 1024;
    char                buffer[1024];
    QUEX_TYPE_TOKEN*    token_p = 0x0;
    QUEX_TYPE_TOKEN_ID  token_id = 0;
    char                file_name[256];
    quex_EHLexer        qlex;
    char*               memory = "abcde";
    const uint8_t*      BeginP = (uint8_t*)&memory[0];
    const uint8_t*      EndP   = (uint8_t*)&memory[strlen(memory)+1];

    QUEX_NAME(ByteLoader_Memory)* blm = QUEX_NAME(ByteLoader_Memory_new)(BeginP, EndP);
    QUEX_NAME(ByteLoader_Probe)*  blp = QUEX_NAME(ByteLoader_Probe_new)((QUEX_NAME(ByteLoader)*)blm);

    if( strcmp(argv[0], "forward") == 0 ) {
        blp->on_after_load = self_on_after_load_forward;
    }
    else {
        blp->on_seek       = self_on_seek_backward;
        blp->on_after_load = self_on_after_load_backward;
    }

    snprintf(file_name, (size_t)256, "./examples/%s.txt", (const char*)argv[1]);
    /* printf("%s\n", file_name); */
    QUEX_NAME(from_file_name)(&qlex, file_name, NULL); 
    FLUSH();

    fprintf(stderr, "| [START]\n");
    FLUSH();

    do {
        QUEX_NAME(receive)(&qlex, &token_p);
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

    blp->base.delete_self((QUEX_NAME(ByteLoader)*)blp);

    return 0;
}

size_t
self_on_after_load_forward(struct QUEX_NAME(ByteLoader_Probe_tag)* me, 
                           void*        buffer, 
                           const size_t LoadedN, 
                           bool*        end_of_stream_f)
{
    return 0; 
}

QUEX_TYPE_STREAM_POSITION
self_on_seek_backward(struct QUEX_NAME(ByteLoader_Probe_tag)* me,
                      QUEX_TYPE_STREAM_POSITION               Position)
{
    QUEX_TYPE_STREAM_POSITION current_position = me->source->tell((QUEX_NAME(ByteLoader)*)me);
    bool*                     seek_backward_f = (bool*)(me->reference_object);
    if( Position < current_position ) {
        *seek_backward_f = true;
    }
    return Position;
}

size_t
self_on_after_load_backward(struct QUEX_NAME(ByteLoader_Probe_tag)* me, 
                            void*        buffer, 
                            const size_t LoadedN, 
                            bool*        end_of_stream_f)
{
    bool*                     seek_backward_f = (bool*)(me->reference_object);
    return (*seek_backward_f) ? 0 : LoadedN;
}
