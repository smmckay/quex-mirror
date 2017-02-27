include ../Makefile.lexer

X = Simple

# -DQUEX_OPTION_DEBUG_SHOW 

all: lexer-iconv lexer-icu

lexer-iconv: Simple.cpp
	$(LDCPP_ICONV) $(X).cpp ../lexer.cpp $(DEFINES) -o $@ \
		-DQUEX_SETTING_BUFFER_SIZE=65536 
	

lexer-icu: Simple.cpp
	$(LDCPP_ICU) $(X).cpp ../lexer.cpp $(DEFINES) -o $@ \
		-DQUEX_SETTING_BUFFER_SIZE=65536 $(LIB_ICU) 


Simple.cpp: simple.qx
	@quex -i $< -o Simple --bet wchar_t --token-policy single --debug-exception


clean:
	@rm -rf Simple-*
	@rm -rf Simple.cpp
	@rm -rf Simple
	@rm -rf a.out lexer-iconv lexer-icu
