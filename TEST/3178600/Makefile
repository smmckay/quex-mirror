# PURPOSE: Makefile Demo Application of Quex
#
# ABSOLUTELY NO WARRANTY
#_______________________________________________________________________________
include ../Makefile.lexer

.PHONY: clean

ifndef QUEX_PATH
    $(error The environment variable QUEX_PATH is not defined!)
endif

ifdef ASSERTS_ENABLED_F
	CCFLAG_ASSERTS=# By default asserts are enabled
else 
	CCFLAG_ASSERTS=-DQUEX_OPTION_ASSERTS_DISABLED
endif

CC := $(CC) -c -Wconversion -pedantic   \
     # -DQUEX_OPTION_DEBUG_SHOW_MODES \
     # -DQUEX_OPTION_DEBUG_SHOW       \
	 $(CCFLAG_ASSERTS) 
     # -DQUEX_OPTION_ASSERTS_DISABLED
     # -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED 
   
LD := $(LDC) 

lexer:          example.c EasyLexer/EasyLexer.c
	$(LD) -o $@ $^
          
EasyLexer/EasyLexer.c: example.qx $(QUEX_CORE)
	quex -i         example.qx   \
	     -o   EasyLexer    \
		 --comment-state-machine \
		 --language C          --debug-exception

# (*) HELPERS __________________________________________________________________
clean:	
	rm -f EasyLexer*
	rm -f *.o
	rm -f *.bak
	rm -f *.E
	rm -f lexer
