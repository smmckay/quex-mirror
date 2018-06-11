
SOURCES := test.c \
	       EasyLexer/EasyLexer.c

INCLUDES := -I. -I$(QUEX_PATH) -I$(HWUT_PATH)/support/C

CC := gcc $(INCLUDES) $(SOURCES) -Wall -Werror \
	  -DQUEX_SETTING_BUFFER_SIZE_EXT=5 

# Other useful options for debugging:
# -DQUEX_OPTION_ASSERTS_EXT_DISABLED_EXT
# -DQUEX_OPTION_ASSERTS_EXT_WARNING_MESSAGE_DISABLED_EXT 
# -DQUEX_OPTION_DEBUG_SHOW_EXT

all: lexer

hwut-info:
	@echo lexer

lexer: no-drop.qx test.c Makefile
	quex -i no-drop.qx --language C -o EasyLexer
	$(CC) -DPRINT_TOKEN -o $@
	rm -rf EasyLexer 

clean:
	rm -rf EasyLexer* *.o lexer tmp.* *.dot
