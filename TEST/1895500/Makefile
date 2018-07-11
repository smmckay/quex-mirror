include ../Makefile.lexer

all: lexer-iconv lexer-icu

lexer-iconv: Simple/Simple.cpp
	$(LDCPP_ICONV) Simple/Simple.cpp ../lexer.cpp -o $@ > tmp.txt 2>&1
	@cat tmp.txt
	@rm  tmp.txt
	
lexer-icu: Simple/Simple.cpp
	$(LDCPP_ICONV) Simple/Simple.cpp ../lexer.cpp -o $@ $(LIB_ICU) > tmp.txt 2>&1
	@cat tmp.txt
	@rm  tmp.txt

Simple/Simple.cpp: indigo.qx
	@quex --cbm -i indigo.qx -o Simple -b 4 --debug-exception


clean:
	@rm -rf Simple*
	@rm -rf a.out lexer-icu lexer-iconv
