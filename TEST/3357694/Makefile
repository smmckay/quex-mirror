include ../Makefile.lexer
.PHONY: SOURCES

ICU_LFLAGS=$(shell icu-config --ldflags)

test: lexer.o Simple.o
	$(LDC_ICU) -o $@ $^ $(ICU_LFLAGS)

lexer.o: ../lexer.c SOURCES
	$(CC_ICU) -o $@ -DPRINT_TOKEN $< 

Simple.o: Simple.c SOURCES
	$(CC) -o $@ $< 

Simple \
Simple.cpp: SOURCES

SOURCES: 
	quex -b 2 -i test.qx -o Simple --language C $(ADD_OPTION) --debug-exception

clean:
	rm -f Simple*
	rm -f *.o
	rm -f test
