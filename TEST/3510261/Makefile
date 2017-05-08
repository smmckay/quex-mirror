include ../Makefile.lexer

# Leave the generated code for debugging etc.
.SECONDARY: Simple.c 

test: Simple.o lexer.o
	$(LDC) -o $@ $^ -ggdb

%.o: %.c
	$(CC) -o $@ $< 

%.o: ../%.c
	$(CC) -o $@ $<                 \
		-DPRINT_LINE_COLUMN_NUMBER \
		-DPRINT_TOKEN                  

Simple.c: test.qx
	quex -i $< -o $* --language C --encoding utf8

clean:
	rm -f Simple*
	rm -f test
	rm -f *.o
