PROGRAMS := push-pop.exe \
	        push-pop-repetition.exe

all:       $(PROGRAMS) 

MYFLAGS   := -ggdb -Wall -Werror  \
		     -I. \
		     -DQUEX_OPTION_COUNTER_LINE  \
		     -DQUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER \
		     -DQUEX_SETTING_ACCUMULATOR_INITIAL_SIZE=0 \
		     -DQUEX_SETTING_ACCUMULATOR_GRANULARITY_FACTOR=1 \
		     -DQUEX_OPTION_COUNTER_COLUMN \
			 -DQUEX_OPTION_ASSERTS \
			 -DQUEX_TKN_TERMINATION

CC        := gcc  -I../ -I. -DQUEX_OPTION_PLAIN_C -I$(HWUT_PATH) -ggdb $(MYFLAGS)

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

