# PURPOSE: Multiple Lexers same Token
#
# License: MIT; Project http://quex.sourceforge.net
# (C) Frank-Rene Schaefer; FREE OF CHARGE--ABSOLUTELY NO WARRANTY.
#_______________________________________________________________________________
.PHONY:     clean
.SECONDARY:

COMPILER := gcc -pedantic -Wconversion -Wall -Werror -W # -ggdb
LD       := $(COMPILER) -I./ $(ADD_FLAGS) -DQUEX_OPTION_MULTI 
# HINTS:    -DQUEX_OPTION_ASSERTS_DISABLED
#           -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED 
#           -DQUEX_OPTION_DEBUG_SHOW

all: lexer

lexer: max/Lexer.c moritz/Lexer.c boeck/Lexer.c lexer.c A_B_C/A_B_C-token.c
	$(LD) $^ -o  $@ `icu-config --ldflags` 
	 
COMMON_TOKEN_OPTIONS = --token-class-file A_B_C/A_B_C-token.h \
	                   --suppress         0 1 6

max/Lexer.c:    max.qx A_B_C/A_B_C-token.c A_B_C-token_ids.h
	quex -i $< -o max::Lexer --odir max -b 4 $(COMMON_TOKEN_OPTIONS) --language C 

moritz/Lexer.c: moritz.qx A_B_C/A_B_C-token.c A_B_C-token_ids.h
	quex -i $< -o moritz::Lexer --odir moritz -b 4 $(COMMON_TOKEN_OPTIONS) --language C 

boeck/Lexer.c:  boeck.qx A_B_C/A_B_C-token.c A_B_C-token_ids.h
	quex -i $< -o boeck::Lexer --odir boeck -b 4 $(COMMON_TOKEN_OPTIONS) --language C

A_B_C-token_ids.h \
A_B_C/A_B_C-token.c: 
	quex -i token_ids.qx               \
	     -o ::A_B_C                    \
		 --token-class-only            \
		 --token-class     A_B_C_Token \
		 -b                4           \
		 --token-id-prefix TKN_ --language C 

clean:
	rm -rf max/ moritz/ boeck/ A_B_C/ *.o lexer tmp.* C
