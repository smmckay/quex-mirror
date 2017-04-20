include ../Makefile.lexer

all:
	quex -i simple.qx --language C -o Simple 
	$(LDC) point.c Simple.c -o a.out 

clean:
	rm Simple*
	rm a.out
