PROGRAMS := push-pop.exe \
	        push-pop-repetition.exe

all:       $(PROGRAMS) 

MYFLAGS   := -ggdb -Wall -Werror  \
		     -I. -I$(QUEX_PATH) \
		     -DQUEX_OPTION_COUNTER_LINE  \
		     -DQUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER \
		     -DQUEX_SETTING_ACCUMULATOR_INITIAL_SIZE=0 \
		     -DQUEX_SETTING_ACCUMULATOR_GRANULARITY_FACTOR=1 \
		     -DQUEX_OPTION_COUNTER_COLUMN 

CC        := gcc  -I../ -I$(QUEX_PATH) -D__QUEX_OPTION_PLAIN_C -I$(HWUT_PATH) -ggdb

%.exe: %.c common_token.c
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

