# PURPOSE: Makefile Demo Application of Quex
#
# ABSOLUTELY NO WARRANTY
#_______________________________________________________________________________
include ../Makefile.lexer

.PHONY: clean ERROR GOOD

ifndef QUEX_PATH
    $(error The environment variable QUEX_PATH is not defined!)
endif

# (*) SETUP ____________________________________________________________________
# -- INPUT
# -- FILES PRODUCED BY QUEX
#
# (*) COMPILER SETTINGS ________________________________________________________
CPP := $(CPP) $(EXT_CFLAGS) 

# (*) RULES ____________________________________________________________________
all: error good

# -- application
error: ../lexer-simply.cpp 
	@quex -i error.qx -o Simple > tmp.txt 2>&1
	@$(LDCPP) $< Simple.cpp -DPRINT_LINE_COLUMN -o $@ -ggdb

good: ../lexer-simply.cpp 
	@quex -i good.qx -o Simple --debug-exception > tmp.txt 2>&1
	@$(LDCPP) $< Simple.cpp -DPRINT_LINE_COLUMN -o $@ 



# (*) HELPERS __________________________________________________________________
clean:	
	@rm -f $(ENGINE_SOURCES)
	@rm -f Simple*
	@rm -f Good*
	@rm -f lexer.o
	@rm -f lexer
	@rm -f *.bak
	@rm -f tmp.txt
	@rm -f good error
	@echo "clean"

