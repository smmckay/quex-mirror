# PURPOSE: Makefile Demo Application of Quex
#
# ABSOLUTELY NO WARRANTY
#_______________________________________________________________________________
include ../Makefile.lexer
.PHONY: clean

ifndef QUEX_PATH
    $(error The environment variable QUEX_PATH is not defined!)
endif


CPP := $(CPP) \
	 -DPRINT_TOKEN                                   \
	 -DPRINT_LINE_COLUMN_NUMBER
     # -DQUEX_OPTION_ASSERTS_DISABLED
     # -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED 
     # -DQUEX_OPTION_DEBUG_SHOW
   
# (*) RULES ____________________________________________________________________
# -- application
lexer:          example.o EasyLexer.o
	$(LDCPP) -o $@ example.o EasyLexer.o 
          
# Object files:
EasyLexer.o: EasyLexer/EasyLexer.cpp 
	$(CPP) $< -o $@ 

example.o: $q/demo/Cpp/example.cpp  EasyLexer/EasyLexer.cpp
	$(CPP) $< -o $@ 

# Macro expansions (only for debugging):
%.E: %.cpp    
	$(CPP) -E $< -o $@ 

EasyLexer.cpp: masm.qx 
	quex -i masm.qx  -o  EasyLexer --debug-exception 

# (*) HELPERS __________________________________________________________________
clean:	
	rm -f EasyLexer* *.o *.bak *.E lexer
