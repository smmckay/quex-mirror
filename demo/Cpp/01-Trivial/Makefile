# PURPOSE: Makefile Demo Application of Quex
#
# ABSOLUTELY NO WARRANTY
#_______________________________________________________________________________
.PHONY: clean
.SECONDARY:

CCFLAG_ASSERTS=-DQUEX_OPTION_ASSERTS_DISABLED

# (*) COMPILER SETTINGS ________________________________________________________
#     (change COMPILER to whatever you use as compiler on the command line,
#      e.g. "make COMPILER=icpc" will use intel's c++ compiler)
COMPILER := g++ -ggdb -pedantic -Wconversion -Wall -Werror -W
CC       := $(COMPILER) -c -I./ $(CCFLAG_ASSERTS) 
# Other useful options for debugging:
# -DQUEX_OPTION_ASSERTS_DISABLED
# -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED 
# -DQUEX_OPTION_DEBUG_SHOW
   
LD       := $(COMPILER) 

# (*) RULES ____________________________________________________________________
#
lexer: lexer.o Easy.o
	$(LD) -o $@ lexer.o Easy.o 
          
Easy.o: easy/Easy.cpp 
	$(CC) $< -I. -o $@ 

lexer.o: lexer.cpp easy/Easy.cpp
	$(CC) $< -o $@ 

easy/Easy.cpp: easy.qx 
	quex -i easy.qx -o Easy --odir easy --token-id-offset  0x1000

# Macro expansions (only for debugging):
%.E: %.cpp    
	$(CC) -E $< -o $@ 

clean:	
	rm -rd lexer easy/
