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
     -DQUEX_SETTING_BUFFER_SIZE=$(BUFFER_SIZE) \
	 -DQUEX_OPTION_ACTIVATE_ASSERTS \
	 -DPRINT_TOKEN \
	 -DTEST_PROLOG='' \
	 -DTEST_EPILOG='printf("Buffer Size = %i\n", QUEX_SETTING_BUFFER_SIZE);'
	 # -D__QUEX_OPTION_UNIT_TEST \
     # -DQUEX_OPTION_DEBUG_SHOW \

LD = $(LDC)

# (*) RULES ____________________________________________________________________
all: lexer

# -- application
lexer: lexer.o Simple.o 
	$(LD) lexer.o Simple.o -o $@ \
		`icu-config --ldflags`      

# -- engine and object files
lexer.o: ../lexer.c Simple.c
	$(CC) -Wall -Werror -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED $< -ggdb -o $@

%.o: %.c Simple.c
	$(CC) -Wall -Werror -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED $< -ggdb -o $@

Simple.c: simple.qx
	@quex -i simple.qx -o Simple --language C --debug-exception > tmp.txt 2>&1

# (*) HELPERS __________________________________________________________________
mostlyclean:
	@rm -f Simple.o
	@rm -f lexer.o
	@rm -f lexer
	@rm -f *.bak
	@rm -f tmp.txt
	@echo "clean"

clean:	
	@touch simple.qx
	@rm -f Simple*
	@rm -f Simple.o
	@rm -f lexer.o
	@rm -f lexer
	@rm -f token_ids
	@rm -f *.bak
	@rm -f tmp.txt
	@echo "clean"

