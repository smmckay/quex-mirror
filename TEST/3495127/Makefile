include ../Makefile.lexer

all: Simple.c 
	@echo "Compiling"
	@$(LDC) Simple.c lexer.c  \
			-DPRINT_TOKEN                                  \
	        -DQUEX_OPTION_SEND_AFTER_TERMINATION_ADMISSIBLE 
		
# -DQUEX_OPTION_DEBUG_SHOW  

Simple.E: Simple.c
	$(LDC) -E -I./ -I$(QUEX_PATH) Simple.c -o Simple.E

Simple.c: $(TOKEN_POLICY).qx
	@echo "Call to quex"
	quex -i $(TOKEN_POLICY).qx -o Simple --language C --debug-exception --token-policy $(TOKEN_POLICY) ##

clean:
	rm -rf Simple*
	rm -rf a.out
	# touch test.qx
