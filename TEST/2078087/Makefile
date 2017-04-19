include ../Makefile.lexer

.PHONY: lexer

CFLAGS = \
	 -DQUEX_OPTION_DEBUG_SHOW_MODES \
     -DQUEX_OPTION_LINE_NUMBER_COUNTING_DISABLED \
     -DQUEX_OPTION_COLUMN_NUMBER_COUNTING_DISABLED \
	 #-DQUEX_OPTION_DEBUG_SHOW

lexer:
	quex -i $(INPUT) -o Simple --language C --debug-exception
	$(LDC_ICONV) -DPRINT_TOKEN $(CFLAGS) ../lexer.c Simple*.c -o lexer

lexer.E:
	quex -i $(INPUT) -o Simple --language C --debug-exception
	$(LDC) -I$(QUEX_PATH) -I. -Wall -E $(CFLAGS) ../lexer.c -o lexer.E
