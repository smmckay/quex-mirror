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
static void show_buffer(CLexer* lexer);

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
    feeder = new QUEX_NAME(Feeder)(lexer);

    while( (received_n = receiver_get_pointer_to_received(&rx_content_p)) != 0 ) {

        feeder->feed(&rx_content_p[0], &rx_content_p[received_n]);

        show_buffer(lexer);

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

    show_buffer(lexer);

    delete feeder;
    delete lexer;
}

static void
show_buffer(CLexer* lexer)
{
#   ifdef QUEX_EXAMPLE_WITH_CONVERTER
    printf("     raw: ");
    QUEX_NAME(Buffer_print_content_core)(1, 
                                         lexer->filler->raw_buffer.begin_p,
                                         &lexer->filler->raw_buffer.memory_end_p[-1],
                                         (const uint8_t*)0, 
                                         lexer->filler->raw_buffer.end_p,
                                         /* BordersF */ false);
    printf("\n");
#   endif
    printf("        : ");
    QUEX_NAME(Buffer_print_content)(&lexer->buffer);
    printf("\n");
}
