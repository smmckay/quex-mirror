
PROGRAMS = statistics.exe

all:       $(PROGRAMS) 

.PHONY: hwut-info
hwut-info: 
	@echo $(PROGRAMS)

MYFLAGS = \
     -ggdb \
	 -Wall -Werror \
	 -I$(QUEX_PATH) \
     -DQUEX_OPTION_COUNTER_LINE  \
     -DQUEX_OPTION_COUNTER_COLUMN 

CC = g++ $(MYFLAGS)

counter-%.exe:   counter-%.cpp 
	$(CC) -I./. $< -o $@ 

nonsense.exe: nonsense.cpp 
	$(CC) -I./. $< -o $@ 

statistics.exe: statistics.c 
	gcc $(MYFLAGS) -I./. -I$(HWUT_PATH) $< -o $@ \
		-D__QUEX_OPTION_PLAIN_C

%.E:   %.cpp 
	$(CC) -E -I./. $< -o $@ 

clean: 
	rm -f *.o
	rm -f *.E
	rm -f $(PROGRAMS)

