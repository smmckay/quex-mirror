/* ARGS: $1: 'bad'  => construct a lexer based on a 'wchar_t' stream that 
 *                     feeds a converter which expects UTF8.
 *                  => expected break up upon construction time.
 *           'good' => constructs a lexical analyzer that runs directly on
 *                     UTF8. There the 'wchar_t' stream works fine, even if
 *                     it carries only byte values.
 *
 * (C) Frank-Rene Schaefer                                                    */
#include <cstdio> 
#include "IConv_Lexer"
#include "Codec_Lexer"

/* When using multiple lexical analyzers, it must be compiled with 
 * QUEX_OPTION_MULTI and 'multi.i' must be included in one single file.      */
#include <quex/code_base/multi.i>

using namespace std;

int main(int argc, char** argv) 
{        
    wstring        str(L"max und moritz");
    wstringstream* istr = new std::wstringstream(str);

    if( argc > 1 && strcmp(argv[1], "bad") == 0 ) {
        QUEX_NAME(ByteLoader)*  byte_loader = QUEX_NAME(ByteLoader_wstream)(istr);
        IConv::Lexer lex(byte_loader, 
                         QUEX_NAME(Converter_IConv_new),
                         "UTF8"); // Should break right here!
    }
    else /* 'good' */ {
        Codec::Lexer  lex(istr); 
        Codec::Token* token;

        do {
            (void)lex.receive(&token);

            wcout << L"Token: ";
            wcout << token->get_string();
            wcout << L"\n";

        } while( token->type_id() != CODEC_TKN_TERMINATION );
    }

    return 0;
}
