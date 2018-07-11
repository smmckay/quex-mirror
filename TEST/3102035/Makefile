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
	 -Wall -Werror -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT -W -Wconversion -pedantic                 \
	 -DQUEX_SETTING_BUFFER_SIZE_EXT=4 \
	 $(CCFLAG_ASSERTS)                               \
	 -DPRINT_TOKEN                                   \
	 -DPRINT_LINE_COLUMN_NUMBER
     # -DQUEX_OPTION_ASSERTS_DISABLED_EXT
     # -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT 
     # -DQUEX_OPTION_DEBUG_SHOW_EXT
   
# (*) RULES ____________________________________________________________________
# -- application
# Object files:
Case%: Simple/Case%.c 
	$(LDC) -c $< -o $@.o

# Macro expansions (only for debugging):
%.E: %.c    
	$(CC) -E $< -o $@ 

Case4: $(QUEX_PATH)/TEST/lexer.c
	quex --cbm -i case4.qx  -o Simple --language C --debug-exception
	$(LDC) $^ Simple/Simple.c -o $@ 

Case5: $(QUEX_PATH)/TEST/lexer.c
	quex --cbm -i case5.qx  -o Simple --language C --debug-exception
	$(LDC) $^ Simple/Simple.c -o $@ 

Simple/Case2.c: case2.qx 
	## Case2 causes an error message which we want to see: no '--debug-exception'
	quex --cbm -i $<  -o Case2 --odir Simple --language C 

Simple/Case%.c: case%.qx 
	quex --cbm -i $<  -o Case$* --odir Simple --language C --debug-exception

# (*) HELPERS __________________________________________________________________
clean:	
	rm -rf Simple* Case?  *.o *.bak *.E lexer
