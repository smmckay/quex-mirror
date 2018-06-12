PROGRAMS := accumulator.exe 

all:       $(PROGRAMS) 

TESTENV   := $(QUEX_PATH)/quex/code_base/TESTS

MYFLAGS   := -ggdb -Wall -Werror  \
		     -I. \
		     -DQUEX_OPTION_COUNTER_LINE_EXT  \
		     -DQUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER_EXT \
		     -DQUEX_SETTING_ACCUMULATOR_INITIAL_SIZE_EXT=0 \
		     -DQUEX_SETTING_ACCUMULATOR_GRANULARITY_FACTOR_EXT=1 \
		     -DQUEX_OPTION_COUNTER_COLUMN_EXT 
		     -DQUEX_TYPE_LEXATOM_EXT=char 
             # -DQUEX_OPTION_TOKEN_TAKE_TEXT_SUPPORT_EXT  default with TestAnalyzer

CC        := g++ $(MYFLAGS) -ggdb -DQUEX_INLINE=inline

test_cpp/TestAnalyzer-dummy.cpp: test_cpp
	mkdir -p test_cpp
	cp $(TESTENV)/test_cpp/TestAnalyzer* ./test_cpp
	
	# Remove the inclusion of converter helpers
	# cat tmp_dir/TestAnalyzer-token | awk 'BEGIN{ bad=0; } /define *__QUEX_INCLUDE_GUARD__CONVERTER_HELPER__TMP_DISABLED/ { bad=1; } { if( ! bad ) { print; } } /undef *__QUEX_INCLUDE_GUARD__CONVERTER_HELPER__TMP_DISABLED/ { bad=0; } ' > code.tmp
	# mv code.tmp tmp_dir/TestAnalyzer-token

	# Remove 'C' versions of the TestAnalyzer
	find ./test_cpp -name "TestAnalyzer*.[ch]" -delete

	# Generate a 'TestAnalyzer-token' class just for the experiment
	# => print out on 'take_text'
	quex -i UT_Token.qx --token-class-only -o TestAnalyzer --odir test_cpp

accumulator.exe: accumulator.cpp test_cpp/TestAnalyzer-dummy.cpp
	$(CC) $^ -o $@ 

%.E:   %.cpp 
	$(CC) -E -I./. $< -o $@ 

test_cpp:
	python $(TESTENV)/code_base_instatiation.py test_cpp
	quex --co -o TestAnalyzer --odir test_cpp --encoding unicode --bet char --csn lexeme

clean: 
	rm -rf *.o *.E tmp.* test_cpp $(PROGRAMS)

.PHONY: hwut-info
hwut-info: 
	@echo $(PROGRAMS)

