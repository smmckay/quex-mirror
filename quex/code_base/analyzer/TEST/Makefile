PROGRAMS := statistics.exe # 
# 		counter-column_line.exe \
# 		counter-column_line-indentation.exe \
# 		counter-column_line-indentation-x.exe \
# 		counter-column_line-x.exe

all:       $(PROGRAMS) 

.PHONY: hwut-info
hwut-info: 
	@echo $(PROGRAMS)

MYFLAGS := -ggdb \
	       -Wall -Werror \
	       -I. -I../../TESTS -I$(HWUT_PATH) \
           -DQUEX_OPTION_COUNTER_LINE  \
           -DQUEX_OPTION_COUNTER_COLUMN \
		   -DQUEX_OPTION_ASSERTS

CC = g++ $(MYFLAGS)

counter-%.exe:  counter-%.cpp ut
	$(CC) $< -o $@ 

statistics.exe: statistics.c ut
	gcc $(MYFLAGS) $< -o $@ -D__QUEX_OPTION_PLAIN_C -DQUEX_INLINE= 

nonsense.exe: nonsense.cpp 
	$(CC) $< -o $@ 

ut:
	python ../../TESTS/code_base_instatiation.py ut 

clean: 
	rm -rf $(PROGRAMS) ut

