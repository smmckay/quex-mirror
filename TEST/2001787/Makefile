X = Simple

# -DQUEX_OPTION_DEBUG_SHOW 

all: lexer-iconv lexer-icu

lexer-iconv: Simple.cpp
	@g++ -I./ -I$(QUEX_PATH) \
		Simple.cpp                    \
		../lexer-simply.cpp           \
		-ggdb                         \
		-o $@                         \
		-DQUEX_OPTION_CONVERTER_ICONV \
		-DQUEX_SETTING_BUFFER_SIZE=65536 \
		> tmp.txt 2>&1
	@cat tmp.txt
	@rm  tmp.txt
	

lexer-icu: Simple.cpp
	@g++ -I./ -I$(QUEX_PATH) \
		Simple.cpp                    \
		../lexer-simply.cpp           \
		-ggdb                         \
		-o $@                         \
		-DQUEX_OPTION_CONVERTER_ICU   \
		-DQUEX_SETTING_BUFFER_SIZE=65536 \
		> tmp.txt 2>&1
	@cat tmp.txt
	@rm  tmp.txt


Simple.cpp: simple.qx
	@quex -i $< -o Simple --bet wchar_t --iconv --token-policy single --debug-exception


clean:
	@rm -rf Simple-*
	@rm -rf Simple.cpp
	@rm -rf Simple
	@rm -rf a.out lexer-iconv lexer-icu
