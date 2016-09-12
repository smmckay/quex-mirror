# (C) Frank-Rene Schaefer
# ABSOLUTELY NO WARRANTY
#_______________________________________________________________________________

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

COMPILER     := gcc -ggdb -Wall -Werror -pedantic # -std=c89

# Buffer size is chosen to something tiny. This way, the effect of reaching
# borders can be observed.
CC_PLAIN     := $(COMPILER) -I./ -I$(QUEX_PATH) $(CCFLAG_ASSERTS) \
	              -DQUEX_SETTING_BUFFER_SIZE=12 

CC_CONVERTER := $(COMPILER) -I./ -I$(QUEX_PATH) $(CCFLAG_ASSERTS) \
	              -DQUEX_SETTING_TRANSLATION_BUFFER_SIZE=6        \
	              -DQUEX_SETTING_BUFFER_SIZE=16                   \
			      -DQUEX_TYPE_LEXATOM=wchar_t                     \
			      -DQUEX_EXAMPLE_WITH_CONVERTER
			  
# -DQUEX_OPTION_DEBUG_SHOW    
# -DQUEX_OPTION_ASSERTS_DISABLED
# -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED

# (*) RULES ____________________________________________________________________
all: $(FILES)

feeder-plain.exe:       lexer-feeder.c receiver.c lexPlain.c
	$(CC_PLAIN)     -o $@ $^ 
          
feeder-converter.exe:   lexer-feeder.c receiver.c lexConverter.c
	$(CC_CONVERTER) -o $@ $^ 

gavager-plain.exe:      lexer-gavager.c receiver.c lexPlain.c
	$(CC_PLAIN)     -o $@ $^ 
          
gavager-converter.exe:  lexer-gavager.c receiver.c lexConverter.c
	$(CC_CONVERTER) -o $@ $^ 

point-plain.exe:        lexer-point.c lexPlain.c
	$(CC_PLAIN)     -o $@ -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 $^

point-converter.exe:    lexer-point.c lexConverter.c
	$(CC_CONVERTER) -o $@ -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 $^ 
          
%.E: %.c  
	$(COMPILER) -E $< -o $@  
          
lexPlain.c: lexPlain.qx 
	quex -i             lexPlain.qx  \
		 -o             lexPlain     \
		 --token-policy single       \
		 --language     C            

lexConverter.c: lexConverter.qx 
	quex -i                    lexConverter.qx   \
		 -o                    lexConverter      \
		 --iconv                                 \
		 --token-policy        single            \
		 --buffer-element-type wchar_t           \
		 --language            C            

# (*) HELPERS __________________________________________________________________
clean:	
	rm -f lexPlain.c         lexPlain-configuration     lexPlain-token     \
	      lexPlain-token_ids lexPlain
	rm -f lexConverter.c     lexConverter-configuration lexConverter-token \
		  lexConverter-token_ids lexConverter
	rm -f $(FILES)
	rm -f *.exe
	rm -f *.o
	rm -f *.E
	rm -f *.bak
	rm -f tmp*
	rm -f *~
