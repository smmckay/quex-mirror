include ../Makefile.lexer

all: Simple.c 
	@echo "Compiling"
	@$(LDC) Simple.c lexer.c -DPRINT_TOKEN -ggdb
		
# -DQUEX_OPTION_DEBUG_SHOW  

Simple.E: Simple.c
	$(LDC) -E -I./ -I$(QUEX_PATH) Simple.c -o Simple.E

Simple.c: queue.qx
	@echo "Call to quex"
	quex -i queue.qx -o Simple --language C --debug-exception ##
	cat Simple.c | awk '! /\# *line/' > tmp.c; mv tmp.c Simple.c

clean:
	rm -rf Simple*
	rm -rf a.out
	# touch test.qx
