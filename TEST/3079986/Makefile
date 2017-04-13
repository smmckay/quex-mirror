simple.qx:
	@sed "s/Parserbase-XXX/Parserbase-$(TESTCASE)/" simple-XXX.qx > $@

Lexer: simple.qx
	@echo "(0) quexify -- no output is good output"
	@quex -i simple.qx --token-id-prefix scope1::scope2::scope3::TKN_ \
		  --foreign-token-id-file Parserbase-$(TESTCASE).h \
		  --debug-exception 2>&1

check: Lexer
	@echo "(1) check out generated sources"
	@awk ' /TKN_/ { print; }' Lexer.cpp Lexer-token 2>&1 

compile: Lexer
	@echo "(2) compile -- no output is good output"
	@g++ -I$(QUEX_PATH) -c Lexer.cpp -I. -Wall -Werror -Wconversion 2>&1

clean:
	@rm -f *.exe *.o Lexer* simple.qx > /dev/null 2>&1

