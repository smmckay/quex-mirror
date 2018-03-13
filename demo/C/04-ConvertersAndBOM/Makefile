# PURPOSE: Makefile for Demo Application of Quex
# 
# USAGES:
# 
#     make lexer CONVERTER=iconv   
#
#         creates a lexer using the iconv library. This is actually the
#         default which is done even if no 'CONVERTER' is specified.
#
#     make lexer CONVERTER=icu   
#
#         creates a lexer using the icu library.
#
# ABSOLUTELY NO WARRANTY
#_______________________________________________________________________________
.PHONY: clean
.SECONDARY: # avoid remove of intermediate targets => faster unit testing

ifndef QUEX_PATH
    $(error The environment variable QUEX_PATH is not defined!)
endif

BYTES_PER_CHARACTER = 2 

# (*) COMPILER SETTINGS ________________________________________________________
#     (change COMPILER to whatever you use as compiler on the command line,
#      e.g. "make COMPILER=icpc" will use intel's c++ compiler)
COMPILER = gcc -ggdb -W -pedantic $(ADD_FLAGS)

CC = $(COMPILER) -c \
	 -I./ -I$(QUEX_PATH)                             \
	 -Wall -Werror -Wconversion                      \
	 $(ADD_FLAGS)                                    \
	 -DENCODING_NAME='"UTF8"'                        \
     -DQUEX_OPTION_CONVERTER_ICONV 
	 # -DQUEX_OPTION_ASSERTS_DISABLED
	 # -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED \
     # -DQUEX_OPTION_DEBUG_SHOW
   
LD = $(COMPILER) 

# (*) Determining the Converter Lib (IConv or ICU) ____________________________
#
# Some compiler distributions have iconv in a separate lib:
#    -- Intel's icpc (tm)
#    -- MS's cl (tm)
#    -- Digital Mars dmc (tm)
#    -- g++ on apple (tm)
ifneq (,$(or $(findstring apple, $(shell $(COMPILER) --version)), \
             $(findstring $(COMPILER),icpc cl dmc)))
	LIBICONV=-liconv
else
    LIBICONV=#
endif

CONVERTER=undefined # (overidden by command line specification)
ifeq ($(CONVERTER),icu)
	LIB_CONV  = `icu-config --ldflags`
else
	LIB_CONV  = $(LIBICONV)
endif

all: lexer lexer-with-bom

lexer:          example.o Easy/Easy.o
	$(LD) -o $@ example.o Easy/Easy.o $(LIB_CONV) 
          
lexer-with-bom: lexer-with-bom.o Easy/Easy.o
	$(LD) -o $@ lexer-with-bom.o Easy/Easy.o $(LIB_CONV) 
          
Easy.o: Easy/Easy.c 
	$(CC) $< -o $@ 

example.o: lexer.c  Easy/Easy.h
	$(CC) -DQUEX_OPTION_CONVERTER_ICONV $< -o $@ 

lexer-with-bom.o: lexer-with-bom.c Easy/Easy.h
	$(CC) -DQUEX_OPTION_CONVERTER_ICONV $< -o $@ 

Easy/Easy.c \
Easy/Easy.h: definitions.qx end_of_file.qx program.qx 
	quex -i                definitions.qx end_of_file.qx program.qx \
	     -o                Easy                   \
		 --token-id-offset 0x1000                 \
	     -b                $(BYTES_PER_CHARACTER) \
		 --language        C                      \
		 $(QUEX_FLAG)

# (*) HELPERS __________________________________________________________________
clean: clean_lexer clean_lexer-with-bom

clean_lexer:	
	rm -rf lexer Easy/ *.o tmp.*
clean_lexer-with_bom:	
	rm -rf lexer-with-bom Easy/ *.o tmp.*
