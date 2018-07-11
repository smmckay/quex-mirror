include ../Makefile.lexer

lexer: 
	quex --cbm -i error-$(CASE).qx -o Simple 
	$(LDCPP) -DQUEX_SETTING_BUFFER_SIZE_EXT=11 ../lexer.cpp Simple/Simple.cpp -o lexer # -DQUEX_OPTION_DEBUG_SHOW_EXT -DQUEX_SETTING_DEBUG_OUTPUT_CHANNEL_EXT=stdout -ggdb

Simple.E:
	g++ -c -E -I$(QUEX_PATH) -I. \
		-DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT \
		Simple.h -o $@

clean: 
	rm -f *.o
	rm -rf Simple*
	rm -f lexer
