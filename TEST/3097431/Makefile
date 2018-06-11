# PURPOSE: Makefile Demo Application of Quex
#
# ABSOLUTELY NO WARRANTY
#_______________________________________________________________________________
include ../Makefile.lexer
.PHONY: clean

CPP := $(CPP) -I. \
	 -DPRINT_TOKEN                                   \
	 -DPRINT_LINE_COLUMN_NUMBER
     # -DQUEX_OPTION_ASSERTS_EXT_DISABLED_EXT
     # -DQUEX_OPTION_ASSERTS_EXT_WARNING_MESSAGE_DISABLED_EXT 
     # -DQUEX_OPTION_DEBUG_SHOW_EXT
   
# (*) RULES ____________________________________________________________________
# -- application
lexer:   ../lexer.cpp  Simple/Simple.cpp
	$(LDCPP) -o $@ $^
          
Simple/Simple.cpp: masm.qx 
	quex -i masm.qx  -o  Simple --debug-exception 

# (*) HELPERS __________________________________________________________________
clean:	
	rm -rf Simple* *.o *.bak *.E lexer
