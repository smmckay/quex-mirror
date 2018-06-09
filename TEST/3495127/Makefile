include ../Makefile.lexer

all: Simple/Simple.c 
	@echo "Compiling"
	@$(LDC) Simple/Simple.c lexer.c -DPRINT_TOKEN -ggdb -I$(HWUT_PATH)
		
# -DQUEX_OPTION_DEBUG_SHOW_EXT  

Simple.E: Simple/Simple.c
	$(LDC) -E -I./ -I$(QUEX_PATH) Simple/Simple.c -o Simple.E

Simple/Simple.c: queue.qx
	@echo "Call to quex"
	quex -i queue.qx -o Simple --language C --debug-exception ##
	cat Simple/Simple.c | awk '! /\# *line/' > tmp.c; mv tmp.c Simple/Simple.c

clean:
	rm -rf Simple*
	rm -rf a.out
	# touch test.qx
