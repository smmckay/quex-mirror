#include <stdio.h>

#ifdef QUEX_EXAMPLE_WITH_CONVERTER
#   include "converter/lexConverter.h"
#   include "converter/lib/buffer/lexatoms/converter/iconv/Converter_IConv"
#   include "converter/lib/buffer/lexatoms/converter/iconv/Converter_IConv.i"
#   include "converter/lib/analyzer/adaptors/Feeder.i"
#   include "converter/lib/buffer/Buffer_print"
#else
#   include "plain/lexPlain.h"
#   include "plain/lib/analyzer/adaptors/Feeder.i"
#   include "plain/lib/buffer/Buffer_print"
#endif

#include "receiver.h"

typedef QUEX_TYPE_ANALYZER CLexer;
typedef QUEX_TYPE_TOKEN    CToken;
typedef QUEX_TYPE_FEEDER   CFeeder;

static void show_buffer(CLexer* lexer, 
                        const uint8_t* RawBeginP, const uint8_t* RawEndP);

int 
main(int argc, char** argv) 
{        
    CToken*   token;
#   if   defined(QUEX_OPTION_CONVERTER_ICONV)
    CLexer_Converter*    converter = CLexer_Converter_IConv_new("UTF8", NULL);
#   elif defined(QUEX_OPTION_CONVERTER_ICU)
    CLexer_Converter*    converter = CLexer_Converter_ICU_new("TF8", NULL);
#   else
#   define               converter NULL
#   endif
    CLexer    lexer;
    CFeeder   feeder;
    size_t    received_n;
    uint8_t*  rx_content_p;
    char      buffer[256];
    (void)argc; (void)argv;

    CLexer_from_ByteLoader(&lexer, (CLexer_ByteLoader*)0, converter);
    QUEX_NAME(Feeder_construct)(&feeder, &lexer, QUEX_TKN_BYE);

    token = (CToken*)0;
    while( ! token || token->id != QUEX_TKN_BYE ) {

        if( ! token ) {
            received_n = receiver_get_pointer_to_received(&rx_content_p);

            feeder.feed(&feeder, &rx_content_p[0], &rx_content_p[received_n]);

            show_buffer(&lexer, &rx_content_p[0], &rx_content_p[received_n]);
        }

        token = feeder.deliver(&feeder);
        /* token == NULL, if the feeder only requires more content.
         * else,          if a valid token that has been returned.       */
        if( lexer.error_code != E_Error_None ) {
            lexer.print_this(&lexer);
            break;
        }

        if( token ) {
            printf("   TOKEN: %s\n", CLexer_get_string(token, &buffer[0], sizeof(buffer)));
        }
    }

    show_buffer(&lexer, &rx_content_p[0], &rx_content_p[received_n]);

    CLexer_destruct(&lexer);
    /* Feeders do not need destruction. */
}

static void
show_buffer(CLexer* lexer, const uint8_t* RawBeginP, const uint8_t* RawEndP)
{
#   ifdef QUEX_EXAMPLE_WITH_CONVERTER
    printf("     raw: ");
    CLexer_Buffer_print_content_core(1, RawBeginP, &RawEndP[-1], 
                                     (const uint8_t*)0, RawEndP,
                                     /* BordersF */ false);
    printf("\n");
#   endif
    (void)RawBeginP; (void)RawEndP;
    printf("        : ");
    CLexer_Buffer_print_content(&lexer->buffer);
    printf("\n");
}
