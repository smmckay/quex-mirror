include ../Makefile.lexer

DEFINES := -DPRINT_TOKEN \
           -DQUEX_SETTING_BUFFER_SIZE_EXT=65536 

# -DQUEX_OPTION_DEBUG_SHOW_EXT 

all: lexer-iconv lexer-icu

lexer-iconv: Simple/Simple.cpp
	$(LDCPP_ICONV) -ggdb Simple/Simple.cpp ../lexer.cpp $(DEFINES) -o $@ 
		
	

lexer-icu: Simple/Simple.cpp
	$(LDCPP_ICU) Simple/Simple.cpp ../lexer.cpp $(DEFINES) -o $@ $(LIB_ICU) 


Simple/Simple.cpp: simple.qx
	@quex -i $< -o Simple --bet wchar_t --debug-exception


clean:
	@rm -rf Simple* a.out lexer-iconv lexer-icu
