# PURPOSE: Makefile Demo Application of Quex
#
# ABSOLUTELY NO WARRANTY
#_______________________________________________________________________________
.PHONY: clean
.SECONDARY:

COMPILER := g++ -ggdb -pedantic -Wconversion -Wall -Werror -W
LD       := $(COMPILER) -I./ $(ADD_FLAGS) 
#           Useful options for debugging:
#           -DQUEX_OPTION_ASSERTS_DISABLED
#           -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED 
#           -DQUEX_OPTION_DEBUG_SHOW

all:   lexer lexer2

lexer: easy.qx 
	quex -i patterns.qx tokens.qx common.qx easy.qx -o Easy
	$(LD) lexer.cpp Easy/Easy.cpp -o $@ 
         
lexer2: easy2.qx 
	quex -i patterns.qx tokens.qx common.qx easy2.qx -o Easy2
	$(LD) -DLEXER2 lexer.cpp Easy2/Easy2.cpp -o $@ 

clean:	
	rm -rf lexer Easy/ Easy2/ *.o tmp.*
