#include <stdio.h>

#ifdef QUEX_EXAMPLE_WITH_CONVERTER
#   include "lexUTF8"
#else
#   include "lexPlain"
#endif

typedef QUEX_TYPE_ANALYZER CLexer;
typedef QUEX_TYPE_TOKEN    CToken;
#include "receiver.h"

/* Content by 'copying' or 'filling'.
 *                                                                           */
static bool   content_copy(CLexer* lexer, MemoryChunk* chunk);
static bool   content_fill(CLexer* lexer, MemoryChunk* chunk);
static bool (*get_content)(CLexer* lexer, MemoryChunk* chunk);
static void   show_buffer(CLexer* lexer);

int 
main(int argc, char** argv) 
/* Running a lexical analysis process. It works with an examplary 'receiver
 * framework'. The precise analysis process is configured by the command line.
 *
 * [1] "syntactic" --> receive loop handles chunks which are expected not to 
 *                     cut in between matching lexemes.
 *     "arbitrary" --> chunks may be cut in between lexemes.
 *
 * [2] "fill"      --> content is provided by user filling as dedicated region.
 *     "copy"      --> user provides content to be copied into its 'place'.
 *                                                                           */
{        
    using namespace quex;

    CLexer*            lexer;
    MemoryChunk        chunk = { 0, 0 };
    QUEX_TYPE_TOKEN_ID token_id;

    if( strcmp(argv[1], "fill") == 0 ) get_content = content_fill;
    else                               get_content = content_copy;

    lexer = new QUEX_TYPE_ANALYZER((QUEX_NAME(ByteLoader)*)0, "UTF-8");

    while( get_content(lexer, &chunk) ) {
        show_buffer(lexer);

        token_id = lexer->receive();

        /* TERMINATION => possible reload 
         * BYE         => end of game                                        */
        if     ( token_id == QUEX_TKN_TERMINATION ) continue;
        else if( token_id == QUEX_TKN_BYE )         break; 

        printf("   Token: %s\n", lexer->token->get_string().c_str());
    }

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
        received_n     = receiver_get_pointer_to_received_syntax_chunk(&rx_buffer);               
        if( ! received_n ) return false;
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
    received_n = receiver_fill_syntax_chunk(chunk->begin_p, 
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
