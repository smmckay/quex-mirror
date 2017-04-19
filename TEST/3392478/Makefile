include ../Makefile.lexer

# Leave the generated code for debugging etc.
.SECONDARY: Simple.c 

test: Simple.o lexer.o
	$(LDC) $^ -o $@ 

%.o: %.c
	$(CC) -o $@ -I$(QUEX_PATH) -I. $<                 

%.o: ../%.c
	$(CC) -o $@ -I$(QUEX_PATH) -I. $< \
		-DPRINT_LINE_COLUMN_NUMBER    \
		-DPRINT_TOKEN                  

Simple.c: test.qx
	$(QUEX_PATH)/quex-exe.py \
		                     --codec utf8          \
							 -b 1                  \
							 -i $<                 \
							 -o $*                 \
							 --language C --debug-exception

clean:
	rm -f Simple*
	rm -f test
	rm -f *.o
