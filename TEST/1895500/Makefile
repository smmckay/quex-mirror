
lexer-iconv: Simple.cpp
	@$(LDC_ICONV) Simple.cpp ../lexer.cpp -o $@ > tmp.txt 2>&1
	@cat tmp.txt
	@rm  tmp.txt
	
lexer-icu: Simple.cpp
	@$(LDC_ICONV) Simple.cpp ../lexer.cpp -o $@ $(LIB_ICU) > tmp.txt 2>&1
	@cat tmp.txt
	@rm  tmp.txt

Simple.cpp: indigo.qx
	@quex -i indigo.qx -o Simple -b 4 --debug-exception


clean:
	@rm -rf Simple*
	@rm -rf a.out lexer-icu lexer-iconv
