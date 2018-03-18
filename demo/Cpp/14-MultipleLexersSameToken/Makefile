# PURPOSE: Multiple Lexers same Token
#
# License: MIT; Project http://quex.sourceforge.net
# (C) Frank-Rene Schaefer; FREE OF CHARGE--ABSOLUTELY NO WARRANTY.
#_______________________________________________________________________________
.PHONY:     clean
.SECONDARY:

COMPILER := g++ -pedantic -Wconversion -Wall -Werror -W # -ggdb
LD       := $(COMPILER) -I./ $(ADD_FLAGS) -DQUEX_OPTION_MULTI 
# HINTS:    -DQUEX_OPTION_ASSERTS_DISABLED
#           -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED 
#           -DQUEX_OPTION_DEBUG_SHOW

all: lexer

lexer: max/Lexer.cpp moritz/Lexer.cpp boeck/Lexer.cpp lexer.cpp A_B_C/C-token.cpp
	$(LD) $^ -o  $@ `icu-config --ldflags` 
	 
COMMON_TOKEN_OPTIONS = --token-class-file A_B_C/C-token \
	                   --suppress         0 1 6

max/Lexer.cpp:    max.qx A_B_C/C-token.cpp A_B_C/C-token_ids.h
	quex -i $< -o max::Lexer --odir max -b 4 $(COMMON_TOKEN_OPTIONS) 

moritz/Lexer.cpp: moritz.qx A_B_C/C-token.cpp A_B_C/C-token_ids.h
	quex -i $< -o moritz::Lexer --odir moritz -b 4 $(COMMON_TOKEN_OPTIONS)

boeck/Lexer.cpp:  boeck.qx A_B_C/C-token.cpp A_B_C/C-token_ids.h
	quex -i $< -o boeck::Lexer --odir boeck -b 4 $(COMMON_TOKEN_OPTIONS)

A_B_C/C-token_ids.h \
A_B_C/C-token.cpp: 
	quex -i token_ids.qx                  \
		 -o A::B::C         --odir A_B_C  \
		 --token-class-only               \
		 --token-class      Token         \
		 -b                4              \
		 --token-id-prefix TKN_     

clean:
	rm -rf max/ moritz/ boeck/ A_B_C/ *.o lexer tmp.* 
