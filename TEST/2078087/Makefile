include ../Makefile.lexer

.PHONY: lexer

CFLAGS = \
	 -DQUEX_OPTION_DEBUG_SHOW_MODES_EXT \
	 #-DQUEX_OPTION_DEBUG_SHOW_EXT

lexer:
	quex --cbm -i $(INPUT) -o Simple --language C --debug-exception --no-count-lines --no-count-columns 
	$(LDC_ICONV) -DPRINT_TOKEN $(CFLAGS) ../lexer.c Simple/Simple.c -o lexer

lexer.E:
	quex --cbm -i $(INPUT) -o Simple --language C --debug-exception --no-count-lines --no-count-columns
	$(LDC) -I$(QUEX_PATH) -I. -Wall -E $(CFLAGS) ../lexer.c -o lexer.E

clean:
	@rm -rf Simple *.o tmp*.txt lexer
