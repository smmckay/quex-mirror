PROGRAMS := accumulator.exe 

all:       $(PROGRAMS) 

MYFLAGS := -ggdb -Wall -Werror  \
		   -I$(QUEX_PATH) \
		   -DQUEX_OPTION_LINE_NUMBER_COUNTING  \
		   -DQUEX_OPTION_COLUMN_NUMBER_COUNTING 

CC      := g++ $(MYFLAGS)

DUMMY   := $(QUEX_PATH)/quex/code_base/extra/test_environment/TestAnalyzer-dummy.cpp

accumulator.exe: accumulator.cpp $(DUMMY)
	$(CC) -I./. $^ -o $@ 

%.E:   %.cpp 
	$(CC) -E -I./. $< -o $@ 

clean: 
	rm -f *.o
	rm -f *.E
	rm -f $(PROGRAMS)

.PHONY: hwut-info
hwut-info: 
	@echo $(PROGRAMS)

