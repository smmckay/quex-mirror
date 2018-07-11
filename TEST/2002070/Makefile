include ../Makefile.lexer

DEF_SIZE := -DQUEX_SETTING_BUFFER_SIZE_EXT=64

all: lexer-iconv lexer-icu 

lexer-iconv: Simple/Simple.cpp text.345
	$(LDCPP_ICONV) Simple/Simple.cpp ../lexer.cpp -o $@ $(DEF_SIZE) \
		-DQUEX_SETTING_LEXATOM_LOADER_CONVERTER_BUFFER_SIZE_EXT=1024 > tmp.txt 2>&1
	@cat tmp.txt
	@rm  tmp.txt
	
lexer-icu: Simple/Simple.cpp text.345
	$(LDCPP_ICU) Simple/Simple.cpp ../lexer.cpp -o $@ $(DEF_SIZE) $(LIB_ICU) \
		-DQUEX_OPTION_UNIT_TEST_INPUT_STRATEGY_ICU_EXT > tmp.txt 2>&1
	@cat tmp.txt
	# @rm  tmp.txt

Simple/Simple.cpp: simple.qx
	@quex --cbm -i $< -o Simple --bet wchar_t --debug-exception

text.345: 
	bzip2 -kd text.345.bz2

clean:
	rm -rf Simple-*
	rm -rf Simple/Simple.cpp
	rm -rf Simple
	rm -rf a.out lexer-iconv lexer-icu
	rm  -f  text.345
