# Two lines to generate and compile the lexer:

all: lexer

tiny.cpp: tiny.qx
	# (1) Generate the lexical analyzer
	quex -i tiny.qx -o tiny

lexer: lexer.cpp tiny.cpp
	# (2) Compile the lexical analyzer
	g++ lexer.cpp tiny.cpp -I$(QUEX_PATH) \
		-Wall -Werror -o lexer 

clean:
	rm -f lexer \
		  tiny tiny-configuration tiny.cpp \
		  tiny-token tiny-token_ids
