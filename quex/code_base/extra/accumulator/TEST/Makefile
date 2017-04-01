PROGRAMS := accumulator.exe 

all:       $(PROGRAMS) 

MYFLAGS := -ggdb -Wall -Werror  \
		   -I. -I$(QUEX_PATH) \
		   -DQUEX_OPTION_LINE_NUMBER_COUNTING  \
		   -DQUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER \
		   -DQUEX_SETTING_ACCUMULATOR_INITIAL_SIZE=0 \
		   -DQUEX_SETTING_ACCUMULATOR_GRANULARITY_FACTOR=1 \
		   -DQUEX_OPTION_COLUMN_NUMBER_COUNTING 

CC      := g++ $(MYFLAGS)

DUMMY   := $(QUEX_PATH)/quex/code_base/extra/test_environment/TestAnalyzer-dummy.cpp

TestAnalyzer-token:
	# Generate a 'TestAnalyzer-token' class just for the experiment
	# => print out on 'take_text'
	quex -i TokenCpp.qx --token-class-only -o TestAnalyzer

accumulator.exe: accumulator.cpp $(DUMMY)
	$(CC) $^ -o $@ 

%.E:   %.cpp 
	$(CC) -E -I./. $< -o $@ 

clean: 
	rm -f *.o
	rm -f *.E
	rm -f TestAnalyzer-token*
	rm -f $(PROGRAMS)

.PHONY: hwut-info
hwut-info: 
	@echo $(PROGRAMS)

