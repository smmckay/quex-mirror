#include <stdio.h> 

// (*) include lexical analyser header
#include "UTF16Lex.h"

int 
main(int argc, char** argv) 
{        
    quex_Token*              token_p     = 0x0;
    bool                     BigEndianF  = (argc < 2 || (strcmp(argv[1], "BE") == 0)); 
    const char*              file_name   = BigEndianF ? "example-utf16be.txt" : "example-utf16le.txt";
    QUEX_NAME(ByteLoader)*   byte_loader = QUEX_NAME(ByteLoader_FILE_new_from_file_name)(file_name);
    quex_UTF16Lex            qlex;
    size_t                   BufferSize = 1024;
    char                     buffer[1024];
    bool                     byte_order_reversion_f;

    if( argc == 1 ) {
        printf("Required at least one argument: 'LE' or 'BE'.\n");
        return -1;
    }
   
    QUEX_NAME(from_ByteLoader)(&qlex, byte_loader, NULL);

    /* System's endianness is 'little' => reversion if 'big'
     *                     is 'big'    => reversion if 'little' (not 'big'). */
    byte_order_reversion_f = QUEXED(system_is_little_endian)() ?  BigEndianF : ! BigEndianF;
    QUEX_NAME(byte_order_reversion_set)(&qlex, byte_order_reversion_f);

    printf("## input file           = %s\n", file_name);
    printf("## byte order reversion = %s\n", QUEX_NAME(byte_order_reversion)(&qlex) ? "true" : "false");
    
    do {
        QUEX_NAME(receive)(&qlex, &token_p);

        /* Print the lexeme in utf8 format. */
        printf("%s \n", QUEX_NAME_TOKEN(get_string)(token_p, buffer, BufferSize));

        // (*) check against 'termination'
    } while( token_p->_id != TKN_TERMINATION );

    QUEX_NAME(destruct)(&qlex);
    return 0;
}
