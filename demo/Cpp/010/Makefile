# PURPOSE: Makefile building example applications for manual buffer filling.
#
# ABSOLUTELY NO WARRANTY
#_______________________________________________________________________________
.PHONY: clean UTF8 NON_UTF8

FILES := lexer-syntactic-plain.exe \
	     lexer-arbitrary-plain.exe \
         lexer-syntactic-utf8.exe \
         lexer-arbitrary-utf8.exe \
         point.exe

ifndef QUEX_PATH
    $(error The environment variable QUEX_PATH is not defined!)
endif

# (*) SETUP ____________________________________________________________________
OBJS      := lexPlain.o receiver-plain.o
UTF8_OBJS := lexUTF8.o  receiver-utf8.o

# (*) COMPILER SETTINGS ________________________________________________________
#     (change COMPILER to whatever you use as compiler on the command line,
#      e.g. "make COMPILER=icpc" will use intel's c++ compiler)
ifdef ASSERTS_ENABLED_F
	CCFLAG_ASSERTS=# By default asserts are enabled
else 
	CCFLAG_ASSERTS=-DQUEX_OPTION_ASSERTS_DISABLED
endif

COMPILER := g++ -ggdb -Wall -Werror -pedantic -DQUEX_SETTING_BUFFER_SIZE=16

CC       := $(COMPILER) -I./ -I$(QUEX_PATH) $(CCFLAG_ASSERTS) 
            # -DQUEX_OPTION_DEBUG_SHOW    
            # -DQUEX_OPTION_ASSERTS_DISABLED
   	        # -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED

CC_UTF8  := $(CC) -DQUEX_TYPE_LEXATOM=wchar_t \
				  -DQUEX_EXAMPLE_WITH_CONVERTER

# (*) RULES ____________________________________________________________________
all: $(FILES)

lexer-%-plain.exe:   lexer-%-plain.o $(OBJS)  
	$(CC) -o $@ $< $(OBJS) 
          
lexer-%-utf8.exe:    lexer-%-utf8.o $(UTF8_OBJS)  
	$(CC_UTF8) -o $@ $< $(UTF8_OBJS) 

point.exe:           point.cpp $(OBJS)  
	## All related files must be compiled with fallback_n = 0 
	$(CC)      -o $@ -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 $< $(OBJS) 
          
%-plain.o: %.cpp  lexPlain.cpp
	$(CC)      -c $< -o $@ 
          
%-utf8.o:  %.cpp  lexUTF8.cpp
	$(CC_UTF8) -c $< -o $@ 
          
lexPlain.o: lexPlain.cpp  
	$(CC)   -c $< -o $@  
          
lexUTF8.o:  lexUTF8.cpp  
	$(CC)   -c $< -o $@  
          
%.E:            %.cpp  
	$(CC)      -E $< -o $@  
          
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
