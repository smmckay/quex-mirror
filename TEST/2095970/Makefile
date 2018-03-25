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
# -- FILES PRODUCED BY QUEX

# (*) COMPILER SETTINGS ________________________________________________________
CC := $(LDCPP) $(EXT_CFLAGS) 

# (*) RULES ____________________________________________________________________
all: lexer

# -- application
lexer: ../lexer-simply.cpp Simple/Simple.cpp
	$(CC) $< Simple/Simple.cpp -o $@  -ggdb

Simple.E: Simple/Simple.cpp
	$(CC) -E $< -o $@ 

Simple/Simple.cpp: $(EXT_MODE_FILE)
	quex -i $(EXT_MODE_FILE) common.qx token.qx -o Simple $(EXT_TOKEN_QUEUE_FLAG) > tmp.txt 2>&1


# (*) HELPERS __________________________________________________________________
clean:	
	@rm -rf Simple* lexer.o lexer token_ids *.bak tmp.txt

