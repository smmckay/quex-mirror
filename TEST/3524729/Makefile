all lexer: Lexer-token
	@echo Compile -- No output is good output ________________________________
	g++ -I. Lexer/Lexer-token.cpp -c 2>&1

Lexer-token:
	@echo Generate token class _______________________________________________
	quex --cbm -i token_type.qx --token-class-only --debug-exception

clean:
	rm -rf Lexer* tmp.txt

