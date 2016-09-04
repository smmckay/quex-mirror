#include <stdio.h>

#ifdef QUEX_EXAMPLE_WITH_CONVERTER
#   include "lexUTF8"
#else
#   include "lexPlain"
#endif

typedef QUEX_TYPE_ANALYZER CLexer;
typedef QUEX_TYPE_TOKEN    CToken;
#include "receiver.h"

/* Input chunks: at syntactic/arbitrary boarders.
 *                                                                           */
static bool  loop_syntactic_chunks(CLexer* lexer);
static bool  loop_arbitrary_chunks(CLexer* lexer);

/* Content by 'copying' or 'filling'.
 *                                                                           */
static void  content_copy(CLexer* lexer, MemoryChunk* chunk);
static void  content_fill(CLexer* lexer, MemoryChunk* chunk);


typedef struct {
/* Configuration: 
 *
 * The analysis process is configured by a set of function 
 * pointers to specify construction, destruction, the receive loop, and the
 * way how content is filled into the engine's buffer. If a codec name is
 * given, a converter is used for filling.                                   
 *                                                                           */
    bool        (*loop)(CLexer* lexer);
    void        (*provide_content)(CLexer* lexer, MemoryChunk* chunk);
    size_t      (*receiver_copy)(ELEMENT_TYPE* BufferBegin, 
                                 size_t        BufferSize);
    size_t      (*receiver_fill)(ELEMENT_TYPE** buffer);

    const char* codec_name;
} Configuration;

static bool  Configuration_from_command_line(Configuration* p, int argc, char** argv);

Configuration     cfg;

#define PRINT_FUNCTION() printf("called: %s;\n", __func__);

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

    static CToken   token;  
    CLexer*         qlex;
    MemoryChunk     chunk = { 0, 0 };

    if( ! Configuration_from_command_line(&cfg, argc, argv) ) {
        printf("Error, not enough command line arguments.\n");
        return -1;
    }

    QUEX_NAME_TOKEN(construct)(&token);
    qlex = new QUEX_TYPE_ANALYZER((QUEX_NAME(ByteLoader)*)0, cfg.codec_name);
    (void)QUEX_NAME(token_p_swap)(qlex, &token);

    while( 1 + 1 == 2 ) {
        cfg.provide_content(qlex, &chunk);

        if( ! cfg.loop(qlex) ) break;
    }

    delete qlex;
    QUEX_NAME_TOKEN(destruct)(&token);
}

static bool
Configuration_from_command_line(Configuration* p, int argc, char** argv)
/* Interpret command line to configure the analysis process. The process'
 * behavior is controlled by a set of function pointers which are set here.
 *
 * RETURNS: true, configuration ok.
 *          false, else.
 *                                                                           */
{
    if(argc < 3) {
        printf("[1] --> 'syntactic' or 'arbitrary'\n");
        printf("[2] --> 'fill' or 'copy'\n");
        return false;
    }

    if( strcmp(argv[1], "syntactic") == 0 ) {
        p->loop          = loop_syntactic_chunks;
        p->receiver_copy = receiver_copy_syntax_chunk;
        p->receiver_fill = receiver_fill_syntax_chunk;
    } else {
        p->loop          = loop_arbitrary_chunks;
        p->receiver_copy = receiver_copy;
        p->receiver_fill = receiver_fill;
    }
    p->provide_content = (strcmp(argv[2], "copy") == 0) ? content_copy : content_fill;

#   ifdef QUEX_EXAMPLE_WITH_CONVERTER
    p->codec_name      = "UTF8";
#   else
    p->codec_name      = (const char*)0;
#   endif

    return true;
}

static void
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
    PRINT_FUNCTION();

    /* NOTE: 'chunk' is initialized to '{ 0, 0 }'.
     *       => safe to assume that 'begin_p == end_p' upon first run.       */

    /* Receive content from some messaging framework.                        */
    if( chunk->begin_p == chunk->end_p ) {                                   
        /* If the receive buffer has been read, it can be released.          */
        /* Receive and set 'begin' and 'end' of incoming chunk.              */
        received_n     = cfg.receiver_fill(&rx_buffer);               
        chunk->begin_p = rx_buffer;                                      
        chunk->end_p   = chunk->begin_p + received_n;                    
    } else {                                                                 
        /* If begin_p != end_p => first digest remainder.                    */
    }

    /* Copy buffer content into the analyzer's buffer-as much as possible.
     * 'fill()' returns a pointer to the first not-eaten byte.               */
    chunk->begin_p = (uint8_t*)lexer->buffer.fill(&lexer->buffer, 
                                                  chunk->begin_p, chunk->end_p);
}

