include ../Makefile.lexer

all: string.qx main.c
	quex --cbm -i string.qx common.qx --language C -o ::Lexer --debug-exception
	$(LDC) *.c Lexer/Lexer.c -o string 

clean:
	rm -rf Lexer* 
