# PURPOSE: Makefile Demo Application of Quex
#
# ABSOLUTELY NO WARRANTY
#_______________________________________________________________________________
include ../Makefile.lexer

.PHONY: clean

ifndef QUEX_PATH
    $(error The environment variable QUEX_PATH is not defined!)
endif


ifeq ($(QX_FILE),example.qx)
	ADD_DEFINES=-DQUEX_SETTING_BUFFER_SIZE_EXT=8
else
	ADD_DEFINES=-DQUEX_SETTING_BUFFER_SIZE_EXT=11 -DPRINT_LINE_COLUMN_NUMBER
endif

CCFLAG_ASSERTS=-DQUEX_OPTION_ASSERTS

CC := $(CC) -c -I./ \
	 -Wall -Werror -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT -Wconversion -pedantic \
	 -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT \
	 -DPRINT_TOKEN                                  \
	 $(ADD_DEFINES)
   
# -DQUEX_OPTION_DEBUG_SHOW_EXT                       \
	
LD := $(LDC) 

all: lexer

lexer:          example.o Simple.o
	$(LD) -o $@ example.o Simple.o 
          
# Object files:
Simple.o: Simple/Simple.c 
	$(CC) $< -o $@ 

example.o: $(QUEX_PATH)/TEST/lexer.c  Simple/Simple.c
	$(CC) -DPRINT_LINE_COLUMN_NUMBER $< -o $@ 

Simple/Simple.c: $(QX_FILE) 
	quex -i $(QX_FILE) -o Simple --language C --debug-exception

clean:	
	rm -rf Simple* *.o *.bak lexer
