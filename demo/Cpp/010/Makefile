# (C) Frank-Rene Schaefer
# ABSOLUTELY NO WARRANTY
#_______________________________________________________________________________
.SECONDARY:

FILES := feeder-plain.exe  feeder-converter.exe  \
	     gavager-plain.exe gavager-converter.exe \
         point-plain.exe

ifndef QUEX_PATH
    $(error The environment variable QUEX_PATH is not defined!)
endif

# (*) COMPILER SETTINGS ________________________________________________________
ifdef ASSERTS_ENABLED_F
	CCFLAG_ASSERTS=# By default asserts are enabled
else 
	CCFLAG_ASSERTS=-DQUEX_OPTION_ASSERTS_DISABLED
endif

COMPILER     := g++ -ggdb -Wall -Werror -pedantic

# Buffer size is chosen to something tiny. This way, the effect of reaching
# borders can be observed.
CC_PLAIN     := $(COMPILER) -I./ -I$(QUEX_PATH) $(CCFLAG_ASSERTS) \
	              -DQUEX_SETTING_BUFFER_SIZE=13 

CC_CONVERTER := $(COMPILER) -I./ -I$(QUEX_PATH) $(CCFLAG_ASSERTS) \
	              -DQUEX_SETTING_TRANSLATION_BUFFER_SIZE=6        \
	              -DQUEX_SETTING_BUFFER_SIZE=16                   \
			      -DQUEX_TYPE_LEXATOM=wchar_t                     \
			      -DQUEX_EXAMPLE_WITH_CONVERTER                   \
			      -DQUEX_OPTION_CONVERTER_ICONV
			  
# -DQUEX_OPTION_DEBUG_SHOW    
# -DQUEX_OPTION_ASSERTS_DISABLED
# -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED

# (*) RULES ____________________________________________________________________
all: $(FILES)

feeder-plain.exe:       lexer-feeder.cpp receiver.cpp lexPlain.cpp
	$(CC_PLAIN)     -o $@ $^ 
          
feeder-converter.exe:   lexer-feeder.cpp receiver.cpp lexConverter.cpp
	$(CC_CONVERTER) -o $@ $^ 

gavager-plain.exe:      lexer-gavager.cpp receiver.cpp lexPlain.cpp
	$(CC_PLAIN)     -o $@ $^ 
          
gavager-converter.exe:  lexer-gavager.cpp receiver.cpp lexConverter.cpp
	$(CC_CONVERTER) -o $@ $^ 

point-plain.exe:        lexer-point.cpp lexPlain.cpp
	$(CC_PLAIN)     -o $@ -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 $^

point-converter.exe:    lexer-point.cpp lexConverter.cpp
	$(CC_CONVERTER) -o $@ -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 $^ 
          
%.E: %.cpp  
	$(COMPILER) -E $< -o $@  
          
lexPlain.cpp: lexPlain.qx 
	quex -i             lexPlain.qx  \
		 -o             lexPlain     \
		 --token-policy single       \

lexConverter.cpp: lexConverter.qx 
	quex -i                    lexConverter.qx   \
		 -o                    lexConverter      \
		 --token-policy        single            \
		 --buffer-element-type wchar_t           

# (*) HELPERS __________________________________________________________________
clean:	
	rm -f lexPlain-*     lexPlain.cpp     lexPlain
	rm -f lexConverter-* lexConverter.cpp lexConverter
	rm -f $(FILES)
	rm -f *.exe
	rm -f *.o
	rm -f *.E
	rm -f *.bak
	rm -f tmp*
	rm -f *~
