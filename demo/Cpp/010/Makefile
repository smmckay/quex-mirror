# PURPOSE: Makefile building example applications for manual buffer filling.
#
# ABSOLUTELY NO WARRANTY
#_______________________________________________________________________________
.PHONY: clean UTF8 NON_UTF8

FILES := lexer-plain.exe \
         lexer-utf8.exe  \
         point.exe

ifndef QUEX_PATH
    $(error The environment variable QUEX_PATH is not defined!)
endif

# (*) COMPILER SETTINGS ________________________________________________________
ifdef ASSERTS_ENABLED_F
	CCFLAG_ASSERTS=# By default asserts are enabled
else 
	CCFLAG_ASSERTS=-DQUEX_OPTION_ASSERTS_DISABLED
endif

COMPILER := g++ -ggdb -Wall -Werror -pedantic

CC       := $(COMPILER) -I./ -I$(QUEX_PATH) $(CCFLAG_ASSERTS) \
	          -DQUEX_SETTING_BUFFER_SIZE=14

CC_UTF8  := $(COMPILER) -I./ -I$(QUEX_PATH) $(CCFLAG_ASSERTS) \
	          -DQUEX_SETTING_BUFFER_SIZE=16                   \
			  -DQUEX_TYPE_LEXATOM=wchar_t                     \
			  -DQUEX_EXAMPLE_WITH_CONVERTER
			  
# -DQUEX_OPTION_DEBUG_SHOW    
# -DQUEX_OPTION_ASSERTS_DISABLED
# -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED

# (*) RULES ____________________________________________________________________
all: $(FILES)

fill-plain.exe:   lexer-feeder.cpp receiver.cpp lexPlain.cpp
	$(CC)      -o $@ $^ $(OBJS) 
          
fill-utf8.exe:    lexer-feeder.cpp receiver.cpp lexUTF8.cpp
	$(CC_UTF8) -o $@ $^ $(UTF8_OBJS) 

point-plain.exe:  lexer-point.cpp receiver.cpp lexPlain.cpp
	$(CC)      -o $@ -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 $^

point-utf8.exe:   lexer-point.cpp receiver.cpp lexPlain.cpp
	$(CC_UTF8) -o $@ -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 $^ 
          
%.E:        %.cpp  
	$(CC)   -E $< -o $@  
          
lexPlain lexPlain.cpp: lexPlain.qx 
	quex -i             lexPlain.qx  \
		 -o             lexPlain     \
		 --token-policy single       \

lexUTF8 lexUTF8.cpp: lexUTF8.qx 
	quex -i                    lexUTF8.qx   \
		 -o                    lexUTF8      \
		 --iconv                            \
		 --token-policy        single       \
		 --buffer-element-type wchar_t      \

# (*) HELPERS __________________________________________________________________
clean:	
	rm -f lexPlain.cpp lexPlain-configuration lexPlain-token lexPlain-token_ids lexPlain
	rm -f lexUTF8.cpp  lexUTF8-configuration  lexUTF8-token  lexUTF8-token_ids lexUTF8
	rm -f $(FILES)
	rm -f *.exe
	rm -f *.o
	rm -f *.E
	rm -f *.bak
	rm -f tmp*
	rm -f *~
