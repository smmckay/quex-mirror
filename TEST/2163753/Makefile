include ../Makefile.lexer
X = Simple

# -DQUEX_OPTION_DEBUG_SHOW 
#
all: $(X).c 
	@echo "Compiling"
	@$(LDC_ICU) $(X).c ../lexer.c  $(LIB_ICU) -DPRINT_TOKEN 

$(X).c: simple.qx
	@echo "Call to quex"
	quex -i $< -o $(X) --language C --debug-exception


clean:
	rm -rf $(X)-*
	rm -rf $(X).[ch]
	rm -rf $(X)
	rm -rf a.out
	touch simple.qx
