include ../Makefile.lexer

lexer: simple.qx main.c
	quex --cbm -i  simple.qx common.qx -o Simple --language C --debug-exception
	$(LDC) -I. main.c Simple/Simple.c -o lexer 

clean: 
	rm -rf Simple* lexer
