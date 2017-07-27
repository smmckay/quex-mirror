# PURPOSE: Makefile Demo Application of Quex
#
# ABSOLUTELY NO WARRANTY
#_______________________________________________________________________________
include ../Makefile.lexer
.PHONY: clean

a.out: Simple.cpp
	$(LDCPP)  point.cpp Simple.cpp -I. -I$(QUEX_PATH)

Simple.cpp:
	quex -i simple.qx -o Simple --debug-exception 

clean:
	rm -rf Simple* *.o *.exe tmp.* *~

