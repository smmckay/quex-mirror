# PURPOSE: Makefile Demo Application of Quex
#
# ABSOLUTELY NO WARRANTY
#_______________________________________________________________________________
.PHONY: clean
.SECONDARY:

COMPILER := gcc -ggdb -pedantic -Wconversion -Wall -Werror -W
LD       := $(COMPILER) -I./ $(ADD_FLAGS) 
#           Useful options for debugging:
#           -DQUEX_OPTION_ASSERTS_DISABLED
#           -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED 
#           -DQUEX_OPTION_DEBUG_SHOW

all:   lexer lexer2

lexer: easy.qx 
	quex -i patterns.qx tokens.qx common.qx easy.qx -o Easy --language C
	$(LD) lexer.c Easy/Easy.c -o $@ 
         
lexer2: easy2.qx 
	quex -i patterns.qx tokens.qx common.qx easy2.qx -o Easy2 --language C
	$(LD) -DLEXER2 lexer.c Easy2/Easy2.c -o $@ 

clean:	
	rm -rf lexer Easy/ Easy2/ *.o tmp.*
