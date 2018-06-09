include ../Makefile.lexer

all: lex_iconv lex_icu lex_codec

DEFINES := -DQUEX_SETTING_BUFFER_SIZE_EXT=64            \
		   -DQUEX_SETTING_TRANSLATION_BUFFER_SIZE_EXT=64 

lex_iconv: 
	@echo "Call to quex"
	@quex -i simple.qx -o Simple --bet wchar_t --debug-exception
	@echo "Compiling"
	$(LDCPP_ICONV) Simple/Simple.cpp ../lexer.cpp $(DEFINES) -o $@

lex_icu: 
	@echo "Call to quex"
	@quex -i simple.qx -o Simple --bet wchar_t 
	@echo "Compiling"
	$(LDCPP_ICU) Simple/Simple.cpp ../lexer.cpp $(DEFINES) -o $@ $(LIB_ICU)

lex_codec: 
	@echo "Call to quex"
	@quex -i simple.qx -o Simple --encoding utf8  
	@echo "Compiling"
	$(LDCPP) Simple/Simple.cpp ../lexer.cpp $(DEFINES) -o $@
clean:
	rm -rf Simple* a.out lex_iconv lex_icu lex_codec *.o
