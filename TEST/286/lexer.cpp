#include "iostream"
#include "tokenizer_it"
#include <quex/code_base/buffer/lexatoms/converter/iconv/Converter_IConv>
#include <quex/code_base/buffer/lexatoms/converter/iconv/Converter_IConv.i>

int main(int argc, char** argv)
{
	using namespace std;
	using namespace quex;

	quex::Token              token;
    QUEX_NAME(Converter)*    converter = QUEX_NAME(Converter_IConv_new)("UTF8", NULL);
	quex::tokenizer_it       qlex((QUEX_NAME(ByteLoader)*)NULL, converter); 
    uint8_t*                 begin_p;
    const uint8_t*           end_p;
    size_t                   received_n;

	qlex.token_p_swap(&token);
	while (cin) {
		qlex.buffer.fill_prepare(&qlex.buffer, (void**)&begin_p, (const void**)&end_p);
        // printf("#fr: %p (%i)\n", begin_p, (size_t)(end_p - begin_p));
		// Read a line from standard input

		cin.getline((std::basic_istream<char>::char_type*)begin_p, 
                    (size_t)(end_p - begin_p)); 

        received_n = cin.gcount();
		if( ! received_n ) return 0;

        /* getline() cuts the newline. To be able to trace the character index
         * correctly, the newline needs to be re-inserted manually.          */
        begin_p[received_n-1] = '\n';

        printf("line: (%i) [", (int)received_n); 
        for(int i=0; i < (int)received_n; ++i) printf("%02X.", (int)begin_p[i]);
        printf("]\n");

		qlex.buffer.fill_finish(&qlex.buffer, &begin_p[received_n]);

		while (true) {
			const QUEX_TYPE_TOKEN_ID TokenID = qlex.receive();

			if (TokenID == QUEX_TKN_TERMINATION)
				break;
			else if (TokenID == QUEX_TKN_EOS) {
				cout << endl;
			} else {
				int offset = qlex.tell() - token.text.size();
				cout << offset << '\t' << quex::unicode_to_char(token.text) << endl;
			}
		}
	}
}

