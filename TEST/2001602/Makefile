include ../Makefile.lexer
X = Simple

#-DQUEX_OPTION_DEBUG_SHOW_EXT \
#-DQUEX_OPTION_UNIT_TEST_EXT \

DEFINES := -DQUEX_SETTING_BUFFER_SIZE_EXT=64 \
		   -DQUEX_SETTING_TRANSLATION_BUFFER_SIZE_EXT=64 

all: lex_icu lex_iconv lex_codec

lex_iconv: 
	@echo "Call to quex"
	@quex -i simple.qx -o $(X) -b 2 --debug-exception
	@echo "Compiling"
	$(LDCPP_ICONV) $(X)/$(X).cpp ../lexer.cpp $(DEFINES) -o $@ 

lex_icu: 
	@echo "Call to quex"
	@quex -i simple.qx -o $(X) -b 2 --debug-exception
	@echo "Compiling"
	$(LDCPP_ICU) $(X)/$(X).cpp ../lexer.cpp $(DEFINES) -o $@ $(LIB_ICU)

lex_codec: 
	@echo "Call to quex"
	@quex -i simple.qx -o $(X) --encoding utf8 --debug-exception
	@echo "Compiling"
	$(LDCPP) $(X)/$(X).cpp ../lexer.cpp $(DEFINES) -o $@ 

#-DQUEX_OPTION_DEBUG_SHOW_EXT 

clean:
	rm -rf Simple* a.out lex_icu lex_iconv lex_codec stats.log *.o
