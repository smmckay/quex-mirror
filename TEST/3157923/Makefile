include ../Makefile.lexer

lexer: simple.qx main.c
	quex -i  simple.qx common.qx -o Simple --language C --debug-exception
	$(LDC) main.c Simple/Simple.c -o lexer 

clean: 
	rm -f Simple*
	rm -f lexer
