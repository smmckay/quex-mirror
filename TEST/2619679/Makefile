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
# -- INPUT
MODE_FILES       = simple.qx
# -- FILES PRODUCED BY QUEX
ENGINE_NAME      = Simple# NOTE: a whitespace after this name creates chaos!
ENGINE_SOURCES   = $(ENGINE_NAME)                     \
                   $(ENGINE_NAME).cpp                 \
                   $(ENGINE_NAME)-token_ids           \
                   $(ENGINE_NAME)-token               
# -- OUTPUT
APPLICATION      = lexer

# (*) COMPILER SETTINGS ________________________________________________________
#     (change COMPILER to whatever you use as compiler on the command line,
#      e.g. "make COMPILER=icpc" will use intel's c++ compiler)
CCP = $(CPP) -DQUEX_OPTION_ASSERTS_DISABLED 

# (*) RULES ____________________________________________________________________
# -- application
$(APPLICATION): ../lexer-simply.cpp $(ENGINE_NAME).cpp 
	@echo "##"
	@echo "## The issue here was that there were warnings about double defined macros."
	@echo "##"
	$(CPP) -o $(APPLICATION) \
		  ../lexer-simply.cpp $(ENGINE_NAME).cpp 
          
$(ENGINE_SOURCES): $(MODE_FILES) 
	quex -i $(MODE_FILES) -o $(ENGINE_NAME) 

# (*) HELPERS __________________________________________________________________
clean:	
	touch $(MODE_FILES)
	rm -f $(ENGINE_SOURCES)
	rm -f $(ENGINE_NAME).o
	rm -f $(ENGINE_NAME)-configuration
	rm -f lexer.o
	rm -f lexer
	rm -f token_ids
	rm -f *.bak
