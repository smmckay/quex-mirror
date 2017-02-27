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
	$(LDC) $^ Simple.c -o $@ -DPRINT_TOKEN 

more: $(QUEX_PATH)/TEST/lexer.c 
	quex -i                 more.qx  \
	     -o           Simple   \
		 --token-id-offset  0x1000   \
		 --language         C        \
		 --debug-exception
	$(LDC) $^ Simple.c -o $@ -DPRINT_TOKEN 

# (*) HELPERS __________________________________________________________________
clean:	
	rm -f Simple*
	rm -f More*
	rm -f *.o
	rm -f *.bak
	rm -f *.E
	rm -f simple more
