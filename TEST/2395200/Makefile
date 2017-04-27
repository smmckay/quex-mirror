include ../Makefile.lexer

.PHONY: lexer error-lexer

CFLAGS = \
	 -DQUEX_OPTION_DEBUG_SHOW_MODES                \
     -DQUEX_OPTION_COUNTER_LINE_DISABLED   \
     -DQUEX_OPTION_COUNTER_COLUMN_DISABLED \
	 -DQUEX_SETTING_BUFFER_SIZE=128                \
	 -DSTRANGE_STREAM                              \
     -D__QUEX_OPTION_UNIT_TEST
	 #-DQUEX_OPTION_DEBUG_SHOW

lexer:
	quex -i simple.qx -o Simple --debug-exception
	$(LDCPP) $(CFLAGS) ../lexer-simply.cpp Simple.cpp -o lexer

clean:
	rm -f Simple*
	rm -f *.o
	rm -f lexer error-lexer
