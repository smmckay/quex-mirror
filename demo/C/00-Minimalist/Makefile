# Two lines to generate and compile the lexer:

all: lexer

tiny.c: tiny.qx
	# (1) Generate the lexical analyzer
	quex -i tiny.qx -o tiny --language C

lexer: lexer.c tiny.c
	# (2) Compile the lexical analyzer
	gcc lexer.c tiny.c -I$(QUEX_PATH) \
		-Wall -Werror -o lexer 

clean:
	rm -f lexer \
		  tiny.h tiny-configuration.h tiny.c \
		  tiny-token.h tiny-token_ids.h
