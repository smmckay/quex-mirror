X = Simple

all: $(X).c 
	@echo "Compiling"
	@gcc -I./ -I$(QUEX_PATH) \
		$(X).c             \
		../lexer.c  \
		-ggdb \
		-DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED \
		`icu-config --ldflags`      \
		-DPRINT_TOKEN 
	   	# -DQUEX_OPTION_DEBUG_SHOW 


$(X).c: simple.qx
	@echo "Call to quex"
	quex -i $< -o $(X) --language C --debug-exception


clean:
	rm -rf $(X)-*
	rm -rf $(X).[ch]
	rm -rf $(X)
	rm -rf a.out
	touch simple.qx
