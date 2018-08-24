PROGRAMS := push-pop.exe \
	        push-pop-repetition.exe

all:       $(PROGRAMS) 

MYFLAGS   := -ggdb -Wall -Werror  \
		     -I. -I../../TESTS -I$(HWUT_PATH) \
		     -DQUEX_SETTING_ACCUMULATOR_INITIAL_SIZE_EXT=0 \
		     -DQUEX_SETTING_ACCUMULATOR_GRANULARITY_FACTOR_EXT=1 \
		     -DQUEX_OPTION_COUNTER_LINE_EXT  \
		     -DQUEX_OPTION_COUNTER_COLUMN_EXT \
			 -DQUEX_INDICATE_CONFIGURATION_FILE_PASSED \
		     -DQUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER_EXT \
			 -DQUEX_TKN_TERMINATION \
			 -DQUEX_OPTION_PLAIN_C_EXT 

CC        := gcc  -ggdb $(MYFLAGS)

%.exe: %.c common_token.c ut
	$(CC) $< common_token.c -o $@ 

%.E:   %.cpp 
	$(CC) -E -I./. $< -o $@ 

clean: 
	rm -rf *.o *.E tmp.* tmp_dir/* $(PROGRAMS) ut

ut:
	python ../../TESTS/code_base_instatiation.py ut token quex --lang-C

.PHONY: hwut-info
hwut-info: 
	@echo $(PROGRAMS)

