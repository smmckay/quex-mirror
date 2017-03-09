#include<cstdio> 

// (*) include lexical analyser header
#include "UTF16Lex"

using namespace std;

int 
main(int argc, char** argv) 
{        
    using namespace quex;

    if( argc == 1 ) {
       printf("Required at least one argument: 'LE' or 'BE'.\n");
       return -1;
    }

    Token*                   token;
    bool                     BigEndianF  = (strcmp(argv[1], "BE") == 0); 
    const char*              file_name   = BigEndianF ? "example-utf16be.txt" : "example-utf16le.txt";
    QUEX_NAME(ByteLoader)*   byte_loader = QUEX_NAME(ByteLoader_FILE_new_from_file_name)(file_name);
    UTF16Lex*                qlex;

    qlex = UTF16Lex::from_ByteLoader(byte_loader, NULL);
    /* System's endianness is 'little' => reversion if 'big'
     *                     is 'big'    => reversion if 'little' (not 'big'). */
    qlex->byte_order_reversion_set(QUEXED(system_is_little_endian)() ? 
                                   BigEndianF : ! BigEndianF);

    printf("## input file           = %s\n", file_name);
    printf("## byte order reversion = %s\n", E_Boolean_NAME(qlex->byte_order_reversion()));
    
    do {
        qlex->receive(&token);

        /* Print the lexeme in utf8 format. */
        printf("%s\n", (char*)(string(*token).c_str()));

        // (*) check against 'termination'
    } while( token->type_id() != TKN_TERMINATION );

    delete qlex;
    return 0;
}
