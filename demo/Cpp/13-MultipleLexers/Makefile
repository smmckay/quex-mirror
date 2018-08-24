# PURPOSE: Multiple Lexers
#
# License: MIT; Project http://quex.sourceforge.net
# (C) Frank-Rene Schaefer; FREE OF CHARGE--ABSOLUTELY NO WARRANTY.
#_______________________________________________________________________________
.PHONY: clean
.SECONDARY:

COMPILER := g++ -pedantic -Wconversion -Wall -Werror -W
LD       := $(COMPILER) -I./ $(ADD_FLAGS) 
# HINTS:    -DQUEX_OPTION_ASSERTS_DISABLED_EXT
#           -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT 
#           -DQUEX_OPTION_DEBUG_SHOW_EXT

lexer: lexer.cpp max/Lexer.cpp moritz/Lexer.cpp boeck/Lexer.cpp
	$(LD) $^ -o $@ 
	 
max/Lexer.cpp:    max.qx
	quex -i token.qx $< -o max::Lexer --odir max/ -b 4 \
	     --token-id-prefix MAX_TKN_ --suppress 6 --no-lib-quex

moritz/Lexer.cpp: moritz.qx
	quex -i token.qx $< -o moritz::Lexer --odir moritz/ -b 2 \
		 --token-id-prefix MORITZ_TKN_ --suppress 6 --no-lib-quex

boeck/Lexer.cpp:  boeck.qx
	quex -i token.qx $< -o boeck::Lexer --odir boeck/ --encoding utf8 \
		 --token-id-prefix TKN_ --suppress 6 # for once: lib-quex

clean:
	rm -rf max/ moritz/ boeck/ *.o lexer tmp.*
