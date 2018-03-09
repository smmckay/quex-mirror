# PURPOSE: Trivial Demo Application
#
# License: MIT; Project http://quex.sourceforge.net
# (C) Frank-Rene Schaefer; FREE OF CHARGE--ABSOLUTELY NO WARRANTY.
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

all: lexer

lexer: lexer.o Easy.o
	$(LD) -o $@ lexer.o Easy.o 
          
Easy.o: easy/Easy.c 
	$(CC) $< -I. -o $@ 

lexer.o: lexer.c easy/Easy.c
	$(CC) $< -o $@ 

easy/Easy.c: easy.qx 
	quex -i easy.qx -o Easy --odir easy --token-id-offset 0x1000 --language C

%.E: %.cpp    # Macro expansions (only for debugging)
	$(CC) -E $< -o $@ 

clean:	
	rm -rf lexer easy/ *.o
