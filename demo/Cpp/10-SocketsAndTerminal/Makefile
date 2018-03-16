# PURPOSE: Sockets and Terminal Applications
#
# License: MIT; Project http://quex.sourceforge.net
# (C) Frank-Rene Schaefer; FREE OF CHARGE--ABSOLUTELY NO WARRANTY.
#_______________________________________________________________________________
.PHONY: clean
.SECONDARY:

COMPILER := g++ -ggdb -pedantic -Wconversion -Wall -Werror -W
LD       := $(COMPILER) -I./ $(ADD_FLAGS) 
#           Useful options for debugging:
#           -DQUEX_OPTION_ASSERTS_DISABLED
#           -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED 
#           -DQUEX_OPTION_DEBUG_SHOW

FILES := lexer-command-line lexer-command-line-utf8 \
	     lexer-stdin        lexer-stdin-utf8        \
	     lexer-socket       lexer-socket-utf8       \
	     feed-socket

all: $(FILES)

lexer-socket:            lexer-socket.cpp       lex_ascii/LexAscii.cpp 
	$(LD) -o $@  $^                  

lexer-stdin:             lexer-stdin.cpp        lex_ascii/LexAscii.cpp
	$(LD) -o $@  $^

lexer-command-line:      lexer-command-line.cpp lex_ascii/LexAscii.cpp
	$(LD) -o $@  $^

feed-socket:             feed-socket.cpp
	$(LD) -o $@  $^                  
                                     
lexer-socket-utf8:       lexer-socket.cpp       lex_utf8/LexUtf8.cpp 
	$(LD) -DWITH_UTF8 -o $@  $^                  

lexer-stdin-utf8:        lexer-stdin.cpp        lex_utf8/LexUtf8.cpp
	$(LD) -DWITH_UTF8 -o $@  $^
          
lexer-command-line-utf8: lexer-command-line.cpp lex_utf8/LexUtf8.cpp
	$(LD) -DWITH_UTF8 -o $@  $^
          
lex_utf8/LexUtf8.cpp:    utf8.qx 
	quex -i utf8.qx -o LexUtf8 --bet wchar_t --odir lex_utf8
		 
lex_ascii/LexAscii.cpp:  ascii.qx 
	quex -i ascii.qx -o LexAscii --odir lex_ascii
		 
clean:	
	rm -rf lex_ascii/ lex_utf8/ *.o $(FILES) tmp.*
