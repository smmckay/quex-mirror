include ../Makefile.lexer

X = Simple
LIB_CONV  = `icu-config --ldflags --cppflags`

DEFINES := -DQUEX_SETTING_BUFFER_SIZE_EXT=64 \
		   -DQUEX_SETTING_LEXATOM_LOADER_CONVERTER_BUFFER_SIZE_EXT=64 \
	       -DPRINT_TOKEN_FIRST_NUMBER='402508 - 20' 

# C++ Versions ________________________________________________________________
# 
lex_iconv: 
	@echo "Call to quex"
	@quex --cbm -i simple.qx -o $(X) --bet wchar_t 
	@echo "Compiling"
	$(LDCPP_ICONV) $(X)/$(X).cpp ../lexer.cpp $(DEFINES) -o $@

lex_icu: 
	@echo "Call to quex"
	@quex --cbm -i simple.qx -o $(X) --bet wchar_t 
	@echo "Compiling"
	$(LDCPP_ICU) $(X)/$(X).cpp ../lexer.cpp $(DEFINES) -o $@ $(LIB_ICU)

lex_codec: 
	@echo "Call to quex"
	@quex --cbm -i simple.qx -o $(X) --encoding utf8  
	@echo "Compiling"
	$(LDCPP) $(X)/$(X).cpp ../lexer.cpp $(DEFINES) -o $@ 

# C Versions ________________________________________________________________
# 
lex_iconv_c: 
	@echo "Call to quex"
	@quex --cbm -i simple.qx -o $(X) --bet wchar_t --language c
	@echo "Compiling"
	$(LDC_ICONV) $(X)/$(X).c ../lexer.c $(DEFINES) -DPRINT_TOKEN -o $@

lex_icu_c: 
	@echo "Call to quex"
	@quex --cbm -i simple.qx -o $(X) --bet wchar_t --language c
	@echo "Compiling"
	$(LDC_ICU) $(X)/$(X).c ../lexer.c $(DEFINES) -DPRINT_TOKEN -o $@ $(LIB_ICU)

lex_codec_c: 
	@echo "Call to quex"
	@quex --cbm -i simple.qx -o $(X) --encoding utf8  --language C
	@echo "Compiling"
	$(LDC) $(X)/$(X).c ../lexer.c $(DEFINES) -DPRINT_TOKEN -o $@ 

wiki.txt: wiki.txt.bz2
	bzip2 -dk wiki.txt.bz2

clean:
	rm -rf $(X)
	rm -rf $(X).cpp
	rm -rf $(X).c
	rm -rf $(X).h
	rm -rf $(X)
	rm -rf lex_iconv   lex_icu   lex_codec
	rm -rf lex_iconv_c lex_icu_c lex_codec_c
	rm -rf wiki.txt
