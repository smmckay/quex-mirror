include ../Makefile.lexer

.PHONY: compile-error-list

CPP := $(CPP) $(CFLAGS) 

without-include-stack:
	quex -i simple.qx -o Simple 
	$(LDCPP) -DQUEX_OPTION_INCLUDE_STACK_DISABLED lexer.cpp Simple*.cpp -o lexer

with-include-stack:
	quex -i simple.qx -o Simple 
	$(LDCPP) lexer.cpp Simple*.cpp -o lexer

clean:
	rm -f Simple*
	rm -f *.o
	rm -f lexer error-lexer
