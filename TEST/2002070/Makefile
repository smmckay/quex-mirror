DEF_SIZE := -DQUEX_SETTING_BUFFER_SIZE=64

lexer-iconv: Simple.cpp text.345
	$(LDCPP_ICONV) Simple.cpp ../lexer.cpp -o $@ $(DEF_SIZE) \
		-DQUEX_SETTING_TRANSLATION_BUFFER_SIZE=1024 > tmp.txt 2>&1
	@cat tmp.txt
	@rm  tmp.txt
	
lexer-icu: Simple.cpp text.345
	$(LDCPP_ICU) Simple.cpp ../lexer.cpp -o $@ $(DEF_SIZE) $(LIB_ICU) \
		-D__QUEX_OPTION_UNIT_TEST_INPUT_STRATEGY_ICU > tmp.txt 2>&1
	@cat tmp.txt
	# @rm  tmp.txt

Simple.cpp: simple.qx
	@quex -i $< -o Simple --bet wchar_t --debug-exception

text.345: 
	bzip2 -kd text.345.bz2

clean:
	rm -rf Simple-*
	rm -rf Simple.cpp
	rm -rf Simple
	rm -rf a.out lexer-iconv lexer-icu
	rm  -f  text.345
