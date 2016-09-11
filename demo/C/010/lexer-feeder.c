#include <stdio.h>

#ifdef QUEX_EXAMPLE_WITH_CONVERTER
#   define  CODEC_NAME "UTF-8"
#   include "lexConverter.h"
#else
#   define  CODEC_NAME ((const char*)0)
#   include "lexPlain.h"
#endif
#include "quex/code_base/analyzer/adaptors/Feeder.i"

#include "receiver.h"

typedef QUEX_TYPE_ANALYZER CLexer;
typedef QUEX_TYPE_TOKEN    CToken;

/* Content by 'copying' or 'filling'.
 *                                                                           */
static void show_buffer(CLexer* lexer, 
                        const uint8_t* RawBeginP, const uint8_t* RawEndP);

int 
main(int argc, char** argv) 
{        
    using namespace quex;
    CLexer             lexer;
    CToken*            token;
    QUEX_NAME(Feeder)  feeder;
    size_t             received_n;
    uint8_t*           rx_content_p;

    QUEX_NAME(construct_from_memory)(&lexer, (QUEX_NAME(ByteLoader)*)0, CODEC_NAME);
    QUEX_NAME(Feeder_construct)(&feeder, lexer, QUEX_TKN_BYE);

    token = (CToken*)0;
    while( ! token || token->_id != QUEX_TKN_BYE ) {

        if( ! token ) {
            received_n = receiver_get_pointer_to_received(&rx_content_p);

            feeder->feed(feeder, &rx_content_p[0], &rx_content_p[received_n]);

            show_buffer(lexer, &rx_content_p[0], &rx_content_p[received_n]);
        }

        token = feeder->deliver(feeder);
        /* token == NULL, if the feeder only requires more content.
         * else,          if a valid token that has been returned.       */

        if( token ) {
            printf("   TOKEN: %s\n", token->get_string().c_str());
        }
    }

    show_buffer(lexer, &rx_content_p[0], &rx_content_p[received_n]);

    QUEX_NAME(destruct)(&lexer);
    feeder->destruct(feeder);
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
