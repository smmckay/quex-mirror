include ../Makefile.lexer

CFLAGS:=-Wimplicit
QUEX_PARAMS:=-DQUEX_OPTION_ASSERTS_EXT_DISABLED_EXT -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N_EXT=0 #-DQUEX_OPTION_DEBUG_SHOW_EXT

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
