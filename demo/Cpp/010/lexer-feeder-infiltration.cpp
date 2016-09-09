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
    CToken*            token;
    QUEX_NAME(Feeder)* feeder;
    size_t             received_n;
    uint8_t*           rx_content_p;

    lexer  = new QUEX_TYPE_ANALYZER((QUEX_NAME(ByteLoader)*)0, CODEC_NAME);
    feeder = new QUEX_NAME(Feeder)(lexer, QUEX_TKN_BYE);

    token = (CToken*)0;
    while( ! token || token->_id != QUEX_TKN_BYE ) {

        if( ! token ) {
            received_n = feeder->infiltrate_access(&begin_p, &end_p); 
            
            receiver_get_pointer_to_received(&rx_content_p);

            feeder->feed(&rx_content_p[0], &rx_content_p[received_n]);

            show_buffer(lexer, &rx_content_p[0], &rx_content_p[received_n]);
        }

        token = feeder->deliver();
        /* token == NULL, if the feeder only requires more content.
         * else,          if a valid token that has been returned.       */

        if( token ) {
            printf("   TOKEN: %s\n", token->get_string().c_str());
        }
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
