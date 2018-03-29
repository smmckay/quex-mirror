PROGRAMS := accumulator.exe 

all:       $(PROGRAMS) 

TESTENV   := $(QUEX_PATH)/quex/code_base/TESTS

MYFLAGS   := -ggdb -Wall -Werror  \
		     -I. \
		     -DQUEX_OPTION_COUNTER_LINE  \
		     -DQUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER \
		     -DQUEX_SETTING_ACCUMULATOR_INITIAL_SIZE=0 \
		     -DQUEX_SETTING_ACCUMULATOR_GRANULARITY_FACTOR=1 \
		     -DQUEX_OPTION_COUNTER_COLUMN \
             -DQUEX_OPTION_TOKEN_TAKE_TEXT_SUPPORT

CC        := g++ $(MYFLAGS) -ggdb

test_environment/TestAnalyzer-dummy.cpp: test_environment
	cp $(TESTENV)/test_environment/TestAnalyzer* ./test_environment
	
	# Remove the inclusion of converter helpers
	# cat tmp_dir/TestAnalyzer-token | awk 'BEGIN{ bad=0; } /define *__QUEX_INCLUDE_GUARD__CONVERTER_HELPER__TMP_DISABLED/ { bad=1; } { if( ! bad ) { print; } } /undef *__QUEX_INCLUDE_GUARD__CONVERTER_HELPER__TMP_DISABLED/ { bad=0; } ' > code.tmp
	# mv code.tmp tmp_dir/TestAnalyzer-token

	# Remove 'C' versions of the TestAnalyzer
	find ./test_environment -name "TestAnalyzer*.[ch]" -delete

	# Generate a 'TestAnalyzer-token' class just for the experiment
	# => print out on 'take_text'
	quex -i UT_Token.qx --token-class-only -o TestAnalyzer --odir test_environment

accumulator.exe: accumulator.cpp test_environment/TestAnalyzer-dummy.cpp
	$(CC) $^ -o $@ 

%.E:   %.cpp 
	$(CC) -E -I./. $< -o $@ 

test_environment:
	python $(TESTENV)/code_base_instatiation.py test_environment

clean: 
	rm -rf *.o *.E tmp.* test_environment $(PROGRAMS)

.PHONY: hwut-info
hwut-info: 
	@echo $(PROGRAMS)

