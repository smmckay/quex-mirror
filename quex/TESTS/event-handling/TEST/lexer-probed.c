#include<string.h>
#include<stdio.h>

#include "EHLexer.h"
#include "quex/code_base/buffer/bytes/ByteLoader_Probe.i"
#include "quex/code_base/buffer/bytes/ByteLoader_Memory.i"

#define FLUSH() do { fflush(stdout); fflush(stderr); } while(0)

static size_t self_on_after_load_forward(struct       EHLexer_ByteLoader_Probe_tag*, 
                                         void*        buffer, 
                                         const size_t LoadedN, 
                                         bool*        end_of_stream_f);
static QUEX_TYPE_STREAM_POSITION 
              self_on_seek_backward(struct EHLexer_ByteLoader_Probe_tag* me, 
                                    QUEX_TYPE_STREAM_POSITION            Pos);
static size_t self_on_after_load_backward(struct EHLexer_ByteLoader_Probe_tag*, 
                                          void*        buffer, 
                                          const size_t LoadedN, 
                                          bool*        end_of_stream_f);
typedef struct {
    EHLexer* lexer;
    bool     seek_backward_f;
} extra_t;

int 
main(int argc, char** argv) 
{        
    const size_t        BufferSize = 1024;
    char                buffer[1024];
    EHLexer_Token*      token_p = 0x0;
    EHLexer_token_id_t  token_id = 0;
    char                file_name[256];
    quex_EHLexer        qlex;
    char*               memory = "abcx";
    const uint8_t*      BeginP = (uint8_t*)&memory[0];
    const uint8_t*      EndP   = (uint8_t*)&memory[strlen(memory)+1];
    extra_t             extra;

    EHLexer_ByteLoader_Memory* blm = (EHLexer_ByteLoader_Memory*)EHLexer_ByteLoader_Memory_new(BeginP, EndP);
    EHLexer_ByteLoader_Probe*  blp = (EHLexer_ByteLoader_Probe*)EHLexer_ByteLoader_Probe_new((EHLexer_ByteLoader*)blm, 
                                                                                             (void*)&extra);

    extra.lexer           = &qlex;
    extra.seek_backward_f = false;

    if( strcmp(argv[1], "forward") == 0 ) {
        blp->on_after_load = self_on_after_load_forward;
    }
    else {
        blp->on_seek       = self_on_seek_backward;
        blp->on_after_load = self_on_after_load_backward;
    }

    snprintf(file_name, (size_t)256, "./examples/%s.txt", (const char*)argv[1]);
    /* printf("%s\n", file_name); */
    EHLexer_from_file_name(&qlex, file_name, NULL); 
    EHLexer_from_ByteLoader(&qlex, &blp->base, NULL);
    FLUSH();

    fprintf(stderr, "| [START]\n");
    FLUSH();

    do {
        qlex->receive(&qlex, &token_p);
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

    blp->base.delete_self((EHLexer_ByteLoader*)blp);

    return 0;
}

size_t
self_on_after_load_forward(struct QUEX_NAME(ByteLoader_Probe_tag)* me, 
                           void*        buffer, 
                           const size_t LoadedN, 
                           bool*        end_of_stream_f)
{
    extra_t*  x = (extra_t*)(me->reference_object);
    /* CRITERIA for LOAD_FAILURE: -- 'end_p = end of memory'
     *                            -- return move_distance == 0                */
    x->lexer->buffer.input.end_p = x->lexer->buffer._memory._back;
    return 0; 
}

QUEX_TYPE_STREAM_POSITION
self_on_seek_backward(struct QUEX_NAME(ByteLoader_Probe_tag)* me,
                      QUEX_TYPE_STREAM_POSITION               Position)
{
    QUEX_TYPE_STREAM_POSITION current_position = me->source->tell((QUEX_NAME(ByteLoader)*)me);
    extra_t*                  x = (extra_t*)(me->reference_object);

    if( Position < current_position ) {
        x->seek_backward_f = true;
    }
    return Position;
}

size_t
self_on_after_load_backward(struct QUEX_NAME(ByteLoader_Probe_tag)* me, 
                            void*        buffer, 
                            const size_t LoadedN, 
                            bool*        end_of_stream_f)
{
    extra_t*  x = (extra_t*)(me->reference_object);
    return (x->seek_backward_f) ? 0 : LoadedN;
}
