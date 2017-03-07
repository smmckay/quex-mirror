#include <stdio.h>

#ifdef QUEX_EXAMPLE_WITH_CONVERTER
#   include "lexConverter.h"
#   include <quex/code_base/buffer/lexatoms/converter/iconv/Converter_IConv>
#   include <quex/code_base/buffer/lexatoms/converter/iconv/Converter_IConv.i>
#else
#   include "lexPlain.h"
#endif

#include "quex/code_base/analyzer/adaptors/Gavager.i"
#include "quex/code_base/buffer/Buffer_print"

#include "receiver.h"

typedef QUEX_TYPE_ANALYZER CLexer;
typedef QUEX_TYPE_TOKEN    CToken;
typedef QUEX_TYPE_GAVAGER  CGavager;

static void show_buffer(CLexer* lexer, 
                        const uint8_t* RawBeginP, const uint8_t* RawEndP);

int 
main(int argc, char** argv) 
{        
    CToken*         token;
#   if   defined(QUEX_OPTION_CONVERTER_ICONV)
    QUEX_NAME(Converter)*    converter = QUEX_NAME(Converter_IConv_new)("UTF8", NULL);
#   elif defined(QUEX_OPTION_CONVERTER_ICU)
    QUEX_NAME(Converter)*    converter = QUEX_NAME(Converter_ICU_new)("UTF8", NULL);
#   else
#   define                   converter NULL
#   endif
    CLexer          lexer;
    CGavager        gavager;
    size_t          received_n;
    uint8_t*        begin_p;
    const uint8_t*  end_p;
    char            buffer[256];

    QUEX_NAME(from_ByteLoader)(&lexer, (QUEX_NAME(ByteLoader)*)0, converter);
    QUEX_NAME(Gavager_construct)(&gavager, &lexer, QUEX_TKN_BYE);

    token = (CToken*)0;
    while( ! token || token->_id != QUEX_TKN_BYE ) {

        if( ! token ) {
            gavager.access(&gavager, (void**)&begin_p, (const void**)&end_p); 
            
            received_n = receiver_receive_in_this_place(begin_p, end_p);

            gavager.gavage(&gavager, received_n);

            show_buffer(&lexer, &begin_p[0], &begin_p[received_n]);
        }

        token = gavager.deliver(&gavager);
        /* token == NULL, if the feeder only requires more content.
         * else,          if a valid token that has been returned.       */

        if( token ) {
            printf("   TOKEN: %s\n", QUEX_NAME_TOKEN(get_string)(token, &buffer[0], sizeof(buffer)));
        }
    }

    show_buffer(&lexer, &begin_p[0], &begin_p[received_n]);

    QUEX_NAME(destruct)(&lexer);
    /* Gavagers do not need destruction. */
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
