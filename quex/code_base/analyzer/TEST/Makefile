PROGRAMS := statistics.exe \
			counter-column_line.exe \
			counter-column_line-indentation.exe \
			counter-column_line-indentation-x.exe \
			counter-column_line-x.exe

all:       $(PROGRAMS) 

.PHONY: hwut-info
hwut-info: 
	@echo $(PROGRAMS)

MYFLAGS = \
     -ggdb \
	 -Wall -Werror \
	 -I. -I../../TESTS \
     -DQUEX_OPTION_COUNTER_LINE  \
     -DQUEX_OPTION_COUNTER_COLUMN 

CC = g++ $(MYFLAGS)

counter-%.exe:   counter-%.cpp ut
	$(CC) $< -o $@ 

statistics.exe: statistics.c ut
	gcc $(MYFLAGS) -I$(HWUT_PATH) $< -o $@ -D__QUEX_OPTION_PLAIN_C

nonsense.exe: nonsense.cpp 
	$(CC) $< -o $@ 

ut:
	python ../../TESTS/code_base_instatiation.py ut analyzer compatibility

clean: 
	rm -rf $(PROGRAMS) ut

