include ../Makefile.lexer

.PHONY: lexer error-lexer

CFLAGS = \
	 -DQUEX_OPTION_DEBUG_SHOW_MODES_EXT  \
	 -DQUEX_SETTING_BUFFER_SIZE_EXT=128  \
	 -DSTRANGE_STREAM                \
     -DQUEX_OPTION_UNIT_TEST_EXT
	 #-DQUEX_OPTION_DEBUG_SHOW_EXT

lexer:
	quex --cbm -i simple.qx -o Simple --debug-exception --no-count-lines no-count-columns
	$(LDCPP) $(CFLAGS) ../lexer-simply.cpp Simple/Simple.cpp -o lexer

clean:
	rm -rf Simple* *.o lexer error-lexer
