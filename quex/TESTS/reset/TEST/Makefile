
FILES = lexer codec-lexer iconv-lexer icu-lexer lexer-x

CC = g++ -I. \
	 -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT \
	 -ggdb -Wall -fsanitize=address
     # -DQUEX_OPTION_DEBUG_SHOW_EXT 
	 # 

all: $(FILES)

codec-lexer: lexer.cpp 
	quex -i simple-hindi.qx -o Simple --encoding utf8 --debug-exception
	$(CC) lexer.cpp Simple/Simple.cpp  -o $@ \
		  -DQUEX_SETTING_BUFFER_SIZE_EXT=39                     \
	      -DQUEX_SETTING_TEST_UTF8     

iconv-lexer: lexer.cpp 
	quex -i simple-hindi.qx -o Simple --bet wchar_t --debug-exception
	$(CC) lexer.cpp Simple/Simple.cpp  -o $@ \
		  -DQUEX_SETTING_BUFFER_SIZE_EXT=20                     \
		  -DQUEX_OPTION_CONVERTER_ICONV                         \
		  -DQUEX_SETTING_LEXATOM_LOADER_CONVERTER_BUFFER_SIZE_EXT=20         \
		  -DQUEX_SETTING_TEST_UTF8               

icu-lexer: lexer.cpp 
	quex -i simple-hindi.qx -o Simple --bet wchar_t --debug-exception
	$(CC) lexer.cpp Simple/Simple.cpp  -o $@ \
		  `icu-config --ldflags`                            \
		  -DQUEX_SETTING_BUFFER_SIZE_EXT=20                     \
		  -DQUEX_OPTION_CONVERTER_ICU                           \
		  -DQUEX_SETTING_LEXATOM_LOADER_CONVERTER_BUFFER_SIZE_EXT=20         \
		  -DQUEX_SETTING_TEST_UTF8               

lexer: lexer.cpp 
	quex -i simple.qx common.qx -o Simple --debug-exception
	$(CC) lexer.cpp Simple/Simple.cpp  -o $@ \
		 -DQUEX_SETTING_BUFFER_SIZE_EXT=14                 \
		 -DQUEX_SETTING_LEXATOM_LOADER_CONVERTER_BUFFER_SIZE_EXT=9           
		 #-DQUEX_OPTION_DEBUG_SHOW_EXT                      \

lexer-x: lexer-x.cpp
	quex -i simple.qx common.qx -o Simple --debug-exception
	echo Must call quex here
	$(CC) lexer-x.cpp Simple/Simple.cpp  -o $@ \
		 -DQUEX_SETTING_BUFFER_SIZE_EXT=14                      \
		 -DQUEX_SETTING_LEXATOM_LOADER_CONVERTER_BUFFER_SIZE_EXT=9           

hwut-info:
	@echo $(FILES)

clean:
	rm -rf Simple*
	rm -f $(FILES)
