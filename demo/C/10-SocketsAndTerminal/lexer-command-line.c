/* Lexical FSM fed from a Command Line
 * -----------------------------------------
 *
 * In this example, user interaction results in a command line which is then
 * lexically analyzed. This example requires the 'GNU readline' library to
 * be installed.
 *_____________________________________________________________________________
 *
 *  EXAMPLE:
 *  
 *    Ascii-codec command line:
 *
 *          > ./lexer-command-line
 *        
 *          type here: A message of a kilobyte
 *              read: 24 [byte]
 *              Token: ARTICLE 'A'
 *              Token: SUBJECT 'message'
 *              Token: PREPOSITION 'of'
 *              Token: ARTICLE 'a'
 *              Token: SUBJECT 'kilobyte'
 *              Token: <TERMINATION> ''
 *          type here: starts with a single bit
 *              read: 25 [byte]
 *              Token: SUBJECT 'starts'
 *              Token: PREPOSITION 'with'
 *              Token: ARTICLE 'a'
 *              Token: ATTRIBUTE 'single'
 *              Token: STORAGE_UNIT 'bit'
 *              Token: <TERMINATION> ''
 *          type here: ^C
 *        
 *    Similarly, the UTF8 command line parser may be used:
 *        
 *          > ./lexer-command-line-utf8
 *          
 *_____________________________________________________________________________
 *
 * (C) Frank-Rene Schaefer                                                   */

#include <stdio.h>
#if ! defined(WITH_UTF8)
#   include <lex_ascii/LexAscii.h>
#   define  LEXER_CLASS   quex_LexAscii
#else
#   include <lex_utf8/LexUtf8.h>
#   define  LEXER_CLASS   quex_LexUtf8
#   include <lex_utf8/lib/buffer/lexatoms/converter/iconv/Converter_IConv>
#   include <lex_utf8/lib/buffer/lexatoms/converter/iconv/Converter_IConv.i>
#endif

static void  print_token(quex_Token*  token);

int 
main(int argc, char** argv) 
{        
    quex_Token*              token = 0;
    LEXER_CLASS              qlex;   
    size_t                   size = 4096;
    char                     buffer[4096];
    char*                    p;
    ssize_t                  received_n;
    (void)argc; (void)argv;

#if defined(WITH_UTF8)
    QUEX_NAME(Converter)*    converter = QUEX_NAME(Converter_IConv_new)("UTF8", NULL);
#   else
#   define                   converter NULL
#endif
    QUEX_NAME(from_ByteLoader)(&qlex, NULL, converter);

    while( ! token || token->id != QUEX_TKN_BYE ) {
        printf("type here: ");
        p    = &buffer[0];
        size = 4096;
        if( (received_n = getline(&p, &size, stdin)) == -1 ) break;

        printf("    read: %i [byte]\n", (int)received_n);
        qlex.reset(&qlex);
        qlex.buffer.fill(&qlex.buffer, &p[0], &p[received_n]);

        do {
            qlex.receive(&qlex, &token);
            print_token(token);
        } while( token->id != QUEX_TKN_TERMINATION && token->id != QUEX_TKN_BYE );
    }
        
    QUEX_NAME(destruct)(&qlex);
    printf("<terminated>\n");
    return 0;
}

static void
print_token(quex_Token*  token)
{
    size_t PrintBufferSize = 1024;
    char   print_buffer[1024];

    printf("   Token: %s\n", QUEX_NAME_TOKEN(get_string)(token, print_buffer, 
                                                         PrintBufferSize));
}

