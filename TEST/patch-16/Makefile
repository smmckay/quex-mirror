include ../Makefile.lexer

CFLAGS:=-Wimplicit
QUEX_PARAMS:=-DQUEX_OPTION_ASSERTS_DISABLED -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 #-DQUEX_OPTION_DEBUG_SHOW

all: simple/simple.c main.c
	$(LDC) -o lexer simple/simple.c main.c

%.E: %.c
	gcc -E -I$(QUEX_PATH) $(QUEX_PARAMS) -I. $(CFLAGS) $< -o $@

simple/simple.c: simple.qx Makefile
	quex -i $< --language C --debug-exception -o simple

clean:
	touch simple.qx
	rm -rf simple *.o lexer

main.o: simple.c
