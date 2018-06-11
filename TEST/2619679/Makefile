# PURPOSE: Makefile Demo Application of Quex
#
# ABSOLUTELY NO WARRANTY
#_______________________________________________________________________________
include ../Makefile.lexer

.PHONY: clean

ifndef QUEX_PATH
    $(error The environment variable QUEX_PATH is not defined!)
endif


# (*) SETUP ____________________________________________________________________
MODE_FILES       = simple.qx
APPLICATION      = lexer

# (*) COMPILER SETTINGS ________________________________________________________
#     (change COMPILER to whatever you use as compiler on the command line,
#      e.g. "make COMPILER=icpc" will use intel's c++ compiler)

# (*) RULES ____________________________________________________________________
# -- application
$(APPLICATION): ../lexer-simply.cpp Simple/Simple.cpp 
	@echo "##"
	@echo "## The issue here was that there were warnings about double defined macros."
	@echo "##"
	$(LDCPP) -DQUEX_OPTION_ASSERTS_EXT_DISABLED_EXT -o $(APPLICATION) \
		  ../lexer-simply.cpp Simple/Simple.cpp 
          
Simple/Simple.cpp: $(MODE_FILES) 
	quex -i $(MODE_FILES) -o Simple

# (*) HELPERS __________________________________________________________________
clean:	
	touch $(MODE_FILES)
	rm -rf Simple lexer.o lexer token_ids *.bak
