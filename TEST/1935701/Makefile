include ../Makefile.lexer

TEST_FILES = bug-1935701.exe


DEBUGF = -ggdb -DQUEX_OPTION_UNIT_TEST_EXT 
TESTENV := ../../quex/code_base/TESTS

INCLUDES = -I./ -I. -I$(TESTENV)

OPTF   = # -Os
FLAGS  = #-lefence

all: $(TEST_FILES) 

hwut-info:
	@echo $(TEST_FILES) 

%.exe: %.cpp ut 
	$(LDCPP) $(INCLUDES) $(DEBUGF) $(OPTF) $< -o $@

ut:
	python $(TESTENV)/code_base_instatiation.py ut

clean:
	rm -rf $(TEST_FILES) ut
	rm -f *.o
