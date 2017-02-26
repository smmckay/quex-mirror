include ../Makefile.lexer

all:
	quex -i error.qx -o Simple --debug-exception
	$(LDCPP) *.cpp ../lexer-simply.cpp -o the_test 

Simple.E:
	g++ -E -I$(QUEX_PATH) -I. Simple.cpp > $@ 

clean:
	rm -f Simple*
	rm -f the_test

