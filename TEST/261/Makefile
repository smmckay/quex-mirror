# PURPOSE: Makefile Demo Application of Quex
#
# ABSOLUTELY NO WARRANTY
#_______________________________________________________________________________
include ../Makefile.lexer

.PHONY: clean

ifndef QUEX_PATH
    $(error The environment variable QUEX_PATH is not defined!)
endif

# (*) COMPILER SETTINGS ________________________________________________________
#     (change COMPILER to whatever you use as compiler on the command line,
#      e.g. "make COMPILER=icpc" will use intel's c++ compiler)

CC := $(LDC)        \
	 -DPRINT_LINE_COLUMN_NUMBER \
	 -I./ -I$(QUEX_PATH)  # -DQUEX_OPTION_DEBUG_SHOW_EXT
     # -DQUEX_OPTION_ASSERTS_DISABLED_EXT
     # -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT 
   
case1:
	quex --cbm -i           case1.qx  \
	     -o                 Simple  \
		 --token-id-offset  0x1000     --debug-exception --language C
	$(CC) -o $@ ../lexer.c Simple/Simple.c `icu-config --ldflags`      
          
case2:
	quex --cbm -i           case2.qx  \
	     -o                 Simple  \
		 --token-id-offset  0x1000     --debug-exception --language C
	$(CC) -o $@ ../lexer.c Simple/Simple.c `icu-config --ldflags`      

# (*) HELPERS __________________________________________________________________
clean:	
	rm -rf Simple*
	rm -f *.o
	rm -f *.bak
	rm -f *.E
	rm -f case1 case2
