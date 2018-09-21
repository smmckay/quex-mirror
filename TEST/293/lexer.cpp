/* ARGS: $1: 'bad'  => construct a lexer based on a 'wchar_t' stream that 
 *                     feeds a converter which expects UTF8.
 *                  => expected break up upon construction time.
 *           'good' => constructs a lexical analyzer that runs directly on
 *                     UTF8. There the 'wchar_t' stream works fine, even if
 *                     it carries only byte values.
 *
 * (C) Frank-Rene Schaefer                                                    */
#include <cstdio> 
#include "IConv/Lexer"
/* Include after 'IConv_Lexer' to ensure they 'land' in  correct namespace.   */
#include <IConv/lib/buffer/lexatoms/converter/iconv/Converter_IConv>
#include <IConv/lib/buffer/lexatoms/converter/iconv/Converter_IConv.i>

#include "Codec/Lexer"

using namespace std;

int main(int argc, char** argv) 
{        
    wstring        str(L"max und moritz");
    wstringstream* istr = new std::wstringstream(str);

    if( argc > 1 && strcmp(argv[1], "bad") == 0 ) {
        IConv::Lexer_ByteLoader*  byte_loader = IConv::Lexer_ByteLoader_wstream_new(istr);
        IConv::Lexer_Converter*   converter   = IConv::Lexer_Converter_IConv_new("UTF8", NULL);
        IConv::Lexer lex(byte_loader, converter); // Should break HERE!
    }
    else /* 'good' */ {
        Codec::Lexer_ByteLoader*  byte_loader = Codec::Lexer_ByteLoader_wstream_new(istr);
        Codec::Lexer              lex(byte_loader, NULL); 
        Codec::Lexer_Token*       token;

        do {
            (void)lex.receive(&token);

            cout << "Token: ";
            cout << token->get_string();
            cout << "\n";

        } while( token->id != CODEC_TKN_TERMINATION );
    }

    return 0;
}
