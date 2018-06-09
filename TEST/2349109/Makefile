include ../Makefile.lexer

INPUT=newline-skipper-utf8 # This is overidden by a command line argument of the for INPUT=something

all: $(INPUT)

# -DQUEX_OPTION_DEBUG_SHOW_EXT

newline-skipper: 
	@quex -i token.qx newline-skipper.qx -o Simple --debug-exception
	@$(LDCPP) Simple/Simple*.cpp ../lexer-simply.cpp -o lexer \
		-DPRINT_LINE_COLUMN \
		-DQUEX_OPTION_COUNTER_LINE_EXT \
		-DQUEX_OPTION_COUNTER_COLUMN_EXT \
		-DQUEX_SETTING_BUFFER_SIZE_EXT=4

newline-skipper-utf8: 
	@quex -i token.qx newline-skipper-utf8.qx -o Simple  -b 2 --debug-exception
	@$(LDCPP_ICONV) ../lexer-simply.cpp Simple/Simple*.cpp -o lexer \
		-DPRINT_LINE_COLUMN \
		-DCONVERTER_ENCODING='"UTF-8"' \
		-DQUEX_OPTION_COUNTER_LINE_EXT \
		-DQUEX_OPTION_COUNTER_COLUMN_EXT \
		-DQUEX_OPTION_UNIT_TEST_UTF8___EXT \
		-DQUEX_SETTING_BUFFER_SIZE_EXT=1000 

non-newline-skipper: 
	@quex -i token.qx non-newline-skipper.qx -o Simple --debug-exception
	@$(LDCPP) Simple/Simple*.cpp ../lexer-simply.cpp -o lexer \
		-DPRINT_LINE_COLUMN \
		-DPRINT_TOKEN \
		-DQUEX_OPTION_COUNTER_LINE_EXT \
		-DQUEX_OPTION_COUNTER_COLUMN_EXT \
		-DQUEX_SETTING_BUFFER_SIZE_EXT=4

clean:
	@rm -rf lexer Simple*
