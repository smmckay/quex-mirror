include ../Makefile.lexer

# -DQUEX_OPTION_DEBUG_SHOW_EXT 
#
all: Simple/Simple.c 
	@echo "Compiling"
	@$(LDC_ICU) Simple/Simple.c ../lexer.c  $(LIB_ICU) -DPRINT_TOKEN 

Simple/Simple.c: simple.qx
	@echo "Call to quex"
	quex -i $< -o Simple --language C --debug-exception


clean:
	rm -rf Simple* a.out
	touch simple.qx
