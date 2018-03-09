# PURPOSE: Makefile Demo Application of Quex
#
# ABSOLUTELY NO WARRANTY
#_______________________________________________________________________________
.PHONY: clean
.SECONDARY:

COMPILER := gcc -ggdb -pedantic -Wconversion -Wall -Werror -W
LD       := $(COMPILER) 
CC       := $(COMPILER) -c -I./ $(ADD_FLAGS) 
#           Useful options for debugging:
#           -DQUEX_OPTION_ASSERTS_DISABLED
#           -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED 
#           -DQUEX_OPTION_DEBUG_SHOW

# (*) RULES ____________________________________________________________________
# -- application
lexer:          example.o EasyLexer.o
	$(LD) -o $@ example.o EasyLexer.o 
          
# Object files:
EasyLexer.o: EasyLexer.c 
	$(CC) $< -o $@ 

example.o: ../example.c EasyLexer.c
	$(CC) $< -o $@ 

# Macro expansions (only for debugging):
%.E: %.c    
	$(CC) -E $< -o $@ 

EasyLexer.c: simple.qx 
	quex -i                 simple.qx  common.qx \
	     -o                 EasyLexer  \
		 --token-id-offset  0x1000     \
		 --language         C          

clean:	
	rm -rf lexer easy/ *.o
