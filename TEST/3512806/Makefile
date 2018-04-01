include ../Makefile.lexer

all: Cpp C

Cpp: lexer/tiny_lexer.cpp
	$(LDCPP) -fexceptions -DQUEX_SETTING_BUFFER_SIZE=0 -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 \
		     -DQUEX_TYPE_LEXATOM='unsigned char' -DQUEX_OPTION_TERMINATION_ZERO_DISABLED -g \
			 -DQUEX_OPTION_ASSERTS_DISABLED \
		     -Ilexer -c lexer/tiny_lexer.cpp -o tiny_lexer.o
	@echo Compiling Done

C:   lexer/tiny_lexer.c
	$(LDC) -fexceptions -DQUEX_SETTING_BUFFER_SIZE=0 -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 \
		   -DQUEX_TYPE_LEXATOM='unsigned char' -DQUEX_OPTION_TERMINATION_ZERO_DISABLED -g \
		   -DQUEX_OPTION_ASSERTS_DISABLED \
		   -Ilexer -c lexer/tiny_lexer.c -o tiny_lexer.o 
	@echo Compiling Done


lexer/tiny_lexer.cpp: 
	quex -i cpp.qx -o tiny_lexer --odir lexer \
		 --token-id-offset 2 --token-id-prefix TKN_ \
		 --debug-exception
	@echo Code Generation Done


lexer/tiny_lexer.c: 
	quex -i cpp.qx -o tiny_lexer --odir lexer \
		 --token-id-offset 2 --token-id-prefix TKN_ \
		 --language C --debug-exception
	@echo Code Generation Done

clean: 
	rm -rf ./lexer ./tiny_lexer*
