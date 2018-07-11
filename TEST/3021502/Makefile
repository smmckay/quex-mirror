include ../Makefile.lexer

all:
	quex --cbm -i simple.qx --language C -o Simple 
	$(LDC) point.c Simple/Simple.c -o a.out 

clean:
	rm -rf Simple* a.out
