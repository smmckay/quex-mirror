include ../Makefile.lexer

all:
	quex -i simple.qx --language C --debug-exception -o Simple
	$(LDC) -c Simple/Simple.c -DQUEX_OPTION_DEBUG_SHOW -DQUEX_OPTION_COUNTER_LINE -DQUEX_OPTION_COUNTER_COLUMN 

clean:
	rm -rf Simple* tmp.txt

