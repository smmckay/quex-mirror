include ../Makefile.lexer

.PHONY: compile-error-list

CPP := $(CPP) $(CFLAGS) 

all: without-include-stack with-include-stack

without-include-stack:
	quex --cbm -i simple.qx -o Simple 
	$(LDCPP) -DQUEX_OPTION_INCLUDE_STACK_DISABLED_EXT lexer.cpp Simple/Simple*.cpp -o lexer

with-include-stack:
	quex --cbm -i simple.qx -o Simple 
	$(LDCPP) lexer.cpp Simple/Simple*.cpp -o lexer

clean:
	rm -rf Simple* *.o lexer 
