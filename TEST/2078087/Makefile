include ../Makefile.lexer

.PHONY: lexer

CFLAGS = \
	 -DQUEX_OPTION_DEBUG_SHOW_MODES \
     -DQUEX_OPTION_COUNTER_LINE_DISABLED \
     -DQUEX_OPTION_COUNTER_COLUMN_DISABLED \
	 #-DQUEX_OPTION_DEBUG_SHOW

lexer:
	quex -i $(INPUT) -o Simple --language C --debug-exception
	$(LDC_ICONV) -DPRINT_TOKEN $(CFLAGS) ../lexer.c Simple*.c -o lexer

lexer.E:
	quex -i $(INPUT) -o Simple --language C --debug-exception
	$(LDC) -I$(QUEX_PATH) -I. -Wall -E $(CFLAGS) ../lexer.c -o lexer.E
