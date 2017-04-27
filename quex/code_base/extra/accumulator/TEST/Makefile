PROGRAMS := accumulator.exe 

all:       $(PROGRAMS) 

MYFLAGS   := -ggdb -Wall -Werror  \
		     -I. -I$(QUEX_PATH) \
		     -DQUEX_OPTION_COUNTER_LINE  \
		     -DQUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER \
		     -DQUEX_SETTING_ACCUMULATOR_INITIAL_SIZE=0 \
		     -DQUEX_SETTING_ACCUMULATOR_GRANULARITY_FACTOR=1 \
		     -DQUEX_OPTION_COUNTER_COLUMN 

CC        := g++ $(MYFLAGS)

DUMMY_CPP := ./tmp_dir/TestAnalyzer-dummy.cpp

$(DUMMY_CPP):
	cp $(QUEX_PATH)/quex/code_base/extra/test_environment/TestAnalyzer* ./tmp_dir
	
	# Remove the inclusion of converter helpers
	# cat tmp_dir/TestAnalyzer-token | awk 'BEGIN{ bad=0; } /define *__QUEX_INCLUDE_GUARD__CONVERTER_HELPER__TMP_DISABLED/ { bad=1; } { if( ! bad ) { print; } } /undef *__QUEX_INCLUDE_GUARD__CONVERTER_HELPER__TMP_DISABLED/ { bad=0; } ' > code.tmp
	# mv code.tmp tmp_dir/TestAnalyzer-token

	# Remove 'C' versions of the TestAnalyzer
	find ./tmp_dir -name "TestAnalyzer*.[ch]" -delete

	# Generate a 'TestAnalyzer-token' class just for the experiment
	# => print out on 'take_text'
	quex -i TokenCpp.qx --token-class-only -o TestAnalyzer --odir ./tmp_dir

accumulator.exe: accumulator.cpp $(DUMMY_CPP)
	$(CC) $^ -o $@ 

%.E:   %.cpp 
	$(CC) -E -I./. $< -o $@ 

clean: 
	rm -f *.o
	rm -f *.E tmp.*
	rm -f tmp_dir/*
	rm -f $(PROGRAMS)

.PHONY: hwut-info
hwut-info: 
	@echo $(PROGRAMS)

