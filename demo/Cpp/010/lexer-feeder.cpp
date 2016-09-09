#include <stdio.h>

#ifdef QUEX_EXAMPLE_WITH_CONVERTER
#   define  CODEC_NAME "UTF-8"
#   include "lexConverter"
#else
#   define  CODEC_NAME ((const char*)0)
#   include "lexPlain"
#endif
#include "quex/code_base/analyzer/Feeder.i"

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
    CLexer*            lexer;
    CToken*            token = (CToken*)0;
    QUEX_NAME(Feeder)* feeder;
    size_t             received_n;
    uint8_t*           rx_content_p;

    lexer  = new QUEX_TYPE_ANALYZER((QUEX_NAME(ByteLoader)*)0, CODEC_NAME);
    feeder = new QUEX_NAME(Feeder)(lexer, QUEX_TKN_BYE);

    while( ! token || token->_id != QUEX_TKN_BYE ) {

        received_n = receiver_get_pointer_to_received(&rx_content_p);

        feeder->feed(&rx_content_p[0], &rx_content_p[received_n]);

        show_buffer(lexer, &rx_content_p[0], &rx_content_p[received_n]);

        while( (token = feeder->deliver()) != 0 ) {
            /* token == NULL, if the feeder only requires more content.
             * else,          if a valid token that has been returned.       */

            if( token ) {
                printf("   TOKEN: %s\n", token->get_string().c_str());
                if( token->_id == QUEX_TKN_BYE ) break;
            }
        }

        /* 'token == 0', means 'request to refill'. That is, all content of 
         * 'rx_content_p' has been consumed or copied into internal buffer.   
         * => 'rx_content_p' can be freed.                                   */
    }

    show_buffer(lexer, &rx_content_p[0], &rx_content_p[received_n]);

    delete feeder;
    delete lexer;
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
