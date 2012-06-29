Cpp: ./lexer tiny_lexer.cpp
	g++ -Wall -fexceptions -DQUEX_SETTING_BUFFER_SIZE=0 -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 -DQUEX_TYPE_CHARACTER=char -DQUEX_OPTION_TERMINATION_ZERO_DISABLED -g -DQUEX_OPTION_ASSERTS_DISABLED -Ilexer -c lexer/tiny_lexer.cpp -o tiny_lexer.o
	@echo Compiling Done

C: ./lexer tiny_lexer.c
	gcc -Wall -fexceptions -DQUEX_SETTING_BUFFER_SIZE=0 -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 -DQUEX_TYPE_CHARACTER=char -DQUEX_OPTION_TERMINATION_ZERO_DISABLED -g -DQUEX_OPTION_ASSERTS_DISABLED -Ilexer -c lexer/tiny_lexer.c -o tiny_lexer.o
	@echo Compiling Done


./lexer:
	@mkdir -p ./lexer # Do not trigger error if it exists '-p' does that too.

tiny_lexer.cpp:
	quex -i cpp.qx --engine tiny_lexer --buffer-based --token-policy single --token-memory-management-by-user --token-id-offset 2 --token-id-prefix TKN_ --source-package lexer
	@echo Code Generation Done


tiny_lexer.c:
	quex -i cpp.qx --engine tiny_lexer --buffer-based --token-policy single --token-memory-management-by-user --token-id-offset 2 --token-id-prefix TKN_ --source-package lexer --language C
	@echo Code Generation Done

clean: 
	rm -rf ./lexer
	rm -f ./tiny_lexer.o