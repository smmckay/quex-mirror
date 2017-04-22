include ../Makefile.lexer

all: string.qx main.c
	quex -i string.qx common.qx --language C -o ::Lexer --debug-exception
	$(LDC) *.c -o string 

clean:
	rm Lexer* -f
