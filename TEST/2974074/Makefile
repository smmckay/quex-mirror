include ../Makefile.lexer

all:
	quex -i error.qx -o Simple --debug-exception
	$(LDCPP) Simple/*.cpp ../lexer-simply.cpp -o the_test 

clean:
	rm -rf Simple*
	rm -f the_test

