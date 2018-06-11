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
#     e.g. "make COMPILER=icpc" will use intel's c++ compiler)
#     
#     Buffer sizes:   28 --> buffer overflow
#                     29 --> OK
CC := $(CC) -fPIC $(NDEBUG_F) \
     -DQUEX_SETTING_BUFFER_SIZE_EXT=$(BUFFER_SIZE) \
	 -DQUEX_OPTION_ACTIVATE_ASSERTS_EXT \
	 -DPRINT_TOKEN \
	 -DTEST_PROLOG='' \
	 -DTEST_EPILOG='printf("Buffer Size = %i\n", QUEX_SETTING_BUFFER_SIZE);'
	 # -DQUEX_OPTION_UNIT_TEST_EXT \
     # -DQUEX_OPTION_DEBUG_SHOW_EXT \

LD = $(LDC)

# (*) RULES ____________________________________________________________________
all: lexer

# -- application
lexer: lexer.o Simple.o 
	$(LD) lexer.o Simple.o -o $@ `icu-config --ldflags`      

# -- engine and object files
lexer.o: ../lexer.c Simple/Simple.c
	$(CC) -Wall -Werror -DQUEX_OPTION_ASSERTS_EXT_WARNING_MESSAGE_DISABLED_EXT $< -ggdb -o $@

Simple.o: Simple/Simple.c
	$(CC) -Wall -Werror -DQUEX_OPTION_ASSERTS_EXT_WARNING_MESSAGE_DISABLED_EXT $< -ggdb -o $@

%.o: %.c Simple/Simple.c
	$(CC) -Wall -Werror -DQUEX_OPTION_ASSERTS_EXT_WARNING_MESSAGE_DISABLED_EXT $< -ggdb -o $@

Simple/Simple.c: simple.qx
	@quex -i simple.qx -o Simple --language C --debug-exception > tmp.txt 2>&1

# (*) HELPERS __________________________________________________________________
mostlyclean:
	@rm -rf Simple* lexer.o lexer *.bak tmp.txt
	@echo "clean"

clean:	
	@touch simple.qx
	@rm -rf Simple* lexer.o lexer *.bak tmp.txt
	@echo "clean"

