#include <stdio.h>

#ifdef QUEX_EXAMPLE_WITH_CONVERTER
#   define  CODEC_NAME "UTF-8"
#   include "lexConverter"
#else
#   define  CODEC_NAME ((const char*)0)
#   include "lexPlain"
#endif
#include "quex/code_base/analyzer/adaptors/Gavager.i"

#include "receiver.h"

using namespace quex;
typedef QUEX_TYPE_ANALYZER CLexer;
typedef QUEX_TYPE_TOKEN    CToken;
typedef QUEX_TYPE_GAVAGER  CGavager;

static void show_buffer(CLexer* lexer, 
                        const uint8_t* RawBeginP, const uint8_t* RawEndP);

int 
main(int argc, char** argv) 
{        
    CToken*         token;
    CLexer          lexer((QUEX_NAME(ByteLoader)*)0, CODEC_NAME);
    CGavager        gavager(&lexer, QUEX_TKN_BYE);
    size_t          received_n;
    uint8_t*        begin_p;
    const uint8_t*  end_p;

    token = (CToken*)0;
    while( ! token || token->_id != QUEX_TKN_BYE ) {

        if( ! token ) {
            gavager.access((void**)&begin_p, (const void**)&end_p); 
            
            received_n = receiver_receive_in_this_place(begin_p, end_p);

            gavager.gavage(received_n);

            show_buffer(&lexer, &begin_p[0], &begin_p[received_n]);
        }

        token = gavager.deliver();
        /* token == NULL, if the feeder only requires more content.
         * else,          if a valid token that has been returned.       */

        if( token ) {
            printf("   TOKEN: %s\n", token->get_string().c_str());
        }
    }

    show_buffer(&lexer, &begin_p[0], &begin_p[received_n]);
}

static void
show_buffer(CLexer* lexer, const uint8_t* RawBeginP, const uint8_t* RawEndP)
{
    using namespace quex;
#   ifdef QUEX_EXAMPLE_WITH_CONVERTER
    printf("     raw: ");
    QUEX_NAME(Buffer_print_content_core)(1, RawBeginP, &RawEndP[-1], 
                                         (const uint8_t*)0, RawEndP,
                                         /* BordersF */ false);
    printf("\n");
#   endif
    (void)RawBeginP; (void)RawEndP;
    printf("        : ");
    QUEX_NAME(Buffer_print_content)(&lexer->buffer);
    printf("\n");
}
