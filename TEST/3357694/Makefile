include ../Makefile.lexer
.PHONY: SOURCES

ICU_LFLAGS=$(shell icu-config --ldflags)

test: lexer.o Simple.o
	$(LDC_ICU) -o $@ $^ $(ICU_LFLAGS)

lexer.o: ../lexer.c Simple/Simple.c
	$(CC_ICU) -o $@ -DPRINT_TOKEN $< 

Simple.o: Simple/Simple.c 
	$(CC) -o $@ $< 

Simple/Simple.c: 
	quex -b 2 -i test.qx -o Simple --language C $(ADD_OPTION) --debug-exception

clean:
	rm -rf Simple* *.o test
