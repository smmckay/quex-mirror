# PURPOSE: Makefile Demo Application of Quex
#
# ABSOLUTELY NO WARRANTY
#_______________________________________________________________________________
include ../Makefile.lexer

.PHONY: clean

LD = $(LDC) 

# (*) RULES ____________________________________________________________________
simple: $(QUEX_PATH)/TEST/lexer.c  
	quex -i                 simple.qx  \
	     -o           Simple     \
		 --token-id-offset  0x1000     \
		 --language         C          \
		 --debug-exception
	$(LDC) $^ Simple/Simple.c -o $@ -DPRINT_TOKEN 

more: $(QUEX_PATH)/TEST/lexer.c 
	quex -i                 more.qx  \
	     -o           Simple   \
		 --token-id-offset  0x1000   \
		 --language         C        \
		 --debug-exception
	$(LDC) $^ Simple/Simple.c -o $@ -DPRINT_TOKEN 

# (*) HELPERS __________________________________________________________________
clean:	
	rm -rf Simple* More* *.o *.bak *.E simple more
