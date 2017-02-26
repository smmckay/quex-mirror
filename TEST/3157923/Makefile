include ../Makefile.lexer

lexer: simple.qx main.c
	quex -i  simple.qx -o Simple --post-categorizer --language C --debug-exception
	$(LDC) main.c Simple.c -o lexer 

clean: 
	rm -f Simple*
	rm -f lexer
