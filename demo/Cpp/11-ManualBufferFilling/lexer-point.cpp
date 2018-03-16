/* Pointing -- Running a lexical analyzer directly on a chunk of memory.
 *
 * This is the very fastest, but least flexible method of feeding a lexical
 * analyzer. The lexical analyzer receives begin and end pointer of content
 * on which it has to work. Since lexical analyzer buffers are framed with
 * limit codes, the buffer content also, must contain a buffer limit code at
 * the beginning and the end. 
 *
 * The default buffer limit code is '0' which fits the C-language strings.
 * Nevertheless, in this example a zero is inserted at the beginning of the
 * strings to fit the lower border requirement. 
 *                                                                           */
#include<stdio.h>    
#include<string.h> 

#include "plain/lexPlain"

/* Terminating zero is implicitly added by the C-Language.                   */
static uint8_t Memory0[] = 
"\0A little nonsense now and then is cherished by the wisest men";
static uint8_t Memory1[] = 
"\0One advantage of talking to yourself is that you know at least somebody is listening";

#define Memory0Size (sizeof(Memory0)/sizeof(Memory0[0]))
#define Memory1Size (sizeof(Memory1)/sizeof(Memory1[1]))
       
static void  test(QUEX_TYPE_ANALYZER* lexer, uint8_t* memory, size_t Size);


int 
main(int argc, char** argv) 
{        
    QUEX_TYPE_ANALYZER  lexer((QUEX_TYPE_LEXATOM*)&Memory0[0], 
                              Memory0Size,
                              (QUEX_TYPE_LEXATOM*)&Memory0[Memory0Size-1]); 
    (void)argc; (void)argv;

    test(&lexer, NULL, 0);                  /* memory given during construct.  */
    test(&lexer, &Memory1[0], Memory1Size); /* memory given upon reset.        */

    return 0;
}

static void  
test(QUEX_TYPE_ANALYZER* lexer, uint8_t* memory, size_t Size)
{
    QUEX_TYPE_TOKEN*  token_p = NULL;
    if( memory ) {
        /* Fill at 'memory + 1'; 'memory + 0' holds buffer limit code.       */
        lexer->reset((QUEX_TYPE_LEXATOM*)&memory[0], Size, 
                     (QUEX_TYPE_LEXATOM*)&memory[Size-1]);
    }

    /* Loop until the 'termination' token arrives                            */
    do {
        lexer->receive(&token_p);

        printf("   Token: %s\n", token_p->get_string().c_str());
        
    } while( token_p->id != QUEX_TKN_TERMINATION );

    printf("<terminated>\n");
}

