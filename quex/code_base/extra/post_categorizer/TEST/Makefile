
PROGRAMS = \
		   post-categorizer-enter.exe \
		   post-categorizer-remove.exe \
		   post-categorizer-remove-2.exe \
		   post-categorizer-remove-total.exe \
		   post-categorizer-find.exe 

all:       $(PROGRAMS) 

.PHONY: hwut-info
hwut-info: 
	@echo $(PROGRAMS)

MYFLAGS = \
     -ggdb \
	 -Wall -Werror \
	 -I. -I../../../TESTS \
     -DQUEX_OPTION_COUNTER_LINE  \
     -DQUEX_OPTION_COUNTER_COLUMN 

CC = g++ $(MYFLAGS)

post-categorizer-%.exe: post-categorizer-%.cpp ut
	$(CC) -I./. $< post-categorizer-common.cpp -o $@ 

ut:
	python ../../../TESTS/code_base_instatiation.py ut 

clean: 
	rm -rf $(PROGRAMS) ut *.o *.E

