
PROGRAMS = \
		   post-categorizer-enter.exe \
		   post-categorizer-remove.exe \
		   post-categorizer-remove-2.exe \
		   post-categorizer-remove-total.exe \
		   post-categorizer-find.exe 

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

post-categorizer-%.exe:   post-categorizer-%.cpp 
	$(CC) -I./. $< post-categorizer-common.cpp -o $@ 

%.E:   %.cpp 
	$(CC) -E -I./. $< -o $@ 

clean: 
	rm -f *.o
	rm -f *.E
	rm -f $(PROGRAMS)

