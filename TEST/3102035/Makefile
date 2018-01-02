# PURPOSE: Makefile Demo Application of Quex
#
# ABSOLUTELY NO WARRANTY
#_______________________________________________________________________________
include ../Makefile.lexer
.PHONY: clean
# .SECONDARY: Case1.c

ifndef QUEX_PATH
    $(error The environment variable QUEX_PATH is not defined!)
endif

LDC := $(LDC) \
	 -I./ -I$(QUEX_PATH)                             \
	 -Wall -Werror -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED -W -Wconversion -pedantic                 \
	 -DQUEX_SETTING_BUFFER_SIZE=4 \
	 $(CCFLAG_ASSERTS)                               \
	 -DPRINT_TOKEN                                   \
	 -DPRINT_LINE_COLUMN_NUMBER
     # -DQUEX_OPTION_ASSERTS_DISABLED
     # -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED 
     # -DQUEX_OPTION_DEBUG_SHOW
   
# (*) RULES ____________________________________________________________________
# -- application
# Object files:
Case%: Case%.c 
	$(LDC) -c $< -o $@.o

# Macro expansions (only for debugging):
%.E: %.c    
	$(CC) -E $< -o $@ 

Case4: $(QUEX_PATH)/TEST/lexer.c
	quex -i case4.qx  -o Simple --language C --debug-exception
	$(LDC) $^ Simple.c -o $@ 

Case5: $(QUEX_PATH)/TEST/lexer.c
	quex -i case5.qx  -o Simple --language C --debug-exception
	$(LDC) $^ Simple.c -o $@ 

Case2.c: case2.qx 
	## Case2 causes an error message which we want to see: no '--debug-exception'
	quex -i $<  -o $(@:.c=) --language C 

Case%.c: case%.qx 
	quex -i $<  -o $(@:.c=) --language C --debug-exception

# (*) HELPERS __________________________________________________________________
clean:	
	rm -f Simple*
	rm -f Case*
	rm -f *.o
	rm -f *.bak
	rm -f *.E
	rm -f lexer
