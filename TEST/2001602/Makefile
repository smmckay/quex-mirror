include ../Makefile.lexer
X = Simple

#-DQUEX_OPTION_DEBUG_SHOW \
#-D__QUEX_OPTION_UNIT_TEST \
#-D__QUEX_OPTION_UNIT_TEST_QUEX_BUFFER_LOADS \

DEFINES := -DQUEX_SETTING_BUFFER_SIZE=64 \
		   -DQUEX_SETTING_TRANSLATION_BUFFER_SIZE=64 

all: lex_icu lex_iconv lex_codec

lex_iconv: 
	@echo "Call to quex"
	@quex -i simple.qx -o $(X) -b 2 --debug-exception
	@echo "Compiling"
	$(LDCPP_ICONV) $(X).cpp ../lexer.cpp $(DEFINES) -o $@ 

lex_icu: 
	@echo "Call to quex"
	@quex -i simple.qx -o $(X) -b 2 --debug-exception
	@echo "Compiling"
	$(LDCPP_ICU) $(X).cpp ../lexer.cpp $(DEFINES) -o $@ $(LIB_ICU)

lex_codec: 
	@echo "Call to quex"
	@quex -i simple.qx -o $(X) --codec utf8 --debug-exception
	@echo "Compiling"
	$(LDCPP) $(X).cpp ../lexer.cpp $(DEFINES) -o $@ 

#-DQUEX_OPTION_DEBUG_SHOW 

clean:
	rm -rf EasyLexer*
	rm -rf Simple*
	rm -rf $(X)-*
	rm -rf $(X).cpp
	rm -rf $(X)
	rm -rf a.out
	rm -rf lex_icu lex_iconv lex_codec
	rm -rf stats.log