static void
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
    PRINT_FUNCTION();

    /* Initialize the filling of the fill region                             */
    lexer->buffer.fill_prepare(&lexer->buffer, 
                               (void**)&chunk->begin_p, (const void**)&chunk->end_p);

    /* Call the low level driver to fill the fill region                     */
    received_n = cfg.receiver_copy(chunk->begin_p, chunk->end_p - chunk->begin_p); 

    /* Current token becomes previous token of next run.                     */
    lexer->buffer.fill_finish(&lexer->buffer, &chunk->begin_p[received_n]);
}

static bool
loop_syntactic_chunks(CLexer* lexer)
/* Loop until the 'TERMINATION' token arrives. Here, considering input which 
 * is 'chunked' at syntax boarders, the 'prev_token' is not considered.
 *                                                                      
 * RETURNS: true, if analysis may continue; BYE has not been received.
 *          false, if analysis may NOT continue; BYE has been received.      */
{
    QUEX_TYPE_TOKEN_ID    token_id;
    PRINT_FUNCTION();

    while( 1 + 1 == 2 ) {
        token_id = QUEX_NAME(receive)(lexer);

        /* TERMINATION => possible reload 
         * BYE         => end of game                                        */
        if( token_id == QUEX_TKN_TERMINATION ) break;
        if( token_id == QUEX_TKN_BYE )         break; 

        printf("   Token: %s\n", lexer->token->get_string().c_str());
    }
    
    return token_id != QUEX_TKN_BYE; /* 'Bye' token ends the lexing session. */
}

static bool
loop_arbitrary_chunks(CLexer* lexer)
/* Loop over received tokens until 'TERMINATION' or 'BYE' occurs. The previous
 * token must be tracked to identify a 'BYE, TERMINATION' sequence. The 
 * start of the lexeme must be tracked, so that after re-filling the inter-
 * rupted match cycle may restart. 
 *
 * RETURNS: true, if analysis may continue; BYE has not been received.
 *          false, if analysis may NOT continue; BYE has been received.      */
{
    CToken*             orig_token   = lexer->token;
    CToken              prev_token;
    CToken*             prev_token_p = &prev_token;
    QUEX_TYPE_TOKEN_ID  token_id;
    QUEX_TYPE_LEXATOM*  last_incomplete_lexeme_p;

    QUEX_NAME_TOKEN(construct)(&prev_token);

    PRINT_FUNCTION();

    last_incomplete_lexeme_p = lexer->input_pointer_get();
    lexer->token->_id        = QUEX_TKN_TERMINATION;

    /* Loop until 'TERMINATION' or 'BYE' is received.                   
     *   TERMINATION => possible reload/refill
     *   BYE         => end of game                                          */
    while( 1 + 1 == 2 ) {
        /* Current token becomes previous token of next run.                 */
        prev_token_p = QUEX_NAME(token_p_swap)(lexer, prev_token_p);

        token_id     = lexer->receive();
        if( token_id == QUEX_TKN_BYE ) {
            return false;                                   /* Done!         */
        }
        else if( token_id == QUEX_TKN_TERMINATION ) {
            lexer->input_pointer_set(last_incomplete_lexeme_p);
            lexer->token_p_swap(orig_token);
            return true;                                    /* There's more! */
        }
        else if( prev_token_p->_id != QUEX_TKN_TERMINATION ) {
            /* Previous token not followed by 'BYE' or 'TERMINATION'.
             * => The matching was not interrupted by end of content.
             * => Lexeme is complete. Previous token can be considered.      */
            printf("   Token: %s\n", prev_token_p->get_string().c_str());
            last_incomplete_lexeme_p = lexer->lexeme_start_pointer_get();
        }
    }
}

