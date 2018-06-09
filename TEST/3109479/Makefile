# PURPOSE: Makefile Demo Application of Quex
#
# ABSOLUTELY NO WARRANTY
#_______________________________________________________________________________
include ../Makefile.lexer

.PHONY: clean

ifndef QUEX_PATH
    $(error The environment variable QUEX_PATH is not defined!)
endif


CCFLAG_ASSERTS=-DQUEX_OPTION_ASSERTS_EXT

# (*) COMPILER SETTINGS ________________________________________________________
#     (change COMPILER to whatever you use as compiler on the command line,
#      e.g. "make COMPILER=icpc" will use intel's c++ compiler)
COMPILER = gcc -ggdb 

ifdef N
	QX_FILE=test$(N).qx
else
	QX_FILE=setting_of_N_not_specified_on_command_line_to_make
endif
	

CC := $(CC) \
	 -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT \
	 -DPRINT_TOKEN
     # -DQUEX_OPTION_DEBUG_SHOW_EXT \
	 $(CCFLAG_ASSERTS) 
     # -DQUEX_OPTION_ASSERTS_DISABLED_EXT
     # -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT 
   
   LD := $(LDC) 

# (*) RULES ____________________________________________________________________
# -- application
lexer: example.o Simple.o
	$(LDC) -o $@ example.o Simple.o 
          
# Object files:
Simple.o: Simple/Simple.c 
	$(CC) $< -o $@ 

example.o: $(QUEX_PATH)/TEST/lexer.c  Simple/Simple.c
	$(CC) $< -o $@ 

# Macro expansions (only for debugging):
%.E: %.c    
	$(CC) -E $< -o $@ 

Simple/Simple.c: $(QX_FILE) 
	quex -i $(QX_FILE) -o Simple --language C #--debug-exception

# (*) HELPERS __________________________________________________________________
clean:	
	rm -rf Simple*
	rm -f *.o
	rm -f *.bak
	rm -f *.E
	rm -f lexer
