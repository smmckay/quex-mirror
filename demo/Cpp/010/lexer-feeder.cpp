#include <stdio.h>

#ifdef QUEX_EXAMPLE_WITH_CONVERTER
#   include "lexConverter"
#else
#   include "lexPlain"
#endif
#include "quex/code_base/analyzer/Feeder.i"

#include "receiver.h"

typedef QUEX_TYPE_ANALYZER CLexer;
typedef QUEX_TYPE_TOKEN    CToken;

/* Content by 'copying' or 'filling'.
 *                                                                           */
static bool   content_copy(CLexer* lexer, MemoryChunk* chunk);
static bool   content_fill(CLexer* lexer, MemoryChunk* chunk);
static bool (*get_content)(CLexer* lexer, MemoryChunk* chunk);
static void   show_buffer(CLexer* lexer);

int 
main(int argc, char** argv) 
{        
    using namespace quex;
    CLexer*            lexer;
    CToken*            token;
    QUEX_NAME(Feeder)* feeder;
    MemoryChunk        chunk = { 0, 0 };

    if( strcmp(argv[1], "fill") == 0 ) get_content = content_fill;
    else                               get_content = content_copy;

    lexer    = new QUEX_TYPE_ANALYZER((QUEX_NAME(ByteLoader)*)0, /* CodecName */NULL);
    feeder  = new QUEX_NAME(Feeder)(lexer);

    while ( get_content(lexer, &chunk) ) {
        show_buffer(lexer);

        while( (token = feeder->deliver()) != 0 ) {
            /* token == NULL, if the feeder only requires more content.
             * else,          if a valid token that has been returned.       */

            if( token ) {
                printf("   Token: %s\n", token->get_string().c_str());
                if( token->_id == QUEX_TKN_BYE ) break;
            }
        }
    }

    delete feeder;
    delete lexer;
}

static bool
content_copy(CLexer* lexer, MemoryChunk* chunk)
/* Fill the analyzer's buffer by copying data into it, that is the function
 *
 *                            '.fill(...)' 
 *
 * of the buffer is called directly. Data is received from an examplary 
 * 'receiver framework' which fills data into an 'rx_buffer'.     
 *
 * This process involves some extra copying of data compared to to 'filling'.*/
{
    uint8_t*   rx_buffer = 0x0;             /* A pointer to the receive buffer 
    *                                        * of the messaging framework.   */
    size_t     received_n = (size_t)-1;

    /* NOTE: 'chunk' is initialized to '{ 0, 0 }'.
     *       => safe to assume that 'begin_p == end_p' upon first run.       */

    /* Receive content from some messaging framework.                        */
    if( chunk->begin_p == chunk->end_p ) {                                   
        /* If the receive buffer has been read, it can be released.          */
        /* Receive and set 'begin' and 'end' of incoming chunk.              */
        received_n = receiver_get_pointer_to_received(&rx_buffer);
        if( ! received_n ) {
            return false;
        }
        chunk->begin_p = rx_buffer;                                      
        chunk->end_p   = chunk->begin_p + received_n;                    
    } else {                                                                 
        /* If begin_p != end_p => first digest remainder.                    */
    }

    /* Copy buffer content into the analyzer's buffer-as much as possible.
     * 'fill()' returns a pointer to the first not-eaten byte.               */
    chunk->begin_p = (uint8_t*)lexer->buffer.fill(&lexer->buffer, 
                                                  chunk->begin_p, chunk->end_p);
    return true;
}

static bool
content_fill(CLexer* lexer, MemoryChunk* chunk)
/* Filling the analyzer's buffer by 'filling'. That is the buffer provides the
 * user with two pointers that boarder the region where content needs to be 
 * filled. Then an examplary messaging framework fills the content directly
 * into it. Then, the buffer needs to 'finish' the filled data. This process
 * evolves around the two functions.
 *
 *   .fill_prepare(...) ---> providing 'begin_p' and 'end_p' where to fill.
 *   .fill_finish(...) ---> post processing the content.
 *
 * Filling involves less copying of data than 'copying'.                     */
{
    size_t received_n = (size_t)-1;

    /* Initialize the filling of the fill region                             */
    lexer->buffer.fill_prepare(&lexer->buffer, 
                               (void**)&chunk->begin_p, 
                               (const void**)&chunk->end_p);

    /* Call the low level driver to fill the fill region                     */
    received_n = receiver_fill(chunk->begin_p, 
                               chunk->end_p - chunk->begin_p); 
    if( ! received_n ) {
        return false;
    }

    /* Current token becomes previous token of next run.                     */
    lexer->buffer.fill_finish(&lexer->buffer, 
                              &chunk->begin_p[received_n]);
    return true;
}

static void
show_buffer(CLexer* lexer)
{
    printf("          ");
    QUEX_NAME(Buffer_print_content)(&lexer->buffer);
    printf("\n");
}
