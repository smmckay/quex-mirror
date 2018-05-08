#include "iostream"
#include "tokenizer_it/tokenizer_it"
#include <tokenizer_it/lib/buffer/lexatoms/converter/iconv/Converter_IConv>
#include <tokenizer_it/lib/buffer/lexatoms/converter/iconv/Converter_IConv.i>

int main(int argc, char** argv)
{
	using namespace std;
	using namespace quex;

	quex::Token*             token_p;
    QUEX_NAME(Converter)*    converter = QUEX_NAME(Converter_IConv_new)("UTF8", NULL);
	quex::tokenizer_it       qlex((QUEX_NAME(ByteLoader)*)NULL, converter); 
    uint8_t*                 begin_p;
    const uint8_t*           end_p;
    size_t                   received_n;

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
			qlex.receive(&token_p);
            const tokenizer_it_token_id_t TokenID = token_p->id;

			if (TokenID == QUEX_TKN_TERMINATION)
				break;
			else if (TokenID == QUEX_TKN_EOS) {
				cout << endl;
			} else {
				int offset = qlex.tell() - QUEX_NAME(lexeme_length)(token_p->text);
				cout << offset << '\t' << QUEX_NAME(lexeme_to_pretty_char)(token_p->text) << endl;
			}
		}
	}
}

