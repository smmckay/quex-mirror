#include <stdio.h>

#ifdef QUEX_EXAMPLE_WITH_CONVERTER
#   include "lexConverter.h"
#   include <quex/code_base/buffer/lexatoms/converter/iconv/Converter_IConv>
#   include <quex/code_base/buffer/lexatoms/converter/iconv/Converter_IConv.i>
#else
#   include "lexPlain.h"
#endif
#include "quex/code_base/analyzer/adaptors/Feeder.i"
#include "quex/code_base/buffer/Buffer_print"

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
    QUEX_NAME(Converter)*    converter = QUEX_NAME(Converter_IConv_new)("UTF8", NULL);
#   elif defined(QUEX_OPTION_CONVERTER_ICU)
    QUEX_NAME(Converter)*    converter = QUEX_NAME(Converter_ICU_new)("UTF8", NULL);
#   else
#   define                   converter NULL
#   endif
    CLexer    lexer;
    CFeeder   feeder;
    size_t    received_n;
    uint8_t*  rx_content_p;
    char      buffer[256];

    QUEX_NAME(from_ByteLoader)(&lexer, (QUEX_NAME(ByteLoader)*)0, converter);
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
            QUEX_NAME(print_this)(&lexer);
            break;
        }

        if( token ) {
            printf("   TOKEN: %s\n", QUEX_NAME_TOKEN(get_string)(token, &buffer[0], sizeof(buffer)));
        }
    }

    show_buffer(&lexer, &rx_content_p[0], &rx_content_p[received_n]);

    QUEX_NAME(destruct)(&lexer);
    /* Feeders do not need destruction. */
}

static void
show_buffer(CLexer* lexer, const uint8_t* RawBeginP, const uint8_t* RawEndP)
{
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
