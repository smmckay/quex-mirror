include ../Makefile.lexer

all:
	quex -i simple.qx --language C --debug-exception -o Simple
	$(LDC) -c Simple/Simple.c -DQUEX_OPTION_DEBUG_SHOW_EXT -DQUEX_OPTION_COUNTER_LINE_EXT -DQUEX_OPTION_COUNTER_COLUMN_EXT 

clean:
	rm -rf Simple* tmp.txt

