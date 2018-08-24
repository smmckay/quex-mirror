
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
	 -I. -I../../../TESTS -I../../../\
	 -DQUEX_TestAnalyzer_SETTING_USER_CLASS_DECLARATION_EPILOG_EXT= \
     -DQUEX_OPTION_COUNTER_LINE_EXT  \
	 -DQUEX_OPTION_ASSERTS \
     -DQUEX_OPTION_COUNTER_COLUMN_EXT \
     -DQUEX_TKN_TERMINATION=0 

CC = g++ $(MYFLAGS) -DQUEX_INLINE=inline

post-categorizer-%.exe: post-categorizer-%.cpp 
	$(CC) -I./. $< post-categorizer-common.cpp -o $@ 

post-categorizer-%.E: post-categorizer-%.cpp 
	$(CC) -I./. $< post-categorizer-common.cpp -E > $@ 

clean: 
	rm -rf $(PROGRAMS) *.o *.E


